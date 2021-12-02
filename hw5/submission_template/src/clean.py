import argparse
from datetime import datetime, time, timezone
import json
from json.decoder import JSONDecodeError
import os

def load_input(input_file_path):
    input_file_path = os.path.abspath(args.input)
    with open(input_file_path, 'r') as f:
        return f.readlines()

def try_load_post(line):
    try:
        return json.loads(line)
    except JSONDecodeError:
        return None


def check_contains_title(post):
    return 'title' in post or 'title_text' in post

def rename_title_field(post):
    # we have been told that there will be either title_text or title, never both
    if 'title_text' in post:
        post['title'] = post['title_text']
        del post['title_text']
    return post

def fix_tags(post):
    if 'tags' not in post:
        return post

    new_tags = []
    for tag in post['tags']:
        if ' ' in tag:
            split_tags = tag.split()
            new_tags += split_tags
        else:
            new_tags.append(tag)

    post['tags'] = new_tags
    return post

def valid_author_field(post):
    return not ('author' not in post or post['author'] == '' or post['author'] == None or post['author'] == 'null' or post['author'] == 'N/A')

def try_cast_count(post):
    if 'total_count' not in post:
        return post

    total_count = post['total_count']

    if type(total_count) is str:
        try:
            post['total_count'] = int(total_count)
            return post
        except ValueError:
            return None

    elif type(total_count) is float:
        post['total_count'] = round(total_count)
        return post

    elif type(total_count) is int:
        return post
    else:
        return None

def try_standardize_created_at(post):
    try:
        created_at = datetime.strptime(post['createdAt'], '%Y-%m-%dT%H:%M:%S%z')
        utc_created_at = created_at.astimezone(tz=timezone.utc)
        post['createdAt'] = utc_created_at.isoformat()
        return post
    except ValueError:
        return None

def write_output(output_file_path, objs):
    output_file_path = os.path.abspath(output_file_path)
    with open(output_file_path, 'w') as f:
        for obj in objs:
            line = json.dumps(obj)
            f.write(f"{line}\n")

def try_transform_posts(posts, fn):
    new_posts = []
    for post in posts:
        tried_post = fn(post)
        if tried_post:
            new_posts.append(tried_post)

    return new_posts

def transform_posts(posts, fn):
    return [fn(post) for post in posts]

def check_posts(posts, fn):
    return [post for post in posts if fn(post)]

def main(args):
    lines = load_input(args.input)

    # remove all the posts that are invalid JSON dictionaries
    posts = try_transform_posts(lines, try_load_post)

    # remove all the posts that don’t have either a title or title_text field
    posts = check_posts(posts, check_contains_title)

    # for objects with a title_text field, rename the field in the output object to title
    posts = transform_posts(posts, rename_title_field)

    # remove all the posts where the author field is empty, null, or N/A
    posts = check_posts(posts, valid_author_field)

    # The tags field should be a list of individual words(where each word does NOT contain a space).  
    # any element that contains spaces should be split into separate words. 
    # if the tags field is not present, you do not have to drop the record; keep the record in the output file. 
    # In the input files we'll use, tags will always be a list. 
    # Do not worry about conversions.
    # E.g., if tags is [“golf”, “tennis”, “football games”], after processing it should be [“golf”, “tennis”,“football”, “games”]
    posts = transform_posts(posts, fix_tags)

    # The value in the total_count can only be type int,float, str. You must attempt to cast float and str to an int value.  
    # Some examples: “3”→3; “27”→27 “twenty”→INVALID 22.1→22; 22.9→22
    # If you are unable to cast total_count to int, remove the post.
    # Remove all posts if the type of total_count is anything else rather than int, float, str.
    # If total_count is not present, you do not have to remove the JSON object; keep it in the output file
    cleaned_count_posts = try_transform_posts(posts, try_cast_count)

    # remove all the posts with invalid date time that can’t be parsed using the ISO datetime standard
    # standardize all createdAt date times to the UTC timezone
    cleaned_posts = try_transform_posts(cleaned_count_posts, try_standardize_created_at)

    # posts that haven’t been flagged for removal should be written to the output file in the order they appear inthe input file
    write_output(args.output, cleaned_posts)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i')
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    main(args)