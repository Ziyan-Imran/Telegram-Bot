# Simple bot program to add /Caps and Caps inline commands
import logging

import telegram 
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram import Update
from telegram import update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext, inlinequeryhandler
from config import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Begin creating functions for /caps and Caps inline commands

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text = text_caps)

# Bot now has in-line commands
# Use @Memebot or @ZTele_bot to let start function
def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(inline_caps)


def main() -> None:
    """Run bot"""
    # Create the Update and pass it my bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands 
    dispatcher.add_handler(CommandHandler("scream", caps))
    dispatcher.add_handler(inline_caps_handler)

    # Start the bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

