from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from .streamFilter import parametrosButton


def ButtonConstructor(*args):
        # args = ( {'nome1': 'evento1', 'nome2': 'evento2'} )
        butoes = args[0] # Retira tudo da tupla
        markup = markup = InlineKeyboardMarkup()
        
        for text, evento in butoes.items():
            button = markup.add(InlineKeyboardButton(text=text, callback_data=evento))
        parametrosButton.clear()
        return markup