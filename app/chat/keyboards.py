from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.chat.buttons import YES, REMOVE, NO
from app.chat.organizations import BUKLOD, KADIWA, BINHI

_image_reception_buttons = [
    [
        InlineKeyboardButton(BUKLOD, callback_data=BUKLOD),
        InlineKeyboardButton(KADIWA, callback_data=KADIWA),
        InlineKeyboardButton(BINHI, callback_data=BINHI),
    ],
    [InlineKeyboardButton(REMOVE, callback_data=REMOVE)],
]

_image_reception_removal_confirmation_buttons = [
    [
        InlineKeyboardButton(YES, callback_data=YES),
        InlineKeyboardButton(NO, callback_data=NO),
    ]
]

_start_buttons = [
    [
        InlineKeyboardButton(BUKLOD, callback_data=BUKLOD),
        InlineKeyboardButton(KADIWA, callback_data=KADIWA),
        InlineKeyboardButton(BINHI, callback_data=BINHI),
    ]
]

image_reception_keyboard = InlineKeyboardMarkup(_image_reception_buttons)
image_reception_removal_confirmation_keyboard = InlineKeyboardMarkup(
    _image_reception_removal_confirmation_buttons
)
start_keyboard = InlineKeyboardMarkup(_start_buttons)
