import backtrader as bt
import pandas as pd
from loguru import logger

class PandasData(bt.feeds.PandasData):
    cols = (('volume','volume'),)

class MAStrategy(bt.Strategy):
    params = dict(
        rsi_period=14,
        macd_fast=12,
        macd_slow=26,
        macd_signal=9,
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.rsi_period)
        self.macd = bt.indicators.MACD(self.data.close, period_me1=self.p.macd_fast, period_me2=self.p.macd_slow, period_signal=self.p.macd_signal)
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if not self.position:
            if self.rsi < 30 and self.crossover > 0:
                self.buy()
        else:
            if self.rsi > 70 and self.crossover < 0:
                self.close()

def run_backtest(df, cash=10000):
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)
    cerebro.addstrategy(MAStrategy)
    cerebro.broker.setcash(cash)
    start = cerebro.broker.getvalue()
    cerebro.run()
    end = cerebro.broker.getvalue()
    logger.info(f'Backtest start: {start} end: {end} pnl: {end-start}')
    try:
        cerebro.plot(style='candlestick')
    except Exception:
        pass
