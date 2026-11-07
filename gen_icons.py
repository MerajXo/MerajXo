#!/usr/bin/env python3
"""Generate placeholder PNG icons for the web/ folder.

Run once before `flutter build web` to silence favicon + PWA icon 404s.
Replace with real branded icons when you have them.
"""
import struct
import zlib
import os

def _png(w: int, h: int, rgb: tuple[int, int, int]) -> bytes:
    """Build a solid-color PNG (no PIL dependency)."""
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + bytes(rgb) * w for _ in range(h))
    idat = zlib.compress(raw)

    def chunk(t: bytes, d: bytes) -> bytes:
        return (struct.pack('>I', len(d)) + t + d +
                struct.pack('>I', zlib.crc32(t + d) & 0xffffffff))

    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')


def main(web_dir: str) -> None:
    icons_dir = os.path.join(web_dir, 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    # Brand colors from the iOS theme.
    blue = (10, 132, 255)        # systemBlue dark
    indigo = (94, 92, 230)       # systemIndigo dark

    files = {
        'favicon.png': (32, 32, blue),
        'icons/Icon-192.png': (192, 192, blue),
        'icons/Icon-512.png': (512, 512, blue),
        'icons/Icon-maskable-192.png': (192, 192, indigo),
        'icons/Icon-maskable-512.png': (512, 512, indigo),
    }
    for rel, (w, h, rgb) in files.items():
        path = os.path.join(web_dir, rel)
        with open(path, 'wb') as f:
            f.write(_png(w, h, rgb))
        print(f'  wrote {rel} ({w}x{h})')

    print(f'\nDone. Replace these placeholders with branded icons before going live.')


if __name__ == '__main__':
    import sys
    web_dir = sys.argv[1] if len(sys.argv) > 1 else 'web'
    if not os.path.isdir(web_dir):
        print(f'error: {web_dir} is not a directory')
        sys.exit(1)
    main(web_dir)
