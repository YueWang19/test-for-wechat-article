#!/usr/bin/env python3
"""Fetch YouTube metadata and English JSON3 captions; never synthesize text."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def english_tracks(tracks):
    return sorted((k for k in tracks if re.fullmatch(r'en(?:[-_][A-Za-z0-9]+)*', k)),
                  key=lambda k: (k != 'en', k))


def transcript(data):
    rows = []
    previous = []
    previous_end = -1
    for event in data.get('events', []):
        value = ''.join(s.get('utf8', '') for s in event.get('segs', []))
        words = value.split()
        if not words:
            continue
        start = event.get('tStartMs', 0)
        end = start + event.get('dDurationMs', 0)
        original = words[:]
        if start < previous_end:
            for size in range(min(len(previous), len(words)), 0, -1):
                if previous[-size:] == words[:size]:
                    words = words[size:]
                    break
        if words:
            seconds = start // 1000
            rows.append(f'[{seconds // 3600:02}:{seconds // 60 % 60:02}:{seconds % 60:02}] ' + ' '.join(words))
        previous, previous_end = original, end
    if not rows:
        raise ValueError('Caption file contains no usable text')
    return '\n'.join(rows) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    host = (urlparse(args.url).hostname or '').lower()
    if host not in ('youtube.com', 'www.youtube.com', 'm.youtube.com', 'youtu.be'):
        parser.error('Provide a YouTube video URL')
    args.out.mkdir(parents=True, exist_ok=True)
    if any(args.out.iterdir()):
        parser.error('Output directory must be empty to avoid overwriting prior artifacts')
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({'skip_download': True, 'noplaylist': True,
                              'retries': 1, 'extractor_retries': 1, 'socket_timeout': 30}) as ydl:
            info = ydl.extract_info(args.url, download=False)
            inventory = {kind: {lang: sorted({f.get('ext', '') for f in formats})
                                for lang, formats in info.get(kind, {}).items()}
                         for kind in ('subtitles', 'automatic_captions')}
            meta = {k: info.get(k) for k in ('id', 'title', 'channel', 'uploader', 'duration', 'upload_date', 'webpage_url')}
            meta['caption_inventory'] = inventory
            meta_path = args.out / 'metadata.json'
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
            chosen = None
            for kind in ('subtitles', 'automatic_captions'):
                tracks = info.get(kind, {})
                for lang in english_tracks(tracks):
                    formats = [f for f in tracks[lang] if f.get('ext') == 'json3'
                               and 'tlang' not in parse_qs(urlparse(f.get('url', '')).query)]
                    if formats:
                        chosen = kind, lang, formats[0]
                        break
                if chosen:
                    break
            if not chosen:
                raise ValueError('No original English JSON3 captions available; provide a transcript')
            kind, lang, fmt = chosen
            meta['selected_caption'] = {'type': 'human' if kind == 'subtitles' else 'automatic', 'language': lang}
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
            with ydl.urlopen(fmt['url']) as response:
                raw = response.read()
            (args.out / 'captions.json3').write_bytes(raw)
            data = json.loads(raw)
            text = transcript(data)
            (args.out / 'transcript.txt').write_text(text, encoding='utf-8')
            print(json.dumps({'status': 'ok', 'selected': meta['selected_caption'], 'out': str(args.out)}, ensure_ascii=False))
    except Exception as exc:
        (args.out / 'retrieval-error.txt').write_text(str(exc) + '\n', encoding='utf-8')
        raise SystemExit(f'Retrieval failed: {exc}')


if __name__ == '__main__':
    main()
