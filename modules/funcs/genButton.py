
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_markup(ButtonName, callbackData):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(ButtonName, callback_data=callbackData))
    return markup
