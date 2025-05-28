import asyncio
from monitor import TICKERS, DROP_THRESHOLD, RISE_THRESHOLD, check_price_drop
from TelegramNotifier import TelegramNotifier

async def notify_if_major_movement(notifier):
    for ticker in TICKERS:
        latest_price, past_price, change = check_price_drop(ticker)
        if latest_price is None or past_price is None or change is None:
            continue

        if change <= -DROP_THRESHOLD:
            message = (
                f"🚨 *MAJOR PRICE DROP* 🚨\n"
                f"${ticker}\n"
                f"Current: ${latest_price:.2f}\n"
                f"Prev: ${past_price:.2f}\n"
                f"Change: {change * 100:.2f} %"
            )
            await notifier.send_message(escape_markdown(message))
        elif change >= RISE_THRESHOLD:
            message = (
                f"🚀 *MAJOR PRICE RISE* 🚀\n"
                f"${ticker}\n"
                f"Current: ${latest_price:.2f}\n"
                f"Prev: ${past_price:.2f}\n"
                f"Change: {change * 100:.2f} %"
            )
            await notifier.send_message(escape_markdown(message))
        else:
            message = (
                f"😴😴 *No major movement* 😴😴\n"
                f"${ticker}\n"
                f"Current: ${latest_price:.2f}\n"
                f"Prev: ${past_price:.2f}\n"
                f"Change: {change * 100:.2f} %"
            )
            await notifier.send_message(escape_markdown(message))

def escape_markdown(text):
    escape_chars = r'-.!'
    return ''.join('\\' + c if c in escape_chars else c for c in text)

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()
    # Token and group_id come from the .env file
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    group_id = os.getenv("TELEGRAM_GROUP_ID")
    notifier = TelegramNotifier(token, group_id)
    asyncio.run(notify_if_major_movement(notifier))