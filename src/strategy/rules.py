from .indicators import rsi, macd

def rsi_signal(df, period=14, low=30, high=70):
    df = df.copy()
    df['rsi'] = rsi(df['close'], period)
    if df['rsi'].isna().all():
        return 'HOLD'
    val = df['rsi'].iloc[-1]
    if val < low:
        return 'BUY'
    if val > high:
        return 'SELL'
    return 'HOLD'

def macd_signal(df, fast=12, slow=26, signal_period=9):
    df = df.copy()
    macd_line, signal_line, hist = macd(df['close'], fast, slow, signal_period)
    if len(macd_line) < 2:
        return 'HOLD'
    if (macd_line.iloc[-1].item() > signal_line.iloc[-1].item()) and (macd_line.iloc[-2].item() <= signal_line.iloc[-2].item()):
        return 'BUY'
    # OLD CODE : CAUSES "ValueError: The truth value of a Series is ambiguous" 
    #if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
    #    return 'BUY'
    # if macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]:
    if (macd_line.iloc[-1].item() > signal_line.iloc[-1].item()) and (macd_line.iloc[-2].item() >= signal_line.iloc[-2].item()):
        return 'SELL'
    return 'HOLD'
