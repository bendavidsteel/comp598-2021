import os

import pandas as pd

def load_dataset():
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(this_dir_path, "..", "dataset.tsv")
    return pd.read_csv(dataset_path, sep='\t')

def save_as_tsv(df):
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    tsv_path = os.path.join(this_dir_path, "..", "results.tsv")
    df.to_csv(tsv_path, header=True, sep='\t', index=False)

def main():
    # load dataset from file
    df = load_dataset()

    # check for percentage of tweets with Trump mention
    num_tweets = len(df)
    num_mentioning_trump = len(df.loc[df['trump_mention']])
    percent_trump_mention = round((num_mentioning_trump / num_tweets) * 100, 3)

    # create dataframe to save the data
    results_df = pd.DataFrame(data = {'result': ['frac-trump-mentions'], 'value': [percent_trump_mention]})

    # write back out to file as TSV
    save_as_tsv(results_df)


if __name__ == "__main__":
    main()