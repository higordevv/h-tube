from pytube import YouTube


def Download(choice: int, url, path: str):
    pastVideo = YouTube(url)
    if choice == '1':
        urlInTray = pastVideo.streams.get_by_itag(137)
        print("Baixando....")
        urlInTray.download(path)
        return 'Download concluido!'
    if choice == '2':
        urlInTray = pastVideo.streams.get_by_itag(22)
        print("Baixando.....")
        urlInTray.download(path)
        return 'Dowload concluido!'
    if choice == '3':
        urlInTray = pastVideo.streams.get_by_itag(135)
        print("Baixando.....")
        urlInTray.download(path)
        return 'Dowload concluido!'
    if choice == '4':
        urlInTray = pastVideo.streams.get_by_itag(18)
        print('Baixando....')
        urlInTray.download(path)
        return 'Dowload concluido!'
    if choice == '5':
        urlInTray = pastVideo.streams.get_by_itag(133)
        print('Baixando....')
        urlInTray.download(path)
        return 'Dowload concluido!'
    if choice == '6':
        urlInTray = pastVideo.streams.get_by_itag(160)
        print('Baixando....')
        urlInTray.download(path)
        return 'Dowload concluido!'
    else:
        return 'Nada foi passado'
