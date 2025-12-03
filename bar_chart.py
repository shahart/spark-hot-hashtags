"""Renders trends csv"""

# TODO render via web app, and not via direct connect to Spark's driver machine

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ipywidgets as widgets
import logging
import collections
import os
import time

UPDATE_INTERVAL_IN_SEC = 5
MINIMUM_START_OVERLAP = 3

figure, ax = plt.subplots()
prev_ordered = ''

def show():
    plt.show()
    

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    ani = animation.FuncAnimation(figure, animate_func, interval=UPDATE_INTERVAL_IN_SEC * 1000)
    show()
    # year_range_slider = widgets.IntRangeSlider(
    #     value=[1, 2],
    #     min=1,
    #     max=2,
    #     step=0.1,
    #     description='x:',
    #     continues_update=False
    # )
    # widgets.interact(show)    


def animate_func(i):
    try:
        if int(time.time()) - os.path.getmtime('trends.csv') > 2 * 60:
            logging.error("Some data flow error, check logs of spark, and then twitter_access")

        f = open('trends.csv', 'r')
        graph_data = f.read()
        # trends is a tiny csv, read all of it is safe
        f.close()

        lines = graph_data.split('\n')
        dictionary = get_lines(lines)

        if len(dictionary) <= 1:
            logging.error("Some data flow error, check logs of twitter_access")

        ordered = collections.OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

        global prev_ordered
        if prev_ordered != str(ordered):
            logging.info(ordered)
            prev_ordered = str(ordered)

        ind = range(len(ordered))
        ax.clear()
        plt.bar(ind, ordered.values())
        plt.xticks(ind, ordered.keys())

    except Exception as e:
        logging.error(e)


def get_lines(lines):
    dictionary = {}
    for line in lines:
        splits = line.split(',')
        if len(splits) >= 2:

            # if len(splits) >= 3:
            #     logging.warn('invalid line %s' % (line))  # possible if hashtag contains a comma >> TODO escaping

            hashtag = splits[0]
            count = int(splits[-1])
            if count > 0:
                s = hashtag  # TODO support non-ascii, unicode(hashtag, 'utf8')

                # Union based on s.find, like #hiring and #hiring!
                # TODO smarter inclusion (NLP like), like hires and hiring

                found = False

                if len(s) >= MINIMUM_START_OVERLAP:
                    dictionary, found = handle_substring_hashtag(count, dictionary, s)

                if not found:
                    dictionary[s] = count

    return dictionary


def handle_substring_hashtag(count, dictionary, s):
    found = False

    for hashtag in dictionary.keys():
        if len(hashtag) >= MINIMUM_START_OVERLAP and hashtag.find(s) > -1:
            logging.debug('union %s into %s' % (s, hashtag))
            dictionary[hashtag] = dictionary.get(hashtag) + count
            found = True
            break

    if not found:
        for hashtag in dictionary.keys():
            if len(hashtag) >= MINIMUM_START_OVERLAP and s.find(hashtag) > -1:
                logging.debug('union %s into %s' % (hashtag, s))
                dictionary[s] = dictionary.get(hashtag) + count
                dictionary = dict(dictionary)
                del dictionary[hashtag]
                found = True
                break

    return dictionary, found


if __name__ == "__main__":
    main()
