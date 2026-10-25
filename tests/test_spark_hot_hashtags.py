"""Tests the pure stream parsing helpers."""

import unittest

import spark_hot_hashtags


class TestSparkHotHashtags(unittest.TestCase):
    """Checks conversion of incoming lines to Spark count pairs."""

    def test_parse_line_returns_one_pair_per_word(self):
        self.assertEqual(
            spark_hot_hashtags.parse_line('#python #spark'),
            [('#python', 1), ('#spark', 1)],
        )

    def test_parse_line_handles_repeated_words(self):
        """Repeated words are preserved so Spark can aggregate their counts."""
        self.assertEqual(
            spark_hot_hashtags.parse_line('#python #python'),
            [('#python', 1), ('#python', 1)],
        )

    def test_parse_line_accepts_arbitrary_whitespace(self):
        self.assertEqual(
            spark_hot_hashtags.parse_line('  #python\t#spark  '),
            [('#python', 1), ('#spark', 1)],
        )

    def test_parse_line_returns_empty_for_blank_input(self):
        self.assertEqual(spark_hot_hashtags.parse_line('  \t '), [])


if __name__ == '__main__':
    unittest.main()
