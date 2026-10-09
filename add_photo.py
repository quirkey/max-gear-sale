"""Add or replace a photo in img/, resized and with all metadata (including GPS) stripped.

    python3 add_photo.py ~/Downloads/vox-ac-30.jpeg vox-ac30
    python3 add_photo.py ~/Downloads/wall.jpeg wall-of-pedals --max 900
    python3 add_photo.py ~/Downloads/vox-ac-30.jpeg vox-ac30 --crop 40,0,1000,960

Then use the key (e.g. vox-ac30) as `photo:` in items.yaml.
"""
import argparse, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from PIL import Image, ImageOps
except ImportError:
    # Pillow lives in the project venv; re-run under it so `python3 add_photo.py` just works.
    venv = os.path.join(HERE, '.venv')
    venv_py = os.path.join(venv, 'bin', 'python')
    if os.path.exists(venv_py) and os.path.realpath(sys.prefix) != os.path.realpath(venv):
        os.execv(venv_py, [venv_py, *sys.argv])
    sys.exit("Pillow is missing. Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt")

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('src', help='source image (JPEG, PNG, ...)')
ap.add_argument('key', help='photo key; saved as img/<key>.jpg')
ap.add_argument('--max', type=int, default=520, help='longest side in pixels (default 520; Max header photos use 720)')
ap.add_argument('--crop', help='crop box x0,y0,x1,y1 in source pixels, applied before resizing')
args = ap.parse_args()

im = ImageOps.exif_transpose(Image.open(os.path.expanduser(args.src))).convert('RGB')
if args.crop:
    im = im.crop(tuple(int(v) for v in args.crop.split(',')))
im.thumbnail((args.max, args.max), Image.LANCZOS)

buf = io.BytesIO()
im.save(buf, 'JPEG', quality=72, optimize=True, progressive=True)  # no exif= argument, so no metadata is written
data = buf.getvalue()
assert not dict(Image.open(io.BytesIO(data)).getexif()), 'metadata survived re-encode'

out = os.path.join(HERE, 'img', f'{args.key}.jpg')
existed = os.path.exists(out)
open(out, 'wb').write(data)
print(f"{'Replaced' if existed else 'Added'} {os.path.relpath(out, HERE)}: {im.width}x{im.height}, {len(data) // 1024}KB, metadata stripped")
