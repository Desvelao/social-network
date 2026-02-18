import os
import argparse
import datetime
import markdown
import xml.etree.ElementTree as ET
from email.utils import format_datetime
from rfeed import Feed, Item, Extension, Guid, Serializable
import re
import unicodedata
import os
import typer
from functools import wraps

DEFAULT_CONFIG_FILE = "config.conf"

class CustomTyper(typer.Typer):
    def __init__(self, *args, config_file="config.json", **kwargs):
        super().__init__(*args, **kwargs)
        self.config = {}
        self.config_file = config_file  # Accept the default config file as a parameter

    def __call__(self, *args, **kwargs):
        # Load the configuration file before running any command
        self.load_config()
        super().__call__(*args, **kwargs)

    def load_config(self):
        """Load the configuration file and parse settings."""
        config_path = self.config_file
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                for line in f:
                    # Skip empty lines and comments
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Parse the setting in the format `setting_name: value`
                    if "=" in line:
                        key, value = line.split("=", 1)
                        self.config[key.strip()] = value.strip()
            typer.secho(f"✅ Loaded configuration from {config_path}", fg=typer.colors.GREEN)
        else:
            typer.secho(f"⚠️  Configuration file not found: {config_path}", fg=typer.colors.YELLOW)

app = CustomTyper(config_file=os.path.join(os.path.dirname(__file__), DEFAULT_CONFIG_FILE), help="A CLI tool to generate RSS feeds from markdown files")

def parse_markdown_file(path):
    """
    Extract metadata and content from a markdown file.
    Supports simple YAML-like front matter:
    ---
    title: My Post
    date: 2025-01-01
    link: https://example.com/my-post
    ---
    """
    content_lines = []

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    frontmatter = {}
    # Detect front matter
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            line = lines[i].strip()

            fields = ["title", "date"]

            for field in fields:
                prefix = f"{field}:"
                if line.startswith(prefix):
                    frontmatter[field] = line.replace(prefix, "").strip()
            i += 1
        content_lines = lines[i+1:]
    else:
        content_lines = lines

    # Fallback title
    if not frontmatter.get("title"):
        frontmatter["title"] = os.path.splitext(os.path.basename(path))[0]

    # Fallback date (file modified time)
    if not frontmatter.get("date"):
        ts = os.path.getmtime(path)
        frontmatter["date"] = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

    html_content = markdown.markdown("".join(content_lines))

    return {
        "title": frontmatter["title"],
        "date": datetime.datetime.strptime(frontmatter["date"], "%Y-%m-%dT%H:%M:%SZ") if "T" in frontmatter["date"] else datetime.datetime.strptime(frontmatter["date"], "%Y-%m-%d"),
        "content": html_content,
        "path": path
    }

def slugify(text):
    # Normalize accents (á → a, ñ → n, ü → u)
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    ascii_text = ascii_text.lower()

    # Replace any non‑alphanumeric group with a single hyphen
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)

    # Remove leading/trailing hyphens
    ascii_text = ascii_text.strip("-")

    return ascii_text

def generate_rss(title, link, description, author, language, build_date, items):
    class AtomLinkNamespace(Extension):
        def get_namespace(self):
            return {"xmlns:atom": "http://www.w3.org/2005/Atom"}

    class AtomLink(Serializable):
        def __init__(self, href):
            Serializable.__init__(self)
            self.href = href

        def publish(self, handler):
            Serializable.publish(self, handler)
            self._write_element("atom:link", None, {"href": self.href, "rel": "self"})

    feed_items = []
    for item in items:
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        id = item.get("id") or slugify(item['path'])
        feed_items.append(
            Item(
                title = item.get("title"),
                link = item.get("link") or f"{link}/feed/{id}",
                description = item.get("content"),
                author = f"{author['name']} ({author['email']})",
                guid = Guid(id),
                pubDate = item["date"],
            )
        )
    feed = Feed(
        title = title,
        link = link,
        description = description,
        language = language,
        lastBuildDate = build_date,
        items = feed_items,
        extensions = [AtomLinkNamespace(),AtomLink(link)])
 
    return feed.rss()


