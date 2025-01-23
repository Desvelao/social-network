# Utilities

- generate_qr: generate a QR for vCard or text.

# generate_qr

- Generate a QR for vCard or string.

## Install the dependencies

```
pip install -r requirements.txt
```

Tested with Python v3.10.12.

## Usage

Create a QR for text:
```
python generate_qr --data "https://github.com/Desvelao/social-network" --output qr.png
```

Create a QR for vCard:
```
python generate_qr --data "$(cat <VCARD>)" --output qr.png
```

Create a QR for text with image:
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
- `<IMAGE>`: path to image.

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
docker run --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../docs/vcard.vcf:/tmp/vcard.vcf" -v "$(pwd)/../docs/profile.jpg:/tmp/image.jpg" -w "/home/python/app" python:3.10.12-alpine3.18 sh -c 'pip install -r requirements.txt --quiet && python generate_qr --data "$(cat /tmp/vcard.vcf)" --image /tmp/image.jpg --output qr-vcard.png'
```

## Develop with Docker

```
docker run -itd --name generate_qr --rm -v "$(pwd):/home/python/app" -v "$(pwd)/../docs/vcard.vcf:/tmp/vcard.vcf" -w "/home/python/app" python:3.10.12-alpine3.18
```

## QR code schema

## Phone calls

tel:

```
python generate_qr --data 'tel:+TEL'
python generate_qr --data 'tel:+TEL' --caption-bottom '+TEL'
python generate_qr --data 'tel:+TEL' --caption-bottom '+TEL' --caption-top 'NAME'
```

### Wifi

WIFI:T:WPA;S:SSID_NAME;P:PASSWORD;;

Reference:
- https://www.wi-fi.org/system/files/WPA3%20Specification%20v3.2.pdf#page=25


