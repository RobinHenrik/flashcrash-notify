from telegram import Bot

class TelegramNotifier:
    def __init__(self, token, group_id):
        self.bot = Bot(token=token)
        self.group_id = group_id

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.group_id, text=message, parse_mode="MarkdownV2")