import argparse
from pyfiglet import Figlet
from yts import info, comments, media, wordcloud


def art():
    f = Figlet(font='larry3d')
    print(f.renderText('YTScraper'))


def main():
    art()
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--info", help="Extract info such as views, likes, dislikes, upload date and many more", action="store_true")
    parser.add_argument("-c", "--comments", help="Scrap all comments", action="store_true")
    parser.add_argument("-t", "--track", help="Extract audio from youtube video", action="store_true")
    parser.add_argument("-vi", "--video", help="Download video file", action="store_true")
    parser.add_argument("-w", "--wordcloud", help="Wordcloud visualization", action="store_true")
    args = parser.parse_args()
    videoinfo = args.info
    scrapcomments = args.comments
    exaudio = args.track
    videodwld = args.video
    wordcloudv = args.wordcloud

    if videoinfo:
        info.main()

    elif scrapcomments:
        comments.main()

    elif exaudio:
        media.track()

    elif videodwld:
        media.video()

    elif wordcloudv:
        wordcloud.main()