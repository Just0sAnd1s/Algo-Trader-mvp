import argparse, time
from src.config_loader import load_config
from src.logger import logger
from src.data import get_stock_data
from src.strategy.engine import combined_signal
from src.trading import execute_buy
from src.backtest import run_backtest

import schedule

parser = argparse.ArgumentParser()
parser.add_argument("--mode", choices=['live','backtest','once'], required=True, help='live/backtest/once')
parser.add_argument("--symbol", default=None)
args = parser.parse_args()

cfg = load_config()
symbols = cfg.get('strategy', {}).get('symbols', ['AAPL'])

def run_once(symbol):
    df = get_stock_data(symbol, days=365)
    if df is None or df.empty:
        logger.error(f"No data for {symbol}")
        return
    if args.mode=='backtest':
        run_backtest(df)
        return
    sig, votes = combined_signal(df, cfg.get('strategy', {}))
    logger.info(f"{symbol} signal: {sig} votes: {votes}")
    if sig=='BUY':
        res = execute_buy(symbol, qty=cfg.get('trading', {}).get('buy_qty',1))
        logger.info(f"Order result: {res}")

def job():
    for s in ( [args.symbol] if args.symbol else symbols ):
        run_once(s)

if args.mode=='live':
    # use schedule to run at interval
    interval = cfg.get('scheduler', {}).get('interval_minutes',5)
    schedule.every(interval).minutes.do(job)
    logger.info(f"Starting live scheduler every {interval} minutes for {symbols}")
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    # single run
    if args.symbol:
        run_once(args.symbol)
    else:
        for s in symbols:
            run_once(s)
