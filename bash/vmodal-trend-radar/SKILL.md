---
name: vmodal-trend-radar
description: >-
  Measure fashion trends over time in VModal street-style video collections: for each trend item (garment, color, print, accessory) search every season / sub-collection, verify every counted scene on real frames, and build an item × period matrix that says what is rising, fading, stable or evergreen, with proof frames. Use when the user asks "what's trending", "trend radar", "is X rising / fading", "evergreen pieces", or compares seasons or street vs brand, e.g. "Run a Milan trend radar for suede and leopard. Collection: fashion_milan". Requires the vmodal MCP and the vmodal-find skill.
---

# vmodal-trend-radar

Turn search hits into a **verified** trend matrix. A cell counts a scene only if its
frame was viewed and passed. Periods come from a script, never from guessing.

This skill builds on **vmodal-find**. Read `<skill_dir>/../vmodal-find/SKILL.md` for the
spec checklist (step 2), scene grouping (step 4), frame verification (steps 5–6) and
PASS / PARTIAL / FAIL verdicts (step 7). Follow those rules exactly. Batching and stop-rule
wording follow `<skill_dir>/../vmodal-track/SKILL.md`. Default items, budgets and a worked
example are in [reference.md](reference.md). `<skill_dir>` means this SKILL.md's folder.

## 1. Scope

- **Collection** (required; default for Milan requests: `fashion_milan`). Call
  `collection_subcollections_list(collection_name=...)`; the **columns** of the grid are the
  exact sub-collection names (for `fashion_milan`: summer, fall, winter).
- **Optional brand column**: if the user says "street vs brand / runway", add
  `fashion_all` + `fashion_brand_milan` as one extra column.
- **Items**: the user's list, else the default 12 from reference.md. Max 12 per run;
  say so if the user gave more and run the first 12.
- Make a run folder: `RUN=${TMPDIR:-/tmp}/vmodal-trend/<collection>_<yyyymmdd_hhmm>`.

Show one line before searching:
`Radar: 4 items × 3 sub-collections · fashion_milan · budget ≤ 6 scenes per cell`.

## 2. Spec per item

Each item becomes a vmodal-find spec checklist. Keep it the **garment alone + at most one
attribute** ("suede jacket", "leopard print", "burgundy coat"). A trend item's core spec is
the garment/print/color; "on a person in the street" is implied, not a spec.
Colors: be strict (burgundy ≠ red ≠ brown). Prints: the print must cover a garment, not a
shop sign or a bag lining.

Every scene also gets a **source**: `street` (worn by a person) or `window` (mannequin,
shop window, rack). Milan vlogs are full of shop windows, and a bare item query
("suede jacket") mostly returns mannequins. Window scenes are kept, but in their own matrix.

## 3. Search grid (parallel)

For every item × column, run `find(collection_name, sub_collection_name, limit=20)` with
`query_text = "woman wearing a <item> walking on the street"`. This pulls up people
instead of mannequins (in testing, the bare item query returned mostly windows). No `mode` /
`version_id` / `save_images`. Send all calls of one item, or of several items, in **one
parallel batch**. Fetch `offset=20` only for cells that end up with fewer than 6 scenes
after grouping. Add the bare item query only if the user asks for "shop windows" / "retail".

## 4. Group and pick

Group each cell's hits into scenes (vmodal-find step 4). Keep the top **6 scenes per cell**,
and spread them: at most **2 scenes per video** in a cell, so one long vlog cannot fill the
column. Record for each scene `filename`, `stream_name`, first/last `ts_unix_13digits`.

## 5. Verify

For each batch of ≤ 20 representative hits:
`image_download_from_records(records=[...hits as returned...], root_folder="$RUN/raw")`
(older MCP builds: `image_get_url_bulk` → `image_get_bulk_from_urls`) →
`bash <skill_dir>/../vmodal-find/scripts/frames_to_png.sh $RUN/frames <saved_path>...`
→ Read each PNG. `results[i].input_index` maps a frame back to its record. Give each scene
PASS / PARTIAL / FAIL for its item (vmodal-find step 7; second look for `unclear` only),
and its source. Material specs (suede, leather, wool) are often `unclear` at 640 px: say so,
don't guess.

