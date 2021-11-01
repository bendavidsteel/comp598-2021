import argparse
import hashlib
import json
import os

import requests
import bs4

def get_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)

    cache_dir_path = os.path.abspath(config["cache_dir"])
    target_people = config["target_people"]

    return cache_dir_path, target_people

def get_html_from_cache_or_source(person, cache_dir_path):
    hash = hashlib.sha1(person.encode("UTF-8")).hexdigest()

    cached_file_path = os.path.join(cache_dir_path, hash)
    if os.path.exists(cached_file_path):
        with open(cached_file_path, 'r') as f:
            return f.read()
    
    else:
        r = requests.get(f'https://www.whosdatedwho.com/dating/{person}')
        html = r.text

        # ensure dir exists
        if not os.path.exists(cache_dir_path):
            os.makedirs(cache_dir_path)

        with open(cached_file_path, 'w') as f:
            f.write(html)

        return html

def get_relationships_from_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')

    relationships = []

    # get title of relationships section
    relationships_title = soup.find('h4', 'ff-auto-relationships')

    # go through next elements, stopping when they are no longer paragraphs, which means another section has started
    for relationships_section in relationships_title.next_siblings:
        if relationships_section.name != 'p':
            break

        # find the hyperlinks in the paragraph
        relation_urls = [link['href'] for link in relationships_section.find_all('a')]
        # parse the formatted name from the hyperlink
        relationships += [link.split('/')[-1] for link in relation_urls]

    return relationships

def main(args):
    config_path = os.path.abspath(args.config)
    # get variables from the config
    cache_dir_path, target_people = get_config(config_path)

    relationships = {}
    for person in target_people:
        # get the raw html from either the cache of the website
        html = get_html_from_cache_or_source(person, cache_dir_path)
        # parse the html to get the relationships
        relationships[person] = get_relationships_from_html(html)

    # save to desired file
    output_file_path = os.path.abspath(args.output)
    with open(output_file_path, 'w') as f:
        json.dump(relationships, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    main(args)