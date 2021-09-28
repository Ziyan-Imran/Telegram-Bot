from typing import Text
import telegram
from config import *

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())

updates = bot.get_updates()
print(updates[0])

bot.send_message(text="Hi Me again!", chat_id=chatId)