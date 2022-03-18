from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import REGISTER
from app.chat.group import Manager
from app.chat.message.template import greet_user
from app.chat.types import GROUP, SUPERGROUP
from app.config import CONFIG


def register_group(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    user = update.message.from_user
    if chat.type != SUPERGROUP:
        text = (
            greet_user(user.id, user.first_name)
            + " Ito po ay magagamit lamang sa loob po ng supergroup."
        )
        if chat.type == GROUP:
            text += (
                " Maano pong paki convert itong group sa supergroup"
                " at mag-reissue po ng /register command."
            )
        update.message.reply_text(text, "html")
        return
    if user.id in CONFIG["ADMIN_IDS"]:
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Mga system admin lamang po ang maaaring mag-issue nito."
    )
    update.message.reply_text(text, "html")


handler = CommandHandler(REGISTER, register_group)
