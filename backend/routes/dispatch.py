"""Dispatch API routes — real-time operations and forecasting."""
from fastapi import APIRouter, Query
from datetime import datetime
from backend.config import HEAT_RATE, O_AND_M_COST, FACILITY_SIZE_MW
from backend.services.ercot_client import get_current_lmp, get_historical_lmp
from backend.services.eia_client import get_gas_prices
from backend.services.spread_calculator import calculate_spread, calculate_gen_cost, dispatch_decision, calculate_schedule_savings
from backend.services.forecast_engine import generate_forecast, generate_24h_history
from backend.services.ai_service import generate_operator_briefing
from backend.data.regimes import get_regime, classify_regime
from backend.data.sites_data import get_site_by_id, get_all_sites

router = APIRouter(prefix="/api/dispatch", tags=["dispatch"])


def _get_site_context(site_id: str):
    """Return site-specific parameters for dispatch calculations."""
    site = get_site_by_id(site_id) if site_id else None
    if site is None:
        site = get_all_sites()[0]  # Default to Midland

    # Map gas hub to price key
    # Map gas hub to price key
    gh = site.get("gas_hub", "Henry Hub")
    if gh == "Waha":
        gas_key = "waha"
    elif gh == "SoCal Border":
        gas_key = "socal"
    else:
        gas_key = "henry_hub"

    return {
        "site": site,
        "settlement_point": site["settlement_point"],
        "location": site["label"],
        "gas_hub": gh,
        "gas_key": gas_key,
        "lat": site["lat"],
        "lng": site["lng"],
        "site_id": site["id"]
    }


@router.get("/current")
async def get_current_dispatch(site_id: str = Query(default="midland", description="Site ID")):
    """
    Get current dispatch status — the hero data for the spread ticker.
    Returns: current spread, LMP, gas price, gen cost, regime, recommendation.
    """
    ctx = _get_site_context(site_id)
    site = ctx["site"]

    lmp_data = await get_current_lmp(ctx["settlement_point"], site_id=ctx["site_id"], lat=ctx["lat"], lng=ctx["lng"])
    gas_data = get_gas_prices()

    lmp = lmp_data["lmp"]
    gas_price = gas_data.get(ctx["gas_key"], gas_data["henry_hub"])
    temp_f = lmp_data.get("weather", {}).get("temp_f", 75)
    gen_cost = calculate_gen_cost(gas_price, temp_f=temp_f)
    spread = calculate_spread(lmp, gas_price, temp_f=temp_f)
    decision = dispatch_decision(spread)
    regime = get_regime(lmp_data["regime"])

    # 24-hour history for sparkline
    history = generate_24h_history(lmp, gas_price)

    return {
        "lmp": round(lmp, 2),
        "gas_price": gas_price,
        "gas_hub": ctx["gas_hub"],
        "gen_cost": round(gen_cost, 2),
        "spread": round(spread, 2),
        "decision": decision,
        "regime": {
            "id": regime["id"],
            "name": regime["name"],
            "icon": regime["icon"],
            "color": regime["color"],
            "badge_bg": regime["badge_bg"],
            "description": regime["description"],
            "dispatch_note": regime["dispatch_note"],
            "confidence": lmp_data.get("regime_confidence", 80),
        },
        "settlement_point": ctx["settlement_point"],
        "location": ctx["location"],
        "heat_rate": HEAT_RATE,
        "facility_mw": FACILITY_SIZE_MW,
        "timestamp": lmp_data["timestamp"],
        "history_24h": history,
        "weather": lmp_data.get("weather", {"temp_f": 75, "wind_speed": 10})
    }


