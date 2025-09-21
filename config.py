ORIGINS = [
    "http://localhost:5173",
    "https://pornokuningad.pro",
]

#rsi_utils.py
RSI_UPPER_LIMIT = 70 # Overbought
RSI_LOWER_LIMIT = 30 # Oversold

#alert_state.py
COOLDOWN_SECONDS = 30 * 60 # 30 minutes

#monitor.py
DROP_THRESHOLD = 0.045 # 10% drop in stock price
RISE_THRESHOLD = 0.045 # 10% rise in stock price
LOOKBACK_MINUTES = 60 # Lookback period in minutes in which the drop threshold is checked against

#TelegramNotifier.py
LY_LINK = "https://lightyear.app.link/"