from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler
from app.chat.group import load_group_manager
from app.chat.types import PRIVATE, SUPERGROUP
from app.user_saves import LAST_PRIVATE_MESSAGE_ID, LAST_SUPERGROUP_MESSAGE_ID


def receive_image(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    message = update.message
    user_data = context.user_data
    group_manager = load_group_manager()
    if chat.type == PRIVATE:
        user_data[LAST_PRIVATE_MESSAGE_ID] = message.message_id
        return
    if chat.type != SUPERGROUP:
        return
    if chat.id in group_manager.main_groups:
        user_data[str(chat.id) + LAST_SUPERGROUP_MESSAGE_ID] = message.message_id
        return
    if chat.id in group_manager.subgroups:
        return
    return


handler = MessageHandler(Filters.photo, receive_image)
