import os
import joblib
import numpy as np
import lightgbm as lgb
import pandas as pd

class RegimeClassifierML:
    """
    ML-powered regime classifier using trained LightGBM model.
    Falls back to rule-based classification if model files are missing.
    """
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
        self.model_path = os.path.join(self.models_dir, "regime_classifier.txt")
        self.le_path = os.path.join(self.models_dir, "regime_label_encoder.pkl")
        self.feat_path = os.path.join(self.models_dir, "regime_features.pkl")
        
        self.model = None
        self.le = None
        self.features = None
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model = lgb.Booster(model_file=self.model_path)
                self.le = joblib.load(self.le_path)
                self.features = joblib.load(self.feat_path)
                print("✅ ML Regime Classifier loaded successfully.")
        except Exception as e:
            print(f"⚠️ Failed to load ML Regime Classifier: {e}")

    def classify(self, feature_dict):
        """
        Classifies current regime based on ML model or fallback rules.
        Returns: (regime_name, confidence_score)
        """
        if self.model and self.le and self.features:
            try:
                # Build feature vector in correct order
                X = [feature_dict.get(f, 0) for f in self.features]
                probs = self.model.predict([X])[0]
                idx = np.argmax(probs)
                regime = self.le.classes_[idx]
                confidence = float(probs[idx])
                return regime, confidence
            except Exception as e:
                print(f"⚠️ ML Prediction failed: {e}")
        
        # Rule-based fallback
        return self._rule_based_classify(feature_dict), 0.85

    def _rule_based_classify(self, fd):
        lmp = fd.get("lmp", 35)
        spread = fd.get("spread", 5)
        temp = fd.get("temp_f", 75)
        wind = fd.get("wind_speed", 10)

        if lmp >= 5000: return "uri_emergency"
        if lmp >= 500 and temp <= 20: return "winter_storm"
        if lmp >= 200 or (lmp >= 100 and temp >= 95): return "scarcity"
        if temp >= 90 and lmp >= 50: return "heat_dome"
        if lmp <= 5 and wind >= 20: return "wind_glut"
        if lmp <= 15 and spread <= 0: return "oversupply"
        return "normal"

regime_classifier_ml = RegimeClassifierML()
