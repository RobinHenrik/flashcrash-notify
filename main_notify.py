import asyncio
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from TelegramNotifier import TelegramNotifier
from alert_state import should_send_alert
from market_utils import is_market_open
from monitor import TICKERS, check_price_drop, fetch_sp500_history, DROP_THRESHOLD, RISE_THRESHOLD

main_handler = logging.FileHandler("flashcrash_logs.log")
main_handler.setLevel(logging.INFO)
main_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
# Set up logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[main_handler]
)


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
        return

    logging.info("Job started")
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
