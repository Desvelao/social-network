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

Go to the GitHub web and creates a new repository.

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

From GitHub UI, click on the "Fork" button in the top right corner of the repository page. This will create a copy of the repository under your GitHub account. Rename the repository if you want.

Then, clone the forked repository to your local machine.

### 1) Build and publish feeds

#### 1) Configure workflow

The `.github/workflows/publish-feeds.yml` file builds and publishes the feeds. This uses under the hood the [callable workflow](https://github.com/Desvelao/dsi-cli/blob/v0.1.0-alpha1/.github/workflows/gha-build-feeds.yml), refer there for more details about the arguments and secrets.

Edit `.github/workflows/publish-feeds.yml`:

- `source_dir` and `feeds_file`: the folder with the markdown sources and the name of the generated feed.
- `feeds_limit`: (Optional) keep only the N newest items in the feed. All the items are published when it is omitted. Do not set it to `0`: that generates an empty feed.
- `command_args`: (Optional) extra arguments passed to `dsi feeds build`, e.g. `--language es-ES`.
- `artifact_name`: (Optional) name of the intermediate artifact with the generated feed. The publish job follows it automatically.
- `dsi_tag`: (Optional) release tag of dsi-cli to install the `dsi` binary from. The template pins it to `v0.1.0-alpha1`; keep it in sync with the `uses:` ref of the callable workflow when upgrading. The latest stable release is used when it is omitted (pre-releases need an explicit tag).
- `dsi_repo_token` (secret): (Optional) token with read access to the dsi-cli releases, only needed for private release repositories.

The title, description, author, email, feed link and variables are passed as secrets (see the next step); the callable workflow also accepts the title, description, author, email, `feed_link` and `feeds_vars` as plain `with:` inputs, but secrets take precedence.

If some change is applied, commit and push the changes.

```bash
git add <FILES_CHANGED>
git commit -m "Update workflow configuration"
git push origin main
```

#### 2) Add required repository secrets

In **Settings → Secrets and variables → Actions → New repository secret**, create:

> These values can be defined directly in the workflow file as well, but using secrets is recommended to avoid hardcoding sensitive information in the repository. Refer to the [callable workflow](https://github.com/Desvelao/dsi-cli/blob/v0.1.0-alpha1/.github/workflows/gha-build-feeds.yml) for more details about the arguments and secrets.

- `FEEDS_TITLE`: The title of the feeds, e.g. "My DSI feeds".
- `FEEDS_DESCRIPTION`: The description of the feeds, e.g. "My DSI feeds description".
- `FEEDS_AUTHOR`: The author of the feeds, e.g. "Desvelao".
- `FEEDS_EMAIL`: The email of the author, e.g. "desvelao@example.com"
- `FEEDS_VARS`: (Optional) A key-value pair string with the variables to pass that can be used to interpolate values in the feeds metadata or content. For example:

```plaintext
my_name_from_secret=Desvelao
another_var=Another value
```

- `FEEDS_LINK`: (Optional) The public URL of the feed file. By default it is built as `https://<GITHUB_USERNAME>.github.io/<REPOSITORY_NAME>/feeds.rss`, so set it when you use a custom domain.
- `FEEDS_SIGN_PRIVATE_KEY` and `FEEDS_SIGN_PUBLIC_KEY`: (Optional, set both) The Ed25519 keypair in PEM format used to sign each feed item. Create it with `dsi key create` and publish the public key in your vCard (`KEY` property). Never commit the private key.

Then, they can be used in the markdown files as:

```
---
title: Hello {{ my_name_from_secret }}!
date: 2026-03-04T19:07:10Z
link: {{ gh_repo_source_base_url }}/{{ file_path }}
---
This feed has a variable from secrets: {{ another_var }}.
```

### 2) Add the first feed

Create a feed file in `feeds` directory in the `main` branch.

Then commit and push the change:

```bash
git add .
git commit -m "feat(feeds): add the first state"
git push origin main
```

This should trigger the GitHub action the builds the feeds file and commit into the `gh-pages`.

### 3) Enable GitHub Pages

In **Settings → Pages**, configure publishing from:

- Branch: `gh-pages`
> Apply when `gh-pages` branch exists after the first workflow run, or create it manually with an empty commit.
- Folder: `/ (root)`

> This will publish the `gh-pages` branch content in `https://<GITHUB_USERNAME>.github.io/<REPOSITORY_NAME>/`.

### 4) (Optional) Use a custom domain

A custom domain makes a better stable address for your identity than the `github.io` one. Configure the DNS records as described in the [GitHub documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site), then:

1. In **Settings → Secrets and variables → Actions → Variables**, create the variable `PAGES_CNAME` with your domain, e.g. `alice.example`. The workflow writes the `CNAME` file in `gh-pages` on every run, so it is not lost between deployments.
2. Create the secret `FEEDS_LINK` with the public URL of the feed, e.g. `https://alice.example/feeds.rss`.
3. In **Settings → Pages**, set the custom domain and enable **Enforce HTTPS**.

## What is published automatically

Only the feed file (`feeds.rss`) is built and published by the workflow. Everything else (vCard, images, other public files) is committed by you directly to the `gh-pages` branch, see [Publish other files](#publish-other-files). The workflow keeps those files (`keep_files: true`), so they are not removed when the feed is updated, and it does not validate them: run `dsi vcard validate <FILE>` before pushing a vCard.

The workflow publishes by pushing to the `gh-pages` branch, it does not use the GitHub Pages artifact deployment.

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


### Publish other files

If the repository was configured to publish the files in the `gh-pages` repository, add the files you want to publish to that branch:

```bash
git checkout gh-pages
```

Create the files, commit and push

```
git add .
git commit -m "feat: add public files"
git push origin gh-pages
```

If the GitHub pages is enabled for this branch, this should run a GitHub action that publishes the files. The files are exposed in:

```
https://<USERNAME>.github.io/<REPOSITORY_NAME>/<PATH_TO_FILE>
```

### Tips

Manage the resource and public files in the repository with the method you prefer:
- Use the GitHub mobile app.
- Use the GitHub web interface.
- Use the `git`
