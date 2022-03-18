from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)
from app.chat.commands import START
from app.chat.message.template import greet_user
from app.chat.states import SELECTING_ORGANIZATION
from app.chat.types import PRIVATE


def start(update: Update, context: CallbackContext) -> int:
    chat = update.message.chat
    user = update.message.from_user
    if chat.type != PRIVATE:
        text = (
            greet_user(user.id, user.first_name)
            + " Ang /start command ay magagamit lamang sa loob po ng private chat."
        )
        update.message.reply_text(text, "html")
        return ConversationHandler.END
    return SELECTING_ORGANIZATION


def first_time_save_organization(update: Update, context: CallbackContext) -> int:
    return


def save_organization(update: Update, context: CallbackContext) -> int:
    return


start_handler = CommandHandler(START, start)
first_time_selection_handler = CallbackQueryHandler(
    first_time_save_organization, pattern=""
)
selection_handler = CallbackQueryHandler(save_organization, pattern="")
organization_selection_handler = ConversationHandler(
    entry_points=[first_time_selection_handler],
    states={SELECTING_ORGANIZATION: [selection_handler]},
    fallbacks=[],
    per_message=True,
    name="organization_selection_handler",
    persistent=True,
)
handler = ConversationHandler(
    entry_points=[start_handler],
    states={SELECTING_ORGANIZATION: [organization_selection_handler]},
    fallbacks=[],
    allow_reentry=True,
    name="start_handler",
    persistent=True,
)
