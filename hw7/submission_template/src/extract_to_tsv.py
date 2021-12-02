import argparse
import json
import os
import random

import pandas as pd

def main(args):
    input_file_path = os.path.abspath(args.input)

    posts = []
    with open(input_file_path, 'r') as f:
        for line in f.readlines():
            posts.append(json.loads(line))

    # sample a selection of these posts
    num_posts = int(args.n)
    if num_posts > len(posts):
        selected_posts = posts
    else:
        selected_posts = random.sample(posts, num_posts)

    # convert json to dataframe
    df = pd.DataFrame([{"Name": post["data"]["name"], "title": post['data']['title'], "coding": ""} for post in selected_posts])

    # write out as tsv
    output_file_path = os.path.abspath(args.output)

    # make dir if it does not exist
    dir_path = os.path.dirname(output_file_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    df.to_csv(output_file_path, sep='\t')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('input')
    parser.add_argument('n')
    args = parser.parse_args()

    main(args)