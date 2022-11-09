import re
from colorama import Fore, Style


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

#     def videoInformation(self):
#         video = YouTube(self.url)
#         Informations(video).printInfo()
#
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
