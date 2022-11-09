from colorama import Fore, Style
import telebot
from modules.main import Manager  


API_TOKEN = 'Arruma o teu'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """Olá,sou o Blue Pen Bot!""")


@bot.message_handler(commands=['baixarvideo'])
def echo_message(message):
    idChat = message.chat.id
    url = message.text[12:]
    print(url)

    if (Manager.isValidUrl(url)):
        bot.send_message(
            idChat, "Olha,não me escreva daquele jeito, me mande" +
            "n uma carta em q seja um pedaço de papel")
        print(f"[{Fore.GREEN}!{Style.RESET_ALL}] Url Valida!")
    else:
        bot.send_message(
            idChat, "Em pleno 2022 voce nao sabe o que é uma URL.")
        print(f"[{Fore.RED}!{Style.RESET_ALL}] Url invalida!")


print("Ligado")
bot.infinity_polling()