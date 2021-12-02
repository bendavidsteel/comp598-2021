import argparse
import collections
import json
import os

import pandas as pd

def main(args):
    # load labelled file
    input_file_path = os.path.abspath(args.input)
    df = pd.read_csv(input_file_path, sep='\t')

    count = dict(collections.Counter(df["coding"]))

    stats = {
        "course-related": count["c"] if "c" in count else 0,
        "food-related": count["f"] if "f" in count else 0,
        "residence-related": count["r"] if "r" in count else 0,
        "other": count["o"] if "o" in count else 0
    }

    if args.output is None:
        print(json.dumps(stats, indent=0))
    else:
        output_file_path = os.path.abspath(args.output)
        with open(output_file_path, 'w') as f:
            json.dump(stats, f, indent=0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    main(args)