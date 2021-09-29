# Simple bot program to in line query commands and a /caps command
import logging
from uuid import uuid4

import telegram 
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, ParseMode
from telegram import Update
from telegram import update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackContext, inlinequeryhandler
from telegram.utils.helpers import escape_markdown
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
def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id = str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]
    context.bot.answer_inline_query(update.inline_query.id, results)

    update.inline_query.answer(results)

inline_caps_handler = InlineQueryHandler(inline_query)



def main() -> None:
    """Run bot"""
    # Create the Update and pass it my bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands 
    dispatcher.add_handler(CommandHandler("scream", caps))

    # on non command i.e message - echo the mesasge on Telegram
    dispatcher.add_handler(InlineQueryHandler(inline_query))

    # Start the bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

