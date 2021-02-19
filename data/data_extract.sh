#!/bin/bash

# get tweets
python3 extract_real_and_fake_tweets_coaid.py --data_type 1 # real
python3 extract_real_and_fake_tweets_coaid.py --data_type 2 # fake

# get dataset
python3 generate_full_dataset.py full_dataset_label_ids.csv coaid_tweets_real.csv coaid_tweets_fake.csv

# merge datasets for deFEND
python3 merge_claim_tweets_fake.py
python3 merge_claim_tweets_real.py
python3 merge_news_tweets_fake.py
python3 merge_news_tweets_real.py