Append one JSON line per verified scene to `$RUN/verdicts.jsonl` (data contract):

```json
{"item": "suede jacket", "stream_name": "...", "filename": "...", "ts_start_ms": 892000, "ts_end_ms": 894000, "verdict": "PASS", "evidence": "brown suede jacket, dark midi skirt, walking", "frame_png": "/abs/path.png", "source": "street"}
```

One frame can serve several items: if a frame viewed for one item clearly shows another
radar item (a burgundy skirt seen while checking suede), you may add a row for that item
too, with the same frame.

Write the file with the Write tool (or append via Edit); don't invent rows for scenes you
didn't view. PARTIAL and FAIL rows matter: they are the denominator.

## 6. Build the matrix

```bash
python <skill_dir>/scripts/trend_matrix.py build $RUN/verdicts.jsonl                  # street (default)
python <skill_dir>/scripts/trend_matrix.py build $RUN/verdicts.jsonl --source window  # if window rows exist
```

Report the street matrix. If window rows exist, add a short "In shop windows" line
(items seen in windows, with counts). Windows showing an item before the street does is
an interesting lead, but say it is a hint, not a measured trend.

It derives each scene's period from its filename (`fashion_period.py`: month + year →
`2025-11`, year only → `2026-winter`, no year → `summer-unknown`), counts PASS / viewed per
cell, labels each item and writes `$RUN/trend_matrix.json`:

| Label | Rule (counted cells = dated, ≥ 4 viewed) |
|---|---|
| evergreen | ≥ 3 counted periods, PASS rate ≥ 0.5 in all |
| rising / fading | ≥ 3 counted periods, fitted rate change first→last > +0.15 / < −0.15 |
| stable | ≥ 3 counted periods, otherwise |
| insufficient | fewer than 3 counted periods: **no trend claim** |

Never override a label by eye. If many items are `insufficient`, say the collection is too
thin in time for those items, and offer a deeper run (more pages, 8 scenes per cell).

## 7. Report

```markdown
**Radar:** fashion_milan · 4 items × 3 sub-collections · 72 scenes viewed

| Item | 2025-02 | 2025-11 | 2025-12 | 2026-02 | Trend |
|---|---|---|---|---|---|
| suede jacket | 1/4 | 2/4 | 3/5 | 4/4 | rising |

### Rising
- **suede jacket**: 25% → 100% of checked scenes. Proof: <video>, 0:58 → /abs/frame.png — "tan suede bomber over a white tee"
### Fading / Evergreen / Stable
...
Cells are PASS/viewed scenes, a share of what search surfaced, not a census of the street.
Viewed 72 scenes (40 PASS). Periods from filenames; undated: summer-unknown. Index v0.
```

- Paste the table from `trend_matrix.py md $RUN/trend_matrix.json`.
- One proof frame per labeled item (from `evidence`), with a one-line description.
- Always state the caveat line and the footer.

## 8. Heatmap page (when the user wants a page, or by default for ≥ 6 items)

Write one self-contained HTML file to `$RUN/trend_radar.html` from `trend_matrix.json`:
heatmap grid (rows = items, columns = periods, color = PASS rate, cell text `pass/viewed`,
hatch for `viewed < 4`), a trend badge per row, and a click-to-open evidence strip with up to
3 frames per cell. Embed frames as downscaled JPEG data URIs (≤ 480 px wide,
`sips -Z 480 -s format jpeg` on macOS, else `ffmpeg -i in.png -vf scale=480:-1 out.jpg`),
at most 60 frames. Give the user the absolute path to the file.

Do not publish it with an Artifact / canvas / hosted-page tool, even if one is available:
this skill must behave the same in Claude Code, Codex and Gemini, which have no such tool.
