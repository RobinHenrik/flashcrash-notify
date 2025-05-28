import asyncio

from TelegramNotifier import TelegramNotifier
from monitor import TICKERS, check_price_drop, fetch_sp500_history


async def notify_if_major_movement(notifier):
    all_data = fetch_sp500_history()
    for ticker in TICKERS:
        latest_price, past_price, change = check_price_drop(all_data, ticker)
        if latest_price is None or past_price is None or change is None:
            continue

        await notifier.notify(ticker, latest_price, past_price, change)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    # Token and group_id come from the .env file
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    group_id = os.getenv("TELEGRAM_GROUP_ID")
    notifier = TelegramNotifier(token, group_id)
    asyncio.run(notify_if_major_movement(notifier))