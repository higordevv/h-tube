from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup


def ButtonConstructor( evento: str, name: str):
        data: dict = {'text': name, 'evento': evento}
     
        
        markup = markup = InlineKeyboardMarkup()
        for i in data.items():
            button = markup.add(InlineKeyboardButton(text=i.text, callback_data=i.callback_data))
 