@router.get("/forecast")
async def get_forecast(site_id: str = Query(default="midland", description="Site ID")):
    """Get 72-hour spread forecast with p10/p50/p90 confidence bands."""
    ctx = _get_site_context(site_id)

    lmp_data = await get_current_lmp(ctx["settlement_point"], site_id=ctx["site_id"], lat=ctx["lat"], lng=ctx["lng"])
    gas_data = get_gas_prices()
    gas_price = gas_data.get(ctx["gas_key"], gas_data["henry_hub"])
    
    weather = lmp_data.get("weather", {"temp_f": 75, "wind_speed": 10})

    forecast = generate_forecast(
        current_lmp=lmp_data["lmp"],
        current_gas_price=gas_price,
        regime=lmp_data["regime"],
        temp_f=weather["temp_f"],
        wind_speed=weather["wind_speed"],
        site_id=ctx["site_id"],
        current_spread=lmp_data["lmp"] - calculate_gen_cost(gas_price, temp_f=weather["temp_f"])
    )

    return {
        "forecast": forecast,
        "hours": len(forecast),
        "current_regime": lmp_data["regime"],
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@router.get("/schedule")
async def get_dispatch_schedule(site_id: str = Query(default="midland", description="Site ID")):
    """Get optimal 72-hour dispatch schedule with savings calculation."""
    ctx = _get_site_context(site_id)

    lmp_data = await get_current_lmp(ctx["settlement_point"], site_id=ctx["site_id"], lat=ctx["lat"], lng=ctx["lng"])
    gas_data = get_gas_prices()
    gas_price = gas_data.get(ctx["gas_key"], gas_data["henry_hub"])
    weather = lmp_data.get("weather", {"temp_f": 75, "wind_speed": 10})

    forecast = generate_forecast(
        current_lmp=lmp_data["lmp"],
        current_gas_price=gas_price,
        regime=lmp_data["regime"],
        temp_f=weather["temp_f"],
        wind_speed=weather["wind_speed"],
        site_id=ctx["site_id"],
        current_spread=lmp_data["lmp"] - calculate_gen_cost(gas_price, temp_f=weather["temp_f"])
    )

    schedule = []
    for hour_data in forecast:
        schedule.append({
            "hour": hour_data["hour"],
            "timestamp": hour_data["timestamp"],
            "spread": hour_data["spread_p50"],
            "should_generate": hour_data["should_generate"],
            "recommendation": hour_data["recommendation"],
        })

    savings = calculate_schedule_savings(schedule)

    return {
        "schedule": schedule,
        "savings": savings,
    }


@router.get("/briefing")
async def get_operator_briefing(site_id: str = Query(default="midland", description="Site ID")):
    """
    Generate AI operator briefing using OpenAI GPT-4o.
    """
    ctx = _get_site_context(site_id)

    lmp_data = await get_current_lmp(ctx["settlement_point"], site_id=ctx["site_id"], lat=ctx["lat"], lng=ctx["lng"])
    gas_data = get_gas_prices()
    gas_price = gas_data.get(ctx["gas_key"], gas_data["henry_hub"])
    weather = lmp_data.get("weather", {"temp_f": 75, "wind_speed": 10})
    
    spread = lmp_data["lmp"] - calculate_gen_cost(gas_price, temp_f=weather["temp_f"])
    regime = get_regime(lmp_data["regime"])
    forecast = generate_forecast(
        current_lmp=lmp_data["lmp"],
        current_gas_price=gas_price,
        regime=lmp_data["regime"],
        temp_f=weather["temp_f"],
        wind_speed=weather["wind_speed"],
        site_id=ctx["site_id"],
        current_spread=spread
    )

    # Find import windows in forecast
    # ... (skipping unchanged code)

    # Find import windows in forecast
    import_windows = []
    current_window = None
    for h in forecast:
        if not h["should_generate"]:
            if current_window is None:
                current_window = {"start": h["day_label"], "end": h["day_label"]}
            else:
                current_window["end"] = h["day_label"]
        else:
            if current_window:
                import_windows.append(current_window)
                current_window = None
    if current_window:
        import_windows.append(current_window)

    # Build forecast summary for OpenAI
    if import_windows:
        w = import_windows[0]
        forecast_summary = f"A brief import window is forecasted ({w['start']}–{w['end']}) when grid prices will drop below generation cost."
    else:
        forecast_summary = "Sustained positive spreads are expected across the entire 72-hour horizon."

    # Call OpenAI API to generate real-time briefing
    briefing = generate_operator_briefing(
        lmp=lmp_data["lmp"],
        gas_price=gas_price,
        spread=spread,
        regime_name=regime["name"],
        confidence=lmp_data.get("regime_confidence", 80),
        forecast_summary=forecast_summary
    )

    now = datetime.now()
    return {
        "briefing": briefing,
        "updated_at": now.strftime("%H:%M CST"),
        "regime": regime["name"],
        "confidence": lmp_data.get("regime_confidence", 80),
    }
