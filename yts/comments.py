import pandas as pd
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
from yts import api

youtube = build('youtube', 'v3', developerKey=api.API_KEY)

box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]


def getlinkid(LINK):
    meta = LINK.split('?')[1][2:]
    return meta


ID = getlinkid(api.LINK)


def gettitle(LINK):
    response = requests.get(api.LINK)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('meta', attrs={"name": "title"})
    return title.get("content")


def main():
    data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='1000000', textFormat="plainText").execute()

    for i in data["items"]:

        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
        likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
        replies = i["snippet"]['totalReplyCount']

        box.append([name, comment, published_at, likes, replies])

        totalReplyCount = i["snippet"]['totalReplyCount']

        if totalReplyCount > 0:

            parent = i["snippet"]['topLevelComment']["id"]

            data2 = youtube.comments().list(part='snippet', maxResults='1000000', parentId=parent,
                                            textFormat="plainText").execute()

            for j in data2["items"]:
                name = j["snippet"]["authorDisplayName"]
                comment = j["snippet"]["textDisplay"]
                published_at = j["snippet"]['publishedAt']
                likes = j["snippet"]['likeCount']
                replies = ""

                box.append([name, comment, published_at, likes, replies])

    while ("nextPageToken" in data):

        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

            totalReplyCount = i["snippet"]['totalReplyCount']

            if totalReplyCount > 0:

                parent = i["snippet"]['topLevelComment']["id"]

                data2 = youtube.comments().list(part='snippet', maxResults='1000000', parentId=parent,
                                                textFormat="plainText").execute()

                for k in data2["items"]:
                    name = k["snippet"]["authorDisplayName"]
                    comment = k["snippet"]["textDisplay"]
                    published_at = k["snippet"]['publishedAt']
                    likes = k["snippet"]['likeCount']
                    replies = ''

                    box.append([name, comment, published_at, likes, replies])

    df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})

    df.to_csv(r"downloads/csv/{0}.csv".format(gettitle(api.LINK)), index=False, header=False)

    print("Kindly check downloads/csv")