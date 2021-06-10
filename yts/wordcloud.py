import pandas as pd
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from yts import api

youtube = build('youtube', 'v3', developerKey=api.API_KEY)

box = [['Comment']]


def getlinkid(LINK):
    meta = LINK.split('?')[1][2:]
    return meta


ID = getlinkid(api.LINK)


def main():
    data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='1000000', textFormat="plainText").execute()

    for i in data["items"]:
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]

        box.append([comment])

        totalReplyCount = i["snippet"]['totalReplyCount']

        if totalReplyCount > 0:

            parent = i["snippet"]['topLevelComment']["id"]

            data2 = youtube.comments().list(part='snippet', maxResults='1000000', parentId=parent,
                                            textFormat="plainText").execute()

            for j in data2["items"]:
                comment = j["snippet"]["textDisplay"]

                box.append([comment])

    while ("nextPageToken" in data):

        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]

            box.append([comment])

            totalReplyCount = i["snippet"]['totalReplyCount']

            if totalReplyCount > 0:

                parent = i["snippet"]['topLevelComment']["id"]

                data2 = youtube.comments().list(part='snippet', maxResults='1000000', parentId=parent,
                                                textFormat="plainText").execute()

                for k in data2["items"]:
                    comment = k["snippet"]["textDisplay"]

                    box.append([comment])

    df = pd.DataFrame({'Comment': [i[0] for i in box]})

    df.to_csv(r"sample.csv", index=False, header=False)
    print("Finished scraping comments...")
    data = pd.read_csv("sample.csv")
    words = ' '.join([text for text in data['Comment']])
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        random_state=1,
        background_color='black',
        colormap='Set2',
        collocations=False).generate(words)

    plt.figure(figsize=(8, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
