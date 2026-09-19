#!/usr/bin/env python3
"""Prepare web-optimized photography for the Lydiana Imagination landing page."""
from PIL import Image, ImageOps
from pathlib import Path

SRC = Path("/Users/owner/Desktop/EDF APP/Lydiana Imagination Solutions")
OUT = SRC / "workspace/2026-09-18/animated-sites/lydiana-imagination/img"
OUT.mkdir(parents=True, exist_ok=True)

# name, source, crop box (l,t,r,b) in source px or None, target long edge
JOBS = [
    # Lydia with the two coiled hampers, garden — story lead
    ("weaver-hampers", "IMG_9233.JPG", None, 1800),
    ("weaver-lifting", "IMG_9229.JPG", None, 1800),
    # Lydia holding the woven plate — video still, phone chrome cropped away
    ("craft-plate", "IMG_9232.JPG", (0, 148, 561, 1128), 1000),
    # weavers at work
    ("weaver-coiling", "IMG_9230.JPG", None, 900),
    ("weaver-workshop", "IMG_9231.JPG", None, 1400),
    # product
    ("product-lidded-pair", "IMG_9235.JPG", None, 1000),
    # gallery placement — cooperative work on display in a Malawian art gallery
    ("gallery-display", "LYDIA-gallery-display.jpg", None, 1100),
    # product
    ("product-checkerboard", "LYDIA-basket-pink-checkerboard.jpg", None, 900),
    # team
    ("team-olivia", "IMG_9240.JPG", None, 1000),
    ("team-innocent", "IMG_9239.JPG", None, 900),
    # cooperative members
    ("team-lydia", "IMG_9236.JPG", None, 1100),
    ("team-dalitso", "IMG_9238.JPG", (300, 500, 1750, 2300), 1300),
]

for name, src_name, box, long_edge in JOBS:
    src = SRC / src_name
    img = Image.open(src)
    img = ImageOps.exif_transpose(img)
    if box:
        img = img.crop(box)
    img = img.convert("RGB")
    w, h = img.size
    scale = min(1.0, long_edge / max(w, h))
    if scale < 1.0:
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    dest = OUT / f"{name}.webp"
    img.save(dest, "WEBP", quality=82, method=6)
    print(f"{dest.name:26} {img.size[0]}x{img.size[1]}  {dest.stat().st_size//1024}KB  <- {src_name}")

total = sum(p.stat().st_size for p in OUT.glob("*.webp"))
print(f"\nphoto payload: {total/1024/1024:.2f} MB across {len(list(OUT.glob('*.webp')))} files")
