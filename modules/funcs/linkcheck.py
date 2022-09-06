from urllib.parse import urlparse
from colorama import Fore, Style


def checkPlaylist(url: str):
    urlPassed = urlparse(url)
    playlist = '/playlist'
    isPlaylist = False
    if urlPassed.count(playlist) == 0:
        pass
    if urlPassed.count(playlist) == 1:
        print(
            f'[{Fore.RED}!{Style.RESET_ALL}] {Fore.BLUE}Playlist detectada{Style.RESET_ALL}')
        isPlaylist = True

    return isPlaylist


def checkShorts(url: str):
    urlPassed = urlparse(url)
    shorts = '/shorts'
    isShorts = False
    if (urlPassed.count(shorts)) == 0:
        pass
    if urlPassed.count(shorts) == 1:
        print(
            f'[{Fore.RED}!{Style.RESET_ALL}] {Fore.BLUE}O video é um Short{Style.RESET_ALL}')
        isShorts = True

    return isShorts
