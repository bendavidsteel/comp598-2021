import os

import pandas as pd

def load_dataset():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(this_dir_path, "..", "data", "filtered_tweets.tsv")
    return pd.read_csv(dataset_path, sep='\t')

def save_as_tsv(df):
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    tsv_path = os.path.join(this_dir_path, "..", "dataset.tsv")
    df.to_csv(tsv_path, header=True, sep='\t', index=False)

def main():
    # load dataset from file
    df = load_dataset()

    # check for mention of word Trump in tweet
    # ensure that the word is Trump is only surrounded by non-alphanumeric characters
    df['trump_mention'] = df['content'].str.contains('(?:^|[^a-zA-Z\d])Trump(?:[^a-zA-Z\d]|$)')

    # filter dataset to only the columns we need
    df = df[['tweet_id', 'publish_date', 'content', 'trump_mention']]

    # write back out to file as TSV
    save_as_tsv(df)


if __name__ == "__main__":
    main()