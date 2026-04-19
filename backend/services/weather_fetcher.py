import httpx
import asyncio
from datetime import datetime, timedelta

class WeatherFetcher:
    """
    Open-Meteo client for real-time and forecast weather.
    Uses httpx for async non-blocking fetch.
    Cached in-memory for 10 minutes.
    """
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self._cache = {}

    async def get_weather(self, lat, lng):
        """Fetches current temperature and wind speed (async)."""
        cache_key = f"{lat},{lng}"
        now = datetime.now()
        
        if cache_key in self._cache:
            entry_time, data = self._cache[cache_key]
            if now - entry_time < timedelta(minutes=10):
                return data

        params = {
            "latitude": lat,
            "longitude": lng,
            "hourly": "temperature_2m,wind_speed_10m",
            "temperature_unit": "fahrenheit",
            "forecast_days": 1,
            "timezone": "auto"
        }

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(self.base_url, params=params, timeout=2.0)
                if r.status_code == 200:
                    data = r.json().get("hourly", {})
                    hour_idx = now.hour
                    result = {
                        "temp_f": data["temperature_2m"][hour_idx],
                        "wind_speed": data["wind_speed_10m"][hour_idx]
                    }
                    self._cache[cache_key] = (now, result)
                    return result
        except Exception as e:
            print(f"⚠️ Weather fetch timed out or failed (using default): {e}")
        
        return {"temp_f": 75.0, "wind_speed": 10.0}

    async def get_forecast_72h(self, lat, lng):
        """Fetches 72h weather forecast (async)."""
        params = {
            "latitude": lat,
            "longitude": lng,
            "hourly": "temperature_2m,wind_speed_10m,time",
            "temperature_unit": "fahrenheit",
            "forecast_days": 3,
            "timezone": "auto"
        }
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(self.base_url, params=params, timeout=2.5)
                if r.status_code == 200:
                    data = r.json().get("hourly", {})
                    forecast = []
                    times = data.get("time", [])
                    temps = data.get("temperature_2m", [])
                    winds = data.get("wind_speed_10m", [])
                    
                    for i in range(len(times)):
                        forecast.append({
                            "timestamp": times[i],
                            "temp_f": temps[i],
                            "wind_speed": winds[i]
                        })
                    return forecast
        except Exception as e:
            print(f"⚠️ Weather forecast fetch failed: {e}")
            return []

weather_fetcher = WeatherFetcher()
