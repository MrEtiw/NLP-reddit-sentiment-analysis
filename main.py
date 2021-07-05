import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw
import math
import datetime as dt
import pandas as pd
import numpy as np
import os

nltk.download("vader_lexicon")
nltk.download("stopwords")

from initialize_reddit_client import set_credentials_env_var, get_reddit_client


set_credentials_env_var("reddit_credentials.json")
reddit_client = get_reddit_client()


sub_reddits = reddit_client.subreddit("FourSentenceStories")
stocks = ["GME", "AMC"]
# For example purposes. To use this as a live trading tool, you'd want to populate this with tickers that have been mentioned on the pertinent community (WSB in our case) in a specified period.


def commentSentiment(urlT):
    bodyComment = []
    try:
        check = reddit_client.submission(url=urlT)
        subComments = check.comments
    except:
        return 0

    for comment in subComments:
        try:
            bodyComment.append(comment.body)
        except:
            return 0

    sia = SIA()
    results = []
    for line in bodyComment:
        scores = sia.polarity_scores(line)
        scores["headline"] = line

        results.append(scores)

    df = pd.DataFrame.from_records(results)
    df.head()
    df["label"] = 0

    try:
        df.loc[df["compound"] > 0.1, "label"] = 1
        df.loc[df["compound"] < -0.1, "label"] = -1
    except:
        return 0

    averageScore = 0
    position = 0
    while position < len(df.label) - 1:
        averageScore = averageScore + df.label[position]
        position += 1
    averageScore = averageScore / len(df.label)

    return averageScore


def latestComment(ticker, urlT):
    subComments = []
    updateDates = []
    try:
        check = reddit.submission(url=urlT)
        subComments = check.comments
    except:
        return 0

    for comment in subComments:
        try:
            updateDates.append(comment.created_utc)
        except:
            return 0

    updateDates.sort()
    return updateDates[-1]


def get_date(date):
    return dt.datetime.fromtimestamp(date)


submissions = reddit_client.subreddit("FourSentenceStories").search(
    "He speaks", limit=2
)
for sub in submissions:
    print(sub.domain)
    print(sub.num_comments)
    print(sub.url)


submission_statistics = []
d = {}
for ticker in stocks:
    for submission in reddit.subreddit("wallstreetbets").search(ticker, limit=130):
        if submission.domain != "self.wallstreetbets":
            continue
        d = {}
        d["ticker"] = ticker
        d["num_comments"] = submission.num_comments
        d["comment_sentiment_average"] = commentSentiment(ticker, submission.url)
        if d["comment_sentiment_average"] == 0.000000:
            continue
        d["latest_comment_date"] = latestComment(ticker, submission.url)
        d["score"] = submission.score
        d["upvote_ratio"] = submission.upvote_ratio
        d["date"] = submission.created_utc
        d["domain"] = submission.domain
        d["num_crossposts"] = submission.num_crossposts
        d["author"] = submission.author
        submission_statistics.append(d)

dfSentimentStocks = pd.DataFrame(submission_statistics)

_timestampcreated = dfSentimentStocks["date"].apply(get_date)
dfSentimentStocks = dfSentimentStocks.assign(timestamp=_timestampcreated)

_timestampcomment = dfSentimentStocks["latest_comment_date"].apply(get_date)
dfSentimentStocks = dfSentimentStocks.assign(commentdate=_timestampcomment)

dfSentimentStocks.sort_values(
    "latest_comment_date", axis=0, ascending=True, inplace=True, na_position="last"
)

print(dfSentimentStocks)


print(dfSentimentStocks.author.value_counts())


save = False
if save:
    dfSentimentStocks.to_csv("Reddit_Sentiment_Equity.csv", index=False)
