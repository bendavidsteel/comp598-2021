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

def read_subs_and_write(session, subs, file_path):
    all_posts = []
    for subred in subs:
        r = session.get(f'https://www.reddit.com/r/{subred}/new.json?limit=100')
        r_data = r.json()
        sub_posts = r_data['data']['children']
        for idx in range(100):
            all_posts.append(sub_posts[idx])

    assert len(all_posts) == 1000

    with open(file_path, 'w') as f:
        for post in all_posts:
            f.write(f"{json.dumps(post)}\n")

def main():

    s = do_auth()

    this_file_path = os.path.dirname(os.path.abspath(__file__))

    most_sub_subs = ['funny', 'AskReddit', 'gaming', 'aww', 'pics', 'Music', 'science', 'worldnews', 'videos', 'todayilearned']
    file_path = os.path.join(this_file_path, '..', 'sample1.json')
    read_subs_and_write(s, most_sub_subs, file_path)

    most_post_subs = ['AskReddit', 'memes', 'politics', 'nfl', 'nba', 'wallstreetbets', 'teenagers', 'PublicFreakout', 'leagueoflegends', 'unpopularopinion']
    file_path = os.path.join(this_file_path, '..', 'sample2.json')
    read_subs_and_write(s, most_post_subs, file_path)

if __name__ == '__main__':
    main()