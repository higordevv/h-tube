import os
import sys
import time

import telebot
from colorama import Fore, Style
from pytube import YouTube
from telebot.types import InputFile

from modules.funcs.genButton import ButtonConstructor
from modules.funcs.streamFilter import StreamFilter, parametrosButton
from modules.main import Manager

API_TOKEN = '2032060433:AAGsnnvZH8ATveJc1WhHZFIqaqot_to6RQ8'

bot = telebot.TeleBot(API_TOKEN)

bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("/baixarvideo", "/baixavideo <url>"),
    ],)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    idChat = message.chat.id
    bot.send_photo(
        idChat, InputFile('./media/boas_vindas/boas_vindas.jpeg'), "Eu simplesmente não existo")

    bot.send_audio(idChat, InputFile("./media/boas_vindas/manelGome.ogg"))

    print(f"[{Fore.GREEN}Conversa Iniciada{Style.RESET_ALL}]:\nUser: {message.from_user.username} | idChat: {idChat}")


@bot.message_handler(commands=['baixarvideo'])
def baixarVideo(message):
    idChat = message.chat.id
    url = message.text[12:]
    

    if (Manager.isValidUrl(url, message.from_user.username)):
        bot.send_message(
            idChat, "Um momento amigo(a) ✋")
        bot.send_message(
            idChat, "Aqui está 👇")

        video = YouTube(url)
        InfosVideo = Manager.videoInformation(video)
        caption1 = f'\n*Nome:*\n{InfosVideo[0]}\n*Data:* {InfosVideo[2]}\n*Duração:* {InfosVideo[1]}\n*Visualizações:* {InfosVideo[4]}\n\n⬇*Selecione a qualidade do video*⬇️'

        StreamFilter(video.streams)
        bot.send_photo(idChat, InfosVideo[3], caption1, parse_mode='markdown', reply_markup=ButtonConstructor(parametrosButton))
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
