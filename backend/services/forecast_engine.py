import numpy as np
from datetime import datetime, timedelta
from .quantile_forecaster_ml import quantile_forecaster_ml


def _time_of_day_factor(hour: int) -> float:
    """LMP multiplier based on time of day."""
    if 14 <= hour <= 20:
        return 1.4 + 0.3 * np.sin((hour - 14) / 6 * np.pi)
    elif 6 <= hour <= 13:
        return 1.0 + 0.2 * (hour - 6) / 7
    else:
        return 0.6 + 0.1 * np.random.randn()


def _regime_volatility(regime: str) -> float:
    """Volatility multiplier by regime."""
    volatility_map = {
        "normal": 1.0,
        "heat_dome": 2.5,
        "wind_glut": 1.8,
        "scarcity": 4.0,
        "oversupply": 0.8,
        "winter_storm": 5.0,
        "uri_emergency": 8.0,
    }
    return volatility_map.get(regime, 1.0)


def generate_forecast(
    current_lmp: float,
    current_gas_price: float,
    heat_rate: float = 7.5,
    om_cost: float = 3.50,
    regime: str = "normal",
    hours: int = 72,
    temp_f: float = 75.0,
    wind_speed: float = 10.0,
    site_id: str = "midland",
    current_spread: float = 0,
    n_simulations: int = 1000,
    seed: int = None,
) -> list:
    """
    Generate spread forecast using ML (if available) or Monte Carlo simulation.
    """
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed(int(datetime.now().timestamp()) // 3600)

    gen_cost = current_gas_price * heat_rate + om_cost
    now = datetime.now()
    forecast = []

    # Prepare features for ML models
    ml_features = {
        "lmp": current_lmp,
        "spread": current_spread,
        "gas_price": current_gas_price,
        "temp_f": temp_f,
        "wind_speed": wind_speed,
        "hour": now.hour,
        "month": now.month,
        "weekday": now.weekday(),
        "lmp_6h_lag": current_lmp, # Approximation
        "lmp_trend_6h": 0,
    }

    for h in range(hours):
        future_time = now + timedelta(hours=h)
        
        # ── ML Forecast (Primary) ──
        if quantile_forecaster_ml.models:
            q = quantile_forecaster_ml.predict_spread(ml_features, h + 1)
            p10, p50, p90 = q["p10"], q["p50"], q["p90"]
            lmp_p50 = p50 + gen_cost
            future_gen_cost = gen_cost # Assuming flat gas in ML for now
        else:
            # ── Monte Carlo Fallback ──
            hour_of_day = future_time.hour
            tod_factor = _time_of_day_factor(hour_of_day)
            decay = 0.95 ** (h / 24)
            mean_lmp = current_lmp * decay * tod_factor
            
            base_vol = _regime_volatility(regime)
            horizon_vol = base_vol * (1 + 0.02 * h)
            vol = max(5.0, mean_lmp * 0.15 * horizon_vol)
            
            simulated_lmps = np.maximum(0, np.random.normal(mean_lmp, vol, n_simulations))
            future_gas = max(1.0, current_gas_price + 0.05 * np.random.randn() * h / 24)
            future_gen_cost = future_gas * heat_rate + om_cost
            
            spreads = simulated_lmps - future_gen_cost
            p10, p50, p90 = np.percentile(spreads, [10, 50, 90])
            lmp_p50 = np.percentile(simulated_lmps, 50)

        # Recommendation logic
        if p50 > 10:
            recommendation = "GENERATE"
        elif p50 > 0:
            recommendation = "GENERATE (marginal)"
        elif p50 > -10:
            recommendation = "IMPORT (marginal)"
        else:
            recommendation = "IMPORT"

        forecast.append({
            "hour": h,
            "timestamp": future_time.strftime("%Y-%m-%d %H:%M"),
            "hour_label": future_time.strftime("%H:%M"),
            "day_label": future_time.strftime("%a %H:%M"),
            "lmp_p50": round(float(lmp_p50), 2),
            "gen_cost": round(float(future_gen_cost), 2),
            "spread_p10": round(float(p10), 2),
            "spread_p50": round(float(p50), 2),
            "spread_p90": round(float(p90), 2),
            "recommendation": recommendation,
            "should_generate": p50 > 0,
        })

    return forecast


def generate_24h_history(current_lmp: float, current_gas_price: float, heat_rate: float = 7.5, om_cost: float = 3.50) -> list:
    """Generate sparkline history (can be real later)."""
    np.random.seed(int(datetime.now().timestamp()) // 86400)
    gen_cost = current_gas_price * heat_rate + om_cost
    now = datetime.now()
    history = []

    for h in range(24):
        past_time = now - timedelta(hours=24 - h)
        hour_of_day = past_time.hour
        tod_factor = _time_of_day_factor(hour_of_day)
        lmp = max(0, current_lmp * tod_factor * (1 + 0.1 * np.random.randn()))
        history.append({
            "hour": h,
            "timestamp": past_time.strftime("%H:%M"),
            "lmp": round(lmp, 2),
            "spread": round(lmp - gen_cost, 2),
        })
    return history
