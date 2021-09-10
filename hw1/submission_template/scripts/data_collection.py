import os

import pandas as pd

def load_dataset():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(this_dir_path, "..", "data", "IRAhandle_tweets_1.csv")
    return pd.read_csv(dataset_path)

def save_as_tsv(df):
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    tsv_path = os.path.join(this_dir_path, "..", "data", "filtered_tweets.tsv")
    df.to_csv(tsv_path, header=True, sep='\t', index=False)

def main():
    # load dataset from file
    df = load_dataset()

    # only read first 10000 lines
    df = df.head(10000)

    # select only the rows with English tweets
    df = df.loc[df['language'] == "English"]

    # filter out questions
    df = df[~df['content'].str.contains("\?")]

    # write back out to file as TSV
    save_as_tsv(df)


if __name__ == "__main__":
    main()