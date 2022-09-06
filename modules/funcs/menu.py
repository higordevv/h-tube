

from colorama import Fore, Style, Back
from pytube import Playlist
from modules.funcs.linkcheck import checkPlaylist
from modules.funcs.download import Download


def menu(url, path):
    print(f'''
{Fore.YELLOW}
==================
  | [1] 1080p   |
  | [2] 720p    |
  | [3] 480p    |
  | [4] 360p    |
  | [5] 240p    |
  | [6] 144p    |
==================
{Style.RESET_ALL}
''')

    if (checkPlaylist(url)):
        print(f'''
[{Fore.RED}!{Style.RESET_ALL}] {Back.RED} Todos os videos da PlayList vão ser
baixado na resolução selecionada{Style.RESET_ALL}''')
        url = Playlist(url)
        choice: int = input(
            f'{Fore.CYAN}Escolha a resolução:{Style.RESET_ALL}')

        for PlaylistVideos in url.video_urls:
            Download(choice, PlaylistVideos,)

    choice: int = input(f'{Fore.CYAN}Escolha a resolução:{Style.RESET_ALL}')

    Download(choice, url, path=path)
