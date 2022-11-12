from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup


def ButtonConstructor(*args):
        # args = (['nome1', 'evento1'], ['nome2', 'evento2'])
        markup = markup = InlineKeyboardMarkup()

        for butao in args:
        # butao = ['nome1', 'evento1']
            button = markup.add(InlineKeyboardButton(text=butao[0], callback_data=butao[1]))
            
        return markup
 