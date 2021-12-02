import argparse
import collections
import json
import os
import re

import pandas as pd

def main(dialog_path, output_path):
    # read in dialog csv
    dialog = pd.read_csv(dialog_path)

    # read in stopwords
    this_dir_path = os.path.dirname(os.path.abspath(__file__))
    stop_words_path = os.path.join(this_dir_path, '..', 'data', 'stopwords.txt')
    stop_words = set()
    with open(stop_words_path, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                stop_words.add(line.strip())

    # go through characters and get dialog
    char_counts = {
        'twilight sparkle': collections.Counter(),
        'applejack': collections.Counter(), 
        'rarity': collections.Counter(), 
        'pinkie pie': collections.Counter(), 
        'rainbow dash': collections.Counter(), 
        'fluttershy': collections.Counter()
    }
    puncs = "()[],-.?!:;#&"
    for char in char_counts:
        # only getting fullmatch for pony, case insensitive
        all_char_lines = dialog[dialog['pony'].str.fullmatch(char, flags=re.IGNORECASE)]
        for char_line in all_char_lines['dialog']:
            # replace punctuation with spaces
            for punc in puncs:
                char_line = char_line.replace(punc, ' ')

            # cast to lowercase
            line = char_line.lower()

            # split into alpha words
            words = [word for word in line.split(' ') if word.isalpha()]

            # remove stopwords
            words = [word for word in words if word not in stop_words]

            # update char word counter
            char_counts[char].update(words)

    # compile master word count of all speech acts
    all_word_counts = collections.Counter()
    for char in char_counts:
        all_word_counts += char_counts[char]
    all_word_counts = dict(all_word_counts)

    MIN_COUNT = 5
    for char in char_counts:
        char_counts[char] = { word: count for word, count in char_counts[char].items() if all_word_counts[word] >= MIN_COUNT }

    # output char counts
    output_dir_path = os.path.dirname(output_path)
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)

    with open(output_path, 'w') as f:
        json.dump(char_counts, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-d', '--dialog')
    args = parser.parse_args()

    dialog_path = os.path.abspath(args.dialog)
    output_path = os.path.abspath(args.output)
    main(dialog_path, output_path)