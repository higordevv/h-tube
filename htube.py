import os
import time
import platform
from pytube import YouTube
from pytube import Playlist
import youtube_dl
from urllib.parse import urlparse
os.system("clear")

#Area do Termux
Termux = 'OS = Termux-Android'
directo_T = '/data/data/com.termux/files/home/storage/downloads/videosBaixados'

Distro_All = 'Linux'
def System_Detector(Termux):
    oSsys = os.name
    oSplatform = platform.system()
    oSVersion = platform.version()
    if oSsys and oSplatform and oSVersion == '#1 SMP PREEMPT Thu Aug 19 23:19:25 WIB 2021' and '4.9.193-perf-gc285628':
        Termux = 'OS = Termux-Android'
        print(Termux)
        existenceDirectory = os.path.exists(
            '/data/data/com.termux/files/home/storage')
        if existenceDirectory == False:
            print('Falta a permissão do Storage "Digite: termux-setup-storage"')
            return 
        Alreadyexists = os.path.exists(
                '/data/data/com.termux/files/home/storage/downloads/videosBaixados')
        if Alreadyexists == True:
            pass
        else:
            os.system(
                    'cd /data/data/com.termux/files/home/storage/downloads/ && mkdir videosBaixados')
        if oSplatform == 'Linux':
            print('Linux Detectado')
        if oSplatform == 'Windows':
            print('Windows Detectado')
    time.sleep(0.5)

System_Detector(Termux)


print('''⠀
      ⣀⣤⣤⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣦⣤⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀
⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠛⠛⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠛⠛⠋⠁Downloader :]⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀by:Higorkk''')
url = input('Digite a url do Vídeo: ')

#Fazer condição aqui
if System_Detector(Termux) == True:
    diretorio = directo_T
else:
    diretorio = input('Diretorio para o Download: ')



def videoInformation():
    pastVideo_info = YouTube(url)
    print(f'''
===========Informações==============
Titulo: {pastVideo_info.title}
Autor: {pastVideo_info.author}
Visualizações: {pastVideo_info.views}
Data:{pastVideo_info.publish_date}    
===================================
''')
videoInformation()

def urlFilter(url):
    urlPassed = urlparse(url)
    query = '&list'
    if urlPassed.count(query) == 0:
        pass
        if urlPassed.count(query) == 1:
            print('PlayList Detectada [!]')
            PlaylistDetected = input('Deseja fazer o Download completo? [Y/n]')
            if PlaylistDetected == 'Y':
                urlPassed = Playlist(url)
                for Playlist_Download in urlPassed.video_urls:
                    PDs = YouTube(Playlist_Download)
                    ResolutionPlaylistVideos = input('Qual a resolução?')
                    print('''
                ===============
                | [1] 1080p   |
                | [2] 720p    |
                | [3] 480p    |
                | [4] 360p    |
                | [5] 240p    |
                | [6] 144p    |
                =============== ''')
                    if ResolutionPlaylistVideos == '1':
                        process_finnaly = PDs.streams.get_by_itag(137)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    elif ResolutionPlaylistVideos == '2':
                        process_finnaly = PDs.streams.get_by_itag(22)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    elif ResolutionPlaylistVideos == '3':
                        process_finnaly = PDs.streams.get_by_itag(135)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    elif ResolutionPlaylistVideos == '4':
                        process_finnaly = PDs.streams.get_by_itag(18)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    elif ResolutionPlaylistVideos == '5':
                        process_finnaly = PDs.streams.get_by_itag(133)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    elif ResolutionPlaylistVideos == '6':
                        process_finnaly = PDs.streams.get_by_itag(160)
                        print('Baixando....')
                        process_finnaly.download(diretorio)
                    else:
                        return 'Nada foi passado'
urlFilter(url)
def menuResolutions(url):
    pastVideo = YouTube(url)
    print(f'''
===============
| [1] 1080p   |
| [2] 720p    |
| [3] 480p    |
| [4] 360p    |
| [5] 240p    |
| [6] 144p    |
===============
''')
    result = input('Escolha a resolução: ')
    if result == '1':
        urlInTray = pastVideo.streams.get_by_itag(137)
        print("Baixando....")
        urlInTray.download(diretorio)
        return 'Download concluido!'
    elif result == '2':
        urlInTray = pastVideo.streams.get_by_itag(22)
        print("Baixando.....")
        urlInTray.download(diretorio)
        return 'Dowload concluido!'
    elif result == '3':
        urlInTray = pastVideo.streams.get_by_itag(135)
        print("Baixando.....")
        urlInTray.download(diretorio)
        return 'Dowload concluido!'
    elif result == '4':
        urlInTray = pastVideo.streams.get_by_itag(18)
        print("Baixando.....")
        urlInTray.download(diretorio)
        return 'Dowload concluido!'
    elif result == '5':
        urlInTray = pastVideo.streams.get_by_itag(133)
        print("Baixando.....")
        urlInTray.download(diretorio)
        return 'Dowload concluido!'
    elif result == '6':
        urlInTray = pastVideo.streams.get_by_itag(160)
        print("Baixando.....")
        urlInTray.download(diretorio)
        return 'Dowload concluido!'
    else:
        return 'Nada foi passsado'
menuResolutions(url) 
