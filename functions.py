import pandas as pd
import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS


def scrape_A_Comment_with_its_Replies(jsonObj, table):
    """
    This will Scrap only Main Comment along with its Associated Replies
    """
    for i in jsonObj["items"]:
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
        table.append([comment, likes])

        # totalReplyCount = i["snippet"]['totalReplyCount']

        # if totalReplyCount > 0:
        #     parent = i["snippet"]['topLevelComment']["id"]

        #     sub_Comments = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
        #                                            textFormat="plainText").execute()
        #     for j in sub_Comments["items"]:
        #         comment = j["snippet"]["textDisplay"]
        #         likes = j["snippet"]['likeCount']
        #         table.append([comment, likes])


def getting_all_Comments_using_videoID(youtube, commentBox, V_Id):
    """
    This will Scrap All the Comments for a given Video ID
    """
    jsonObj = youtube.commentThreads().list(part='snippet', videoId=V_Id, maxResults='100',
                                            textFormat="plainText", order='relevance').execute()
    scrape_A_Comment_with_its_Replies(jsonObj, table=commentBox)

    Max = 100000
    while Max and "nextPageToken" in jsonObj:
        jsonObj = youtube.commentThreads().list(part='snippet', videoId=V_Id, pageToken=jsonObj["nextPageToken"],
                                                maxResults='100', textFormat="plainText", order='relevance').execute()
        scrape_A_Comment_with_its_Replies(jsonObj, table=commentBox)
        Max -= 1

    # Generating Data frame of Comments & Likes
    df = pd.DataFrame({'Comment': [i[0] for i in commentBox], 'Likes': [i[1] for i in commentBox]})
    df = df.sort_values(by='Likes', ascending=False, ignore_index=True)
    return df


def draw_WordCloud(textt, all_stopwords):
    # wrdCloud = WordCloud(width=800, height=800, stopwords=all_stopwords, background_color='white').generate(textt)

    # plt.figure(figsize=(8, 8), facecolor=None)
    # plt.imshow(wrdCloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()
