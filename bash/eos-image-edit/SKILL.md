---
name: eos-image-edit
description: Edit an EXISTING image file (a phone screenshot from Photos, an exported photo, any PNG/JPG) for publishing — blur private/sensitive regions while keeping the demonstrative content, and crop away chrome (keyboards, status bars, empty margins). Backed by the pure `emptyos.sdk.media.redact_image` helper and its `scripts/redact_screenshot.py` CLI (blur pixel/fraction regions + crop in one pass, `--spec` JSON for batch). Use when the user says "blur this screenshot", "hide the amounts/name/address in this image", "redact this for the blog", "crop the keyboard out", "prepare this photo for the post", or hands over a screenshot with real data to publish. NOT for capturing a live EmptyOS UI (use eos-screenshot — it blurs DOM selectors during capture) and NOT for authoring SVG diagrams (use eos-article-diagrams).
---

# EmptyOS Image Edit — redact + crop an existing image

The complement to `eos-screenshot`. That skill captures a **live UI** and blurs
**CSS selectors** before the shot. This skill edits an **image file that already
exists** — a phone screenshot the user AirDropped from Photos, an exported
photo, a JPG someone pasted — where there is **no DOM to select**, only pixels.
The two risks are the same as always for a Published asset (personal-data leak,
chrome clutter), but the input is a finished raster, so the tool works on
**pixel/fraction regions**, not selectors.

Reference run: the "Chat App as Pocket Console" post
(`30_Resources/Published/posts/telegram-pocket-console-*.md`) — three phone
screenshots redacted (expense amounts, budget, a pharmacy order # + suburb, chat
count) and cropped (iOS keyboards, a ghost-text status bar) while keeping every
demonstrative payload visible.

## When to use / when not

**Use** when the user hands over (or points at) an existing image that needs
private data hidden or chrome removed before it ships in a post.

**Don't use** for:
- Capturing a live EmptyOS page → `eos-screenshot` (selector-blur during capture, `.eos-personal`/`.eos-branding` scan).
- Authoring a diagram → `eos-article-diagrams` (hand-written SVG → `scripts/rasterize_svg.py`).
- Anything that needs real editing (compositing, retouching, recolor) — this skill only does **blur** + **crop**.

## The tool

`scripts/redact_screenshot.py` → `emptyos.sdk.media.redact_image(src, dst, *, blur=[...], crop=..., pixel_block=24, gaussian=8)`. Pure Pillow, no daemon.

- **Boxes are `(x0, y0, x1, y1)`.** Each value is read as a **fraction** of the dimension when `<= 1.0`, as an absolute **pixel** otherwise. Don't mix the two conventions within one box. Out-of-range is clamped.
- **Order is fixed: blur first, then crop**, and every box is in the **original** image's coordinates — so you eyeball regions against the full image once and the crop never shifts them.
- **`blur`** = pixelate + Gaussian; higher `pixel_block` = blockier = more redacted.

Single image:
```bash
python scripts/redact_screenshot.py in.png --out out.png \
  --blur 0.62,0.20,0.98,0.36 --crop 0,0,1,0.90
```

Batch (re-runnable — the right shape for a multi-image post):
```bash
python scripts/redact_screenshot.py --spec redact.json --json
# redact.json: [{"src": "...orig.png", "dst": ".../media/shot.png",
#               "blur": [[0.05,0.15,0.98,0.21]], "crop": [0,0,1,0.90]}]
```

## Workflow (the judgment is the skill)

### 1. Find the exact regions before blurring
`Read` the image — but it downsamples, so coordinates are approximate. To pin a
region precisely, crop a strip with PIL and `Read` **that**:
```python
from PIL import Image
im = Image.open(src); W, H = im.size
im.crop((0, int(0.02*H), int(0.55*W), int(0.16*H))).save("/tmp/strip.png")  # then Read it
```
Convert the strip's pixel position back to a fraction of the full `W`/`H`.

### 2. Decide what to blur — the load-bearing rule
**Blur the PRIVATE data; KEEP the demonstrative content.** The figure's whole
value is usually the thing you're tempted to blur (the payload, the JSON, the
"look, it did X"). Blur only what leaks *personal* information:
- real amounts/totals/budgets, transaction history, account/order numbers, addresses/suburbs, real names (unless the name is the demo), phone/chat counts, other people's data.
- Keep visible: the demonstrated action, the example payload, the button/UI being shown — that's why the screenshot exists.

If blurring a region would gut the point of the figure, you're blurring the wrong thing.

### 3. Decide the crop — remove chrome, keep content
Crop away the parts that carry no argument: the on-screen keyboard + predictive-paste bar, an empty page margin, and any **status-bar ghost/bleed** from a previous screen (these often leak a stray amount). Keep the meaningful content, and keep a small margin so nothing is clipped.

### 4. Always redact from the ORIGINAL — never compound
Re-running blur on an already-blurred file **double-blurs** and drifts. Write a
`--spec` JSON that reads from the pristine originals every time; iterate on the
spec, not on the output. This makes the redaction reproducible for the next post.

### 5. Verify visually, adjust, repeat
`Read` each output. Check: is every private region actually covered (not just
near-missed)? Is any demonstrative content accidentally blurred? Did the crop
clip anything? Fix the coordinates in the spec and re-run.

## Gotchas
- **Never touch the Photos-library originals.** Copy into `30_Resources/Published/media/` and edit the copy; the source in `~/Pictures/Photos Library.photoslibrary/originals/...` stays pristine.
- **Full-res original beats a derivative.** Photos stores a small `resources/derivatives/*.jpeg` and the real one at `originals/<X>/<UUID>.png` — find and use the original (usually 1290×2796 for an iPhone shot).
- **Alt text should be honest about the blur** — say "figures blurred for privacy" so the caption doesn't claim to show data that's hidden.
- Pillow is an optional extra; the SDK lazy-imports it with an install hint (`pip install 'Pillow>=10'`).

## Cross-references
- `emptyos/sdk/media/image_redact.py` — the pure helper (+ `tests/test_unit_image_redact.py`).
- `eos-screenshot` — the live-capture sibling (DOM-selector blur).
- `eos-article-diagrams` — SVG diagrams for the same posts.
- Memory: `reference-article-visual-tooling` (which tool for which visual).
