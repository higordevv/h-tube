import sys
from pytube import YouTube
from colorama import Fore, Style
from modules.funcs.menu import menu
from modules.funcs.linkcheck import checkPlaylist
from modules.funcs.videoInformation import Informations
import re


class Manager:
    def __init__(self, url, dirct):
        self.url: str = url
        self.dirct: str = dirct

    def isValidUrl(self):
        regex = ("((http|https)://)(www.)?" +
                 "[a-zA-Z0-9@:%._\\+~#?&//=]" +
                 "{2,256}\\.[a-z]" +
                 "{2,6}\\b([-a-zA-Z0-9@:%" +
                 "._\\+~#?&//=]*)")

        link = re.compile(regex)

        try:
            if not (self.url):
                return False
            if (re.search(link, self.url)):
                return True
            else:
                raise NameError(
                    print(f"[{Fore.RED}!{Style.RESET_ALL}] Url invalida!"))
        except NameError:
            sys.exit(1)

    def videoInformation(self):
        video = YouTube(self.url)
        Informations(video).printInfo()

    def isPlaylist(self):
        link: str = self.url
        path: str = self.dirct
        if (checkPlaylist(link)):
            menu(link, path)
        else:
            menu(link, path)
