from telegram import Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)
from app.chat.commands import START
from app.chat.keyboards import start_keyboard
from app.chat.message.template import greet_user
from app.chat.organizations import BINHI, BUKLOD, KADIWA
from app.chat.states import SELECTING_ORGANIZATION
from app.chat.types import PRIVATE
from app.user_saves import ORGANIZATION


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
    text = (
        greet_user(user.id, user.first_name)
        + " Paki pili po ang kinabibilangan niyong kapisanan."
    )
    update.message.reply_text(text, "html", reply_markup=start_keyboard)
    return SELECTING_ORGANIZATION


def first_time_save_organization(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    user = update.effective_user
    user_data = context.user_data
    query_data = update.callback_query.data
    user_data[ORGANIZATION] = query_data
    text = (
        greet_user(user.id, user.first_name)
        + " Maaari na po kayo ngayong mag-send ng picture sa group."
        "\n\nIto po ang inyong impormasyon:\n"
        "\nTelegram ID - <code>%s</code>"
        "\nKapisanan - <b>%s</b>"
        "\n\nMaaari po kayong pumili ulit kung mayroong pagbabago."
        % (user.id, user_data[ORGANIZATION])
    )
    update.callback_query.edit_message_text(text, "html", reply_markup=start_keyboard)
    return SELECTING_ORGANIZATION


def save_organization(update: Update, context: CallbackContext) -> int:
    update.callback_query.answer()
    user = update.effective_user
    user_data = context.user_data
    query_data = update.callback_query.data
    user_data[ORGANIZATION] = query_data
    text = (
        greet_user(user.id, user.first_name)
        + "\n\nIto po ang pagbabago sa inyong impormasyon:\n"
        "\nTelegram ID - <code>%s</code>"
        "\nKapisanan - <b>%s</b>"
        "\n\nMaaari po kayong pumili ulit kung mayroong pagbabago."
        % (user.id, user_data[ORGANIZATION])
    )
    update.callback_query.edit_message_text(text, "html", reply_markup=start_keyboard)
    return SELECTING_ORGANIZATION


start_handler = CommandHandler(START, start)
first_time_selection_handler = CallbackQueryHandler(
    first_time_save_organization,
    pattern="^" + BUKLOD + "$|^" + KADIWA + "$|^" + BINHI + "$",
)
selection_handler = CallbackQueryHandler(
    save_organization, pattern="^" + BUKLOD + "$|^" + KADIWA + "$|^" + BINHI + "$"
)
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
