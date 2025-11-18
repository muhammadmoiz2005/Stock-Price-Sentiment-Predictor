import joblib
import os
import numpy as np
import pandas as pd

MODEL_PATH = 'models/price_predictor.pkl'

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError('Model not found. Train model first using model_train.py')
    obj = joblib.load(MODEL_PATH)
    return obj['model'], obj['features']

def predict_from_row(row: pd.Series):
    model, features = load_model()
    X = row[features].values.reshape(1, -1)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X).max()
    return {'direction': 'UP' if pred==1 else 'DOWN', 'confidence': float(proba)}

