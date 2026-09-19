# Lydiana Imagination Solutions — landing page

Scroll-driven landing page for the women-led basket weaving cooperative in Malawi.

## Run it

```bash
cd "/Users/owner/Desktop/EDF APP/Lydiana Imagination Solutions/workspace/2026-09-18/animated-sites/lydiana-imagination" && python3 -m http.server 8099
```

Then open http://127.0.0.1:8099. It must be served over HTTP — opening `index.html`
directly from the filesystem will not load the frame sequence.

## What is here

```
index.html            the whole site (no build step, no dependencies)
frames/desktop/       104 WebP frames, 1200x675   — 10.1 MB
frames/mobile/        104 WebP frames, 680x383    —  4.1 MB
frames/manifest.json  how the sequence was built
img/                  12 photographs, web-optimised — 2.2 MB
```

## Design thesis

A film about a women-led basket weaving cooperative in Malawi, shown through the
visual language of **a coiled basket's own construction notation** — coil rows,
stitch ticks, and a count that builds a vessel one row at a time.

- **Palette** sampled from the cooperative's own logo and deck (forest `#1d5750`,
  gold `#c0912f`, cream `#f4f1e8`) plus its craft photography (sisal, bark,
  terracotta, leaf).
- **Type** Archivo variable + IBM Plex Mono. The display width axis tightens from
  78 to 104 as you scroll, echoing a coil being pulled tight.
- **Signature device** the coil rail along the bottom: chapter, a stitch-tick
  progress fill, and `COIL 048 / 104`.
- **Stitch rule** section dividers are a hairline punctuated by short gold ticks,
  copying the dark stitches that interrupt each coil on the checkerboard baskets.

## The source video — important

The supplied clip (`IMG_9228.MP4`, also the Google Drive link) is **not cinematic
footage**. It is a 2:52, 640x360 screen recording of an investor slide deck with
burned-in subtitles. Used as a scroll sequence it would have produced a blurry
slideshow of deck screenshots and would have published the per-basket cost
structure, revenue model, financial projections and funding ask on a public page.

So the scroll sequence is instead **rendered from the cooperative's own
high-resolution craft photography** — six shots, each with a slow interpolated
camera move, crossfaded at the midpoints between chapter centres. The renderer is
`render_seq.py` (see below). The engine itself is unchanged.

The pitch video is embedded separately, in its own clearly labelled section, from
the public Google Drive link.

**Decide deliberately whether that section stays.** It is a founder's investor
pitch: it states the funding ask, per-basket economics and revenue projections.
That is normal for investors and unusual for a public landing page. Removing it
means deleting the `<section id="pitch">` block — nothing else depends on it.

## Facts on the page, and where each came from

Everything factual is traceable to Lydia's own materials. Nothing was invented.

| Claim | Source |
|---|---|
| Cooperative for women basket weavers; fair wages, design training, cooperative ownership | Lydia's WhatsApp messages |
| Works in weaving and biodiversity, specifically indigenous tree preservation | Lydia's WhatsApp messages |
| $48/month weaver earnings; $5M+ market held by middlemen; 200,000+ in Malawi; 3M+ across Africa | Pitch deck "The Problem", citing World Bank Report on Africa 2022 and Expert Market Research 2025 |
| 11 weavers recruited; 50 baskets sold; pay up 125% | Pitch deck "Traction" — achieved milestones |
| Weaver → cooperative → QC & packaging → client; hotels, lodges, corporate gift partners | Pitch deck "Traction" |
| Team names, roles and credentials | Pitch deck "The Team" |
| Phone, email, P.O. Box | Lydia's WhatsApp messages |
| Cooperative work on display in a Malawian art gallery ("Art, not just storage") | Photograph sent by Lydia, 19 Sep 2026 |

Deliberately **left off**: revenue model, per-basket costs, margin, 3-year
projections, funding allocation and ROI. Those are investor-deck material.

## Pending from Lydia

She is opening a **business email address** and will send it. When it arrives,
replace `lydiafiguereido4@gmail.com` in the contact section, the closing CTA
`mailto:` and the footer — three places in `index.html`. A business address will
read considerably better to wholesale buyers than a personal Gmail.

## Two things to check with Lydia

1. **Dalitso Mbendera** (Business Strategy Advisor) is on the page. She is in the
   pitch deck's team slide but was not in the brief's list of three — confirm she
   should be shown publicly.
2. **Olivia Anthony's title.** The brief says "Production and Quality Control
   Manager"; the deck says "LeadWeaver + Quality Control". The brief's wording is
   used.

## Known gaps

- **The real logo is not on the page.** The only copy available was ~40px wide in
  the 360p video. The header uses a typographic wordmark with a simple coil mark.
  Drop in the real SVG/PNG when Lydia sends it — replace the `.coil-mark` SVG and
  the brand text in `<header class="site-header">`.
- **Photography.** Two photographs (`weaver-coiling` at 416x345, `craft-plate` at
  561x980) are low resolution and are used at small sizes only. Higher-resolution
  product shots would lift the craft gallery considerably. The gallery interior
  (720x901) and the checkerboard basket (559x613) are adequate at the sizes used
  but would not survive being enlarged.
- The people in the garden photographs are captioned as cooperative weavers
  rather than named, because the source material does not identify them.

## Note on the craft gallery

`img/gallery-display.webp` is cropped to landscape on purpose. The portrait
original left a tall column of dead green beside the copy at desktop width. The
crop keeps the woven wall pieces, the starburst plates and all three shelves of
coiled plates — the part that carries the "this is art" argument.

On phones the craft gallery is a two-up tile grid on a shared aspect ratio
(`3/4`, with the opening and closing pieces full width at `4/3`). The earlier
ragged single column left most of the screen empty. Tile captions drop their
index number below 780px, where it only pushed the label onto a third line.

## Regenerating the sequence

`render_seq.py` (kept alongside this README) rebuilds `frames/`. Edit the `SHOTS`
list to change which photograph each chapter sits on, or its start and end crop.
Crop rects are `(centre x, centre y, width)` as fractions of the source image.

```bash
python3 render_seq.py
```

Chapter dwell centres in `index.html` (`DWELL_CENTERS`) and the shot boundaries in
`render_seq.py` (`CENTERS`) must stay in sync — the boundaries are the midpoints
between the centres, so each chapter gets its own shot.

## Verified

- Desktop 1440x900: all six chapters composed in real negative space, header
  legible over both film and cream bands, closing CTA reachable.
- Mobile 375x812 and 320x720: no horizontal overflow, film sits in its letterboxed
  aperture, copy below it, team grid two-up at both widths.
- No console errors; all 208 frames, 12 photographs and the manifest return 200.
- Audited at 1440, 390 and 320: no horizontal overflow, no broken images, no image
  displayed above 1.35x its natural width, every link at least 44px tall.
- One `<h1>`, ordered headings, every image has alt text, the iframe is titled,
  the skip link is visible on focus, touch targets are at least 44px.
- `prefers-reduced-motion` renders a single poster frame with the hero chapter and
  hides the rail.
