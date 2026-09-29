import os
import random
import shutil
import sys
import yt_dlp
from colorama import Fore, Back, Style
from modules.assets.ascii import ascii

RESOLUCOES = {'1': 1080, '2': 720, '3': 480, '4': 360, '5': 240, '6': 144}
AVISO = f'[{Fore.RED}!{Style.RESET_ALL}]'


def formato(altura):
    # sem ffmpeg não dá pra juntar vídeo e áudio separados, então só arquivo único
    if shutil.which('ffmpeg'):
        return f'bv*[height<={altura}]+ba/b[height<={altura}]/w'
    return f'b[height<={altura}]/w'


def mostrar_info(info):
    print(f'{Fore.RED}===========Informações=============={Style.RESET_ALL}')
    if info.get('_type') == 'playlist':
        print(f"{Fore.GREEN}Playlist:{Style.RESET_ALL} {info.get('title')}")
        print(f"{Fore.GREEN}Autor:{Style.RESET_ALL} {info.get('uploader')}")
        print(f"{Fore.GREEN}Vídeos:{Style.RESET_ALL} {len(info.get('entries') or [])}")
        print(f'{AVISO} {Back.RED}Todos os vídeos da playlist serão baixados na resolução selecionada{Style.RESET_ALL}')
    else:
        data = info.get('upload_date') or '????????'
        print(f"{Fore.GREEN}Titulo:{Style.RESET_ALL} {info.get('title')}")
        print(f"{Fore.GREEN}Autor:{Style.RESET_ALL} {info.get('uploader')}")
        print(f"{Fore.GREEN}Visualizações:{Style.RESET_ALL} {info.get('view_count')}")
        print(f"{Fore.GREEN}Data:{Style.RESET_ALL} {data[6:]}/{data[4:6]}/{data[:4]}")
        print(f"{Fore.GREEN}Canal:{Style.RESET_ALL} {info.get('channel_url')}")
    print(f'{Fore.RED}==================================={Style.RESET_ALL}')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + random.choice(ascii) + Style.RESET_ALL)

    url = input('Digite a url do Vídeo: ').strip()
    diretorio = input('Diretorio para o Download: ').strip()
    if not diretorio:
        print(f'{AVISO} Será armazenado no diretorio padrão: ./htube_downloads')
        diretorio = './htube_downloads'

    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': 'in_playlist'}) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError:
        print(f'{AVISO} Url invalida ou vídeo indisponível!')
        sys.exit(1)

    mostrar_info(info)
    print(f'{Fore.YELLOW}')
    for opcao, altura in RESOLUCOES.items():
        print(f'  | [{opcao}] {altura}p')
    print(Style.RESET_ALL)

    escolha = ''
    while escolha not in RESOLUCOES:
        escolha = input(f'{Fore.CYAN}Escolha a resolução:{Style.RESET_ALL} ').strip()

    if not shutil.which('ffmpeg'):
        print(f'{AVISO} ffmpeg não encontrado: acima de 360p pode vir em qualidade menor')

    opcoes = {
        'format': formato(RESOLUCOES[escolha]),
        'outtmpl': os.path.join(diretorio, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ignoreerrors': True,  # um vídeo privado não derruba a playlist inteira
    }
    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])
    print(f'{Fore.GREEN}Download concluido!{Style.RESET_ALL}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGood bye :)')
