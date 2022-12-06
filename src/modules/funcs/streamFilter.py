from pytube import StreamQuery

parametrosButton = {}


def StreamFilter(stream: list):
    listaStreams = StreamQuery(stream).filter(
        mime_type='video/webm', type='video')
    for i in listaStreams:
        v = str(i)
        end = v.find('p', 48, 55)
        qualidade = v[48:end+1]
        parametrosButton[qualidade] = qualidade
        

    return listaStreams
