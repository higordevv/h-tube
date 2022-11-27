from pytube import YouTube


def Download(choice: str, url, idchat):
    path = "./media/videos"
    pastVideo = YouTube(url)
    print(url)
    match choice:
        case "download(1080p)":
            video = pastVideo.streams.get_by_resolution(
                "1080p")
            video.download(path)
        case "download(720p)":
            video = pastVideo.streams.get_by_resolution(
                "720p")
            video.download(path)
        case "download(480p)":
            video = pastVideo.streams.get_by_resolution(
                "480p")
            video.download(path)
        case "download(360p)":
            video = pastVideo.streams.get_by_resolution(
                "360p")
            video.download(path)
        case "download(240p)":
            video = pastVideo.streams.get_by_resolution(
                "240p")
            video.download(path)
        case "download(144p)":
            video = pastVideo.streams.get_by_resolution(
                "144p")
            video.download(path)
