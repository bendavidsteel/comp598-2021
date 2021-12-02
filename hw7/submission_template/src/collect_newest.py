import argparse
import json
import os

from dotenv import load_dotenv
import requests
import requests.auth

def do_auth():

    load_dotenv()

    s = requests.Session()

    user_agent = f"Python:PythonScript:v1.0.0 (by /u/{os.environ['REDDIT_USER']})"
    s.headers.update({
        'User-Agent': user_agent
    })
    return s

def read_subs_and_write(session, sub, file_path):
    r = session.get(f'https://www.reddit.com{sub}/new.json?limit=100')
    r_data = r.json()
    sub_posts = r_data['data']['children'][:100]

    assert len(sub_posts) == 100

    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    with open(file_path, 'w') as f:
        for post in sub_posts:
            f.write(f"{json.dumps(post)}\n")

def main(args):

    s = do_auth()

    file_path = os.path.abspath(args.output)
    read_subs_and_write(s, args.subreddit, file_path)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-s', '--subreddit')
    args = parser.parse_args()

    main(args)