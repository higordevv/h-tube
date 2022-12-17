import re
import pytube
from io import BytesIO
from colorama import Fore, Style
import telebot

# Responsabilidade Unica
class BaixarVideo:
    def __init__(self, youtube_url, bot_token,chat_id):
        self.youtube_url:str = youtube_url
        self.bot_token: str = bot_token
        self.chat_id:str = chat_id
        self.yt = pytube.YouTube(self.youtube_url)
        self.bot = telebot.Telebot(self.bot_token)
        self.stream = self.yt.streams.first()


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
        self.stream.download(output_path=self.buff er)
    def send_video(self):
        self.bot.send_video(chat_id=self.chat_id, video=self.buffer.getvalue())