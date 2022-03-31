from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import UNPIN
from app.chat.message.template import greet_user
from app.chat.types import GROUP, PRIVATE, SUPERGROUP
from app.config import CONFIG
from app.configs import ADMIN_IDS
from app.chat.group import load_group_manager


def unpin(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    user = update.message.from_user
    group_manager = load_group_manager()
    if chat.type == PRIVATE:
        if user.id in CONFIG[ADMIN_IDS]:
            for main_group in group_manager.main_groups.values():
                context.bot.unpin_all_chat_messages(main_group.id)
            for subgroup in group_manager.subgroups.values():
                context.bot.unpin_all_chat_messages(subgroup.id)
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
    if chat.id not in group_manager.main_groups:
        text = (
            greet_user(user.id, user.first_name)
            + " Sa main group lamang po maaaring mag-issue nito."
        )
        return
    group_admins = update.message.chat.get_administrators()
    group_admin_ids = [group_admin.user.id for group_admin in group_admins]
    if user.id in group_admin_ids:
        main_group = group_manager.find_group(chat.id)
        context.bot.unpin_all_chat_messages(main_group.id)
        for subgroup in main_group.subgroups:
            context.bot.unpin_all_chat_messages(subgroup.id)
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Mga group admin lamang po ang maaaring mag-issue nito."
    )
    update.message.reply_text(text, "html")
    return


handler = CommandHandler(UNPIN, unpin)
