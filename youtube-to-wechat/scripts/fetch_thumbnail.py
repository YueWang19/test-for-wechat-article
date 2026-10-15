#!/usr/bin/env python3
"""Download the grabber's Normal Image (480x360) without resizing a substitute."""
import argparse
import io
import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
from PIL import Image

SITE = 'https://youtube-thumbnail-grabber.com/'


def video_id(url):
    parsed = urlparse(url)
    if parsed.scheme != 'https':
        raise ValueError('Use an HTTPS YouTube video URL')
    host = (parsed.hostname or '').lower()
    if host == 'youtu.be':
        value = parsed.path.strip('/')
    elif host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            value = parse_qs(parsed.query).get('v', [''])[0]
        else:
            match = re.fullmatch(r'/(?:shorts|embed|live)/([\w-]{11})/?', parsed.path)
            value = match.group(1) if match else ''
    else:
        value = ''
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', value):
        raise ValueError('Cannot identify a YouTube video ID')
    return value


def fetch(url, limit):
    with urlopen(Request(url, headers={'User-Agent': 'youtube-to-wechat/1.0'}), timeout=30) as response:
        data = response.read(limit + 1)
        if len(data) > limit:
            raise ValueError('Response exceeds expected size')
        return data


def validate_image(data):
    with Image.open(io.BytesIO(data)) as image:
        if image.format != 'JPEG' or image.size != (480, 360):
            raise ValueError(f'Expected 480x360 JPEG; received {image.format} {image.size}')
        image.verify()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('url')
    p.add_argument('--out', required=True, type=Path, help='Existing article output folder')
    a = p.parse_args()
    try:
        ident = video_id(a.url)
        if not a.out.is_dir():
            raise ValueError('Article output folder must already exist')
        target = a.out / 'thumbnail-480x360.jpg'
        provenance = a.out / 'thumbnail-source.json'
        if target.exists() or provenance.exists():
            raise ValueError('Thumbnail artifacts already exist; preserve them or choose another folder')
        # Confirm the requested site still maps Normal/HQ to this exact endpoint.
        html = fetch(SITE, 2_000_000).decode('utf-8')
        if '480x360' not in html or 'hqreslink' not in html:
            raise ValueError('Grabber page changed; inspect its Normal Image control manually')
        if not re.search(r'<script\b[^>]*src=["\']/ytg\.js["\']', html):
            raise ValueError('Grabber script changed; inspect its download control manually')
        js = fetch(SITE + 'ytg.js', 2_000_000).decode('utf-8')
        if not re.search(r'case\s+["\']HQ["\']\s*:\s*return\s+["\']https://i3\.ytimg\.com/vi/["\']\s*\+\s*id\s*\+\s*["\']/hqdefault\.jpg["\']', js):
            raise ValueError('Normal Image download rule changed; use the current website UI')
        image_url = f'https://i3.ytimg.com/vi/{ident}/hqdefault.jpg'
        data = fetch(image_url, 10_000_000)
        validate_image(data)
        # Exclusive creation preserves prior files if another task wrote meanwhile.
        with target.open('xb') as output:
            output.write(data)
        with provenance.open('x', encoding='utf-8') as output:
            json.dump({'video_url': a.url, 'video_id': ident, 'website': SITE,
                       'image_url': image_url, 'size': [480, 360],
                       'method': 'Website HQ rule verified from HTML and ytg.js; direct original-image download'},
                      output, ensure_ascii=False, indent=2)
        print(f'Saved verified 480x360 JPEG: {target}')
    except Exception as exc:
        raise SystemExit(f'Thumbnail download failed: {exc}')


if __name__ == '__main__':
    main()
