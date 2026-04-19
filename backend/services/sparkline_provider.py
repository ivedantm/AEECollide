import os
import pandas as pd
from datetime import datetime, timedelta

class SparklineProvider:
    """
    Provides historical LMP/Spread data from the parquet dataset.
    Used for sparklines and historical trend views.
    """
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      "data", "historical_spreads.parquet")
        self._df = None
        self._last_loaded = None

    def _load_data(self):
        """Lazy loads parquet data and caches for 1 hour."""
        now = datetime.now()
        if self._df is not None and self._last_loaded and now - self._last_loaded < timedelta(hours=1):
            return self._df
        
        if os.path.exists(self.data_path):
            try:
                self._df = pd.read_parquet(self.data_path)
                self._last_loaded = now
                print(f"✅ SparklineProvider: Loaded {len(self._df)} rows from parquet.")
                return self._df
            except Exception as e:
                print(f"⚠️ SparklineProvider load error: {e}")
        return None

    def get_history(self, settlement_point, site_id, hours=24):
        """Returns the last N hours of data for a specific site."""
        df = self._load_data()
        if df is None:
            return []

        # Filter for site
        site_df = df[df["site_id"] == site_id].sort_values("ts")
        if site_df.empty:
            return []

        # Get last N rows
        tail = site_df.tail(hours)
        
        history = []
        for i, (_, row) in enumerate(tail.iterrows()):
            history.append({
                "hour": i,
                "hour_label": row["ts"].strftime("%H:%M"),
                "lmp": float(row["lmp"]),
                "spread": float(row["spread"]),
                "settlement_point": settlement_point
            })
        return history

sparkline_provider = SparklineProvider()
