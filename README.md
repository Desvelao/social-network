# DSI publishing template for GitHub Pages

This repository uses a GitHub Actions workflow to publish the [DSI](https://github.com/Desvelao/dsi-spec) resources:

- Build feeds and publish
> Workflow file: `.github/workflows/publish-feeds.yml`

You can store other public files as images, vCard in the `gh-pages` branch and they will be published.

# Architecture

## Branches

- `main`: source code and feed sources
- `gh-pages`: published feeds and other public files

## Setup

### 0) Prerequisites

Clone or fork the repository.

#### Clone the repository

Configure the `user.name` and `user.email` if you haven't already.

```bash
git clone https://github.com/Desvelao/dsi-publish-template-github-pages.git
cd dsi-publish-template-github-pages
git checkout main
git remote set-url origin <GITHUB_REPOSITORY_GIT_URL>
git push -u origin main
```

### Fork the repository

Fork the repository in GitHub and then clone it:

From GitHub UI, click on the "Fork" button in the top right corner of the repository page. This will create a copy of the repository under your GitHub account.

Then, clone the forked repository to your local machine.

### 1) Enable GitHub Pages

In **Settings → Pages**, configure publishing from:

- Branch: `gh-pages`
> Apply when `gh-pages` branch exists after the first workflow run, or create it manually with an empty commit.
- Folder: `/ (root)`

> This will publish the `gh-pages` branch content in `https://<GITHUB_USERNAME>.github.io/<REPOSITORY_NAME>/`.

### 2) Build and publish feeds

#### 1) Configure workflow

The `.github/workflows/publish-feeds.yml` file builds and publishes the feeds. This uses under the hood the [callable workflow](https://github.com/Desvelao/dsipy/blob/main/.github/workflows/gha-build-feeds.yml), refer there for more details about the arguments and secrets.

Edit `.github/workflows/publish-feeds.yml`:

If some change is applied, commit and push the changes.

```bash
git add <FILES_CHANGED>
git commit -m "Update workflow configuration"
git push origin main
```

#### 2) Add required repository secrets

In **Settings → Secrets and variables → Actions → New repository secret**, create:

> These secrets can be defined directly in the workflow file as well, but using secrets is recommended to avoid hardcoding sensitive information in the repository. Refer to the [callable workflow](https://github.com/Desvelao/dsipy/blob/main/.github/workflows/gha-build-feeds.yml) for more details about the arguments and secrets.

- `FEEDS_TITLE`: The title of the feeds, e.g. "My DSI feeds".
- `FEEDS_DESCRIPTION`: The description of the feeds, e.g. "My DSI feeds description".
- `FEEDS_AUTHOR`: The author of the feeds, e.g. "Desvelao".
- `FEEDS_EMAIL`: The email of the author, e.g. "desvelao@example.com"
- `FEEDS_VARS`: (Optional) A key-value pair string with the variables to pass that can be used to interpolate values in the feeds metadata or content. For example:

```plaintext
my_name_from_secret=Desvelao
another_var=Another value
```

Then, they can be used in the markdown files as:

```
---
title: Hello {{ my_name_from_secret }}!
date: 2026-03-04T19:07:10Z
link: {{ gh_repo_source_base_url }}/{{ file_path }}
---
This feed has a variable from secrets: {{ another_var }}.
```

## Add feeds

The feeds are generated from markdown files in the `main` branch. To add a feed:

1. Create a markdown file with the following structure:

```markdown
---
title: My feed title
date: 2026-03-04T19:07:10Z
link: {{ gh_repo_source_base_url }}/{{ file_path }}
---
Hello to the DSI users! I am here!
```

- `id`: The unique identifier of the feed item. If not provided, it will be generated from the file path.
- `title`: The title of the feed item.
- `date`: The date of the feed item in ISO 8601 format.
- `link`: The link to the source of the feed item.
- `use_html_content`: (optional) If set to `yes` or `true`, the content of the feed item will be interpreted as HTML. Otherwise, it will be interpreted as plain text.
- `image`: (optional) The URL of an image to include in the feed item.

> NOTE: The `link` field should be defined with the template string `{{ gh_repo_source_base_url }}/{{ file_path }}` to point to the source file in the repository. The `gh_repo_source_base_url` and `file_path` variables are provided by the workflow and markdown processor respectively and will be replaced with the actual values. This works if the source directory that contains the markdown level in any nested directory is in the root of the repository, for example the `feeds` directory. In other cases, you could need to redefine the `link` to point to the markdown file.

You can define any variable in the frontmatter and use it in the content or metadata with `{{ variable_name }}`. For example:

```markdown
---
title: My feed title
date: 2026-03-04T19:07:10Z
link: {{ gh_repo_source_base_url }}/{{ file_path }}
my_var: This is a variable from frontmatter
---
The value of my_var is: {{ my_var }}.
```

The precedence of the variables is:
- file metadata
- variables defined using the `--var` argument in the workflow `command_args`
- variables defined in the callable workflow or secrets defined in `FEEDS_VARS` secret.

2. Commit and push the changes:

```bash
git add .
git commit -m "Update feed sources"
git push origin main
```

The `.github/workflows/publish-feeds.yml` workflow will publish the feeds into the GitHub pages.

The URL of the served file should be: `https://<GITHUB_USERNAME>.github.io/<REPOSITORY_NAME>/feeds.rss`.

### Tips

Manage the resource and public files in the repository with the method you prefer:
- Use the GitHub mobile app.
- Use the GitHub web interface.
- Use the `git`
