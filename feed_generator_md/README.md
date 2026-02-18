# Markdown to RSS Feed Generator

This tool generates an RSS feed from a directory of Markdown files. It extracts metadata from the Markdown files and creates an RSS feed based on the provided options.

## Features
- Parses Markdown files with metadata.
- Generates an RSS feed with customizable options.
- Supports limiting the number of posts in the feed.
- Allows specifying author information, feed title, and description.

## Installation

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd feeds_generator_md
   ```
2. Install the required dependencies:
  ```bash
    pip install -r requirements.txt
  ```
3. Create Markdown files in a directory

## Usage

### Configuration

A configuration file can be used `config.conf` located in the same path than the `script.py` file with the following properties:

```text
directory=feeds
author=My Name
email=me@email.com
```

where:

- `directory`: where the feeds files are located
- `author`: author name used to generate the feed file
- `email`: author email used to generate the feed file

### Create new feed file

```bash
python script.py new
```

Then it prompts for some inputs and finanlly generates the file in the directory location.

### Build feeds


```bash
python script.py build <directory> [OPTIONS]
```

Arguments:
directory: Directory containing Markdown files.
Options
`--directory`: Directory where the feed files in Markdown are located.
`--output`: Name of the output RSS file (default: feed.xml).
`--limit`: Limit the number of posts in the feed.
`--title`: Title of the RSS feed (default: My Feed).
`--link`: Base link for items in the feed (default: https://example.com).
`--description`: Description of the RSS feed (default: RSS feed generated from markdown files).
`--language`: Language of the feed (default: en-US).
`--author`: Author information (prompted if not provided).
`--email`: Email of the author (prompted if not provided).

Example:

```bash
python script.py build --directory feeds --output my_feed.xml --limit 10 --title "My Blog" --link "https://myblog.com" --description "Latest posts from my blog" --author alice --email alice@example.com
```

## Development

Setting Up the Development Environment

1. Create a virtual environment:

```console
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
```

2. Install the dependencies:

```console
pip install -r requirements.txt
```

3. Run the tool in development mode:

```
python script.py build --directory posts
```

### Code Structure
- `script.py`: Main entry point for the tool.
- `requirements.txt`: Lists the dependencies.

### Testing
To test the tool, you can create a directory with sample Markdown files containing metadata and run the build command.

# Markdown File Format
Each Markdown file should include metadata in the following format:
```markdown
---
title: My Post
date: 2023-10-01T12:00:00Z
link: https://example.com/my-post
---
Content of the post goes here.
```

> `date` supports the formats: `YYYY-MM-DDTHH:mm:ssZ` (ISO 8601 UTC) or `YYYY-MM-DD` (date only).

# License

This project is licensed under the MIT License. See the `LICENSE` file for details.

# Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
