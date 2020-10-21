import json
import logging
import os
import sys
import time

import pandas as pd
import tweepy
from joblib import Parallel, delayed

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(root_folder, "twitter_key.txt")) as f:
    consumer_credentials = [
        x.split(",") for x in f.readlines()
    ]  # read only a single line

consumer_keys = list(map(lambda x: x[0].strip(), consumer_credentials))
consumer_secrets = list(map(lambda x: x[1].strip(), consumer_credentials))
consumer_credentials = zip(consumer_keys, consumer_secrets)

folder_path = os.path.join(root_folder, "COVID-19-TweetIDs")

api_rate_limit = 900  # rate limit set
sleep_time = 60 * (15 + 1)  # seconds. Sleep for 16 minutes
# See more for rate limits here: https://developer.twitter.com/en/docs/basics/rate-limits

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
tweet_logger = logging.getLogger(__name__)


def get_status(api, tweet_id):
    tweet_returned = False
    dataframe_row = {}

    tweet_id = tweet_id.strip()
    try:
        tweet_info = api.get_status(tweet_id, tweet_mode="extended")  # get full tweet
        lang = tweet_info.lang.strip()
        if lang == "en":
            # english raw text
            tweet_returned = True

            # import code
            # code.interact(local={**locals(), **globals()})
            status_json = json.loads(json.dumps(tweet_info._json))
            dataframe_row = dict([(k, json.dumps(status_json[k])) for k in status_json])
            return tweet_returned, dataframe_row

    except Exception as e:
        if isinstance(e, tweepy.error.TweepError):
            tweet_logger.info(f"API Error on id {tweet_id}. Error is {e}")

    return tweet_returned, dataframe_row


def main():
    # get tweepy auth
    api_objs = []  # api objects = no. of key,secret
    for key, secret in consumer_credentials:
        auth = tweepy.OAuthHandler(key, secret)
        api = tweepy.API(auth)
        api_objs.append(api)

    #  get folder names
    year = "2020"
    month = "05"
    tweet_month = "-".join([year, month])
    tweet_id_folder_path = os.path.join(folder_path, tweet_month)
    csv_folder_path = os.path.join("raw_tweets.csv")

    # open pandas df
    if os.path.exists(csv_folder_path):
        df = pd.read_csv(csv_folder_path)
    else:
        df = pd.DataFrame(columns=["id", "raw_text"])

    # file record dump
    file_dump_path = "file_record_dump.txt"
    if os.path.exists(file_dump_path):
        with open(file_dump_path, "r") as file_dump_obj:
            files_covered = [x.strip() for x in file_dump_obj.readlines()]
    else:
        files_covered = []

    start_time = time.time()
    for file in os.listdir(tweet_id_folder_path):
        if file in files_covered:
            continue  # file

        try:
            tweet_id_file_path = os.path.join(tweet_id_folder_path, file)
            tweet_logger.info(f"Reading from file {tweet_id_file_path}")
            with open(tweet_id_file_path) as tweet_f:
                tweet_ids = tweet_f.readlines()

            tweet_logger.info("Start grabbing tweets")
            chunk_size = 100 * len(api_objs)
            number_of_parallel_jobs = 16 * len(api_objs)  # increase or decrease for performance?
            backend = "threading"  # faster, no GIL is used
            for index in range(0, len(tweet_ids), chunk_size):
                start = index
                end = min(index + chunk_size, len(tweet_ids))  # don't go beyond length

                if (end // api_rate_limit) - (start // api_rate_limit) > 0:
                    # rate limit has been hit
                    tweet_logger.info("Rate Limit Hit. Taking a break...")
                    time.sleep(sleep_time)

                parallel_tweet_ids = [
                    tweet_ids[x]
                    for x in range(start, end)
                    if tweet_ids[x] not in df["id"]
                ]

                # construct arguments
                parallel_api_args = []
                for i in range(len(parallel_tweet_ids)):
                    parallel_api_args.append((api_objs[i % len(api_objs)], parallel_tweet_ids[i]))

                # parallel make api calls
                results = Parallel(n_jobs=number_of_parallel_jobs, backend=backend)(
                    delayed(get_status)(*tweet_arg)
                    for tweet_arg in parallel_api_args
                )

                for save_tweet, row in results:
                    if save_tweet:
                        df = df.append(row, ignore_index=True)

                if index % 100 == 0:
                    tweet_logger.info(f"Progress: {index}")

                # if end % api_rate_limit == 0:
                #     # rate limit has been hit
                #     tweet_logger.info("Rate Limit Hit. Taking a break...")
                #     time.sleep(sleep_time)

        except Exception as e:
            # Any other type of error, then ShutDown
            if isinstance(e, tweepy.error.RateLimitError):
                tweet_logger.info("Rate Limit Error")
            else:
                tweet_logger.info(f"Encountered exception {e}")
            tweet_logger.info("Closing API")
            tweet_logger.info("Dumping currently collected tweets")
            df.to_csv(csv_folder_path, index=False)  # dump current df
            return  # Exit condition

        files_covered.append(file)  # add to files covered
        df.to_csv(csv_folder_path, index=False)  # write to df
        # break
        tweet_logger.info("Pause between files...")
        time.sleep(sleep_time)

    end_time = time.time()
    tweet_logger.info(f"Total time taken: {(end_time - start_time)}")

    df.to_csv(csv_folder_path, index=False)

    with open(os.path.join(root_folder, file_dump_path), "w") as file_dump_obj:
        file_str = "\n".join(files_covered)
        file_dump_obj.write(file_str)


if __name__ == "__main__":
    main()
