from strategies.rsi_macd_strategy import RSIMACDStrategy
import pandas as pd

def test_strategy_outputs_signal():
    strat = RSIMACDStrategy()
    df = pd.DataFrame({"close": [1,2,3], "rsi": [30, 60, 70], "macd": [0.1, -0.2, 0.5], "signal": [0.05, -0.1, 0.3]})
    signal = strat.generate_signal(df)
    assert signal in ["BUY", "SELL", "HOLD"]
