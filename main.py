import logging

from telegram import bot
from telegram.ext.callbackcontext import CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from typing import Text
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler, dispatcher, inlinequeryhandler
from config import *
from capsbot import *
from timerbot import *

# Define a few command handlers
def start(update: Update, _: CallbackContext) -> None:
    _.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def unknown(update: Update, _: CallbackContext) -> None:
    _.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main() -> None:
    
    # Create the Updater and pass it my bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handler
    dispatcher = updater.dispatcher

    # Create inline handler for inline_caps module
    inline_caps_handler = InlineQueryHandler(inline_caps)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("scream", caps))
    dispatcher.add_handler(inline_caps_handler)

    # Start the bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()