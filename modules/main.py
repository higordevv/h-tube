import re
from colorama import Fore, Style
from pytube import YouTube

class Manager:
    # def __init__(self, url, dirct):
    #     self.url: str = url
    #     self.dirct: str = dirct

    def isValidUrl(url, username):
        regex = ("((http|https)://)(www.youtube)?" +
                 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" +
                 "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")

        link = re.compile(regex)

        if re.search(link, url):  # type: ignore
            print(
                f"User: {username} | [{Fore.GREEN}!{Style.RESET_ALL}] Url Valida!")
            return True
        else:
            print(
                f"User: {username} | [{Fore.RED}!{Style.RESET_ALL}] Url Invalida!")
            return False

    def videoInformation(url):
        video = YouTube(url)
        InfosVideo = []

        InfosVideo.append(video.title)
        InfosVideo.append(f"{video.length//60}min e {video.length%60}s")
        InfosVideo.append(f"{video.publish_date.day}/{video.publish_date.month}/{video.publish_date.year}")
        InfosVideo.append(video.thumbnail_url)
        InfosVideo.append(str(video.views))
        
        return InfosVideo

#     def isPlaylist(self):
#         link: str = self.url
#         path: str = self.dirct
#         if (checkPlaylist(link)):
#             menu(link, path)
#         else:
#             menu(link, path)
#
#     def isShort(self):
#         link: str = self.url
#         path: str = self.url
#         if (checkShorts(link)):
#             menu(link, path)
#         else:
#             menu(link, path)
