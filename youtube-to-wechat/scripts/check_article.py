#!/usr/bin/env python3
"""Validate final Markdown structure; editorial fidelity still needs human/model review."""
import argparse
import re
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('article', type=Path)
p.add_argument('--source', required=True)
a = p.parse_args()
s = a.article.read_text(encoding='utf-8')
assert len(re.findall(r'^# .+', s, re.M)) == 1, 'Need one title'
headings = re.findall(r'^## (.+)', s, re.M)
assert len(headings) == 4, 'Need exactly four sections'
assert all(re.search(r'[\u4e00-\u9fff]', h) for h in headings), 'Use descriptive Chinese headings'
assert not re.search(r'^#{3,6} ', s, re.M), 'Avoid additional heading levels'
assert a.source in s, 'Missing original source URL'
parts = re.split(r'^## .+$', s, flags=re.M)
assert all(part.strip() for part in parts[1:]), 'Empty article section'
print('PASS: title, four Chinese sections, nonempty bodies, source URL')
