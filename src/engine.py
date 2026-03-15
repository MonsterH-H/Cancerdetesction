import joblib
import os
import numpy as np
import pandas as pd
import warnings

# Suppress inconsistent version warnings since we handled it by re-saving
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

class PredictionEngine:
    def __init__(self, model_path='models/cancer_risk_model.pkl'):
        self.model_path = model_path
        self._feature_names = [
            "Age", "Gender", "Air Pollution", "Alcohol use", "Dust Allergy", 
            "OccuPational Hazards", "Genetic Risk", "chronic Lung Disease", 
            "Balanced Diet", "Obesity", "Smoking", "Passive Smoker", 
            "Chest Pain", "Coughing of Blood", "Fatigue", "Weight Loss", 
            "Shortness of Breath", "Wheezing", "Swallowing Difficulty", 
            "Clubbing of Finger Nails", "Frequent Cold", "Dry Cough", "Snoring"
        ]
        self.model = self._load_model()
        
    def _load_model(self):
        paths = [self.model_path, 'models/cancer_risk_model.pkl', 'cancer_risk_model.pkl']
        for path in paths:
            if os.path.exists(path):
                try:
                    # Utilisation de joblib pour la compatibilité sklearn
                    return joblib.load(path)
                except Exception:
                    continue
        return None

    def get_feature_importance(self):
        if self.model is None or not hasattr(self.model, 'feature_importances_'):
            return None
        
        importances = self.model.feature_importances_
        if len(importances) != len(self._feature_names):
            features = [f"F{i}" for i in range(len(importances))]
        else:
            features = self._feature_names
            
        df_importance = pd.DataFrame({
            'Feature': features,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        return df_importance

    def predict(self, features_list):
        if self.model is None:
            raise ValueError("Moteur de modèle IA non chargé.")
        
        # DataFrame pour garder les noms de colonnes et éviter les warnings
        X = pd.DataFrame([features_list], columns=self._feature_names)
        
        prediction = self.model.predict(X)[0]
        
        probabilities = None
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(X)[0]
            
        return prediction, probabilities

    def get_feature_names(self):
        return self._feature_names
