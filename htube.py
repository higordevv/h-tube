import os
import random
from colorama import Fore, Style
from modules.main import Manager
from modules.assets.ascii import ascii


try:
    os.system("clear")

    ascii_logo = random.choice(ascii).format()

    print(f'${Fore.RED + ascii_logo + Style.RESET_ALL}')

    url = input('Digite a url do Vídeo: ')

    diretorio = input('Diretorio para o Download: ')

    if not diretorio:
        print(
            f"[{Fore.RED}!{Style.RESET_ALL}] Será armazenado no diretorio " +
            " padrão: /htube_downloads")
        diretorio = './htube_downloads'

    if __name__ == "__main__":
        Manager(url, diretorio).isValidUrl()
        Manager(url, diretorio).videoInformation()
        Manager(url, diretorio).isPlaylist()


except KeyboardInterrupt:
    os.system("clear")
    print("Good bye :)")
