from urllib.parse import urlparse
from colorama import Fore, Style


def checkPlaylist(url: str):
    urlPassed = urlparse(url)
    query = '/playlist'
    isPlaylist = False
    if urlPassed.count(query) == 0:
        pass
    if urlPassed.count(query) == 1:
        print(
            f'[{Fore.RED}!{Style.RESET_ALL}] {Fore.BLUE}Playlist detectada{Style.RESET_ALL}')
        isPlaylist = True

    return isPlaylist
