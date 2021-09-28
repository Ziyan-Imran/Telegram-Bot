from typing import Text
import telegram
from telegram.ext import Updater, dispatcher
from config import *

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())

# Create updater object: Continously fetches new updates from telegram and passes them on to the Dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

updates = bot.get_updates()
print(updates[0])

bot.send_message(text="Hi Me again!", chat_id=chatId)