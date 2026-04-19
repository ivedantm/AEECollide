import os
import random
import asyncio
import time
from datetime import datetime
from .ercot_live import ercot_live
from .caiso_live import caiso_live
from .weather_fetcher import weather_fetcher
from .regime_classifier_ml import regime_classifier_ml
from .sparkline_provider import sparkline_provider

USE_LIVE_DATA = os.getenv("USE_LIVE_DATA", "false").lower() == "true"

# Simple TTL cache to avoid redundant live API calls when multiple
# dispatch endpoints fire simultaneously on tab switch
_lmp_cache = {}  # {settlement_point: {"data": result, "ts": time.time()}}
_CACHE_TTL = 30  # seconds

async def get_current_lmp(settlement_point: str = "LZ_WEST", site_id: str = "midland", lat: float = 31.99, lng: float = -102.08) -> dict:
    """
    Get current LMP and regime assessment (async).
    Fetches weather and pricing in parallel using asyncio.gather.
    Results are cached for 30s to avoid redundant API calls.
    """
    # Check cache first
    cache_key = f"{settlement_point}_{site_id}"
    cached = _lmp_cache.get(cache_key)
    if cached and (time.time() - cached["ts"]) < _CACHE_TTL:
        return cached["data"]

    now = datetime.now()
    lmp = None
    weather = {"temp_f": 75.0, "wind_speed": 10.0}
    
    if USE_LIVE_DATA:
        # 1 & 2. Fetch real weather and LMP in parallel
        try:
            if settlement_point.startswith("LZ_") or settlement_point.startswith("HB_"):
                # ERCOT path
                price_task = ercot_live.get_latest_spp(settlement_point)
            else:
                # CAISO/WECC dynamic path
                price_task = caiso_live.get_latest_lmp(settlement_point)
            
            weather_task = weather_fetcher.get_weather(lat, lng)
            
            # PARALLEL EXECUTION
            lmp, weather = await asyncio.gather(price_task, weather_task)
        except Exception as e:
            print(f"⚠️ Parallel fetch encountered error (falling back): {e}")

    # 3. Fallback to realistic mock if live fetch failed or disabled
    if lmp is None:
        lmp = _generate_realistic_lmp(now.hour)
        if settlement_point == "PALOVRDE": lmp += 5.0 # Palo Verde premium

    # 4. ML Regime Assessment
    feature_dict = {
        "lmp": lmp,
        "temp_f": weather["temp_f"],
        "wind_speed": weather["wind_speed"],
        "hour": now.hour,
        "month": now.month,
        "weekday": now.weekday(),
        "spread": lmp - 35.0 # Rough estimate for classification
    }
    regime, confidence = regime_classifier_ml.classify(feature_dict)

    result = {
        "settlement_point": settlement_point,
        "lmp": round(float(lmp), 2),
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "interval": "15min",
        "regime": regime,
        "regime_confidence": int(confidence * 100),
        "weather": weather
    }

    # Cache for 30s to avoid redundant calls from parallel endpoints
    _lmp_cache[cache_key] = {"data": result, "ts": time.time()}

    return result


def _generate_realistic_lmp(hour: int, regime: str = "normal") -> float:
    """Mock generator fallback."""
    base_curves = {
        0: 22, 1: 19, 2: 17, 3: 16, 4: 17, 5: 20,
        6: 28, 7: 35, 8: 42, 9: 45, 10: 48, 11: 50,
        12: 52, 13: 55, 14: 62, 15: 68, 16: 72, 17: 75,
        18: 70, 19: 65, 20: 58, 21: 48, 22: 38, 23: 28,
    }
    base = base_curves.get(hour, 40)
    regime_mult = {
        "normal": 1.0, "heat_dome": 1.8, "wind_glut": 0.3,
        "scarcity": 3.5, "oversupply": 0.5, "winter_storm": 4.0,
    }
    multiplier = regime_mult.get(regime, 1.0)
    noise = random.gauss(0, base * 0.08)
    return max(-10, round(base * multiplier + noise, 2))


def get_historical_lmp(settlement_point: str = "LZ_WEST", site_id: str = "midland", hours: int = 24) -> list:
    """Provides historical trend for sparklines."""
    # This remains sync for now as it pulls from local parquet
    return sparkline_provider.get_history(settlement_point, site_id, hours)
