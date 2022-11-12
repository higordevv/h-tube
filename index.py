import sys
import time
from colorama import Fore, Style
import telebot
from telebot.types import InputFile
#from modules.funcs.genButton import ButtonConstructor
from modules.main import Manager


API_TOKEN = ' '

bot = telebot.TeleBot(API_TOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/baixarvideo", "/baixavideo <url>"),
    ],)

#b = ButtonConstructor('UI', 'Di mais')
#print(b)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    idChat = message.chat.id
    bot.send_photo(
        idChat, InputFile('./media/boas_vindas/boas_vindas.jpeg'), "Lorem ipsum fermentum ut diam egestas sapien")

    # bot.send_audio(idChat, InputFile("./media/boas_vindas/manelGome.ogg"))

    print(f"[{Fore.GREEN}Conversa Iniciada{Style.RESET_ALL}]:\nUser: {message.from_user.username} | idChat: {idChat}")


@bot.message_handler(commands=['baixarvideo'])
def baixarVideo(message):
    idChat = message.chat.id
    url = message.text[12:]

    if (Manager.isValidUrl(url, message.from_user.username)):
        bot.send_message(
            idChat, "Video bacana")
        
        video = Manager.videoInformation(url)
        # list -> [titulo, duracao, data, imagem, visu]
        caption1 = f'*Nome:* {video[0]}\n*Data:* {video[2]}\n*Duração:* {video[1]}\n*Visus:* {video[4]}'

        bot.send_photo(idChat, video[3], caption1).message_id
    else:
        bot.send_message(
            idChat, "Em pleno 2022 voce nao sabe o que é uma URL.")


def startBot():
    print("status: [ ON ]")
    bot.infinity_polling()
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        startBot()
    except KeyboardInterrupt:
        print('\nBOT DESLIGADO\n')
        sys.exit(0)
