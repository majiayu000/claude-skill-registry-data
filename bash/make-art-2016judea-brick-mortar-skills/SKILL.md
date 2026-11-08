---
name: make-art
description: Generate original AI art / images (backgrounds, plates, illustrations, wallpapers, composites) via Google's Gemini "Nano Banana Pro" image API, with a zero-dependency Python wrapper. Use whenever you want to create, generate, or edit an image/plate/background/wallpaper/illustration, or compose art around an existing image. NOT for charts/dataviz.
---

# make-art — a working AI-image engine

The engine is **Nano Banana Pro = Gemini 3 Pro Image** (`gemini-3-pro-image-preview`) via
the Gemini REST API. A zero-dependency, stdlib-only wrapper lives at `scripts/gen_art.py`.
It reads `GEMINI_API_KEY` from the environment, or from `./.env` (override the path with
`GEMINI_ENV_FILE`). Native output up to 4K, ~35s per image, ~$0.24 per 4K image.
**Billed, no free tier** — a busy week of plates can run into three figures, so put a
budget cap on the Google Cloud project. Use 2K for drafts and keep 4K for finals.

**Delivery:** a folder per job (e.g. `art/<slug>/`, finals numbered by rank, a README with
prompts and cost). Keep generated art out of a personal photo library unless asked.

## Two hard gotchas
1. **Network must be allowed.** If your agent runs shell commands in a sandbox that blocks
   DNS/network, the API call fails; run `gen_art.py` with network access.
2. **Bake text in HTML/PIL, not the prompt.** The model renders text unreliably. Generate a
   *text-free* image, then overlay type yourself (HTML->screenshot, or PIL) so it stays
   crisp. Always add "no text, no lettering" to prompts meant to carry an overlay.

## Usage
```bash
python3 scripts/gen_art.py --prompt "..." --out plate.png --aspect 3:2 --size 4K
python3 scripts/gen_art.py --prompt-file p.txt --out plate.png --aspect 9:16 --size 4K
python3 scripts/gen_art.py --image base.png --prompt "..." --out out.png   # anchor/edit around a base image (repeatable --image)
```
- `--aspect`: `1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9`. Phone wallpaper -> `9:16`; magazine spread -> `3:2`; single page -> `3:4`.
- `--size`: `1K` / `2K` / `4K` (uppercase). `4K` for print/wallpaper; `2K` to save cost on drafts.
- Returns a JPEG or PNG (check the printed mime). For wallpaper, cover-crop to the exact device size afterward.

## When the base image is a paste, not a file

`--image` needs a path, but an image pasted into a Claude Code conversation **is not on
disk**: it lives only as base64 in the session transcript. Extract it:

```python
import json, base64, pathlib
p = pathlib.Path.home() / ".claude/projects/<slug>/<sessionId>.jsonl"   # slug = cwd with / -> -
for line in p.open():
    for blk in (json.loads(line).get("message") or {}).get("content") or []:
        if isinstance(blk, dict) and blk.get("type") == "image":
            src = blk["source"]
            pathlib.Path("base.jpg").write_bytes(base64.b64decode(src["data"]))
```

Look at the extracted file before spending a 4K gen on it. See `claude-usage-mining` for
the transcript layout.

## Prompt craft
- Name the medium + palette up front and keep it consistent across a set. Two styles
  that work well: *"35mm film photograph, visible film grain, muted sun-faded palette of ochre
  and dusty blue, soft natural light, analog imperfection, contemplative, vertical."* and,
  for print plates, *bone paper, near-black ink, a single hot-orange accent, risograph
  texture, flat full-bleed*.
- For overlay-friendly backgrounds: ask for **deep negative space** where the text will sit,
  dark/low-contrast zones, and a single light source / light-leak for interest.
- Vary a pool by shifting time-of-day, weather, motif (sea, dunes, fog, rain, night stars,
  double-exposure, abstract light field) while holding the palette.
- **Full-bleed warning:** the model likes to add a light "paper/riso frame" border
  (especially when you say "poster", "risograph", or "paper texture"). For edge-to-edge
  art, omit those words or trim the border afterward.
  **Don't trim on a visual hunch — probe it.** Measure the run inward from all four edges.
  A real frame is *uniform* on all four sides; wildly asymmetric runs (166px bottom on one
  plate, 720px right on another) are *art* — cloud, snow, sky — legitimately hitting the
  bleed, and cropping it destroys the composition.
  **Probe luminance, not whiteness — the frame is not always pale.** A near-white test is
  blind to the dark "slide mount" border the model also likes. Threshold on
  `0.299R+0.587G+0.114B` at both ends (`<42` and `>238`), sample three lines per edge and
  take the **median** so a patch of legitimate art-black doesn't fool one scanline, then
  apply the uniform-vs-asymmetric test:

  ```
  plate-A      DARK run  L132  R1264  T0   B848   asymmetric -> art (crushed shade)
  plate-B      DARK run  L97   R83    T84  B86    UNIFORM    -> real frame, crop it
  ```

  Crop the **max plus clearance** for corner rounding (150px worked), then restore the
  aspect ratio. TAIL negatives like *"no border, no frame, no film strip, no sprocket
  holes, no white margin"* do **not** reliably prevent the dark mount; the model seems to
  read those as being about pale borders only.

## "One small accent" needs a named carrier

A STEM saying *"one small safety-orange accent"* can hold on four plates and fail on the
fifth when the subject contains large repeated shapes: the engine paints every one of
them orange. Name the carrier and forbid the rest: *"the only orange in the whole image is
a small stripe on the side of each robot; chutes, deck and openings are slate blue and
warm grey."* When a subject has big repeated geometry, "small accent" is not a constraint.

## An edit pass cannot RESIZE a repeated object — rewrite the SUBJECT and roll

Asked via `--image` to "keep everything, only make every unit tall", the engine kept the
flat units and ADDED tall towers beside them. Edit passes are reliable for recolour and
remove; they are not reliable for changing the proportions of many instances or inserting
a stage into a sequence. Put the corrected geometry into the SUBJECT and regenerate.

## See also

`image-riff` — the TASK method on this engine: turning a reference image into a spread of
original plates (invariant STEM / varying SUBJECT / invariant TAIL, vantages, honest
ranking, destination crops). `brand-direction-plates` — several visual languages across
one brand.
