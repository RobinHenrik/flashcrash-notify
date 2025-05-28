import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot

#Move to the main file
load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")
group_id = os.getenv("TELEGRAM_GROUP_ID")
#

class TelegramNotifier:
    def __init__(self, token, group_id):
        self.bot = Bot(token=token)
        self.group_id = group_id

    async def send_message(self, message):
        await self.bot.send_message(chat_id=group_id, text=message, parse_mode="MarkdownV2")


notifier = TelegramNotifier(token, group_id)

async def main():
    await notifier.send_message("omo *ratas*")

asyncio.run(main())