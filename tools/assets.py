#!/usr/bin/env python3
"""Offline asset verification and split/join; no device access."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

BLOCK = 8 * 1024 * 1024

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(BLOCK), b''):
            h.update(b)
    return h.hexdigest()

def within(root, name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Invalid relative path')
    if Path(name).is_absolute() or any(p in ('', '.', '..') for p in name.split('/')):
        raise ValueError('Unsafe relative path')
    target = (root / name).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Path escapes directory')
    return target

def check(row):
    if type(row.get('bytes')) is not int or row['bytes'] < 0:
        raise ValueError('Invalid byte count')
    if not re.fullmatch(r'[0-9a-f]{64}', row.get('sha256', '')):
        raise ValueError('Invalid SHA-256')

def verify(manifest, root):
    rows = json.loads(manifest.read_text(encoding='utf-8-sig'))['files']
    if not rows:
        raise ValueError('Empty manifest')
    seen = set()
    for row in rows:
        check(row)
        p = within(root, row['path'])
        if p in seen:
            raise ValueError('Duplicate path')
        seen.add(p)
        if not p.is_file() or p.stat().st_size != row['bytes'] or digest(p) != row['sha256']:
            raise ValueError('Missing or corrupt asset: ' + row['path'])
        print('OK', row['path'], flush=True)

def split(source, directory, chunk_bytes=1024**3):
    if chunk_bytes < 1 or chunk_bytes >= 2*1024**3:
        raise ValueError('Chunk size must be positive and below 2 GiB')
    if not source.is_file() or source.stat().st_size == 0:
        raise ValueError('Missing or empty input')
    directory.mkdir(parents=True, exist_ok=False)
    rows, total = [], hashlib.sha256()
    with source.open('rb') as src:
        while True:
            data = src.read(min(BLOCK, chunk_bytes))
            if not data:
                break
            name = source.name + '.part' + str(len(rows)+1).zfill(4)
            h, size = hashlib.sha256(), 0
            with (directory/name).open('xb') as dst:
                while data:
                    dst.write(data); h.update(data); total.update(data); size += len(data)
                    if size == chunk_bytes:
                        break
                    data = src.read(min(BLOCK, chunk_bytes-size))
            rows.append({'path': name, 'bytes': size, 'sha256': h.hexdigest()})
    payload = {'schema': 1, 'name': source.name, 'bytes': sum(r['bytes'] for r in rows),
               'sha256': total.hexdigest(), 'parts': rows}
    (directory/'parts.json').write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    return payload

def join(manifest, target):
    payload = json.loads(manifest.read_text(encoding='utf-8-sig'))
    check(payload)
    rows = payload.get('parts', [])
    if not rows:
        raise ValueError('Empty part list')
    seen = set()
    for row in rows:
        check(row)
        p = within(manifest.parent, row['path'])
        if p in seen:
            raise ValueError('Duplicate part')
        seen.add(p)
        if not p.is_file() or p.stat().st_size != row['bytes']:
            raise ValueError('Missing or wrong-size part')
    if sum(r['bytes'] for r in rows) != payload['bytes']:
        raise ValueError('Incomplete part list')
    if target.exists():
        raise FileExistsError('Refusing to overwrite output')
    partial, created = target.with_name(target.name+'.partial'), False
    try:
        with partial.open('xb') as dst:
            created = True
            for row in rows:
                h = hashlib.sha256()
                with within(manifest.parent, row['path']).open('rb') as src:
                    for b in iter(lambda: src.read(BLOCK), b''):
                        dst.write(b); h.update(b)
                if h.hexdigest() != row['sha256']:
                    raise ValueError('Corrupt part: '+row['path'])
        if partial.stat().st_size != payload['bytes'] or digest(partial) != payload['sha256']:
            raise ValueError('Joined hash mismatch')
        # Same-directory hardlink atomically refuses an existing final name.
        os.link(partial, target)
        partial.unlink()
        created = False
    finally:
        if created:
            partial.unlink(missing_ok=True)
    return target

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    s=sub.add_parser('verify'); s.add_argument('manifest',type=Path); s.add_argument('directory',type=Path)
    s=sub.add_parser('split'); s.add_argument('source',type=Path); s.add_argument('directory',type=Path)
    s=sub.add_parser('join'); s.add_argument('manifest',type=Path); s.add_argument('target',type=Path)
    a=p.parse_args()
    if a.action=='verify': verify(a.manifest,a.directory)
    elif a.action=='split': split(a.source,a.directory)
    else: join(a.manifest,a.target)

if __name__=='__main__':
    main()
