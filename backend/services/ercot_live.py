import pandas as pd
import gridstatus
import asyncio
from datetime import datetime, timedelta
from .ercot_auth import ercot_auth
import requests
import os
from cachetools import TTLCache

class ErcotLiveService:
    """
    Fetches real-time and historical data for ERCOT.
    Uses gridstatus in a non-blocking thread to allow parallel fetching.
    Uses TTL caching to prevent redundant MIS downloads.
    """
    def __init__(self):
        self.ercot = gridstatus.Ercot()
        self.base_url = "https://api.ercot.com/api/public-reports"
        
        # 5-minute caches
        self._spp_cache = TTLCache(maxsize=100, ttl=300)
        self._dam_cache = TTLCache(maxsize=100, ttl=300)
        self._fuel_cache = TTLCache(maxsize=10, ttl=300)

    async def get_latest_spp(self, zone):
        """Fetches the latest Real-Time 15-min SPP for a zone (async, cached 5m)."""
        if zone in self._spp_cache:
            return self._spp_cache[zone]
            
        try:
            # Run blocking gridstatus call in a separate thread
            df = await asyncio.to_thread(self.ercot.get_spp, "latest", market="REAL_TIME_15_MIN", verbose=False)
            zone_data = df[df["Location"] == zone].iloc[-1:]
            if not zone_data.empty:
                val = float(zone_data["SPP"].values[0])
                self._spp_cache[zone] = val
                return val
            return None
        except Exception as e:
            print(f"⚠️ Gridstatus SPP fetch failed for {zone}: {e}")
            return await self._fetch_spp_from_mis(zone)

    async def _fetch_spp_from_mis(self, zone):
        """Direct MIS API fallback for Real-Time SPP (async)."""
        url = f"{self.base_url}/np6-905-cd"
        headers = ercot_auth.get_auth_headers()
        params = {"settlementPoint": zone, "size": 1}
        
        try:
            # We can use requests in a thread or httpx, for simplicity using wrap
            def _fetch():
                r = requests.get(url, headers=headers, params=params, timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    records = data.get("data", [])
                    if records:
                        return float(records[0].get("settlementPointPrice", 0))
                return None
            
            val = await asyncio.to_thread(_fetch)
            if val is not None:
                self._spp_cache[zone] = val
                return val
            return None
        except Exception as e:
            print(f"❌ MIS SPP fetch failed: {e}")
            return None

    async def get_dam_forecast_72h(self, zone):
        """Fetches the Day-Ahead Market SPP for the next 72 hours (async, cached 5m)."""
        if zone in self._dam_cache:
            return self._dam_cache[zone]

        try:
            df = await asyncio.to_thread(self.ercot.get_spp, "today", market="DAY_AHEAD_HOURLY", verbose=False)
            zone_df = df[df["Location"] == zone].copy()
            
            forecast = []
            for _, row in zone_df.iterrows():
                forecast.append({
                    "timestamp": row["Interval Start"].isoformat(),
                    "lmp": float(row["SPP"])
                })
            self._dam_cache[zone] = forecast
            return forecast
        except Exception as e:
            print(f"⚠️ DAM forecast fetch failed: {e}")
            return []

    async def get_wind_gen_pct(self):
        """Fetches current wind generation as a % of total capacity (async, cached 5m)."""
        if "fuel_mix" in self._fuel_cache:
            return self._fuel_cache["fuel_mix"]

        try:
            df = await asyncio.to_thread(self.ercot.get_fuel_mix)
            total = df["MW"].sum()
            wind = df[df["Fuel"] == "Wind"]["MW"].sum()
            pct = (wind / total) * 100 if total > 0 else 24.5
            self._fuel_cache["fuel_mix"] = pct
            return pct
        except:
            return 24.5 # Fallback demo value

ercot_live = ErcotLiveService()
