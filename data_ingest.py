import os
import pandas as pd
from datetime import datetime
from typing import Optional

try:
    from pybit.unified_trading import HTTP
except Exception:
    HTTP = None  # fallback if pybit not installed

API_KEY = os.getenv("BYBIT_API_KEY", "")
API_SECRET = os.getenv("BYBIT_API_SECRET", "")

session = None
if HTTP and API_KEY and API_SECRET:
    try:
        session = HTTP(
            testnet=False,  # change to True for Bybit testnet
            api_key=API_KEY,
            api_secret=API_SECRET
        )
        print("✅ Bybit API session initialized successfully.")
    except Exception as e:
        print(f"⚠️ Failed to initialize Bybit session: {e}")
else:
    if not HTTP:
        print("❌ pybit library not installed. Using fallback data.")
    else:
        print("⚠️ BYBIT API keys not set. Using fallback CSV/sample data.")


def get_historical_klines(symbol: str = "BTCUSDT", interval: str = "1", limit: int = 200, save_csv: bool = True) -> pd.DataFrame:
    """
    Returns DataFrame with columns: timestamp, close, volume
    Bybit interval values: 1, 3, 5, 15, 30, 60, 240, D, W, M
    """
    if session is None:
        # fallback: try loading from local CSV or generate synthetic data
        local = os.path.join("data", "historical.csv")
        if os.path.exists(local):
            df = pd.read_csv(local, parse_dates=["timestamp"])
            return df
        # synthetic fallback
        import numpy as np
        now = pd.date_range(end=datetime.utcnow(), periods=limit, freq='T')
        prices = 50000 + (np.cumsum(np.random.randn(limit)) * 20)
        df = pd.DataFrame({
            "timestamp": now,
            "close": prices,
            "volume": np.random.randint(1, 100, size=limit)
        })
        df.to_csv(local, index=False)
        return df

    try:
        response = session.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        data = response['result']['list']
        df = pd.DataFrame(data, columns=[
            "start_time", "open", "high", "low", "close", "volume", "_"
        ])
        df["timestamp"] = pd.to_datetime(df["start_time"], unit='s')
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)
        out = df[["timestamp", "close", "volume"]].sort_values("timestamp")
        if save_csv:
            os.makedirs("data", exist_ok=True)
            out.to_csv("data/historical.csv", index=False)
        return out
    except Exception as e:
        print(f"⚠️ Error fetching Bybit historical data: {e}")
        return pd.DataFrame()


def get_latest_price(symbol: str = "BTCUSDT") -> Optional[float]:
    """Fetch latest live price for the given symbol"""
    if session is None:
        return None
    try:
        ticker = session.get_tickers(category="linear", symbol=symbol)
        price = float(ticker["result"]["list"][0]["lastPrice"])
        return price
    except Exception as e:
        print(f"⚠️ Error fetching latest Bybit price: {e}")
        return None


if __name__ == '__main__':
    df = get_historical_klines(limit=200)
    print(df.tail())
    print('Latest price:', get_latest_price('BTCUSDT'))

