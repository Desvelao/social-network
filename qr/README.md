# Utilities

- generate_qr: generate a QR for vCard or text.

# generate_qr

- Generate a QR for vCard or string.

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

Create a QR for text:
```
python generate_qr --data "https://github.com/Desvelao/social-network" --output qr.png
```

Create a QR for vCard:
```
python generate_qr --data "$(cat <VCARD>)" --output qr.png
```

Create a QR for text:
```
python generate_qr --data "https://github.com/Desvelao/social-network" --image <IMAGE> --output qr.png
```

Create a QR for vCard with image:
```
python generate_qr --data "$(cat <VCARD>)" --image <IMAGE> --output qr.png
```

```
where:
- `<VCARD>`: vcard file.
- `<IMAGE>`: author name of the feeds.

See the available options:
```
python generate_qr --help
```

Example:
```
python generate_qr --data "https://github.com/Desvelao/social-network"
```

## Usage with Docker

```
docker run --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../docs/vcard.vcf:/tmp/vcard.vcf" -v "$(pwd)/image.png:/tmp/image.png" -w "/home/python/app" python:3.10.12-alpine3.18 sh -c 'pip install -r requirements.txt --quiet && python generate_qr --data "$(cat /tmp/vcard.vcf)" --image /tmp/image.png --output qr.png'
```

## Develop with Docker

```
docker run -itd --name generate_qr --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../docs/vcard.vcf:/tmp/vcard.vcf" -v "$(pwd)/image.png:/tmp/image.png" -w "/home/python/app" python:3.10.12-alpine3.18
```

