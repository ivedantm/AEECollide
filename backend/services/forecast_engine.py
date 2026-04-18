"""
Monte Carlo spread forecasting engine.
Generates 72-hour forecasts with p10/p50/p90 confidence bands.
Uses historical LMP volatility patterns and time-of-day demand curves.
"""
import numpy as np
from datetime import datetime, timedelta


def _time_of_day_factor(hour: int) -> float:
    """
    LMP multiplier based on time of day.
    Peak hours (14:00-20:00) have higher prices.
    Off-peak (00:00-06:00) have lower prices.
    """
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
    n_simulations: int = 1000,
    seed: int = None,
) -> list:
    """
    Generate 72-hour spread forecast using Monte Carlo simulation.
    
    Returns list of dicts, one per hour:
    {hour, timestamp, lmp_p50, spread_p10, spread_p50, spread_p90, recommendation}
    """
    if seed is not None:
        np.random.seed(seed)
    else:
        # Use a seed based on the current hour for consistency within demo
        np.random.seed(int(datetime.now().timestamp()) // 3600)

    gen_cost = current_gas_price * heat_rate + om_cost
    base_vol = _regime_volatility(regime)
    now = datetime.now()

    forecast = []

    for h in range(hours):
        future_time = now + timedelta(hours=h)
        hour_of_day = future_time.hour
        tod_factor = _time_of_day_factor(hour_of_day)

        # Mean LMP decays toward base over forecast horizon
        decay = 0.95 ** (h / 24)  # Slow mean reversion
        mean_lmp = current_lmp * decay * tod_factor

        # Volatility increases with forecast horizon
        horizon_vol = base_vol * (1 + 0.02 * h)  # 2% per hour growth
        vol = max(5.0, mean_lmp * 0.15 * horizon_vol)  # Floor at $5 vol

        # Generate simulated LMP paths
        simulated_lmps = np.maximum(0, np.random.normal(mean_lmp, vol, n_simulations))

        # Gas price follows slower random walk
        gas_drift = current_gas_price * (1 + 0.001 * np.random.randn())
        gas_noise = 0.05 * np.random.randn()
        future_gas = max(1.0, current_gas_price + gas_noise * h / 24)
        future_gen_cost = future_gas * heat_rate + om_cost

        # Calculate spread percentiles
        spreads = simulated_lmps - future_gen_cost
        p10 = float(np.percentile(spreads, 10))
        p50 = float(np.percentile(spreads, 50))
        p90 = float(np.percentile(spreads, 90))
        lmp_p50 = float(np.percentile(simulated_lmps, 50))

        # Recommendation based on p50
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
            "lmp_p50": round(lmp_p50, 2),
            "gen_cost": round(future_gen_cost, 2),
            "spread_p10": round(p10, 2),
            "spread_p50": round(p50, 2),
            "spread_p90": round(p90, 2),
            "recommendation": recommendation,
            "should_generate": p50 > 0,
        })

    return forecast


def generate_24h_history(current_lmp: float, current_gas_price: float, heat_rate: float = 7.5, om_cost: float = 3.50) -> list:
    """Generate 24 hours of historical spread data for the sparkline."""
    np.random.seed(int(datetime.now().timestamp()) // 86400)  # Same seed per day

    gen_cost = current_gas_price * heat_rate + om_cost
    now = datetime.now()
    history = []

    for h in range(24):
        past_time = now - timedelta(hours=24 - h)
        hour_of_day = past_time.hour
        tod_factor = _time_of_day_factor(hour_of_day)

        lmp = current_lmp * tod_factor * (1 + 0.1 * np.random.randn())
        lmp = max(0, lmp)
        spread = lmp - gen_cost

        history.append({
            "hour": h,
            "timestamp": past_time.strftime("%H:%M"),
            "lmp": round(lmp, 2),
            "spread": round(spread, 2),
        })

    return history
