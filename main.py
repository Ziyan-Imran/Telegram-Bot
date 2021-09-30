import logging
import constants as keys
import json

from telegram import bot
from telegram.ext.callbackcontext import CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from typing import Text
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler, dispatcher, inlinequeryhandler
from capsbot import *
from timerbot import *
from search_youtube import youtube_search


# Define a few command handlers
def start(update: Update, _: CallbackContext) -> None:
    _.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def error(update: Update, _: CallbackContext) -> None:
    print(f"Update {update} caused error {_.error}")

def unknown(update: Update, _: CallbackContext) -> None:
    _.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main() -> None:
    
    # Create the Updater and pass it my bot's token
    updater = Updater(keys.API_KEY)

    # Get the dispatcher to register handler
    dispatcher = updater.dispatcher

    # Create inline handler for inline_caps module
    inline_query_handler = InlineQueryHandler(inline_query)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("scream", caps))
    dispatcher.add_handler(InlineQueryHandler(inline_query))
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()