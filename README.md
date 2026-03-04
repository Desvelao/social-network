# DSI publishing template for GitHub Pages

This repository uses a GitHub Actions workflow to publish the [DSI](https://github.com/Desvelao/dsi-spec) resources:

- Build feeds and publish
> Workflow file: `.github/workflows/publish-feeds.yml`

You can store other public files as images, vCard in the `gh-pages` branch and they will be published.

## Setup

### 1) Enable GitHub Pages

In **Settings → Pages**, configure publishing from:

- Branch: `gh-pages`
- Folder: `/ (root)`

### 2) Build and publish feeds

#### 1) Configure workflow environment values

Edit `.github/workflows/publish-feeds.yml`:

- `PYTHON_VERSION`: Python runtime (default `3.12`)
- `WHEEL_REPO`: source repository in `OWNER/REPO` format
- `WHEEL_TAG`: release tag to download (set empty string to use latest release)
- `WHEEL_ASSET`: wheel filename pattern (default `*.whl`)
- `FEEDS_FILE`: output filename (default `feeds.rss`)

Example:

```yaml
env:
  PYTHON_VERSION: "3.12"
  WHEEL_REPO: "my-org/my-dsipy-repo"
  WHEEL_TAG: "v1.2.3"
  WHEEL_ASSET: "dsipy-*.whl"
  FEEDS_FILE: "feeds.rss"
```

#### 2) Add required repository secrets

In **Settings → Secrets and variables → Actions → New repository secret**, create:

- `FEEDS_TITLE`
- `FEEDS_DESCRIPTION`
- `FEEDS_AUTHOR`
- `FEEDS_EMAIL`

These are passed to:

```bash
dsipy feeds build feeds \
  --title "$FEEDS_TITLE" \
  --description "$FEEDS_DESCRIPTION" \
  --author "$FEEDS_AUTHOR" \
  --email "$FEEDS_EMAIL"
```

## Add feeds

1. Checkout to the `feeds` branch:

```bash
git checkout feeds
```

2. Create a markdown file with the structure:

```markdown
---
title: My state title
date: 2026-03-04T19:07:10Z
---
Hello to the DSI users! I am here!
```

3. Commit and push the changes:

```bash
git add .
git commit -m "Update feed sources"
git push origin feeds
```

The `.github/workflows/publish-feeds.yml` workflow will publish the feeds into the GitHub pages.

The URL of the served file should be: `https://<GITHUB_USERNAME>.github.io/<REPOSITORY_NAME>/feeds.rss`.
