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


if __name__ == '__main__':
    unittest.main()
