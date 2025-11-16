from .rules import rsi_signal, macd_signal
from .ml_model import MLSignalModel

ML = MLSignalModel()

def combined_signal(df, cfg):
    signals = []
    # RSI
    signals.append(rsi_signal(df, period=cfg.get('rsi_period',14)))
    # MACD
    signals.append(macd_signal(df, fast=cfg.get('macd_fast',12), slow=cfg.get('macd_slow',26), signal_period=cfg.get('macd_signal',9)))
    # ML
    if cfg.get('use_ml_model', False):
        try:
            # attempt training if not trained
            if not ML.is_trained:
                ML.train(df)
            signals.append(ML.predict(df))
        except Exception as e:
            signals.append('HOLD')
    # voting
    buy_votes = signals.count('BUY')
    sell_votes = signals.count('SELL')
    if buy_votes >= 2:
        return 'BUY', signals
    if sell_votes >= 2:
        return 'SELL', signals
    # default: if any BUY and no SELL, small bias
    if buy_votes > sell_votes:
        return 'BUY', signals
    if sell_votes > buy_votes:
        return 'SELL', signals
    return 'HOLD', signals
