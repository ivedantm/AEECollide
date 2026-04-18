"""
EIA API client for natural gas spot prices.
Fetches Henry Hub and Waha Hub pricing data.
Falls back to realistic mock data.
"""
import requests
from backend.config import EIA_API_KEY, DEFAULT_GAS_PRICE, HENRY_HUB_PREMIUM


def get_gas_prices() -> dict:
    """
    Get current gas prices from EIA API.
    Falls back to realistic mock data if no API key.
    """
    if EIA_API_KEY:
        try:
            return _fetch_eia_prices()
        except Exception as e:
            print(f"EIA API error, using mock data: {e}")

    return _mock_gas_prices()


def _fetch_eia_prices() -> dict:
    """Fetch real gas prices from EIA API v2."""
    base_url = "https://api.eia.gov/v2/natural-gas/pri/fut/data/"
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "daily",
        "data[0]": "value",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "offset": 0,
        "length": 5,
    }

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Parse Henry Hub price from response
    henry_hub = DEFAULT_GAS_PRICE + HENRY_HUB_PREMIUM
    if data.get("response", {}).get("data"):
        for record in data["response"]["data"]:
            if record.get("value"):
                henry_hub = float(record["value"])
                break

    waha = henry_hub - HENRY_HUB_PREMIUM

    return {
        "henry_hub": round(henry_hub, 2),
        "waha": round(waha, 2),
        "basis_differential": round(HENRY_HUB_PREMIUM, 2),
        "source": "EIA API",
        "unit": "$/MMBtu",
    }


def _mock_gas_prices() -> dict:
    """Return realistic mock gas prices."""
    return {
        "henry_hub": round(DEFAULT_GAS_PRICE + HENRY_HUB_PREMIUM, 2),
        "waha": DEFAULT_GAS_PRICE,
        "basis_differential": HENRY_HUB_PREMIUM,
        "source": "Mock (EIA API key not configured)",
        "unit": "$/MMBtu",
    }
