from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import ABOUT
from app.chat.group import load_group_manager


def about(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    group_manager = load_group_manager()
    group = group_manager.find_group(chat.id)
    text = str(group)
    update.message.reply_text(text, "html")
    return


handler = CommandHandler(ABOUT, about)
