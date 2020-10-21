#!/usr/bin/env python

import os

import pandas as pd

COAID_PATH = os.path.join(os.path.dirname(__file__), "..", "CoAID")
FAKE_TWEET_PATH = os.getcwd()

df_claim_fake_tweet = pd.read_csv(os.path.join(COAID_PATH, "ClaimFakeCOVID-19_tweets.csv"))

df_claim_fake_tweet.head()

df_claim_fake_tweet["id"] = df_claim_fake_tweet["tweet_id"]
df_claim_fake_tweet = df_claim_fake_tweet.drop(["tweet_id"], axis=1)

df_fake_tweets = pd.read_csv(os.path.join(FAKE_TWEET_PATH, "coaid_tweets_fake.csv"))

df_fake_tweet_claims = pd.merge(df_claim_fake_tweet, df_fake_tweets, on="id", how="left")

df_fake_tweet_claims.to_csv(os.path.join(COAID_PATH, "ClaimFakeCOVID-19_tweets_expanded.csv"), index=False)

df_claim_fake_tweet_replies = pd.read_csv(os.path.join(COAID_PATH, "ClaimFakeCOVID-19_tweets_replies.csv"))
df_claim_fake_tweet_replies = df_claim_fake_tweet_replies.drop(["tweet_id"], axis=1)

df_fake_replies_claims = pd.merge(df_claim_fake_tweet_replies, df_fake_tweets, left_on="reply_id", right_on="id",
                                  how="left")
df_fake_replies_claims = df_fake_replies_claims.drop(["reply_id"], axis=1)

df_fake_replies_claims.to_csv(os.path.join(COAID_PATH, "ClaimFakeCOVID-19_replies_expanded.csv"), index=False)
