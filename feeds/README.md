# Feed utilities

- generate_feed: generate a RSS feed from a csv file.

# generate_feed

RSS specification: https://www.rssboard.org/rss-specification

## Install the dependencies

```
pip install -r requirements.txt
```

Tested with Python v3.10.12.

## Create a csv file

Create a csv file with the following columns:
- date: date on format YYYY-MM-DDTHH:mm:ssZ+zzzz. Example: 2024-05-01T19:23:10Z+0000.
- id: unique identifier.
- link: URL link.
- title: feed title. optional.
- message: feed message.

See `feeds_template.csv` file.

## Usage

Run the script:
```
python generate_feed <FEED_CSV> --author-email <FEED_AUTHOR_EMAIL> --author-name <FEED_AUTHOR_NAME> --title <FEED_TITLE> --link <FEED_LINK> --description <FEED_DESCRIPTION> > <FEED_RSS_OUTPUT>
```
where:
- `<FEED_AUTHOR_EMAIL>`: author email of the feeds.
- `<FEED_AUTHOR_NAME>`: author name of the feeds.
- `<FEED_CSV>`: csv file with the feeds.
- `<FEED_TITLE>`: feed channel title.
- `<FEED_LINK>`: feed channel link.
- `<FEED_DESCRIPTION>`: feed channel description.
- `<FEED_RSS_OUTPUT>`: output file. e.g. feeds.rss

By default, the generated RSS feed uses all the entries sorted by the `date` column. You can use the `--recent-feeds` option to only include the recent feeds by count. For example:

```
python generate_feed --recent-feeds 15 <rest of options>
```

See the available options:
```
python generate_feed --help
```

Example:
```
python generate_feed feeds.csv --author-email "author@example.com" --author-name "Author Name" --title "Author Name's feeds" --link "https://author_name.github.io/social-network/feeds.rss" --description "Recently updated feeds from Author Name" > feeds.rss
```

## Usage with Docker

- RSS
```
docker run --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../feeds.csv:/tmp/feeds.csv" -w "/home/python/app" python:3.10.12-alpine3.18 sh -c 'pip install -r requirements.txt --quiet && python generate_feed /tmp/feeds.csv --author-email "author@example.com" --author-name "Author Name" --title "Author Name's feeds" --link "https://author_name.github.io/social-network/feeds.rss" --description "Recently updated feeds from Author Name" --output-feed rss' > ../feeds.rss
```

ATOM
```
docker run --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../feeds.csv:/tmp/feeds.csv" -w "/home/python/app" python:3.10.12-alpine3.18 sh -c 'pip install -r requirements.txt --quiet && python generate_feed /tmp/feeds.csv --author-email "author@example.com" --author-name "Author Name" --title "Author Name's feeds" --link "https://author_name.github.io/social-network/atom.xml" --description '"Recently updated feeds from Author Name" --output-feed atom' > ../atom.xml
```

## Develop with Docker

```
docker run -itd --name generate_feed --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../feeds.csv:/tmp/feeds.csv" -w "/home/python/app" python:3.10.12-alpine3.18
```

## Validate the feeds

- RSS: https://validator.w3.org/feed/
