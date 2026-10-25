"""checks bar_chart"""

import unittest
import bar_chart


class TestBarChart(unittest.TestCase):
    """checks bar_chart"""

    def test_classic(self):
        """checks no special union"""
        lines = ['#a,2', '#b,4']
        mydict = bar_chart.get_lines(lines)
        self.assertEqual(mydict['#a'], 2)
        self.assertEqual(mydict['#b'], 4)

    def test_sub_first(self):
        """checks a12 substr of a123"""
        lines = ['#a12,2', '#a123,4']
        mydict = bar_chart.get_lines(lines)
        self.assertEqual(mydict['#a123'], 6)
        self.assertEqual(len(mydict), 1)

    def test_sub_second(self):
        """this time a12 is after a123"""
        lines = ['#a123,2', '#a12,4']
        mydict = bar_chart.get_lines(lines)
        self.assertEqual(mydict['#a123'], 6)
        self.assertEqual(len(mydict), 1)

    def test_duplicate_hashtags_are_summed(self):
        """repeated rows for the same hashtag contribute to one total"""
        lines = ['#python,2', '#python,3']
        self.assertEqual(bar_chart.get_lines(lines), {'#python': 5})

    def test_header_and_non_positive_counts_are_ignored(self):
        """the CSV header and zero or negative totals are not charted"""
        lines = ['#HASHTAG-COUNT', '#python,0', '#spark,-2', '#java,4']
        self.assertEqual(bar_chart.get_lines(lines), {'#java': 4})

    def test_short_substrings_are_not_merged(self):
        """hashtags shorter than the overlap threshold remain separate"""
        lines = ['#a,2', '#abc,3']
        self.assertEqual(bar_chart.get_lines(lines), {'#a': 2, '#abc': 3})

    def test_substring_inside_longer_hashtag_is_merged(self):
        """substring matching works when the shorter tag is a prefix"""
        lines = ['#python,2', '#pythonbest,3']
        self.assertEqual(bar_chart.get_lines(lines), {'#pythonbest': 5})

    def test_three_related_rows_accumulate_on_longest_hashtag(self):
        """multiple shorter variants accumulate into the longest variant"""
        lines = ['#python,2', '#pythonbest,3', '#pythonbest2026,4']
        self.assertEqual(bar_chart.get_lines(lines), {'#pythonbest2026': 9})

    def test_unrelated_hashtags_remain_separate(self):
        """hashtags without substring overlap keep independent totals"""
        lines = ['#python,2', '#spark,3', '#java,4']
        self.assertEqual(bar_chart.get_lines(lines), {
            '#python': 2,
            '#spark': 3,
            '#java': 4,
        })

    def test_blank_and_header_lines_are_ignored(self):
        """blank lines and the one-column CSV header do not add entries"""
        lines = ['', '#HASHTAG-COUNT', '#python,2', '']
        self.assertEqual(bar_chart.get_lines(lines), {'#python': 2})


if __name__ == '__main__':
    unittest.main()
