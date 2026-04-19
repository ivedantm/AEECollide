import httpx
import asyncio
import zipfile
import io
import csv
import pandas as pd
from datetime import datetime, timedelta
from cachetools import TTLCache

class CaisoLiveService:
    """
    Direct OASIS API client for CAISO nodes (SP15, NP15, ZP26, PALOVRDE).
    No authentication needed for public data.
    Uses TTL caching and async fetch with aggressive timeouts.
    """
    def __init__(self):
        self.base_url = "http://oasis.caiso.com/oasisapi/SingleZip"
        self._cache = TTLCache(maxsize=100, ttl=300)

    async def get_latest_lmp(self, node="PALOVRDE_ASR-APND"):
        """Fetches the most recent DAM LMP for a specific CAISO node (async, cached 5m)."""
        cache_key = f"latest_lmp_{node}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        now = datetime.utcnow()
        start_str = (now - timedelta(days=1)).strftime("%Y%m%dT07:00-0000")
        end_str = (now + timedelta(days=1)).strftime("%Y%m%dT07:00-0000")

        params = {
            "queryname": "PRC_LMP",
            "market_run_id": "DAM",
            "startdatetime": start_str,
            "enddatetime": end_str,
            "node": node,
            "resultformat": 6,
            "version": 1,
        }

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(self.base_url, params=params, timeout=10.0, follow_redirects=True)
                if r.status_code == 200:
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    for name in z.namelist():
                        if "INVALID" not in name:
                            with z.open(name) as f:
                                content = f.read().decode("utf-8")
                                reader = csv.DictReader(content.strip().split("\n"))
                                rows = [row for row in reader if row.get("LMP_TYPE") == "LMP"]
                                if rows:
                                    latest_row = sorted(rows, key=lambda x: x["INTERVALSTARTTIME_GMT"])[-1]
                                    val = float(latest_row.get("MW", 0))
                                    self._cache[cache_key] = val
                                    return val
        except Exception as e:
            print(f"⚠️ CAISO fetch timed out or failed for {node}: {e}")
        
        return None

    async def get_dam_forecast_72h(self, node="PALOVRDE_ASR-APND"):
        """Fetches the next 72 hours of DAM LMP for a specific CAISO node (async, cached 5m)."""
        cache_key = f"forecast_{node}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        now = datetime.utcnow()
        start_str = (now - timedelta(days=1)).strftime("%Y%m%dT07:00-0000")
        end_str = (now + timedelta(days=3)).strftime("%Y%m%dT07:00-0000")

        params = {
            "queryname": "PRC_LMP",
            "market_run_id": "DAM",
            "startdatetime": start_str,
            "enddatetime": end_str,
            "node": node,
            "resultformat": 6,
            "version": 1,
        }

        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(self.base_url, params=params, timeout=60.0, follow_redirects=True)
                forecast = []
                if r.status_code == 200:
                    z = zipfile.ZipFile(io.BytesIO(r.content))
                    for name in z.namelist():
                        if "INVALID" not in name:
                            with z.open(name) as f:
                                reader = csv.DictReader(f.read().decode("utf-8").strip().split("\n"))
                                rows = [row for row in reader if row.get("LMP_TYPE") == "LMP"]
                                for row in rows:
                                    ts = pd.Timestamp(row["INTERVALSTARTTIME_GMT"]).tz_convert("US/Central").isoformat()
                                    forecast.append({
                                        "timestamp": ts,
                                        "lmp": float(row.get("MW", 0))
                                    })
                sorted_forecast = sorted(forecast, key=lambda x: x["timestamp"])
                if sorted_forecast:
                    self._cache[cache_key] = sorted_forecast
                return sorted_forecast
        except Exception as e:
            print(f"⚠️ CAISO forecast timed out or failed for {node}: {e}")
            return []

caiso_live = CaisoLiveService()
