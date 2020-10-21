import argparse

import pandas as pd


def merge_all(label_path, real_path, fake_path):
    label_id = pd.read_csv(label_path)
    coaid_tweets_real_df = pd.read_csv(real_path)
    coaid_tweets_fake_df = pd.read_csv(fake_path)

    df_real_labels = label_id.merge(coaid_tweets_real_df, left_on='id', right_on='id', how='inner')
    df_fake_labels = label_id.merge(coaid_tweets_fake_df, left_on='id', right_on='id', how='inner')

    df_full = df_fake_labels.append(df_real_labels)

    df_full.to_csv('full_dataset.csv', index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Extraction for Tweets')
    parser.add_argument('data_df', type=str, help='path to dataframe id -> label')
    parser.add_argument('real_df', type=str, help='path to coaid_tweets_real.csv')
    parser.add_argument('fake_df', type=str, help='path to coaid_tweets_fake.csv')
    args = parser.parse_args()
    merge_all(args.data_df, args.real_df, args.fake_df)
