import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from typing import Text
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler
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

# Bot will repeat whatever text that the user sends
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# Bot now has a /caps command that will reply to an argument in CAPS
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text = text_caps)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

# Bot now has in-line commands
# Use @caps to let start function
def inline_caps(update, context):
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
dispatcher.add_handler(inline_caps_handler)

# Add bot command when it's sent an incorrect command
# MUST BE ADDED LAST OR IT WILL TRIGGER BEFORE OTHER COMMANDS
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()

updater.idle()