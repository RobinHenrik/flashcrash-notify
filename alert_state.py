import time
# (ticker, direction) -> timestamp of last alert
ALERT_HISTORY = {}
COOLDOWN_SECONDS = 30 * 60 # 30 minutes

def should_send_alert(ticker, direction):
    if direction == "":
        return False
    key =(ticker, direction)
    now = time.time()
    last_alert = ALERT_HISTORY.get(key)
    if last_alert and now - last_alert < COOLDOWN_SECONDS:
        print(f"Skipped alert for {ticker} ({direction}), still in cooldown.") # Later logging.
        return False
    ALERT_HISTORY[key] = now
    return True
