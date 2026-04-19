import os
import requests
import json
from backend.config import EIA_API_KEY, DEFAULT_GAS_PRICE, HENRY_HUB_PREMIUM
from cachetools import TTLCache

_gas_cache = TTLCache(maxsize=1, ttl=1800)

def get_gas_prices() -> dict:
    """Get real-time gas prices for all hubs used by site selector (cached 30m)."""
    if "prices" in _gas_cache:
        return _gas_cache["prices"]
        
    if EIA_API_KEY:
        try:
            prices = _fetch_eia_prices()
            _gas_cache["prices"] = prices
            return prices
        except Exception as e:
            print(f"⚠️ EIA API Error: {e}")
    return _mock_gas_prices()

def _fetch_eia_prices() -> dict:
    """Fetch Henry Hub using EIA v2 and derive regional hubs."""
    url = "https://api.eia.gov/v2/natural-gas/pri/fut/data/"
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "daily",
        "data[0]": "value",
        "facets[series][]": "RNGWHHD", # Henry Hub
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 1,
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json().get("response", {}).get("data", [])
        
        if data and data[0].get("value"):
            hh = float(data[0]["value"])
            # Regional spreads (Henry Hub as basis)
            return {
                "henry_hub": round(hh, 2),
                "waha": round(hh - 0.85, 2),   # Waha is typically at a discount
                "socal": round(hh + 0.45, 2),  # SoCal border is typically at a premium
                "source": "EIA API (Live)",
                "unit": "$/MMBtu"
            }
    except Exception as e:
        print(f"⚠️ EIA fetch detail error: {e}")
    
    return _mock_gas_prices()

def _mock_gas_prices() -> dict:
    """Mock fallback prices."""
    hh = 2.75
    return {
        "henry_hub": hh,
        "waha": round(hh - 0.80, 2),
        "socal": round(hh + 0.40, 2),
        "source": "Mock (EIA Offline)",
        "unit": "$/MMBtu"
    }
