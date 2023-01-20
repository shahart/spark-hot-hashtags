# spark-hot-hashtags
(streaming hello world)

[Spark-Programming-Guide](http://spark.apache.org/docs/latest/streaming-programming-guide.html)

note: streaming is legacy, migrate to Structured Streaming.
That's an old snapshot, ~ 4 years.

## how to run


* Update my_twitter.ini


* On some machine run `python3 twitter_access.py 9999` 

  ```
   INFO Waiting for a client... either via ncat `127.0.0.1 9999` or `spark_submit spark_hot_hashtags.py localhost 9999`
  ```
  

* `spark_submit spark_hot_hashtags.py localhost 9999` - replace localhost with the twitter-access's machine from above

  ```
     INFO Found... starting... ('127.0.0.1', 58093)
     INFO load hot keywords every second: False
     INFO keywords: ['spacex', 'spark', 'job', 'worldwar2', 'trump', 'hapis']
     INFO Stream connected
     INFO found a hashtag '#3' on a tweet 'RT @claireLTdoodle: DOODLEBLOG #3 ON KO-FI! Featuring shipping updates, Real Life job
  ```

  Monitor via http://localhost:4040/


* On the spark-driver run `python bar_chart.py`

  ```
   INFO OrderedDict([('b', 400), ('a', 300)])
  ```

this renders the chart given something like

  ```
  #bla
  a,300
  b,400
  ```

If no updates, you'll see: `ERROR Some data flow error, check logs of spark, and then twitter_access`


## configurations


* Configure your keywords.txt


* **Optional**, depends if hot keywords.txt change is enabled: Take at least top 20 values from [most_common_words_in_english](https://en.wikipedia.org/wiki/Most_common_words_in_English) into most_common_words_in_english.txt


* **Optional**, you can simulate Twitter access via `netcat 127.0.0.1 9999`
  (on Windows, it's under c:\Program Files (x86)\Nmap\ncat)
