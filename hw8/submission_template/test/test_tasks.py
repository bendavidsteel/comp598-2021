import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

import src.compile_word_counts as compile_word_counts
import src.compute_pony_lang as compute_pony_lang

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        output_path = os.path.join(os.path.dirname(__file__), 'word_counts.json')
        compile_word_counts.main(self.mock_dialog, output_path)

        with open(output_path, 'r') as f:
            counts = json.load(f)

        with open(self.true_word_counts, 'r') as f:
            true_counts = json.load(f)

        self.assertDictEqual(counts, true_counts)

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        tfidf = compute_pony_lang.compute_tfidf(self.true_word_counts)
        
        with open(self.true_tf_idfs, 'r') as f:
            true_tfidf = json.load(f)

        self.assertDictEqual(tfidf, true_tfidf)
    
if __name__ == '__main__':
    unittest.main()