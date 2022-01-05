import sys
import pandas as pd
from functions import getting_all_Comments_using_videoID, draw_WordCloud

from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from nltk.corpus import stopwords
# from wordcloud import WordCloud, STOPWORDS


def get_Sentiments(vid_URL):
    api_key = "AIzaSyCM80koLdCIptOOOkuhB4hh5YgZZ1HNQ1I"

    youtube = build('youtube', 'v3', developerKey=api_key)
    ID = vid_URL[-11:]  # This is YouTube video ID.
    print(ID)

    # Global Comment Box List Container
    commentBox = []

    data = getting_all_Comments_using_videoID(youtube, commentBox, ID)
    data.head()
    if len(data) <= 15:
        print("Comments Data is NOT Sufficient for this Video")
        sys.exit()
    else:
        ### Use this to make a Drop Down List & Filtering as per User needs :)
        print("All Comments   ---->", data.shape[0])
        # print("At Least 1 Like ---->", data[data["Likes"] > 0].shape[0])
        # print("At Least 5 Like ---->", data[data["Likes"] > 5].shape[0])
        # print("At Least 25 Like---->", data[data["Likes"] > 25].shape[0])
        # print("At Least 50 Like---->", data[data["Likes"] > 50].shape[0])
        # print("At Least 100 Like--->", data[data["Likes"] > 100].shape[0])
        # print("At Least 250 Like--->", data[data["Likes"] > 250].shape[0])
    data.replace("[^a-zA-Z]", " ", regex=True, inplace=True)
    data = pd.DataFrame(data["Comment"].str.lower())

    stop = stopwords.words('english')
    # Extend Stopwords manually...
    stop.extend(
        ['br', 'href', 'https', 'http', 'youtube', 'com', 'bhai', 'bro', 'guys', 'hey', 'hi',
         'hello', 'channel', 'yes', 'no', 'dislike', 'trailer'])
    data['clean_transcript'] = data['Comment'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    comments_df = data['clean_transcript'].copy()

    analyzer = SentimentIntensityAnalyzer()

    lis = []
    for row in comments_df:
        emotions_score = analyzer.polarity_scores(row)
        lis.append(emotions_score)
    # Creating dataframe of Sentiments
    sentiments_df = pd.DataFrame(lis)

    # Merging back the Sentiments_df with Comments_df
    df = pd.concat([comments_df.reset_index(drop=True), sentiments_df], axis=1)

    # positive_emo = " ".join(line for line in df[df.compound >= 0.05].clean_transcript)
    # draw_WordCloud(textt=positive_emo, all_stopwords=stop)
    #
    # negative_emo = " ".join(line for line in df[df.compound <= -0.05].clean_transcript)
    # draw_WordCloud(textt=negative_emo, all_stopwords=stop)

    N = df[df["compound"] <= -0.05].count()[0]
    print(f"Overall Negative Opinions = {N}")
    P = df[df["compound"] >= 0.05].count()[0]
    print(f"Overall Positive Opinions = {P}")
    if P > N:
        Result = {"Positive": round(100 * P / (P + N), 2)}
        print(f'Overall Public Sentiment is: {Result["Positive"]}% (Positive ++)')
    else:
        Result = {"Negative": round(100 * N / (P + N), 2)}
        print(f'Overall Public Sentiment is: {Result["Negative"]}% (Negative --)')

    ### showing Top-10 Negative Opinions
    neg_df = df.sort_values(by="compound", ascending=True).head(10)
    # print(neg_df.clean_transcript)

    ### showing Top-10 Positive Opinions
    pos_df = df.sort_values(by="compound", ascending=False).head(10)
    # print(pos_df.clean_transcript)
    return Result
