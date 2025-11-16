from .config_loader import load_config
cfg = load_config()
USE_ALPACA = cfg.get('alpaca', {}).get('enabled', False)

try:
    if USE_ALPACA:
        from alpaca.trading.client import TradingClient
        ALPACA_KEY = cfg['alpaca']['key']
        ALPACA_SECRET = cfg['alpaca']['secret']
        client = TradingClient(ALPACA_KEY, ALPACA_SECRET, paper=True)
except Exception as e:
    USE_ALPACA = False

def execute_buy(symbol, qty=1):
    if USE_ALPACA:
        try:
            order = client.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='day')
            return order
        except Exception as e:
            return None
    else:
        # simulate paper order
        return {'symbol':symbol,'qty':qty,'status':'paper_submitted'}
