"""Integration tests for the hashtag counting Spark transformation."""

import unittest

import pytest

from spark_hot_hashtags import parse_line


pytest.importorskip('pyspark')
from pyspark import SparkConf, SparkContext


class TestSparkHotHashtagsIntegration(unittest.TestCase):
    """Runs the stream parsing and aggregation through a local Spark context."""

    @classmethod
    def setUpClass(cls):
        conf = (SparkConf()
                .setMaster('local[1]')
                .setAppName('spark-hot-hashtags-test')
                .set('spark.ui.enabled', 'false'))
        cls.spark_context = SparkContext.getOrCreate(conf)
        cls.spark_context.setLogLevel('ERROR')

    @classmethod
    def tearDownClass(cls):
        cls.spark_context.stop()

    def test_stream_words_are_aggregated_by_spark(self):
        lines = [
            '#python #spark',
            '#python #testing',
        ]

        counts = dict(
            self.spark_context.parallelize(lines)
            .flatMap(parse_line)
            .reduceByKey(lambda left, right: left + right)
            .collect()
        )

        self.assertEqual(counts, {
            '#python': 2,
            '#spark': 1,
            '#testing': 1,
        })


if __name__ == '__main__':
    unittest.main()
