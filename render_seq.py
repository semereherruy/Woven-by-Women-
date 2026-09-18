#!/usr/bin/env python3
"""
Render the scroll-driven frame sequence for the Lydiana Imagination landing page.

The supplied pitch clip is a 640x360 screen recording of a slide deck, which is
unusable as cinematic footage. This renders the sequence instead from the
cooperative's high-resolution craft photography: six shots, each with a slow
interpolated camera move, crossfaded at the midpoints between chapter centres.
"""
from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path
import json, math, sys

SRC = Path("/Users/owner/Desktop/EDF APP/Lydiana Imagination Solutions")
OUT = SRC / "workspace/2026-09-18/animated-sites/lydiana-imagination/frames"

FRAME_COUNT = 104
AR = 16 / 9
DESKTOP = (1200, 675)
MOBILE = (680, 383)
Q_DESKTOP = 58
Q_MOBILE = 54

# crossfade midpoints between the six chapter dwell centres
CENTERS = [0.045, 0.215, 0.39, 0.565, 0.742, 0.925]
BOUNDS = [(CENTERS[i] + CENTERS[i + 1]) / 2 for i in range(len(CENTERS) - 1)]
FADE = 0.032  # half-width of each crossfade, in progress units


def rect(cx, cy, w):
    """16:9 rect centred on (cx, cy) with width w — all in 0..1 source fractions."""
    return (cx, cy, w)


# shot = (file, start rect, end rect)  — rects are (centre x, centre y, width) fractions
SHOTS = [
    # 1. the baskets — wide, slow push toward the coil pattern
    ("IMG_9233.JPG", rect(0.50, 0.62, 1.00), rect(0.47, 0.393, 0.78)),
    # 2. the workshop — weaver among stacked work, drift up to her face
    ("IMG_9231.JPG", rect(0.50, 0.18, 1.00), rect(0.46, 0.46, 0.80)),
    # 3. a finished hamper lifted — pull back slightly
    ("IMG_9229.JPG", rect(0.40, 0.56, 0.80), rect(0.46, 0.60, 1.00)),
    # 4. the founder
    ("IMG_9236.JPG", rect(0.52, 0.42, 0.98), rect(0.50, 0.38, 0.80)),
    # 5. the people
    ("IMG_9238.JPG", rect(0.53, 0.46, 1.00), rect(0.51, 0.50, 0.88)),
    # 6. macro — the checkerboard coil itself, for the closing frame
    ("IMG_9233.JPG", rect(0.62, 0.74, 0.50), rect(0.58, 0.70, 0.36)),
]


def ease(t):
    return t * t * (3 - 2 * t)


def load(name):
    im = Image.open(SRC / name)
    im = ImageOps.exif_transpose(im).convert("RGB")
    return im


CACHE = {}


def crop_for(name, r, size):
    im = CACHE.setdefault(name, load(name))
    W, H = im.size
    cx, cy, fw = r
    w = fw * W
    h = w / AR
    if h > H:  # rect taller than the source — clamp to source height
        h = H
        w = h * AR
    x = cx * W - w / 2
    y = cy * H - h / 2
    x = max(0, min(W - w, x))
    y = max(0, min(H - h, y))
    box = (round(x), round(y), round(x + w), round(y + h))
    return im.crop(box).resize(size, Image.LANCZOS)


def lerp_rect(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def grade(im):
    """One quiet grade so six different cameras read as a single film."""
    im = ImageEnhance.Color(im).enhance(0.88)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    # warm the shadows a touch toward the sisal/bark end
    r, g, b = im.split()
    b = b.point(lambda v: max(0, v - 6))
    r = r.point(lambda v: min(255, v + 4))
    return Image.merge("RGB", (r, g, b))


def render(size, quality, subdir):
    out = OUT / subdir
    out.mkdir(parents=True, exist_ok=True)
    for i in range(FRAME_COUNT):
        p = i / (FRAME_COUNT - 1)
        # which shot, and how far through it
        seg = 0
        while seg < len(BOUNDS) and p >= BOUNDS[seg]:
            seg += 1
        lo = 0.0 if seg == 0 else BOUNDS[seg - 1]
        hi = 1.0 if seg == len(BOUNDS) else BOUNDS[seg]
        local = ease((p - lo) / (hi - lo)) if hi > lo else 0.0
        name, r0, r1 = SHOTS[seg]
        frame = crop_for(name, lerp_rect(r0, r1, local), size)

        # crossfade into the next shot around each boundary
        if seg < len(BOUNDS):
            d = BOUNDS[seg] - p
            if 0 <= d < FADE:
                mix = ease((FADE - d) / (2 * FADE))
                n_name, n_r0, n_r1 = SHOTS[seg + 1]
                nxt = crop_for(n_name, n_r0, size)
                frame = Image.blend(frame, nxt, mix)
        if seg > 0:
            d = p - BOUNDS[seg - 1]
            if 0 <= d < FADE:
                mix = ease(0.5 - d / (2 * FADE))
                p_name, p_r0, p_r1 = SHOTS[seg - 1]
                prev = crop_for(p_name, p_r1, size)
                frame = Image.blend(frame, prev, mix)

        frame = grade(frame)
        frame.save(out / f"frame-{i+1:04d}.webp", "WEBP", quality=quality, method=6)

    files = sorted(out.glob("*.webp"))
    total = sum(f.stat().st_size for f in files)
    print(f"  {subdir:8} {len(files)} frames @ {size[0]}x{size[1]}  "
          f"{total/1024/1024:.2f}MB  ({total//len(files)//1024}KB avg)")
    return {"resolution": f"{size[0]}x{size[1]}", "count": len(files),
            "total_mb": round(total / 1024 / 1024, 2)}


print("rendering scroll sequence")
d = render(DESKTOP, Q_DESKTOP, "desktop")
m = render(MOBILE, Q_MOBILE, "mobile")

manifest = {
    "note": ("Sequence rendered from the cooperative's high-resolution craft "
             "photography. The supplied pitch clip (IMG_9228.MP4) is a 640x360 "
             "screen recording of an investor slide deck and is embedded "
             "separately rather than used as footage."),
    "shots": [s[0] for s in SHOTS],
    "frames": {"count": FRAME_COUNT, "format": "webp"},
    "chapter_centers": CENTERS,
    "shot_boundaries": [round(b, 4) for b in BOUNDS],
    "recommended_scroll_height": "720vh",
    "desktop": d, "mobile": m,
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
print("\nmanifest written")
