from colorama import Fore, Style
import telebot
from telebot.types import InputFile
from modules.main import Manager


API_TOKEN = 'Arruma o teu'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    idChat = message.chat.id

    bot.send_photo(
        idChat, InputFile('./media/boas_vindas/boas_vindas.jpeg'), "Lorem ipsum fermentum ut diam egestas sapien")

    # bot.send_audio(idChat, InputFile("./media/boas_vindas/manelGome.ogg"))

    print(f"[{Fore.GREEN}Conversa Iniciada{Style.RESET_ALL}]:\nUser: {message.from_user.username} | idChat: {idChat}")


@bot.message_handler(commands=['baixarvideo'])
def echo_message(message):
    idChat = message.chat.id
    url = message.text[12:]

    if (Manager.isValidUrl(url, message.from_user.username)):
        bot.send_message(
            idChat, "Video bacana")
    else:
        bot.send_message(
            idChat, "Em pleno 2022 voce nao sabe o que é uma URL.")


# Esse parametro func ?
# pode tirar
print("Liguei")
bot.infinity_polling()
