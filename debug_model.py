import pickle
import os

model_path = 'c:/AI/Machine Learning/PACK_PREMIUM_CANCER_AI/models/cancer_risk_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        if hasattr(model, 'feature_names_in_'):
            print("Feature Names In:", model.feature_names_in_)
        else:
            print("No feature_names_in_ found")
else:
    print("Model not found")
