from telegram import Bot
from monitor import DROP_THRESHOLD, RISE_THRESHOLD

LINK = "https://lightyear.app.link/"

def escape_markdown(text):
    escape_chars = r'-.!'
    return ''.join('\\' + c if c in escape_chars else c for c in text)

def format_message(ticker, latest_price, past_price, change):
    message = ""
    if change <= -DROP_THRESHOLD:
        message += f"🚨 *MAJOR PRICE DROP* 🚨\n"
    elif change >= RISE_THRESHOLD:
        message += f"🚀 *MAJOR PRICE RISE* 🚀\n"
    else:
        message += f"😴😴 *No major movement* 😴😴\n"

    message += (
        f"[${ticker}]({LINK})\n"
        f"Current: ${latest_price:.2f}\n"
        f"Prev: ${past_price:.2f}\n"
        f"Change: {change * 100:.2f} %"
    )
    return escape_markdown(message)


class TelegramNotifier:
    def __init__(self, token, group_id):
        self.bot = Bot(token=token)
        self.group_id = group_id

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.group_id, text=message, parse_mode="MarkdownV2")

    async def notify(self, ticker, latest_price, past_price, change):
        if change <= -DROP_THRESHOLD or change >= RISE_THRESHOLD:
            message = format_message(ticker, latest_price, past_price, change)
            await self.send_message(message)
        '''
        else:
            await self.send_message(format_message(ticker, latest_price, past_price, change))
        '''