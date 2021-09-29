import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from typing import Text
import telegram
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters
from config import *

# Create updater object: Continously fetches new updates from telegram and passes them on to the Dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())

# Function called when the Bot receievs a certain command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Bot responds to when user types the '/start/ command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()