# Repository Guidelines

## Project Structure & Module Organization
This repository is a small script-based Python project for streaming hashtags into Spark and visualizing the results. Main entrypoints live at the repo root:

- `twitter_access.py`: connects to Twitter and sends hashtags over a socket.
- `spark_hot_hashtags.py`: Spark Streaming consumer that aggregates hashtags and writes `trends.csv`.
- `bar_chart.py`: reads `trends.csv` and renders a live chart.
- `tests/test_bar_chart.py`: unit tests for CSV parsing and hashtag merging logic.

Runtime data and local configuration also live at the root: `keywords.txt`, `most_common_words_in_english.txt`, `my_twitter.ini`, and generated outputs such as `trends.csv`.

## Build, Test, and Development Commands
- `python -m pip install -r requirements.txt`: install project dependencies.
- `python -m pip install flake8 pytest`: install the same lint/test tools used by CI.
- `python twitter_access.py 9999`: start the Twitter socket publisher after updating `my_twitter.ini`.
- `spark_submit spark_hot_hashtags.py localhost 9999`: run the Spark consumer locally.
- `python bar_chart.py`: render the current `trends.csv` output as a bar chart.
- `python -m pytest`: run the test suite. CI uses `pytest` directly in `.github/workflows/python-app.yml`.

## Coding Style & Naming Conventions
Follow existing Python style: 4-space indentation, module-level constants in `UPPER_SNAKE_CASE`, functions and variables in `snake_case`, and short module docstrings. Keep scripts executable from the repo root and prefer small, single-purpose functions so logic can move into tests. Run `flake8` before opening a PR; no custom formatter config is checked in.

## Testing Guidelines
Tests are in `tests/` and currently use `unittest`, executed through `pytest`. Name files `test_*.py` and test methods `test_*`. Focus new tests on pure logic such as parsing, aggregation, and substring-merging behavior; avoid networked Twitter or Spark integration tests unless they can run deterministically in CI.

## Commit & Pull Request Guidelines
Recent commits use short, imperative subjects such as `pytest via github actions` and `Create test_bar_chart.py`. Keep commit titles concise and action-oriented. PRs should include a brief summary, note any config or sample-data changes, link related issues when applicable, and attach a screenshot if chart output changes.

## Configuration & Security
Do not commit real Twitter credentials. Treat `my_twitter.ini` as local-only developer config and sanitize any sample values before sharing logs or screenshots.
