import requests
import youtube_dl
import pytube
from bs4 import BeautifulSoup
from yts import api


def gettitle(LINK):
    response = requests.get(LINK)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('meta', attrs={"name": "title"})
    return title.get("content")


# get rid of unwanted strings
class logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def track():
    def hook(d):
        if d['status'] == 'finished':
            print("Finished: ", gettitle(api.LINK) + ".mp3")


    def hook1(hook):
        if hook['status'] == 'finished':
            print("File saved in downloads/track directory")


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/track/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': logger(),
        'progress_hooks': [hook] + [hook1]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([api.LINK])


def video():
    youtube = pytube.YouTube(api.LINK)
    video = youtube.streams.get_highest_resolution()
    video.download(r'downloads/video/')
    print("Kindly check downloads/video")