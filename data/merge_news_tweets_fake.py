#!/usr/bin/env python

import os

import pandas as pd

COAID_PATH = os.path.join(os.path.dirname(__file__), "..", "CoAID")
FAKE_TWEET_PATH = os.getcwd()

df_news_fake_tweet = pd.read_csv(os.path.join(COAID_PATH, "NewsFakeCOVID-19_tweets.csv"))

df_news_fake_tweet["id"] = df_news_fake_tweet["tweet_id"]
df_news_fake_tweet = df_news_fake_tweet.drop(["tweet_id"], axis=1)

df_fake_tweets = pd.read_csv(os.path.join(FAKE_TWEET_PATH, "coaid_tweets_fake.csv"))

df_fake_tweet_newss = pd.merge(df_news_fake_tweet, df_fake_tweets, on="id", how="left")

df_fake_tweet_newss.to_csv(os.path.join(COAID_PATH, "NewsFakeCOVID-19_tweets_expanded.csv"), index=False)

df_news_fake_tweet_replies = pd.read_csv(os.path.join(COAID_PATH, "NewsFakeCOVID-19_tweets_replies.csv"))
df_news_fake_tweet_replies = df_news_fake_tweet_replies.drop(["tweet_id"], axis=1)

df_fake_replies_newss = pd.merge(df_news_fake_tweet_replies, df_fake_tweets, left_on="reply_id", right_on="id",
                                 how="left")
df_fake_replies_newss["id"] = df_fake_replies_newss["reply_id"]
df_fake_replies_newss = df_fake_replies_newss.drop(["reply_id"], axis=1)

df_fake_replies_newss.to_csv(os.path.join(COAID_PATH, "NewsFakeCOVID-19_tweets_replies_expanded.csv"), index=False)
