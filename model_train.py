import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['return'] = df['close'].pct_change()
    df['ma_3'] = df['close'].rolling(3).mean()
    df['ma_10'] = df['close'].rolling(10).mean()
    df['vol_3'] = df['volume'].rolling(3).mean()
    df['target'] = (df['return'].shift(-1) > 0).astype(int)
    df = df.dropna().reset_index(drop=True)
    return df

def train_and_save(model_path: str = 'models/price_predictor.pkl'):
    os.makedirs('models', exist_ok=True)
    df = pd.read_csv('data/historical.csv', parse_dates=['timestamp'])
    data = prepare_features(df)
    features = ['return','ma_3','ma_10','vol_3']
    X = data[features]
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print('Classification report:\n', classification_report(y_test, preds))
    joblib.dump({'model': model, 'features': features}, model_path)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_and_save()
