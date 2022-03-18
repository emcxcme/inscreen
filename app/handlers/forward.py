from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import FORWARD
from app.chat.message.template import greet_user
from app.chat.types import GROUP, PRIVATE, SUPERGROUP
from app.config import CONFIG
from app.saves import GROUP_MANAGER
from app.chat.group import GroupManager


def forward(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    user = update.message.from_user
    if chat.type == PRIVATE:
        if user.id in CONFIG["ADMIN_IDS"]:
            return
        text = (
            greet_user(user.id, user.first_name)
            + " Mga system admin lamang po ang maaaring mag-issue nito."
        )
        update.message.reply_text(text, "html")
        return
    if chat.type != SUPERGROUP:
        text = (
            greet_user(user.id, user.first_name)
            + " Ito po ay magagamit lamang sa loob po ng supergroup."
        )
        if chat.type == GROUP:
            text += (
                " Maano pong paki convert itong group sa supergroup"
                " at mag-issue po ng /register command."
            )
        update.message.reply_text(text, "html")
        return
    group_manager: GroupManager = context.bot_data[GROUP_MANAGER]
    if chat.id not in group_manager.main_groups:
        text = (
            greet_user(user.id, user.first_name)
            + " Sa main group lamang po maaaring mag-issue nito."
        )
        return
    if user in update.message.chat.get_administrators():
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Mga group admin lamang po ang maaaring mag-issue nito."
    )
    update.message.reply_text(text, "html")
    return


handler = CommandHandler(FORWARD, forward)