def create_post(destination: str, content: str):
    if os.path.exists(destination):
        typer.secho(f"❌ A feed '{destination}' already exists.", fg=typer.colors.RED)
        raise typer.Exit()
    with open(destination, "w", encoding="utf-8") as f:
        f.write(content)
    typer.secho(f"✅ New post created: {destination}", fg=typer.colors.GREEN)


def inject_settings(*settings):
    """
    A decorator to inject specific settings from the configuration file into the command.
    If a setting is not provided via the command arguments, it will be loaded from the configuration file.
    """
    def decorator(func):
        @wraps(func)  # Preserve the original function metadata
        def wrapper(*args, **kwargs):
            # Inject each requested setting
            for setting in settings:
                if setting not in kwargs or kwargs[setting] is None:
                    value = app.config.get(setting)
                    if value is None:
                        continue
                        # typer.secho(
                        #     f"❌ The '{setting}' parameter is not defined and cannot be loaded from the configuration file.",
                        #     fg=typer.colors.RED,
                        # )
                        # raise typer.Exit()
                    kwargs[setting] = value
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
@app.command()
@inject_settings("directory")
def new(
    directory: str = typer.Option(None, help="Directory to create the feed folder"),
    title: str = typer.Option("", help="Title for the new feed"),
    message: str = typer.Option("This is the post content.", help="Content for the new feed item"),
    filename: str = typer.Option(None, help="Filename for the new feed (only the name, without extension)"),
):   
    # while not filename:
    #     filename = typer.prompt("Provide the filename for the new feed (only the name, without extension)")

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    filename = typer.prompt("Provide the filename for the new feed (only the name, without extension)", default=filename or slugify(now), show_default=True)
    feed_path = os.path.join(directory, f"{filename}.md")

    if os.path.exists(feed_path):
        typer.secho(f"❌ A feed directory with the name '{filename}' already exists. Please choose a different name.", fg=typer.colors.RED)
        raise typer.Exit()

    title = typer.prompt("Provide the title for the new feed", default=title, show_default=True)
    message = typer.prompt("Provide the message for the new feed", default=message, show_default=True)

    attributes = {
        "title": title if title else None,
        "date": now
    }

    # Only include attributes that have a value (non-empty)
    front_matter = "\n".join(f"{key}: {value}" for key, value in attributes.items() if value)

    file_content = f"""---
{front_matter}
---
{message}
"""
    # TODO: add validation to ensure the title or message is not empty

    create_post(feed_path, file_content)

    typer.secho(f"Edit the file with a text editor: {feed_path}", fg=typer.colors.GREEN)

@app.command()
@inject_settings("directory", "author", "email", "title", "link", "description", "language", "limit", "output")
def build(
    directory: str = typer.Option(None, help="Directory where the feed files are located"),
    output: str = typer.Option("feed.xml", help="Output RSS file"),
    limit: int | None = typer.Option(None, help="Limit number of posts"),
    title: str = typer.Option("My Feed", help="RSS feed title"),
    link: str = typer.Option("https://example.com", help="Base link for items"),
    description: str = typer.Option("RSS feed generated from markdown files", help="RSS feed description"),
    language: str = typer.Option("en-US", help="Language of the feed"),
    author: str = typer.Option(None, help="Author information"),
    email: str = typer.Option(None, help="Email of the author")
):

    md_files = [
        os.path.join(root, f)
        for root, _, files in os.walk(directory)
        for f in files
        if f.endswith(".md")
    ]

    posts = [parse_markdown_file(f) for f in md_files]
    posts.sort(key=lambda x: x["date"], reverse=True)

    if limit:
        posts = posts[:limit]

    author_data = {"name": author, "email": email}
    build_date = datetime.datetime.now()

    rss_xml = generate_rss(title, link, description, author_data, language, build_date, posts)

    with open(output, "w") as f:
        f.write(rss_xml)

    typer.secho(f"✅ RSS feed generated: {output}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()
