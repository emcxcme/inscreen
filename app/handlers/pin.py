from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from app.chat.commands import PIN
from app.chat.message.template import greet_user
from app.chat.types import GROUP, PRIVATE, SUPERGROUP
from app.config import CONFIG
from app.configs import ADMIN_IDS
from app.chat.group import load_group_manager
from app.user_saves import LAST_SENT_PRIVATE_MESSAGE_ID, LAST_SENT_SUPERGROUP_MESSAGE_ID


def pin(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    user = update.message.from_user
    user_data = context.user_data
    group_manager = load_group_manager()
    if chat.type == PRIVATE:
        if user.id in CONFIG[ADMIN_IDS]:
            for main_group in group_manager.main_groups.values():
                keyed_last_sent_private_message_id = (
                    str(main_group.id) + LAST_SENT_PRIVATE_MESSAGE_ID
                )
                context.bot.pin_chat_message(
                    main_group.id, user_data[keyed_last_sent_private_message_id],
                )
            for subgroup in group_manager.subgroups.values():
                keyed_last_sent_private_message_id = (
                    str(subgroup.id) + LAST_SENT_PRIVATE_MESSAGE_ID
                )
                context.bot.pin_chat_message(
                    subgroup.id, user_data[keyed_last_sent_private_message_id],
                )
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
        keyed_last_sent_supergroup_message_id = (
            str(main_group.id) + LAST_SENT_SUPERGROUP_MESSAGE_ID
        )
        context.bot.pin_chat_message(
            main_group.id, user_data[keyed_last_sent_supergroup_message_id]
        )
        for subgroup in main_group.subgroups:
            keyed_last_sent_supergroup_message_id = (
                str(subgroup.id) + LAST_SENT_SUPERGROUP_MESSAGE_ID
            )
            context.bot.pin_chat_message(
                subgroup.id, user_data[keyed_last_sent_supergroup_message_id],
            )
        return
    text = (
        greet_user(user.id, user.first_name)
        + " Mga group admin lamang po ang maaaring mag-issue nito."
    )
    update.message.reply_text(text, "html")
    return


handler = CommandHandler(PIN, pin)
