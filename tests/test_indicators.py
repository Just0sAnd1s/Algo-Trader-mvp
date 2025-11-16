import pandas as pd
from core.indicators import compute_rsi, compute_macd

def sample_df():
    return pd.DataFrame({"close": [i for i in range(1, 200)]})

def test_rsi_runs():
    df = compute_rsi(sample_df(), period=14)
    assert "rsi" in df

def test_macd_runs():
    df = compute_macd(sample_df())
    assert "macd" in df
    assert "signal" in df
