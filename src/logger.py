from loguru import logger
import os
os.makedirs("logs", exist_ok=True)
logger.add("logs/trades.log", rotation="10 MB", retention="10 days")
