import re
from io import BytesIO
from colorama import Fore, Style



# Responsabilidade Unica
class BaixarVideo:
    def __init__(self, bot, chatId, streams, retorno):
        self.chatId = chatId
        self.streams = streams
        self.bot = bot
        self.retorno = retorno
        self.buffer = BytesIO()

    def isValidUrl(youtube_url, username):
        regex = ("((http|https)://)(www.youtube)?" +
                 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" +
                 "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")

        link = re.compile(regex)

        if re.search(link, youtube_url):  # type: ignore
            print(
                f"User: {username} | [{Fore.GREEN}!{Style.RESET_ALL}] Url Valida!")
            return True
        else:
            print(
                f"User: {username} | [{Fore.RED}!{Style.RESET_ALL}] Url Invalida!")
            return False

    def videoInformation(video):
        InfosVideo = []

        InfosVideo.append(video.title)
        InfosVideo.append(f"{video.length//60}min e {video.length%60}s")
        InfosVideo.append(
            f"{video.publish_date.day}/{video.publish_date.month}/{video.publish_date.year}")
        InfosVideo.append(video.thumbnail_url)
        InfosVideo.append(str(video.views))

        return InfosVideo

    def download(self):
        buff = self.buffer
        self.bot.send_message(self.chatId, "Buffer criado")
        stream = self.streams.get_by_itag(int(self.retorno))
        video = stream.stream_to_buffer(buff)
        try:
            # Tente enviar o video pegando o valor puro do buffer 
            self.bot.send_message(self.chatId, "Enviando...")
            self.bot.send_video(chat_id=self.chatId, video=buff.getvalue())
            # Se suma
            buff.close()
            # [ ]
        except:
            print("Estou sentindo minhas forças indo embora")
