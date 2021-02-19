Data Extraction
---
The code in this directory can be used to download and pre-process the tweets.

Place your Twitter API credentials in the ```twitter_key.txt``` file. This should include two access tokens, comma separated, i.e., ```twitter_oauth_consumer_key , twitter_oauth_consumer_secret```. You can learn more about Twitter API access [here](https://developer.twitter.com/en/support/twitter-api).

Once ```twitter_key.txt``` is updated, the rest of the data extraction pipeline can be automated with our provided script `data_extract.sh` that can be used to complete all steps below.


### Download the CoAID Dataset
Clone the CoAID dataset [here](https://github.com/cuilimeng/CoAID). 

For this project we only used the files present in `CoAID/05-01-2020/`, so feel free to get rid of rest of the files and move the files present in to the parent folder `CoAID/`.
The `get_coaid_data.sh` script should handle all of this for you. 


## Step-by-step description
`data_extract.sh` contains the following steps:


### Get Raw Tweets
The script `dump_raw_tweets.py` dumps tweets into a csv. 
Run `extract_real_and_fake_tweets_coaid.py` to download the tweets from CoAID dataset. 
```shell script
python3 extract_real_and_fake_tweets_coaid.py --data_type 1
```
Pass `1` or `2` as argument for `data_type`, for real or fake news/claims respectively. 

Make sure you have a Twitter API key in a file named `twitter_key.txt` 

### Generate the Full Dataset
Run `generate_full_dataset.py` to merge all three csv files
```shell script
python3 generate_full_dataset.py data_df real_df fake_df
```
Here the `data_df` is the path to the `full_dataset_label_ids` in this repo. `real_df` and `fake_df` are the paths to the tweet data of real and fake news respectively.

### Generate the Datasets for deFEND
The deFEND model works with news data and claim data in addition to tweets. To generate the datasets for fake and real labels run:
```shell script
python3 merge_claim_tweets_fake.py
python3 merge_claim_tweets_real.py 
python3 merge_news_tweets_fake.py
python3 merge_news_tweets_real.py
```
