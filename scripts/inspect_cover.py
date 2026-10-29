#!/usr/bin/env python3
"""Read-only PNG/JPEG geometry check. Does not inspect typography or modify images."""
import argparse
import json
from pathlib import Path
import struct
import sys


def dimensions(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        if len(data) < 24 or data[12:16] != b'IHDR':
            raise ValueError('Invalid PNG IHDR')
        return (*struct.unpack('>II', data[16:24]), 'PNG')
    if data[:2] == b'\xff\xd8':
        index = 2
        sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
               0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
        while index < len(data):
            if data[index] != 0xFF:
                raise ValueError('Invalid JPEG marker')
            while index < len(data) and data[index] == 0xFF:
                index += 1
            if index >= len(data):
                break
            marker = data[index]
            index += 1
            if marker in {0xD9, 0xDA}:
                break
            if marker == 0x01 or 0xD0 <= marker <= 0xD8:
                continue
            if index + 2 > len(data):
                raise ValueError('Truncated JPEG segment')
            length = struct.unpack('>H', data[index:index + 2])[0]
            if length < 2 or index + length > len(data):
                raise ValueError('Invalid JPEG segment length')
            if marker in sof:
                if length < 8:
                    raise ValueError('Invalid JPEG SOF')
                height, width = struct.unpack('>HH', data[index + 3:index + 7])
                return width, height, 'JPEG'
            index += length
        raise ValueError('JPEG dimensions not found')
    raise ValueError('Only PNG and JPEG are supported')


def main():
    root = Path(__file__).resolve().parents[1]
    presets = json.loads((root / 'references/presets.json').read_text())['formats']
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--preset', choices=presets, default='feishu')
    parser.add_argument('--allow-scaled', action='store_true')
    args = parser.parse_args()
    try:
        width, height, kind = dimensions(args.image)
        if min(width, height) <= 0:
            raise ValueError('Image dimensions must be positive')
        config = presets[args.preset]
        target_w, target_h = config['size']
        exact = [width, height] == config['size']
        # Accept less than half a native pixel of aspect-ratio rounding.
        same_ratio = abs(height - width * target_h / target_w) <= 0.5
        byte_size = args.image.stat().st_size
        not_oversize = byte_size <= config['max_bytes']
        status = exact and not_oversize
        if args.allow_scaled:
            status = same_ratio and not_oversize
        rect = config['safe_rect']
        scaled_rect = [round(rect[0] * width / target_w, 2),
                       round(rect[1] * height / target_h, 2),
                       round(rect[2] * width / target_w, 2),
                       round(rect[3] * height / target_h, 2)]
        report = {
            'path': str(args.image.resolve()), 'encoding': kind,
            'actual_size': [width, height], 'target_size': config['size'],
            'aspect_ratio': round(width / height, 6),
            'exact_pixels': exact, 'same_ratio_with_pixel_rounding': same_ratio,
            'bytes': byte_size, 'under_max_bytes': not_oversize,
            'under_preferred_bytes': byte_size <= config['preferred_bytes'],
            'target_safe_rect': rect,
            'reference_safe_rect_scaled_to_native': scaled_rect,
            'geometry_pass': status,
            'visual_and_text_qa': 'Manual inspection required; coordinates do not prove safe placement.'
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if status else 1
    except (OSError, ValueError, struct.error) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
