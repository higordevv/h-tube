from colorama import Fore, Style


class Informations:
    def __init__(self, url) -> None:
        self.url = url

    def printInfo(self):
        video = self.url
        print(f'''
{Fore.RED}===========Informações=============={Style.RESET_ALL}
{Fore.GREEN}Titulo:{Style.RESET_ALL} {video.title}
{Fore.GREEN }Autor:{Style.RESET_ALL} {video.author}
{Fore.GREEN}Visualizações:{Style.RESET_ALL} {video.views}
{Fore.GREEN }Data:{Style.RESET_ALL} {video.publish_date.day}/{video.publish_date.month}/{video.publish_date.year}
{Fore.GREEN}Canal:{Style.RESET_ALL} {video.channel_url}
{Fore.RED}==================================={Style.RESET_ALL}
        ''')
