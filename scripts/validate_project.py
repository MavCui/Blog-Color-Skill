#!/usr/bin/env python3
"""Validate the installable skill, documentation links, fonts, and image inspector.

Uses only the Python standard library. Never modifies repository assets.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import importlib.util
import json
import re
import struct
import subprocess
import sys
import tempfile
import zlib


ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href') and value:
                self.targets.append(value)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def anchors(text):
    """GitHub-style anchors for the plain headings used in this repository."""
    result, counts = set(), {}
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', text, flags=re.M):
        heading = re.sub(r'<[^>]*>', '', heading).lower().strip()
        heading = re.sub(r'[^\w\-\s]', '', heading, flags=re.UNICODE)
        slug = re.sub(r'\s', '-', heading)
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(slug if count == 0 else f'{slug}-{count}')
    return result


def validate_links():
    count = 0
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        parser = Links()
        parser.feed(text)
        targets = parser.targets + re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text)
        for target in targets:
            parsed = urlsplit(target.strip('<>'))
            if parsed.scheme or parsed.netloc:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            require(destination.is_relative_to(ROOT), f'Link leaves repository: {path}: {target}')
            require(destination.exists(), f'Broken link: {path}: {target}')
            if parsed.fragment and destination.suffix == '.md':
                require(unquote(parsed.fragment) in anchors(destination.read_text(encoding='utf-8')),
                        f'Broken heading link: {path}: {target}')
            count += 1
    return count


def validate_presets_and_fonts():
    presets = json.loads((ROOT / 'references/presets.json').read_text())
    for name, config in presets['formats'].items():
        width, height = config['size']
        x1, y1, x2, y2 = config['safe_rect']
        require(0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height,
                f'Invalid safe rectangle: {name}')
        require(width > height > 0, f'Expected a landscape preset: {name}')
    for name, palette in presets['palettes'].items():
        for key in ('substrate', 'dominant', 'accent'):
            require(re.fullmatch(r'#[0-9A-Fa-f]{6}', palette[key]), f'Invalid color: {name}/{key}')
        require(palette['dominant'] != palette['accent'], f'Duplicate inks: {name}')
        require(sum(palette['printed_mark_ratio']) == 100, f'Invalid ink ratio: {name}')
    require(len(presets.get('styles', {})) == 8, 'Expected eight style families')
    for name, style in presets['styles'].items():
        require(len(style['palettes']) == 3 and len(style['layouts']) == 2, f'Incomplete style: {name}')
        require(style['typography'] in presets['typography'], f'Unknown typography: {name}')
        require(all(x in presets['palettes'] for x in style['palettes']), f'Unknown palette: {name}')
        require(all(x in presets['layouts'] for x in style['layouts']), f'Unknown layout: {name}')
        require((ROOT / style['reference']).is_file(), f'Missing style guide: {name}')
        require((ROOT / style['preview']).is_file(), f'Missing style preview: {name}')
    fonts = ROOT / 'assets/fonts'
    records = json.loads((fonts / 'manifest.json').read_text())
    seen = set()
    for record in records:
        path = fonts / record['file']
        require(record['file'] not in seen, f'Duplicate manifest entry: {path}')
        seen.add(record['file'])
        data = path.read_bytes()
        require(len(data) == record['bytes'], f'Font resource size differs: {path.name}')
        require(hashlib.sha256(data).hexdigest() == record['sha256'], f'Checksum differs: {path.name}')
        require(record['source'].startswith('https://'), f'Missing resource provenance: {path.name}')
        if path.suffix in ('.ttf', '.otf'):
            require(data[:4] in (b'OTTO', b'\x00\x01\x00\x00'), f'Invalid font header: {path.name}')
    for preset in presets['typography'].values():
        for role in ('zh', 'en'):
            require(preset[role]['file'] in seen, f'Missing preset font: {preset[role]["file"]}')
    require(presets['utility_font']['file'] in seen, 'Missing utility font')
    for license_name in ('SourceHanSerif-OFL.txt', 'bodonimoda-OFL.txt',
                         'cormorantgaramond-OFL.txt', 'ibmplexmono-OFL.txt'):
        require('SIL OPEN FONT LICENSE' in (fonts / license_name).read_text(),
                f'Missing font license: {license_name}')
    return len(records)


def png_bytes(width, height):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    header = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    pixels = b''.join(b'\x00' + b'\xff\xff\xff' * width for _ in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header)
            + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))


def validate_inspector():
    script = ROOT / 'scripts/inspect_cover.py'
    spec = importlib.util.spec_from_file_location('cover_inspector', script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in ('A-context.png', 'B-collaboration.png', 'C-judgment.png'):
        width, height, _ = module.dimensions(ROOT / 'assets/examples' / name)
        require(width > height > 0, f'Invalid example geometry: {name}')
    width, height, _ = module.dimensions(ROOT / 'docs/assets/readme-cover.png')
    require(2.2 <= width / height <= 2.5, 'Unexpected README cover aspect ratio')
    with tempfile.TemporaryDirectory(prefix='blog-color-check-') as tmp:
        tmp = Path(tmp)
        exact = tmp / 'exact.png'
        exact.write_bytes(png_bytes(2000, 400))
        scaled = tmp / 'scaled.png'
        scaled.write_bytes(png_bytes(1000, 200))
        wrong = tmp / 'wrong.png'
        wrong.write_bytes(png_bytes(1000, 400))
        invalid = tmp / 'invalid.png'
        invalid.write_bytes(b'not an image')
        checks = [(exact, [], 0), (scaled, [], 1), (scaled, ['--allow-scaled'], 0),
                  (wrong, ['--allow-scaled'], 1), (invalid, [], 2)]
        for path, flags, expected in checks:
            result = subprocess.run([sys.executable, str(script), str(path), '--preset', 'feishu', *flags],
                                    capture_output=True, text=True, check=False)
            require(result.returncode == expected,
                    f'Inspector returned {result.returncode}, expected {expected}: {path.name} {flags}')
        # JPEG SOF metadata fixtures cover baseline and progressive frame markers.
        for marker in (0xC0, 0xC2):
            jpeg = tmp / f'frame-{marker}.jpg'
            frame = bytes([8]) + struct.pack('>HH', 400, 2000) + b'\x01\x01\x11\x00'
            jpeg.write_bytes(b'\xff\xd8\xff' + bytes([marker])
                             + struct.pack('>H', len(frame) + 2) + frame + b'\xff\xd9')
            require(module.dimensions(jpeg) == (2000, 400, 'JPEG'), 'JPEG frame parsing failed')
    return len(checks) + 2


def main():
    try:
        for name in ('SKILL.md', 'README.md', 'README.zh-CN.md', 'LICENSE',
                     'ASSET-LICENSE.md', 'agents/openai.yaml',
                     'references/mono-color-license.txt', 'docs/readme-cover-prompt.txt'):
            require((ROOT / name).is_file(), f'Missing required file: {name}')
        skill = (ROOT / 'SKILL.md').read_text()
        require(skill.startswith('---\n'), 'Missing skill frontmatter')
        frontmatter = skill.split('---', 2)[1]
        require(re.search(r'^name: editorial-wide-cover$', frontmatter, re.M), 'Wrong invocation name')
        require(re.search(r'^description: .+', frontmatter, re.M), 'Missing discovery description')
        require('$editorial-wide-cover' in (ROOT / 'agents/openai.yaml').read_text(),
                'Invocation metadata differs from skill name')
        require('README.zh-CN.md' in (ROOT / 'README.md').read_text(), 'Missing Chinese README link')
        for path in ROOT.rglob('*.json'):
            if '.git' not in path.parts:
                json.loads(path.read_text())
        links = validate_links()
        resources = validate_presets_and_fonts()
        checks = validate_inspector()
        print(f'PASS: installable skill, {links} local links, {resources} font resources, '
              f'4 artwork files, {checks} inspector regression cases.')
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
