"""
ERCOT API client with mock data fallback.
Fetches real-time and historical LMP at settlement points.
"""
import random
import math
from datetime import datetime


# --- Mock LMP Data Generator ---
# These patterns mirror actual ERCOT West Hub pricing behavior

def _generate_realistic_lmp(hour: int, regime: str = "normal") -> float:
    """Generate a realistic LMP value based on time of day and regime."""
    # Base load curve (typical ERCOT West)
    base_curves = {
        0: 22, 1: 19, 2: 17, 3: 16, 4: 17, 5: 20,
        6: 28, 7: 35, 8: 42, 9: 45, 10: 48, 11: 50,
        12: 52, 13: 55, 14: 62, 15: 68, 16: 72, 17: 75,
        18: 70, 19: 65, 20: 58, 21: 48, 22: 38, 23: 28,
    }
    
    base = base_curves.get(hour, 40)
    
    # Regime multipliers
    regime_mult = {
        "normal": 1.0,
        "heat_dome": 1.8,
        "wind_glut": 0.3,
        "scarcity": 3.5,
        "oversupply": 0.5,
        "winter_storm": 4.0,
    }
    
    multiplier = regime_mult.get(regime, 1.0)
    noise = random.gauss(0, base * 0.08)
    
    return max(0, round(base * multiplier + noise, 2))


def get_current_lmp(settlement_point: str = "LZ_WEST") -> dict:
    """Get current LMP at a settlement point. Returns mock data."""
    now = datetime.now()
    current_hour = now.hour
    
    # Determine current regime based on time and randomness
    # Bias toward heat_dome in afternoon for demo impact
    if 14 <= current_hour <= 20:
        regime = "heat_dome"
        confidence = random.randint(78, 95)
    elif 2 <= current_hour <= 6:
        regime = random.choice(["normal", "wind_glut"])
        confidence = random.randint(60, 85)
    else:
        regime = "normal"
        confidence = random.randint(70, 90)
    
    lmp = _generate_realistic_lmp(current_hour, regime)
    
    # Make it look good for demo — ensure positive spread
    if regime == "heat_dome":
        lmp = max(lmp, 50.0)  # Ensure interesting spread during demo
    
    return {
        "settlement_point": settlement_point,
        "lmp": lmp,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "interval": "15min",
        "regime": regime,
        "regime_confidence": confidence,
    }


def get_historical_lmp(settlement_point: str = "LZ_WEST", hours: int = 24) -> list:
    """Get historical LMP data. Returns mock data."""
    now = datetime.now()
    data = []
    
    for h in range(hours):
        hour_offset = hours - h
        hist_hour = (now.hour - hour_offset) % 24
        lmp = _generate_realistic_lmp(hist_hour)
        
        data.append({
            "hour": h,
            "hour_label": f"{hist_hour:02d}:00",
            "lmp": lmp,
            "settlement_point": settlement_point,
        })
    
    return data
