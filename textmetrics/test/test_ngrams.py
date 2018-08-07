"""
Test the ngram extractor is working correctly.
"""

# builtins
import code
import unittest

# local
from textmetrics.custom import ngrams


class TestNgrams(unittest.TestCase):

    def test_uni(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 8
        self.assertEqual(len(set(txt.split())), expected)  # sanity check
        unique_1grams = ngrams.run_ngrams(txt, [1])['overall_unique'][1]
        self.assertEqual(unique_1grams, expected)

    def test_bi(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 8
        unique_2grams = ngrams.run_ngrams(txt, [2])['overall_unique'][2]
        self.assertEqual(unique_2grams, expected)

    def test_tri(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 7
        unique_3grams = ngrams.run_ngrams(txt, [3])['overall_unique'][3]
        self.assertEqual(unique_3grams, expected)

    def test_quad(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 6
        unique_4grams = ngrams.run_ngrams(txt, [4])['overall_unique'][4]
        self.assertEqual(unique_4grams, expected)


if __name__ == '__main__':
    unittest.main()
