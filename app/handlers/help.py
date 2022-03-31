from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import HELP


def help(update: Update, context: CallbackContext) -> None:
    return


handler = CommandHandler(HELP, help)
