from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .streamFilter import parametrosButton


def ButtonConstructor(*args):
        butoes = args[0] # Retira tudo da tupla
        markup = InlineKeyboardMarkup(row_width=2)
        
        for text, evento in butoes.items():
            button = markup.add(InlineKeyboardButton(text=text, callback_data=evento))
        parametrosButton.clear()
        return markup