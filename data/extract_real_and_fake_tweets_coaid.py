import argparse

from dump_raw_tweets import *

folder_path = os.path.join(root_folder, "CoAID")


def get_ids_from_csv(filename, id_columns):
    df = pd.read_csv(os.path.join(folder_path, filename))
    tweet_ids = df[id_columns].values.flatten()
    return list(map(str, tweet_ids))


def get_fake_tweet_ids():
    tweet_ids = set()
    fake_tweet_paths = ["ClaimFakeCOVID-19_tweets.csv", "ClaimFakeCOVID-19_tweets_replies.csv"]
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(fake_tweet_paths[0], ["tweet_id"])))
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(fake_tweet_paths[1], ["tweet_id", "reply_id"])))

    real_tweet_paths = ["NewsFakeCOVID-19_tweets.csv", "NewsFakeCOVID-19_tweets_replies.csv"]
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(real_tweet_paths[0], ["tweet_id"])))
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(real_tweet_paths[1], ["tweet_id", "reply_id"])))
    return list(tweet_ids)


def get_real_tweet_ids():
    tweet_ids = set()
    fake_tweet_paths = ["ClaimRealCOVID-19_tweets.csv", "ClaimRealCOVID-19_tweets_replies.csv"]
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(fake_tweet_paths[0], ["tweet_id"])))
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(fake_tweet_paths[1], ["tweet_id", "reply_id"])))

    real_tweet_paths = ["NewsRealCOVID-19_tweets.csv", "NewsRealCOVID-19_tweets_replies.csv"]
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(real_tweet_paths[0], ["tweet_id"])))
    tweet_ids = tweet_ids.union(set(get_ids_from_csv(real_tweet_paths[1], ["tweet_id", "reply_id"])))
    return list(tweet_ids)


def main(label_type: int = 1):
    if label_type == 1:
        tweet_ids = get_real_tweet_ids()
        new_csv_path = os.path.join("coaid_tweets_real.csv")
    elif label_type == 2:
        tweet_ids = get_fake_tweet_ids()  # all tweet ids
        new_csv_path = os.path.join("coaid_tweets_fake.csv")
    else:
        tweet_logger.info("Label Type unspecified. Quitting...")
        return None

    # get tweepy auth
    api_objs = []  # api objects = no. of key,secret
    for key, secret in consumer_credentials:
        auth = tweepy.OAuthHandler(key, secret)
        api = tweepy.API(auth)
        api_objs.append(api)

    df = pd.DataFrame(columns=["id", "raw_text"])  # new empty dataframe

    start_time = time.time()
    try:
        tweet_logger.info("Start grabbing tweets")
        chunk_size = 100 * len(api_objs)
        number_of_parallel_jobs = 32 * len(api_objs)  # increase or decrease for performance?
        backend = "threading"  # faster, no GIL is used
        for index in range(0, len(tweet_ids), chunk_size):
            start = index
            end = min(index + chunk_size, len(tweet_ids))  # don't go beyond length

            if (end // api_rate_limit) - (start // api_rate_limit) > 0:
                # rate limit has been hit
                tweet_logger.info("Rate Limit Hit. Taking a break...")
                time.sleep(sleep_time)

            parallel_tweet_ids = [
                tweet_ids[k]
                for k in range(start, end)
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
    except Exception as e:
        # Any other type of error, then ShutDown
        if isinstance(e, tweepy.error.RateLimitError):
            tweet_logger.info("Rate Limit Error")
        else:
            tweet_logger.info(f"Encountered exception {e}")
        tweet_logger.info("Closing API")
        tweet_logger.info("Dumping currently collected tweets")
        df.to_csv(new_csv_path, index=False)  # dump current df
        return  # Exit condition
    end_time = time.time()
    tweet_logger.info(f"Total time taken: {(end_time - start_time)}")
    df.to_csv(new_csv_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Extraction for Tweets')
    parser.add_argument('--data_type', type=int, help='1 for Real news/claims and 2 for Fake')
    args = parser.parse_args()
    main(args.data_type)
