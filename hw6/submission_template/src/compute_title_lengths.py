import argparse
import json
import math
import os

def main(args):
    input_file_path = os.path.abspath(args.file)
    with open(input_file_path, 'r') as f:
        posts = [json.loads(line) for line in f.readlines()]

    sum_len = 0
    for post in posts:
        post_title_len = len(post['data']["title"])
        sum_len += post_title_len

    title_len_avg = round(sum_len / len(posts), 2)

    print(f"Average post title length is: {title_len_avg}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    main(args)