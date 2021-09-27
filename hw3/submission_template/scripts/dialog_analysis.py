import argparse
import json
import pathlib

import pandas as pd

def load_dataset(input_file):
    return pd.read_csv(input_file.resolve())

def write_json(output_file, data):

    with open(output_file.resolve(), 'w') as f:
        f.write(json.dumps(data))

def main(output_file, input_file):
    df = load_dataset(input_file)

    speakers = df['pony'].unique()

    char_regexes = {    
        'twilight sparkle': r'[Tt]wilight [Ss]parkle', 
        'applejack': r'[Aa]pplejack', 
        'rarity': r'[Rr]arity', 
        'pinkie pie': r'[Pp]inkie [Pp]ie', 
        'rainbow dash': r'[Rr]ainbow [Dd]ash', 
        'fluttershy': r'[Ff]luttershy'
    }

    char_counts = {}
    for char, regex in char_regexes.items():
        char_counts[char] = len(df[df['pony'].str.count(regex) > 0])

    line_count = len(df)
    char_verbosity = {}
    for char, count in char_counts.items():
        char_verbosity[char] = round(count / line_count, 2)

    out = { 'count': char_counts, 'verbosity': char_verbosity }

    write_json(output_file, out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Dialog analysis.')
    parser.add_argument('input_file', type=pathlib.Path)
    parser.add_argument('-o', '--output', type=pathlib.Path)

    args = parser.parse_args()

    main(args.output, args.input_file)
