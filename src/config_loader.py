import yaml, os
from pathlib import Path

def load_config(path: str = "config.yaml"):
    cfg_path = Path(path)
    if not cfg_path.exists():
        # fall back to example
        cfg_path = Path("config.example.yaml")
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    # override with env vars if set
    alpaca_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret = os.getenv("ALPACA_SECRET_KEY")
    if alpaca_key:
        cfg.setdefault("alpaca", {})["key"] = alpaca_key
        cfg["alpaca"]["enabled"] = True
    if alpaca_secret:
        cfg.setdefault("alpaca", {})["secret"] = alpaca_secret
        cfg["alpaca"]["enabled"] = True
    return cfg
