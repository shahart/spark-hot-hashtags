<!-- Copilot / AI agent instructions for the spark-hot-hashtags repo -->

# Quick context

- Purpose: small demo that streams Twitter text -> Spark Streaming job that counts hashtags -> writes `trends.csv` -> `bar_chart.py` renders results. The code is synchronous/IPC-by-file/socket rather than a full service.
- Primary components:
  - `twitter_access.py` — connects to Twitter (via `tweepy`) and opens a TCP socket to stream lines (hashtags) to a client.
  - `spark_hot_hashtags.py` — legacy Spark Streaming job that reads from the TCP socket, reduces hashtags and writes `trends.csv`.
  - `bar_chart.py` — reads `trends.csv` and renders a live bar chart (uses `matplotlib` + `FuncAnimation`).
  - `tests/test_bar_chart.py` — unit tests for the pure `get_lines` logic in `bar_chart.py`.

# High-level data flow

- `twitter_access.py` -> TCP socket -> `spark_hot_hashtags.py` (via `socketTextStream`) -> `spark_hot_hashtags.foreachRDD` writes `trends.csv` -> `bar_chart.py` reads `trends.csv` and plots.
- Integration points are simple: TCP socket and the file `trends.csv`. There is no REST API or message broker.

# Developer workflows (commands)

- Install dependencies: `python -m venv .venv && source .venv/Scripts/activate` (Windows: `.venv\\Scripts\\activate`) then:

  - `pip install -r requirements.txt`

- Run a local Twitter supplier (use `my_twitter.ini` with credentials):
  - `python twitter_access.py 9999`  # opens a TCP server on localhost:9999

- Produce/consume stream with Spark driver (requires Spark install and `spark-submit` on PATH):
  - `spark_submit spark_hot_hashtags.py localhost 9999`  # point to twitter_access host and port
  - Note: README describes monitoring Spark UI at `http://localhost:4040/`.

- Render chart locally (reads `trends.csv`):
  - `python bar_chart.py`

- Run unit tests (uses `unittest`):
  - `python -m unittest discover -v`

# Project-specific conventions & patterns

- Configuration & secrets: Twitter credentials are loaded from `my_twitter.ini` (section `user1`). Do not commit secrets.
- Keyword lists: `keywords.txt` and (optional) `most_common_words_in_english.txt` are used by `twitter_access.py`. Toggle `HOT_KEYWORDS_RELOAD` in `twitter_access.py` to enable periodic reload behavior.
- Minimal pure logic for testing: the codebase keeps testable, pure functions in `bar_chart.py` (`get_lines`, `handle_substring_hashtag`) — tests in `tests/test_bar_chart.py` assert substring-union behavior.
- Merge behavior: `bar_chart.get_lines` implements a substring-union strategy controlled by `MINIMUM_START_OVERLAP` (default 3). Tests depend on this exact behavior — treat it as authoritative.

# Integration notes and caveats

- Spark dependency: `spark_hot_hashtags.py` expects a Spark runtime (legacy DStream API). Running with `python` alone won't exercise streaming behavior — use `spark-submit` or run unit-level extractions of logic.
- File-based coupling: `trends.csv` is the de-facto contract between Spark job and charting; path is relative to the process working dir. If you change working dirs, update file locations accordingly.
- Network coupling: `twitter_access.py` binds to `localhost` by default; it expects a single client connection (`accept()`). The README shows use of `ncat` / `netcat` for simulating producers.

# Where to look for examples

- `tests/test_bar_chart.py` — canonical examples of expected `get_lines` behavior.
- `twitter_access.py` — shows keyword loading, `tweepy.Stream` subclass, socket accept/send loop, and `HOT_KEYWORDS_RELOAD` behavior.
- `spark_hot_hashtags.py` — shows Spark Streaming wiring and the `foreachRDD` path that writes `trends.csv`.

# Guidance for an AI coding agent

- Prefer changing or adding pure functions (easier to unit test) rather than modifying streaming wiring.
- When modifying hashtag aggregation logic, update `tests/test_bar_chart.py` or add new tests showing exact string-union semantics.
- Do not add or expose credentials in commits; if adding CI or examples, use placeholders and document expected `my_twitter.ini` fields.
- If you need to run Spark-based end-to-end tests, document the required local Spark install and `SPARK_HOME` or use a containerized test environment.

# Quick checklist for changes

- Update `requirements.txt` when adding Python deps.
- If changing the shape or format of `trends.csv`, update `bar_chart.get_lines` and the tests accordingly.
- If enabling keyword reload behavior, verify thread-safety around `keywords` and `lock` in `twitter_access.py`.

---

If you'd like, I can: (a) run the unit tests locally, (b) add a small `CONTRIBUTING.md` snippet describing how to run Spark locally, or (c) expand examples for mocking `tweepy` in tests. Which would you prefer?
