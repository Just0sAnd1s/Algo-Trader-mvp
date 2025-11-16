# Algo Trading MVP

Minimal, opinionated, ready-to-run algorithmic trading prototype.

Provided tools:
- Multi-symbol scanning
- RSI + MACD indicators
- Simple RandomForest ML signal
- Backtesting with Backtrader
- Live paper trading (Alpaca) if keys available
- Scheduler for periodic runs (using GitHub Actions or local loop)

## Quick start (local)
1. Create a virtualenv and activate it.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy example config:
   ```
   cp config.example.yaml config.yaml
   ```
   Then fill in Alpaca keys (optional).
4. Run a backtest:
   ```
   python run.py --mode backtest --symbol AAPL
   ```
5. Run live/paper (will only place paper orders if keys present and enabled):
   ```
   python run.py --mode live
   ```
6. How to run the dashboard
```
pip install streamlit matplotlib pyyaml
streamlit run dashboard/app.py
```
## Notes
- The code will use Alpaca market data if ALPACA keys are present, otherwise it falls back to yfinance for historical data.
- For GitHub Actions scheduling, see `.github/workflows/run-bot.yml`.
- Logs are written to `logs/trades.log`.
