#!/usr/bin/env python

import os

import pandas as pd

COAID_PATH = os.path.join(os.path.dirname(__file__), "..", "CoAID")
REAL_TWEET_PATH = os.getcwd()

df_claim_real_tweet = pd.read_csv(os.path.join(COAID_PATH, "ClaimRealCOVID-19_tweets.csv"))

df_claim_real_tweet["id"] = df_claim_real_tweet["tweet_id"]
df_claim_real_tweet = df_claim_real_tweet.drop(["tweet_id"], axis=1)

df_real_tweets = pd.read_csv(os.path.join(REAL_TWEET_PATH, "coaid_tweets_real.csv"))

df_real_tweet_claims = pd.merge(df_claim_real_tweet, df_real_tweets, on="id", how="left")

df_real_tweet_claims.to_csv(os.path.join(COAID_PATH, "ClaimRealCOVID-19_tweets_expanded.csv"), index=False)

df_claim_real_tweet_replies = pd.read_csv(os.path.join(COAID_PATH, "ClaimRealCOVID-19_tweets_replies.csv"))
df_claim_real_tweet_replies = df_claim_real_tweet_replies.drop(["tweet_id"], axis=1)

df_real_replies_claims = pd.merge(df_claim_real_tweet_replies, df_real_tweets,
                                  left_on="reply_id",
                                  right_on="id", how="left")
df_real_replies_claims = df_real_replies_claims.drop(["reply_id"], axis=1)

df_real_replies_claims.to_csv(os.path.join(COAID_PATH, "ClaimRealCOVID-19_replies_expanded.csv"), index=False)
