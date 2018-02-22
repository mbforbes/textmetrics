"""
Test the ngram extractor is working correctly.
"""

# builtins
import unittest

# local
from . import ngrams


class TestNgrams(unittest.TestCase):

    def test_uni(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 8
        self.assertEqual(len(set(txt.split())), expected)  # sanity check
        self.assertEqual(ngrams.run_ngram(txt, 1), expected)  # test

    def test_bi(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 8
        self.assertEqual(ngrams.run_ngram(txt, 2), expected)  # test

    def test_tri(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 7
        self.assertEqual(ngrams.run_ngram(txt, 3), expected)  # test

    def test_quad(self) -> None:
        txt = 'i like to eat cheese . \n cheese is what i like to eat'
        expected = 6
        self.assertEqual(ngrams.run_ngram(txt, 4), expected)  # test


if __name__ == '__main__':
    unittest.main()
