from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.chat.organizations import BUKLOD, KADIWA, BINHI

_image_reception_buttons = [
    [
        InlineKeyboardButton(BUKLOD, callback_data=BUKLOD),
        InlineKeyboardButton(KADIWA, callback_data=KADIWA),
        InlineKeyboardButton(BINHI, callback_data=BINHI),
    ],
    [InlineKeyboardButton(REMOVE, callback_data=REMOVE)],
]

image_reception_keyboard = InlineKeyboardMarkup(_image_reception_buttons)
