from pytube import StreamQuery

parametrosButton = {}

def StreamFilter(stream: list):
    listaStreams = StreamQuery(stream).filter(mime_type='video/webm', type='video') 
    for i in listaStreams:
        v = str(i)
        end = v.find('p', 48, 55)
        qualidade = v[48:end+1]
        parametrosButton[qualidade] = f'download({qualidade})'

    return listaStreams
# Conteudo de parametrosButton: {nomeDoBotao: evento}
# parametrosButton = {'720p': 'download(720p)', 
#                     '480p': 'download(480p)', 
#                     '360p': 'download(360p)', 
#                     '240p': 'download(240p)', 
#                     '144p': 'download(144p)'}
