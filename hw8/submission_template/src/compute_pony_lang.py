import argparse
import collections
import json
import math
import os

def compute_tfidf(counts_path):
    with open(counts_path, 'r') as f:
        char_counts = json.load(f)

    # compute document freq
    df = collections.Counter()
    for char in char_counts:
        df.update(char_counts[char].keys())

    # compute inverse doc freq
    idf = {}
    for word in df:
        idf[word] = math.log10(len(char_counts) / df[word])

    tfidf = {}
    for char in char_counts:
        tfidf[char] = {}
        # compute tf-idf
        for word in char_counts[char]:
            tfidf[char][word] = char_counts[char][word] * idf[word]

    return tfidf


def main(counts_path, num_words):
    tfidf = compute_tfidf(counts_path)

    top_words = {}
    for char in tfidf:
        # sort tfidf scores
        ranked_tfidf = sorted(list(tfidf[char].items()), key=lambda tup: tup[1], reverse=True)

        # get highest tfidfs
        top_words[char] = [word for word, score in ranked_tfidf[:num_words]]

    # prepare for printing
    ponies = [
        'twilight sparkle',
        'applejack',
        'rarity',
        'pinkie pie',
        'rainbow dash',
        'fluttershy'
    ]
    pony_words = {}
    for pony in ponies:
        pony_words[pony] = top_words[pony] if pony in top_words else []

    print(json.dumps(pony_words, indent=4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--counts')
    parser.add_argument('-n', '--num')
    args = parser.parse_args()

    counts_path = os.path.abspath(args.counts)
    num_words = int(args.num)
    main(counts_path, num_words)