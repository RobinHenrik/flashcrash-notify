from telegram import Bot
import logging

from config import RISE_THRESHOLD, DROP_THRESHOLD, LY_LINK

alerts_handler = logging.FileHandler("alerts.log")
alerts_handler.setLevel(logging.INFO)
alerts_handler.setFormatter(logging.Formatter("%(asctime)s ALERT [%(name)s] %(message)s"))
alert_logger = logging.getLogger('alerts')
alert_logger.addHandler(alerts_handler)
alert_logger.propagate = False  # Prevents alerts from being logged in the main file as well



def escape_markdown(text):
    escape_chars = r'-.!()'
    return ''.join('\\' + c if c in escape_chars else c for c in text)

def format_message(ticker, latest_price, past_price, change, rsi):
    message = ""
    if change <= -DROP_THRESHOLD:
        message += f"🚨 *MAJOR PRICE DROP* 🚨\n"
    elif change >= RISE_THRESHOLD:
        message += f"🚀 *MAJOR PRICE RISE* 🚀\n"
    else:
        message += f"😴😴 *No major movement* 😴😴\n"

    message += (
        f"[${ticker}]({LY_LINK})\n"
        f"Current: ${latest_price:.2f}\n"
        f"Prev: ${past_price:.2f}\n"
        f"Change: {change * 100:.2f}%\n"
        f"14-day RSI: {rsi}"
    )

    if rsi < 30:
        message += " (oversold)"
    elif rsi > 70:
        message += " (overbought)"

    return escape_markdown(message)


class TelegramNotifier:
    def __init__(self, token, group_id):
        self.bot = Bot(token=token)
        self.group_id = group_id

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.group_id, text=message, parse_mode="MarkdownV2")

    async def notify(self, ticker, latest_price, past_price, change, rsi):
        direction = "RISE" if change >= RISE_THRESHOLD else "DROP"
        message = format_message(ticker, latest_price, past_price, change, rsi)
        alert_logger.info(f"Sent {direction} alert for ${ticker}: change={change:.2%} from ${past_price:.2f} to ${latest_price:.2f}, RSi={rsi}")
        await self.send_message(message)