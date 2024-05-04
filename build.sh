#!/bin/env bash
# This script generates
# - RSS feed from csv feeds.csv
# - QR for vCard

author_name="Antonio Gutiérrez"
email="iamdesvelao@gmail.com"
vcard="$(pwd)/docs/vcard.vcf"
image_profile="$(pwd)/docs/profile.jpg"
docs_output="$(pwd)/docs"

# Feeds

feeds_dir="$(pwd)/feeds"
echo "Generating feeds" \
&& docker run --rm -v "$feeds_dir:/home/python/app" \
    -v "$feeds_dir/../feeds.csv:/tmp/feeds.csv" \
    -w "/home/python/app" python:3.10.12-alpine3.18 \
    sh -c "pip install -r requirements.txt --quiet && python generate_feed /tmp/feeds.csv --author-email '$email' --author-name '$author_name' --title '$author_name feeds' --link 'https://desvelao.github.io/social-network/feeds.rss' --description 'Recently updated feeds from $author_name' --output-feed rss" > docs/feeds.rss \
&& echo "Generated feeds"

# QR: vCard
qr_dir="$(pwd)/qr"
image_profile_container="/tmp/profile.jpg"
qr_output_container="qr.png"
echo "Generating QR for vCard" \
&& docker run --rm -v "$qr_dir:/home/python/app" \
    -v "$vcard:/tmp/vcard.vcf" \
    -v "$image_profile:$image_profile_container" \
    -w "/home/python/app" python:3.10.12-alpine3.18 \
    sh -c "pip install -r requirements.txt --quiet && python generate_qr --data \"\$(cat /tmp/vcard.vcf)\" --image \"$image_profile_container\" --output \"$qr_output_container\"" \
&& mv -f "$qr_dir/qr.png" "$docs_output/qr_vcard.png" \
&& echo "Generated QR for vCard"