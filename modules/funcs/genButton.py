from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup


def ButtonConstructor(*args):
        # args = (['nome1', 'evento1'], ['nome2', 'evento2'])
        markup = markup = InlineKeyboardMarkup()

        # args é uma tupla()
        for butoes in args: # retira a lista da tupla
            for butao in butoes:
                # butao = ['nome1', 'evento1']
                #print(butao[0][0], butao[1])
                button = markup.add(InlineKeyboardButton(text=butao[0][0], callback_data=butao[1]))
            
        return markup
#ButtonConstructor([[('1080',), "download(('1080',)"],[('720p',), "download(('720p',)"],
#[('480p',), "download(('480p',)"],
#[('360p',), "download(('360p',)"],
#[('240p',), "download(('240p',)"],
#[('144p',), "download(('144p',)"]])