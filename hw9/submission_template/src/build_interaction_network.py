import argparse
import json
import os

import pandas as pd

def main(args):
    input_path = os.path.abspath(args.input)
    dialog_csv = pd.read_csv(input_path)

    # find the valid characters without 'others', 'ponies', 'and' or 'all' in their name
    stop_words = ['others', 'ponies', 'and', 'all']
    for stop_word in stop_words:
        dialog_csv = dialog_csv[~dialog_csv['pony'].str.contains(rf'\b{stop_word}\b', case=False)]
    # find the dialog counts of these characters
    speaker_counts = dialog_csv[['pony', 'dialog']].groupby('pony').count()
    # get a list of the top 101
    top_speakers = set(speaker_counts.sort_values('dialog', ascending=False).head(101).index)

    # find potential interactions
    raw_interactions = pd.concat([dialog_csv['title'].rename('titleA'), dialog_csv['pony'].rename('ponyA'), dialog_csv['title'].shift(-1).rename('titleB'), dialog_csv['pony'].shift(-1).rename('ponyB')], axis=1)
    # ensure we follow episode boundaries
    interactions = raw_interactions[raw_interactions['titleA'] == raw_interactions['titleB']][['ponyA', 'ponyB']]
    # ponies can't talk to themselves
    interactions = interactions[interactions['ponyA'] != interactions['ponyB']]
    # only ponies in top 101 chars
    interactions = interactions[interactions['ponyA'].isin(top_speakers) & interactions['ponyB'].isin(top_speakers)]

    interaction_network = {}
    for _, interaction in interactions.iterrows():
        pony_a = interaction['ponyA'].lower()
        pony_b = interaction['ponyB'].lower()
        if pony_a not in interaction_network:
            interaction_network[pony_a] = {}
        if pony_b not in interaction_network:
            interaction_network[pony_b] = {}
        if pony_b not in interaction_network[pony_a]:
            interaction_network[pony_a][pony_b] = 0
        if pony_a not in interaction_network[pony_b]:
            interaction_network[pony_b][pony_a] = 0
        interaction_network[pony_a][pony_b] += 1
        interaction_network[pony_b][pony_a] += 1

    output_path = os.path.abspath(args.output)
    dir_out_path = os.path.dirname(output_path)

    if not os.path.exists(dir_out_path):
        os.mkdir(dir_out_path)

    with open(output_path, 'w') as f:
        json.dump(interaction_network, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    main(args)