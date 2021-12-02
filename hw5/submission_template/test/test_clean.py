import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

import src.clean as clean


class CleanTest(unittest.TestCase):
    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
        self.fixtures = {}

        file_dir = os.path.dirname(os.path.abspath(__file__))
        fixture_dir = os.path.join(file_dir, 'fixtures')
        for idx in range(1, 7):
            file_path = os.path.join(fixture_dir, f"test_{idx}.json")
            with open(file_path, 'r') as f:
                self.fixtures[idx] = f.read()
        

    def test_title(self):
        # load good and bad examples of posts with titles
        no_title_line = self.fixtures[1]
        title_line = self.fixtures[2]
        lines = [no_title_line, title_line]
        posts = clean.try_transform_posts(lines, clean.try_load_post)
        _, title_post = posts

        # check them with function from clean
        checked_posts = clean.check_posts(posts, clean.check_contains_title)

        # check we got rid of the bad one
        self.assertEqual(len(checked_posts), 1)
        # check the remaining one is the good one
        self.assertIs(checked_posts[0], title_post)

    def test_standardize_datetime(self):
        # load good and bad examples of posts with createdAt values
        bad_datetime_line = self.fixtures[2]
        good_datetime_line = self.fixtures[1]
        lines = [bad_datetime_line, good_datetime_line]
        posts = clean.try_transform_posts(lines, clean.try_load_post)
        _, good_datetime_post = posts

        # check them with function from clean
        checked_posts = clean.try_transform_posts(posts, clean.try_standardize_created_at)

        # check we got rid of the bad one
        self.assertEqual(len(checked_posts), 1)
        # check the remaining one is the good one
        self.assertIs(checked_posts[0], good_datetime_post)

    def test_load_post(self):
        bad_json_line = self.fixtures[3]
        good_json_line = self.fixtures[1]
        lines = [bad_json_line, good_json_line]

        # try to load good and bad lines
        posts = clean.try_transform_posts(lines, clean.try_load_post)

        # check the one loaded is the valid one
        # and that we filtered out the bad one
        self.assertEqual(len(posts), 1)

        good_json_post = clean.try_load_post(good_json_line)
        self.assertDictEqual(posts[0], good_json_post)

    def test_valid_author(self):
        # load good and bad examples of posts with author values
        bad_author_line = self.fixtures[4]
        good_author_line = self.fixtures[1]
        lines = [bad_author_line, good_author_line]
        posts = clean.try_transform_posts(lines, clean.try_load_post)
        _, good_author_post = posts

        # check them with function from clean
        checked_posts = clean.check_posts(posts, clean.valid_author_field)

        # check we got rid of the bad one
        self.assertEqual(len(checked_posts), 1)
        # check the remaining one is the good one
        self.assertIs(checked_posts[0], good_author_post)

    def test_total_count(self):
        # load good and bad examples of posts with total_count values
        bad_total_count_line = self.fixtures[5]
        good_total_count_line = self.fixtures[1]
        lines = [bad_total_count_line, good_total_count_line]
        posts = clean.try_transform_posts(lines, clean.try_load_post)

        # check that when trying to standardize the createdAt times, the invalid dates get removed
        checked_posts = clean.try_transform_posts(posts, clean.try_cast_count)
        good_total_count_post = clean.try_cast_count(posts[1])

        # check we got rid of the bad one
        self.assertEqual(len(checked_posts), 1)
        # check the remaining one is the good one
        self.assertIs(checked_posts[0], good_total_count_post)
        # check good post has int for total_count
        self.assertEqual(type(good_total_count_post['total_count']), int)

    def test_tags(self):
        tags_line = self.fixtures[6]
        tags_post = clean.try_load_post(tags_line)
        new_tags_post = clean.fix_tags(tags_post)

        # check there are no more spaces in the tags
        for tag in new_tags_post['tags']:
            self.assertNotIn(' ', tag)

        # check there are the correct number of new tags
        correct_num_tags = sum(1 + tag.count(' ') for tag in tags_post['tags'])
        self.assertEqual(len(new_tags_post['tags']), correct_num_tags)
    
if __name__ == '__main__':
    unittest.main()