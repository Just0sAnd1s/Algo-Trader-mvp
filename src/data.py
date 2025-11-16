from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from .config_loader import load_config

cfg = load_config()
USE_ALPACA = cfg.get("alpaca", {}).get("enabled", False)

try:
    if USE_ALPACA:
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame
        ALPACA_KEY = cfg['alpaca']['key']
        ALPACA_SECRET = cfg['alpaca']['secret']
        alpaca_client = StockHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)
except Exception as e:
    USE_ALPACA = False

def get_stock_data(symbol: str, days: int = 365, timeframe: str = "1d"):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    if USE_ALPACA:
        try:
            req = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Day,
                start=start,
                end=end
            )
            bars = alpaca_client.get_stock_bars(req).df
            # alpaca returns multiindex if multiple symbols; keep single symbol
            if isinstance(bars.index, pd.MultiIndex):
                bars = bars.xs(symbol, level=1)
            bars = bars.rename(columns={'timestamp':'datetime', 't':'timestamp'})
            bars = bars.reset_index().set_index('timestamp')
            bars.index = pd.to_datetime(bars.index)
            # ensure OHLCV columns standard names
            bars = bars.rename(columns={'open':'open','high':'high','low':'low','close':'close','volume':'volume'})
            return bars[['open','high','low','close','volume']]
        except Exception as e:
            print('Alpaca data fetch failed:', e)
    # fallback yfinance
    try:
        df = yf.download(symbol, period=f"{days}d", interval='1d', progress=False)
        df = df.rename(columns={'Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'})
        return df[['open','high','low','close','volume']]
    except Exception as e:
        print('yfinance fetch failed:', e)
        return None
