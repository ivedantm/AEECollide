import os
import joblib
import numpy as np
import lightgbm as lgb
from datetime import datetime

class QuantileForecasterML:
    """
    ML-powered spread forecasting using three quantile LightGBM models (p10, p50, p90).
    Provides a probabilistic view of future market conditions.
    """
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
        self.feat_path = os.path.join(self.models_dir, "forecast_features.pkl")
        
        self.models = {}
        self.features = None
        self._load_models()

    def _load_models(self):
        try:
            if os.path.exists(self.feat_path):
                self.features = joblib.load(self.feat_path)
                for p in ["p10", "p50", "p90"]:
                    path = os.path.join(self.models_dir, f"spread_forecaster_{p}.txt")
                    if os.path.exists(path):
                        self.models[p] = lgb.Booster(model_file=path)
                print(f"✅ ML Quantile Forecasters loaded: {list(self.models.keys())}")
        except Exception as e:
            print(f"⚠️ Failed to load ML Forecasters: {e}")

    def predict_spread(self, current_features, horizon_h):
        """
        Predicts spread quantiles for a specific horizon (h hours ahead).
        """
        if not self.models or not self.features:
            # Fallback to simple random drift if no models
            base = current_features.get("spread", 5)
            return {
                "p10": base - 5 - (horizon_h * 0.1),
                "p50": base,
                "p90": base + 10 + (horizon_h * 0.2)
            }

        try:
            # Build feature vector for the target horizon
            # Features: ['lmp', 'spread', 'gas_price', 'temp_f', 'wind_speed', 'hour', 'month', 'weekday', 'lmp_6h_lag', 'lmp_trend_6h', 'horizon', 'hour_sin', 'hour_cos']
            fd = current_features.copy()
            fd["horizon"] = horizon_h
            
            # Predict cyclical hour for the future horizon
            future_hour = (fd.get("hour", 0) + horizon_h) % 24
            fd["hour_sin"] = np.sin(2 * np.pi * future_hour / 24)
            fd["hour_cos"] = np.cos(2 * np.pi * future_hour / 24)

            X = [fd.get(f, 0) for f in self.features]
            
            results = {}
            for p, model in self.models.items():
                results[p] = float(model.predict([X])[0])
            
            return results
        except Exception as e:
            print(f"⚠️ ML Prediction failure for horizon {horizon_h}: {e}")
            return {"p10": 0, "p50": 5, "p90": 20}

quantile_forecaster_ml = QuantileForecasterML()
