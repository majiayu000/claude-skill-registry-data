---
name: motion-ad
description: "Produce short motion-graphics video ads for any product as rendered MP4s, with GSAP-driven HTML beats and frame-by-frame capture."
---

# Motion Ad

Builds a sound-off-friendly motion-graphics ad as one HTML page driven by a paused GSAP timeline, then renders it frame by frame into an H.264 MP4. The bundled [assets/template.html](assets/template.html) is a finished 15s 4:5 ad (hook + phone → before/after scan reveal → 3D wall of outputs → showcase carousel + social proof → brand-color CTA end card). All brand and product content sits in one `CONFIG` object at the top of its script — start there and rewrite beats rather than building from zero. Missing images render as labelled placeholders, so the ad previews before real assets exist.

## CRITICAL

- **Claims must match the page the ad links to.** Read the destination page (WebFetch, or its source if it's in the current repo) before writing copy. Prices, counts, speeds, guarantees and "free" claims must appear on that page. If the user asks for copy that contradicts the page, do it, but flag the mismatch once.
- **Only use real assets** — the user's own images or ones pulled from their live site with `scripts/fetch-images.cjs`. Never invent customers, reviews, ratings or results. If the proof row has no real number to show, set `proof: null`.
- **Never fabricate a person.** If a beat needs more images of someone than exist, use crops/mirrors of real ones and say so.
- **Deliver to `~/Downloads/` with a versioned name** (`<brand>-<topic>-ad-4x5-v2.mp4`). Never overwrite an earlier version.
- **Match the brand**, not the template defaults: primary/accent/page colors, font, logo, tone. Default to no hype, no exclamation marks, no emoji unless the brand uses them.

## Workflow

```
- [ ] Step 1: Research product + destination page
- [ ] Step 2: Set up workdir and gather assets
- [ ] Step 3: Write the storyboard + copy
- [ ] Step 4: Fill CONFIG / edit the timeline
- [ ] Step 5: Render stills, review, fix
- [ ] Step 6: Render full MP4, spot-check transitions, deliver
```

### Step 1: Research

- Ask for (or infer from context) the product, the destination URL, the audience and the format (4:5 feed by default, 9:16 for stories/reels).
- WebFetch the destination page and the homepage/pricing for current facts: headline promise, prices, ratings/review counts, speed, what's free vs paid.
- Pull the brand: colors, font family and logo from the site's CSS/design system, or ask.

### Step 2: Workdir + assets

```bash
S=~/.claude/skills/motion-ad           # wherever this skill is installed
W=<scratchpad>/video && mkdir -p $W/a && cd $W
(cd $S/scripts && npm install)        # one-time: playwright-core + gsap, no browser download
cp $S/assets/template.html index.html
cp $S/scripts/node_modules/gsap/dist/gsap.min.js .
node $S/scripts/fetch-images.cjs --url <destination-url>   # -> a/web/NN.jpg + images.json
python3 $S/scripts/contact-sheet.py images a/web           # -> images.jpg, Read it to pick assets
```

Put the logo(s) in `a/` (light-background and, if available, a white version). Pick the hero before/after pair for the clearest transformation — for a SaaS product that can be "messy input → finished output" screenshots rather than photos. Portrait (≈4:5) images fill the hero and showcase cards best. Ask the user if they want specific images, and use theirs over scraped ones when offered.

### Step 3: Storyboard

Keep 4–5 beats in 15s, one short headline per beat (≤ ~20 chars per line at 82px), big enough to read muted. Template beats and the `CONFIG` fields that drive them:

| Time | Beat | CONFIG fields |
|---|---|---|
| 0–2.2s | Hook headline, phone scrolls a screen capture, finger taps the input | `hook`, `screen`, `screenScroll`, `tap` |
| 2.2–5.4s | Tapped card grows into the hero; scan beam reveals before → after; benefit pills | `reveal`, `before`, `after`, `beforeLabel`, `afterLabel`, `benefits` |
| 5.5–8.7s | Hero shrinks into a tilted 3D wall of outputs | `scale`, `scaleChip`, `gallery` |
| 8.7–11.8s | Showcase carousel (3 cards, optional "before" inset) + proof row | `proofHl`, `showcase`, `showChip`, `proof` |
| 11.8–15s | Brand-color circle wipe → logo, CTA headline, chip, button tap | `cta.headline`, `cta.chip`, `cta.button`, `cta.foot` |

If a beat doesn't fit the product, change or cut it in the timeline rather than forcing it (e.g. no phone step for a desktop tool — start on the hero card).

### Step 4: Fill CONFIG / edit the timeline

- Set `brand`, `logo`, `logoOnDark`, `colors`, and change the Google Fonts `<link>` plus `--font` to the brand font.
- Headlines: `*word*` or `*several words*` marks the accent color, `\n` forces a line break.
- Image paths are relative to `index.html` (e.g. `a/web/03.jpg`). Crop/mirror with PIL when an image needs a different framing.
- Adjust `tap` so the finger lands on the relevant spot of `screen` after it scrolls by `screenScroll`.
- Keep `window.seek`, `window.DURATION`, `window.ready` and the `?render` autoplay guard intact — `render.cjs` depends on them.
- For 9:16, change `html,body,#stage` to 1080×1920, re-space the vertical positions (headlines, phone, hero, carousel, end card), and render with `--size 1080x1920`.

### Step 5: Stills review

```bash
node $S/scripts/render.cjs --stills 0.3,1.9,2.7,3.8,4.9,6.6,9.8,11.5,13.6 && python3 $S/scripts/contact-sheet.py stills
```

Read `stills.jpg`. Check: text overlaps (end-card orbs vs headline), empty gaps, leftover placeholders, labels that contradict the image, duplicate images side by side in the wall, legibility at thumbnail size.

### Step 6: Full render + deliver

```bash
node $S/scripts/render.cjs --out ad-4x5.mp4          # ~1 min for 450 frames
ffprobe -v error -show_entries format=duration:stream=width,height,nb_frames -of csv=p=0 ad-4x5.mp4
mv ad-4x5.mp4 ~/Downloads/<brand>-<topic>-ad-4x5-vN.mp4
```

Spot-check transition frames with `ffmpeg -ss <t> -i <mp4> -frames:v 1 f.png`. Report: file path, the beat-by-beat copy, and any claim/asset caveats (low-res sources, crops, placeholders left in, copy that differs from the landing page).

## Requirements

Node 18+, Google Chrome (or `npx playwright install chromium` in `scripts/` and pass `--channel chromium`), `ffmpeg`, Python 3 with Pillow (`pip install pillow`).

## Troubleshooting

### Symptom: `Cannot find module 'playwright-core'`
**Cause:** The scripts' dependencies aren't installed.
**Fix:** `cd <skill>/scripts && npm install`. Run the scripts by their path in the skill folder, not copies in the workdir, so they resolve their own `node_modules`.

### Symptom: `Failed to launch chrome`
**Cause:** Google Chrome isn't installed.
**Fix:** Install Chrome, or `cd <skill>/scripts && npx playwright install chromium` and add `--channel chromium`.

### Symptom: `HTTP Error 403` or empty files when downloading images
**Cause:** CDNs block default Python/Node user agents.
**Fix:** Use curl with `-A 'Mozilla/5.0'` (fetch-images.cjs already does).

### Symptom: images missing from the fetched page
**Cause:** They lazy-load on scroll or come from client-side state.
**Fix:** Raise `--limit`, lower `--min`, or read them from the page's runtime state with Playwright; otherwise ask the user for the files.

### Symptom: shell command aborts with `no matches found: still-*.jpg`
**Cause:** zsh errors on unmatched globs and kills the whole command line.
**Fix:** Clean up with `find . -maxdepth 1 -name 'still-*.jpg' -delete`.

### Symptom: hero or carousel card looks soft
**Cause:** Site-hosted images are often small thumbnails.
**Fix:** Mention it to the user; drop higher-res originals into `a/` under the same filenames and re-render.
