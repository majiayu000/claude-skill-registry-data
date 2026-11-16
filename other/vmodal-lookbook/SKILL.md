---
name: vmodal-lookbook
description: >-
  Build a capsule wardrobe and outfit lookbook from a style brief (city, month, temperature, occasion, style), grounded in real street-style footage in VModal: discover what people actually wear in that season, plan 8–12 pieces and 5–7 outfit formulas, then prove each outfit with verified real frames. Use when the user asks to "dress me for", "what to wear in Milan in November", "capsule wardrobe", "lookbook", "packing list" or "outfits for a trip", e.g. "Capsule for Milan in November, 8°C, aperitivo in Brera. Collection: fashion_milan". Requires the vmodal MCP and the vmodal-find skill.
---

# vmodal-lookbook

A stylist that may only recommend what it has **seen** on the street. Every piece cites a
verified frame; every outfit shows real examples or is marked unproven.

This skill builds on **vmodal-find**. Read `<skill_dir>/../vmodal-find/SKILL.md` for the
spec checklist (step 2), scene grouping (step 4), frame verification (steps 5–6) and
PASS / PARTIAL / FAIL verdicts (step 7). Follow those rules exactly. Season map, formula
grammar, budgets and a worked example are in [reference.md](reference.md).
`<skill_dir>` means this SKILL.md's folder.

## 1. Brief

Parse into a brief and show it in one line:

| Field | From | Used for |
|---|---|---|
| collection | user, default `fashion_milan` for Milan | search |
| month / season | "November", "3 days in February" | sub-collection (reference.md map) |
| temperature | "8°C" (guess from month if absent, say so) | layering rules (reference.md) |
| occasions | "aperitivo in Brera", "business", "walking day" | one outfit per occasion at least |
| style words | minimal, classic, bold, colorful… | subjective, orders choices, never a hard fail |
| budget, brands, sizes | | **unverifiable**: listed, never checked |

`Brief: fashion_milan · November → Fall sub-collection · 8°C (layers) · aperitivo, walking · minimal`

`RUN=${TMPDIR:-/tmp}/vmodal-lookbook/<collection>_<yyyymmdd_hhmm>`.

## 2. Discover: what is actually worn

Run 4 parallel `find` calls in the season sub-collection, `limit=20`, phrased as people on
the street (bare garment queries mostly return shop-window mannequins):
`woman wearing a coat or jacket walking on the street` · `woman's shoes walking on the street` ·
`woman carrying a handbag on the street` · `woman wearing a knit sweater on the street`
(winter/fall) or `woman wearing a dress on the street` (summer). Add one call per style word
if given ("woman in a minimal neutral outfit on the street"). Group into scenes; pick the
top 8 scenes across all calls (≤ 2 per video) and verify them as frames (vmodal-find
step 5; download with `image_download_from_records(records=[...], root_folder="$RUN/raw")`).
Mannequin frames don't count as evidence; note them as "in shop windows" only.

Here the check is descriptive: for each frame write the **visible pieces** as
`<color> <material?> <garment>` ("camel wool long coat", "black loafers", "brown suede bag").
A piece seen in ≥ 1 frame becomes a **candidate** with that frame as evidence.
If a trend-radar run exists in this session, its `rising` / `evergreen` items may be added
as candidates with their evidence frames.

## 3. Plan: capsule + formulas

- **Capsule**: 8–12 pieces chosen from candidates only, covering roles
  outer · top · bottom · shoes · bag/accessory, fitting temperature and style.
  A piece with no evidence frame is dropped, never invented.
- **Outfit formulas**: 5–7, grammar `outer + top + bottom + shoes [+ accessory]`
  (reference.md), each using capsule pieces only, ≥ 1 per occasion, and maximize reuse
  (each piece in ≥ 2 outfits where possible).

Show the capsule and formulas in short lists before proving them.

## 4. Prove each outfit

For each formula, in parallel batches:

1. `find` with the full formula as a person ("woman wearing a camel long coat, black
   turtleneck, dark straight jeans and black loafers on the street").
2. `find` with its 2 most distinctive pieces only ("woman in a camel long coat and black
   loafers").

Merge, group, verify the top 6 scenes per formula. Spec checklist = each piece of the
formula as an attribute + "outfit worn by one person" as core. Verdicts:

- **PASS** if ≥ 3 formula pieces are `pass` on the same person and none `fail`
  (shoes / bag cut off by the frame are `unclear`, not `fail`).
- Keep up to **2 PASS examples** per outfit, preferring different videos.
- 0 PASS → widen once (next 6 scenes). Still 0 → **"formula unproven"**: keep the outfit in
  the report, flagged, and offer the closest PARTIAL frame with what differs.

Optional period label per example:
`python <skill_dir>/../vmodal-trend-radar/scripts/fashion_period.py period <filename> <stream>`.

## 5. Save `lookbook.json`

Write `$RUN/lookbook.json` (data contract):

```json
{"brief": {"collection": "fashion_milan", "season": "fall", "month": 11, "temp_c": 8, "occasions": ["aperitivo"], "style": ["minimal"]},
 "pieces": [{"name": "camel long coat", "role": "outer", "color": "camel", "evidence": ["/abs/frame.png"]}],
 "outfits": [{"name": "Brera aperitivo", "occasion": "aperitivo", "pieces": ["camel long coat", "black turtleneck"], "status": "proven|unproven",
   "examples": [{"filename": "...", "stream_name": "...", "time": "9:18", "period": "2025-11", "frame_png": "/abs/frame.png", "checks": "coat ✓ turtleneck ✓ jeans ✓ loafers ?"}]}]}
```

## 6. Report

```markdown
**Brief:** fashion_milan · November (fall) · 8°C · aperitivo, walking · minimal

### Capsule (10 pieces)
| Piece | Role | Seen in | In outfits |
|---|---|---|---|
| camel long coat | outer | NOVEMBER 2025 Milan shopping vlog, 9:18 → /abs/frame.png | 1, 3, 5 |

### Outfits
| # | Outfit | Pieces | Proof | Status |
|---|---|---|---|---|
| 1 | Brera aperitivo | camel coat · black turtleneck · dark jeans · loafers | 2 frames (Nov 2025) | proven |

Viewed 8 discovery + 42 proof scenes. 6/7 outfits proven. Not verifiable: budget, brands. Index v0.
```

Under the table, one sentence per proven outfit describing the real example.
Then write a **lookbook page** as one self-contained HTML file (`$RUN/lookbook.html`): one
card per outfit with name, occasion, piece chips, 1–2 real frames (downscaled JPEG data URIs
≤ 480 px, `sips -Z 480 -s format jpeg` on macOS, else `ffmpeg -i in.png -vf scale=480:-1 out.jpg`),
video + time + checks; an "unproven" badge where relevant; a capsule grid at the top.
Give the user the absolute path to the file. Do not publish it with an Artifact / canvas /
hosted-page tool: this skill must behave the same in Claude Code, Codex and Gemini.
