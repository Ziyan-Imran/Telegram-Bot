"""
Split.py will contain an in-line telegram function that receives a numerical total with 2 digits (float)
,a percentage for tip (int), and number of people (int).
It will return a single number (float).
"""

import logging
import config as keys
from telegram import Update
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, InlineQueryHandler, \
    CallbackContext, inlinequeryhandler


def get_bill_total(update: Update, context: CallbackContext, bill: float, tip: int, num_paying: int) -> float:
    """
    Create bill total
    """
    bill_total = bill + (bill * tip)
    bill_per_person = bill_total / num_paying
    return bill_per_person


def send_bill_to_bot(update: Update, context: CallbackContext, payment: float) -> None:
    """
    Make the bot send the bill total in chat
    """
    string_payment = str(payment)
    context.bot.send_message(chat_id=update.effective_chat.id, text=string_payment)

