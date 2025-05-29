import asyncio
import os

from apscheduler.schedulers.blocking import BlockingScheduler

from TelegramNotifier import TelegramNotifier
from market_utils import is_market_open
from monitor import TICKERS, check_price_drop, fetch_sp500_history, DROP_THRESHOLD, RISE_THRESHOLD
from alert_state import should_send_alert
from dotenv import load_dotenv



async def notify_if_major_movement(notifier):
    all_data = fetch_sp500_history()
    for ticker in TICKERS:
        latest_price, past_price, change = check_price_drop(all_data, ticker)
        if latest_price is None or past_price is None or change is None:
            continue
        direction = ""
        if change <= -DROP_THRESHOLD:
            direction = "drop"
        elif change >= RISE_THRESHOLD:
            direction = "rise"
        if should_send_alert(ticker, direction):
            await notifier.notify(ticker, latest_price, past_price, change)


def job():
    if not is_market_open():
        print("market closed")
        return

    print("Job started")
    # Token and group_id come from the .env file
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    group_id = os.getenv("TELEGRAM_GROUP_ID")
    notifier = TelegramNotifier(token, group_id)
    asyncio.run(notify_if_major_movement(notifier))

if __name__ == "__main__":
    load_dotenv() # Load the .env file in
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=1) # Runs jobs sequentially
    scheduler.start()
