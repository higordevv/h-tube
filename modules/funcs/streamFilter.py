from pytube import StreamQuery
from pytube import YouTube
# vou ver a doc
# 
# https://pytube.io/en/latest/api.html#stream-object

def StreamFilter(stream: list):
    return StreamQuery(stream).filter(mime_type='video/webm', type='video') 

for i in StreamFilter(YouTube('https://www.youtube.com/watch?v=sbusfhqi0ZU').fmt_streams):
    print()

# o laco vai retornar isso aq: <Stream: itag="313" mime_type="video/webm" res="2160p" fps="30fps" vcodec="vp9" progressive="False" type="video"> isso e um objeto?
# Como é um array,dá pra fazer u, for i in array: ButtonConstructor(i.res)
# [<Stream: itag="313" mime_type="video/webm" res="2160p" fps="30fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="271" mime_type="video/webm" res="1440p" fps="30fps" vcodec="vp9" progressive="False" type="video">]
#

