"""Flush top 10 hashtags"""
import logging

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from pyspark.sql import Row, SQLContext, SparkSession

import logging
import sys


TOP_HASHTAGS = 10

WINDOW_DURATION_IN_MIN = 30
SLIDE_DURATION = 20
NUM_PARTITIONS = 2
BATCH_DURATION = 1


# TODO isolate the business logic (reduceByKeyAndWindow) for the unit test

def main():
    if len(sys.argv) != 3:
        raise IOError("Indicate the twitter-supplier host, and the port, like: localhost 9999 ")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.getLogger("py4j").setLevel(logging.WARN)
    logging.info("Starting, give it 15 sec")
    sc = SparkContext("local[1]", "hot-hashtags")
    logging.info("Sanity, 3 sec")

    txt = sc.textFile('c:\\temp\\spark-3.3.1-hadoop2\\LICENSE')
    logging.info(txt.count())
    logging.info("Done, Starting..")

    # sc.setLogLevel("WARN")  # WARN # DEBUG

    ssc = StreamingContext(sc, BATCH_DURATION)
    # ssc.checkpoint("checkpoint")
    # ssc.remember(60)

    datastream = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    words = datastream.flatMap(lambda line: line.split(" "))
    hashtags = words.map(lambda x: (x, 1))

    tags_totals = hashtags.reduceByKey( # AndWindow(
        lambda x, y: x + y)
        # lambda x, y: x - y,
        # WINDOW_DURATION_IN_MIN * 60,
        # SLIDE_DURATION,
        # NUM_PARTITIONS,
        # lambda x: x != 0)

    # tags_totals.checkpoint(60)

    tags_totals.foreachRDD(foreachRDD)

    tags_totals.pprint(TOP_HASHTAGS)

    ssc.start()
    ssc.awaitTermination()


def foreachRDD(time, rdd):
    print("========= %s =========" % str(time))
    rdd.pprint()
    if rdd.isEmpty():
        print("empty")
    else:
        # logging.debug(time)
        # logging.warning("test")
        rows = rdd.map(lambda w: Row(hashtag=w[0], count=w[1]))
        sqlcontext = SQLContext.getOrCreate(SparkContext.getOrCreate())

        dataframe = sqlcontext.createDataFrame(rows)
        dataframe.createOrReplaceTempView("hashtags")

        hashtag_counts = sqlcontext.sql(
            "SELECT hashtag, count(*) "
            "FROM hashtags "
            "ORDER BY count "
            "DESC LIMIT " + str(
                TOP_HASHTAGS))  # TODO remove LIMIT, handle even counts (so results might be higher than 10)

        resultset = hashtag_counts.collect()
        hashtag_counts.show()
        f = open('./trends.csv', 'w')
        f.write('#HASHTAG-COUNT\n')
        for row in resultset:
            f.write(row['hashtag'].encode('utf8') + "," + str(row['count']))
            f.write('\n')
        f.close()

        # hashtag_counts.show(TOP_HASHTAGS)


if __name__ == "__main__":
    main()
