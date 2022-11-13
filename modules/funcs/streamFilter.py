from pytube import StreamQuery
from pytube import YouTube

parametrosButton = []

def StreamFilter(stream: list):
    listaStreams = StreamQuery(stream).filter(mime_type='video/webm', type='video') 
    for i in listaStreams:
        lista = []
        v = str(i)
        qualidade = v[48:52],
        lista.append(qualidade)
        lista.append(f'download({qualidade}')
        parametrosButton.append(lista)

    return listaStreams
    # parametrosButton = [['720p', "download('720p')"], 
    #                     ['480p', "download('480p')"], 
    #                     ['360p', "download('360p')"], 
    #                     ['240p', "download('240p')"], 
    #                     ['144p', "download('144p')"]]


#video = YouTube('https://www.youtube.com/watch?v=os8Tq1P-Egg').streams


