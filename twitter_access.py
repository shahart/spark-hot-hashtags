"""Flush Twitter filter by user's keywords"""

import tweepy
import socket
import sys
import logging
import threading
import configparser

HOT_KEYWORDS_RELOAD = False

config = configparser.ConfigParser()
config.read("my_twitter.ini")
consumer_key = config.get("user1", "CONSUMER_KEY")
consumer_secret = config.get("user1", "CONSUMER_SECRET")
access_token = config.get("user1", "ACCESS_TOKEN")
access_token_secret = config.get("user1", "ACCESS_TOKEN_SECRET")

conn = None
keywords = []
lock = threading.Lock()


# TODO log stats every minute/5 to see program is alive (not only via spark's console)

def load_keywords(file):
    keywords = []
    f = open(file, 'r')
    text = f.read().split('\n')
    f.close()

    for line in text:
        if len(line) >= 1:
            keywords.append(line.lower())

    return keywords


def get_all_words(text):
    words = []
    for line in text.split('\n'):
        for word in line.split(' '):
            if len(word) >= 1:
                # TODO trim last comma, period,
                words.append(word.lower())

    return words


def on_error(status):
    # TODO resolve Connection broken: IncompleteRead
    logging.error('on_error with status %s' % (status))


class TweeterStreamListener(tweepy.Stream):
    """
    persist only the hashtags
    """

    def on_status(self, status):

        passed = not HOT_KEYWORDS_RELOAD
        text = status.text
        all_words = get_all_words(text)

        if HOT_KEYWORDS_RELOAD:

            for word in all_words:
                if word in keywords:
                    logging.info("found a keyword '%s' on a tweet '%s'" % (word, text))
                    passed = True
                    break

        if passed:

            for word in all_words:
                if word.startswith('#'):
                    logging.info("found a hashtag '%s' on a tweet '%s'" % (word, text))
                    conn.send((word + '\n').encode('utf-8'))

        return True


def periodically_load_keywords():
    threading.Timer(1.0, periodically_load_keywords).start()
    global keywords
    lock.acquire()
    try:
        curr_keywords = load_keywords('keywords.txt')
        if curr_keywords != keywords:
            logging.info("keywords: %s" % curr_keywords)
            keywords = curr_keywords
    finally:
        lock.release()


def main():
    if len(sys.argv) != 2:
        raise IOError("Indicate the port, like 9999")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    mysocket = socket.socket()
    mysocket.bind(("localhost", int(sys.argv[1])))
    mysocket.listen(1)
    logging.info("Waiting for a client... either via ncat `127.0.0.1 %s` or `spark_submit spark_hot_hashtags.py %s`" % (sys.argv[1], sys.argv[1]))
    global conn
    conn, addr = mysocket.accept()
    logging.info("Found... starting... %s" % (str(addr)))

    logging.info('load hot keywords every second: %s' % HOT_KEYWORDS_RELOAD)
    global keywords
    keywords = load_keywords('keywords.txt')
    logging.info("keywords: %s" % keywords)
    if HOT_KEYWORDS_RELOAD:
        periodically_load_keywords()
        keywords = load_keywords('most_common_words_in_english.txt')

    twitter_stream = TweeterStreamListener(consumer_key, consumer_secret, access_token, access_token_secret)
    twitter_stream.filter(track=keywords, stall_warnings=True)

    # TODO locations via Google Maps; languages


if __name__ == "__main__":
    main()
