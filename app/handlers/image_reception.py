from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, Filters, MessageHandler
from app.chat.group import load_group_manager
from app.chat.types import PRIVATE, SUPERGROUP
from app.chat_saves import MEDIA_GROUP_IDS
from app.user_saves import LAST_PRIVATE_MESSAGE_ID, LAST_SUPERGROUP_MESSAGE_ID


def receive_image(update: Update, context: CallbackContext) -> None:
    chat = update.message.chat
    message = update.message
    chat_data = context.chat_data
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
        if MEDIA_GROUP_IDS not in chat_data:
            chat_data[MEDIA_GROUP_IDS] = set()
        if message.media_group_id in chat_data[MEDIA_GROUP_IDS]:
            return
        text = "Press to change organization or remove sent image/s."
        buttons = [
            [
                InlineKeyboardButton("BUKLOD", callback_data="BUKLOD"),
                InlineKeyboardButton("KADIWA", callback_data="KADIWA"),
                InlineKeyboardButton("BINHI", callback_data="BINHI"),
            ],
            [InlineKeyboardButton("REMOVE", callback_data="REMOVE")],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text, reply_markup=keyboard)
        if message.media_group_id == None:
            return
        chat_data["LAST_MEDIA_GROUP_ID"].add(message.media_group_id)
        return
    return


handler = MessageHandler(Filters.photo, receive_image)
