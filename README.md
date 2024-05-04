# Social network

This repository provides the utilities to expose the decentralized social profile based on vCard (profile) and user feeds (RSS or ATOM).

Based on https://nfraprado.net/post/vcard-rss-as-an-alternative-to-social-media.html

The user info is provided by a vCard. This file contains data about the person and a source link of the user feeds on the `X-FEED` parameter according to the proposition (see https://nfraprado.net/post/vcard-rss-as-an-alternative-to-social-media.html). You can add social media accounts/links using the `X-<NAME>` parameter. You can see my vCard on [./docs/vcard.vcf)](./docs/vcard.vcf).

The user feed is provided by a RSS or ATOM feeds and exposed publicaly, so the other users can subscribe with RSS/Atom feed readers to the feeds to receive the latest posts. [Read about how to public these files](#public_the_files).

The vCard data can be shared using QR or links to your social media profile. See [./qr/README.md](./qr/README.md) for more information.

# Join to the network

1. Create a vCard with your info
2. Copy the feeds_template.csv to feeds.csv
```
cp feeds/feeds_template.csv feeds.csv
```
3. Build the feeds and QRs
```
bash build.sh
```
4. Publish the vCard and feed files. Optionally you could want to publish the QR or copy to your mobile to share with others.

## Add a new post to the feed

1. Add a new row to the `feeds.csv` file
2. Build the feed file
3. Publish the feed file

# Public the files

The vCard and RSS or Atom feeds needs to be exposed publicaly so they can be consumed by others users.

You can expose these files in a personal server exposed to internet or using some free hosting services as GitHub pages. The files should be served with the appropiate `Content-Type` headers so the feed readers can work correctly.

## GitHub pages

1. Store the vCard and feed files in the `docs` directory.
2. Configure the repository to serve the `docs` directory of the `main` branch into GitHub pages.

# My profile

- vCard: https://desvelao.github.io/social-network/vcard.vcf
- Feed: https://desvelao.github.io/social-network/feeds.rss <a href="http://validator.w3.org/feed/check.cgi?url=https%3A//desvelao.github.io/social-network/feeds.rss"><img src="./feeds/valid-rss-rogers.png" alt="[Valid RSS]" title="Validate my RSS feed" /></a>
