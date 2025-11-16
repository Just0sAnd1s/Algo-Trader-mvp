import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml
import os
import sys
sys.path.append("src")

from core.backtester import Backtester
from services.alpaca_client import AlpacaClient

st.set_page_config(page_title="Algo Trading Dashboard", layout="wide")

# ---------- Load config ----------
CONFIG_PATH = "config.yaml"
config = yaml.safe_load(open(CONFIG_PATH))

# ---------- Helper to run backtest ----------
def run_backtest(symbol):
    bt = Backtester(symbol=symbol, config=config)
    df, summary = bt.run()
    return df, summary

# ---------- Sidebar ----------
st.sidebar.header("Settings")

mode = st.sidebar.radio("Mode", ["Backtest", "Live Portfolio"])
symbol = st.sidebar.text_input("Symbol", "AAPL")

if st.sidebar.button("Run"):
    st.session_state["run"] = True

# ---------- Backtest Mode ----------
if mode == "Backtest":
    st.title("📈 Backtest Results")

    if st.session_state.get("run"):
        with st.spinner("Running backtest..."):
            df, summary = run_backtest(symbol)

        st.subheader("Strategy Performance Summary")
        st.json(summary)

        # Plot Equity Curve
        st.subheader("Equity Curve")
        fig, ax = plt.subplots()
        ax.plot(df["equity"])
        ax.set_title("Equity Curve")
        st.pyplot(fig)

        # Plot Drawdown
        st.subheader("Drawdown")
        fig, ax = plt.subplots()
        ax.plot(df["drawdown"])
        ax.set_title("Drawdown")
        st.pyplot(fig)

        # Show Trades
        st.subheader("Trade Log")
        st.dataframe(df[df["trade"].notnull()][["date", "trade", "price", "equity"]])

# ---------- Live Portfolio Mode ----------
else:
    st.title("💼 Live Trading Portfolio")
    alp = AlpacaClient(config)

    acct = alp.get_account()
    positions = alp.get_positions()

    st.subheader("Account Summary")
    st.json(acct)

    st.subheader("Open Positions")
    if positions:
        pos_data = [{
            "symbol": p.symbol,
            "qty": p.qty,
            "avg_price": p.avg_entry_price,
            "current_price": p.current_price,
            "unrealized_pl": p.unrealized_pl
        } for p in positions]
        st.dataframe(pd.DataFrame(pos_data))
    else:
        st.write("No positions currently open.")

st.sidebar.write("---")
st.sidebar.write("Dashboard Ready")
