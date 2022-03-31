from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from typing import List
from app.chat.commands import REGISTER
from app.chat.group import (
    MainGroup,
    Subgroup,
    load_group_manager,
    save_group_manager,
)
from app.chat.message.template import greet_user
from app.chat.types import GROUP, SUPERGROUP
from app.config import CONFIG
from app.configs import ADMIN_IDS


def _is_empty_argument(args: List[str]) -> bool:
    if args == None:
        return True
    if args == []:
        return True
    return False


def _is_valid_argument(args: List[str]) -> bool:
    for arg in args:
        if not arg.isalnum():
            return False
    return True


def alert_empty_argument() -> None:
    return


def alert_invalid_argument() -> None:
    return


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
    if user.id in CONFIG[ADMIN_IDS]:
        if _is_empty_argument(context.args):
            alert_empty_argument()
            return
        if not _is_valid_argument(context.args):
            alert_invalid_argument()
            return
        group_manager = load_group_manager()
        program_name = " ".join(context.args).upper()
        group = group_manager.add_group(chat.id, program_name)
        save_group_manager(group_manager)
        if not (isinstance(group, MainGroup) or isinstance(group, Subgroup)):
            return
        text = "Group registered successfully.\n\n" + str(group)
        update.message.reply_text(text, "html")
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Mga system admin lamang po ang maaaring mag-issue nito."
    )
    update.message.reply_text(text, "html")


handler = CommandHandler(REGISTER, register_group)
