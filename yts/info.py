import youtube_dl
from yts import api


# for views, likes, and dislikes
def compact_short(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


# time conversion
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


# get rid of unwanted strings
class logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


ydl_opts = {
    'logger': logger()
}


def main():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(api.LINK, download=False)
        upload_date_format = meta['upload_date'][:4] + '-' + meta['upload_date'][4:6] + '-' + meta['upload_date'][6::]
        durationConversion = convert(meta['duration'])
        metaV, metaL, metaD = meta['view_count'], meta['like_count'], meta['dislike_count']
        views = f"{metaV}({compact_short(metaV)})"
        likes = f"{metaL}({compact_short(metaL)})"
        dislikes = f"{metaD}({compact_short(metaD)})"

    try:
        print("Title: ", meta['title'])
    except KeyError:
        print("Title: ", "Unknown")
    try:
        print("ID: ", meta['id'])
    except KeyError:
        print("ID: ", "Unknown")
    try:
        print("Extension: ", meta['ext'])
    except KeyError:
        print("Extension: ", "Unknown")
    try:
        print("Upload Date: ", upload_date_format)
    except KeyError:
        print("Upload Date: ", "Unknown")
    try:
        print("Secondary Title: ", meta['alt_title'])
    except KeyError:
        print("Secondary Title: ", "Unknown")
    try:
        print("Uploader: ", meta['uploader'])
    except KeyError:
        print("Uploader: ", "Unknown")
    try:
        print("Creator: ", meta['creator'])
    except KeyError:
        print("Creator: ", "Unknown")
    try:
        print("Uploader ID: ", meta['uploader_id'])
    except KeyError:
        print("Uploader ID: ", "Unknown")
    try:
        print("Channel Name: ", meta['channel'])
    except KeyError:
        print("Channel Name: ", "Unknown")
    try:
        print("Channel ID: ", meta['channel_id'])
    except KeyError:
        print("Channel ID: ", "Unknown")
    try:
        print("Duration: ", durationConversion)
    except KeyError:
        print("Duration: ", "Unknown")
    try:
        print("Views: ", views)
    except KeyError:
        print("Views: ", "Unknown")
    try:
        print("Likes: ", likes)
    except KeyError:
        print("Likes: ", "Unknown")
    try:
        print("Dislikes: ", dislikes)
    except KeyError:
        print("Dislikes: ", "Unknown")
    try:
        print("Average Rating: ", meta['average_rating'])
    except KeyError:
        print("Average Rating: ", "Unknown")
    try:
        print("Resolution: ", meta['resolution'])
    except KeyError:
        print("Resolution: ", "Unknown")
    try:
        print("Frame Rate: ", meta['fps'])
    except KeyError:
        print("Frame Rate: ", "Unknown")
    try:
        print("Playlist: ", meta['playlist'])
    except KeyError:
        print("Playlist: ", "Unknown")



