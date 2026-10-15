---
name: sam2-cutouts
description:
  How to drive the object_cutout tool (Meta SAM 2 video on Replicate) to isolate and
  track a subject into a transparent alpha cutout. Use when cutting out a person or
  object from a clip to overlay, keyframe, or restyle separately — the OpenNolan
  equivalent of Instagram Edits' "Cutouts". Covers click-prompt design, multi-object
  tracking, fixing tracking drift, mask types, and cost/caching.
license: MIT
metadata:
  author: opennolan
  version: '1.0.0'
---

# SAM 2 Cutouts (object_cutout)

`object_cutout` wraps Meta's official `meta/sam-2-video` model on Replicate, then
composites the returned mask into a transparent RGBA `.mov` with FFmpeg. The result is a
tracked subject on a transparent background you can layer, keyframe (Wave 2), or restyle
(Wave 5) independently.

## Mental model

SAM 2 does not guess what to cut out. You point at the object with **clicks**, and it
tracks that object across every frame. There is **no auto mode** here — if you do not
provide a click, the tool fails loudly rather than cut out the wrong subject.

Each click is `{x, y, label, frame, object_id}`:
- `x, y` — pixel location in the frame.
- `label` — `1` = "this IS the object" (positive), `0` = "this is NOT the object"
  (negative, used to carve away a wrong region).
- `frame` — which frame the click refers to (usually `0`, the first frame).
- `object_id` — group clicks into objects. Same id = same object; different ids = separate
  tracked objects, each gets its own mask.

## Writing good prompts

- **Start with one positive click in the center of mass** of the subject on frame 0.
- **Add negative clicks** (`label: 0`) on background that bleeds into the mask (e.g. a wall
  behind the head, a hand you don't want).
- **Multi-object:** give each object its own `object_id` and at least one positive click.
  Example: cut out two people →
  `[{x:200,y:300,label:1,object_id:"left"},{x:900,y:320,label:1,object_id:"right"}]`.
- **Pick the frame where the object is clearest.** If the subject enters at frame 30, click
  on frame 30 (`frame: 30`), not frame 0 where it isn't visible.

## Fixing tracking drift

If the mask wanders off the subject partway through the clip:
1. Find the frame where it breaks.
2. Add a positive click on the subject at that frame, and a negative click on whatever it
   wrongly grabbed.
3. Re-run. More, well-placed clicks beats more runs.

## mask_type

- `binary` (default, **required for a transparent cutout**) — white subject on black; the
  tool alphamerges this into the RGBA `.mov`.
- `highlighted` / `greenscreen` — debugging/preview only. The tool will NOT produce an
  alpha clip for these; it returns the raw mask video and warns you. Use `binary` unless
  you specifically want to eyeball the mask.

## Cost, caching, confirmation

- A fresh run calls a **paid** Replicate model and takes ~30s+. The tool **requires
  `confirm: true`** (or `OBJECT_CUTOUT_AUTOCONFIRM=1` for headless pipelines) before it
  spends anything. Announce the cost to the user first.
- Results are **cached by (video + exact clicks + mask_type)**. Re-running an identical
  request is free and instant — so iterate on clicks freely; only changed prompts re-pay.
- Inputs over 1080p are auto-downscaled before upload (Replicate video models stall above
  that). The cutout is composited back at the source resolution via `scale2ref`.

## When NOT to use this

- **A single still image** → use `bg_remove` (rembg), not this. SAM 2 video is for clips.
- **No usable click point / can't identify the subject** → don't force it.
- **bg_remove is NOT a silent fallback.** If SAM 2 is unavailable (no token), `object_cutout`
  fails and *names* `bg_remove` as a person-only, no-tracking alternative. Switching to it is
  an explicit decision — confirm with the user; it will not track an object across frames.

## Output

`ToolResult.data` carries `cutout_path` (the RGBA `.mov`), `mask_path` (raw mask video),
`object_ids`, and `cache_hit`. The cutout's transparent background lets the edit stage place
it as an `overlays[]` layer and animate it with `overlays[].keyframes` (Wave 2).
