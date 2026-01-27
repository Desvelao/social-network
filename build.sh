#!/bin/env bash
# This script generates
# - RSS feed from csv feeds.csv
# - QR for vCard

script_name="$(basename $0)"
script_version="2026.01.27"
script_description="Utility to generate the feed file from CSV (feeds.csv) and QR for vCard."
script_usage="${script_name} [--author|-a <author>] [--email|-e <email>] [--url|-r <feeds_url>]"
script_commands="
 --author,-a Define the author.
 --email,-e Define the author email.
 --url,-u Define the feeds url.
"
script_usage_examples="
${script_name} --author Author --email author@example.com --url https://mysite/feeds.rss
"

_display_help(){
  echo """${script_name} (${script_version})
${script_description}

Usage: ${script_usage}

Commands:
    -h, --help                               Display the help.${script_commands}

Examples:${script_usage_examples}
"""
}

_question(){
  read -p "$@" -r
  echo "$REPLY"
}

_abort(){
  echo "Aborting..."
  exit 1
}

_ask_for_input(){
    local prompt="$1"
    local input=""
    while [ -z "$input" ]; do
        input=$(_question "$prompt")
    done
    echo "$input"
}

_parse(){
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --author|-a) [ -n "$2" ] && { author_name="$2"; shift 2; } || { exit_with_message "[error] $1 is not defined."; };;
      --email|-e) [ -n "$2" ] && { email="$2"; shift 2; } || { exit_with_message "[error] $1 is not defined."; };;
      --url|-u) [ -n "$2" ] && { feeds_url="$2"; shift 2; } || { exit_with_message "[error] $1 is not defined."; };;
      --help) _display_help; exit 0;;
      *) {
        break
      };;
    esac
  done
}

author_name=""
email=""
feeds_url=""

_parse $@

if [ -z "$author_name" ]; then
    author_name=$(_ask_for_input 'Define the author name: ')
fi

if [ -z "$email" ]; then
    email=$(_ask_for_input 'Define the email: ')
fi

if [ -z "$feeds_url" ]; then
    feeds_url=$(_ask_for_input 'Define the feeds URL where they will be exposed: ')
fi

echo "
==========================
Configuration
==========================
author=${author_name}
email=${email}
feeds_url=${feeds_url}
==========================
"

if ! [[ $(_question "Generate the feeds and QR files? Reply with Y/y to continue: ") =~ ^[Yy]$ ]]; then 
    _abort;
fi;

# Feeds
feeds_dir="$(pwd)/feeds"
echo "Generating feeds" \
&& docker run --rm -v "$feeds_dir:/home/python/app" \
    -v "$feeds_dir/../feeds.csv:/tmp/feeds.csv" \
    -w "/home/python/app" python:3.10.12-alpine3.18 \
    sh -c "pip install -r requirements.txt --quiet && python generate_feed /tmp/feeds.csv --author-email '$email' --author-name '$author_name' --title '$author_name feeds' --link '$feeds_url' --description 'Recently updated feeds from $author_name' --output-feed rss" > docs/feeds.rss \
&& echo "Generated feeds"

# QR: vCard
input_qr_dir="$(pwd)/input_files"
echo "Creating temporal directory at $input_qr_dir"
mkdir -p $input_qr_dir
vcard="$(pwd)/docs/vcard.vcf"
qr_vcard="$(pwd)/docs/qr_vcard.png"
image_profile="$(pwd)/docs/profile.jpg"
docs_output="$(pwd)/docs"
cp $vcard $input_qr_dir/vcard.vcf
cp $image_profile $input_qr_dir/profile.jpg
qr_dir="$(pwd)/qr"
vcard_container="/tmp/vcard.vcf"
image_profile_container="/tmp/profile.jpg"
qr_vcard_container="/tmp/qr.png"
echo "Generating QR code for vCard" \
&& docker run --rm -v "$qr_dir:/home/python/app" \
    -v "$input_qr_dir:/tmp" \
    -w "/home/python/app" python:3.10.12-alpine3.18 \
    sh -c "pip install -r requirements.txt --quiet && python generate_qr --data \"\$(cat $vcard_container)\" --image \"$image_profile_container\" --output \"$qr_vcard_container\"" \
&& mv -f "$input_qr_dir/qr.png" "$docs_output/qr_vcard.png" \
&& rm -rf $input_qr_dir \
&& echo "Generated QR code for vCard"