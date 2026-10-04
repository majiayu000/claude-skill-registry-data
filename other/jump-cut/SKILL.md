---
name: jump-cut
description: Manufacture "multi-cam" hard cuts on static talking-head stretches by alternating a base framing with tighter punch-in reframings of the SAME speaker, each cut snapped to a word start so it lands on speech. Deterministic, no Claude. Timeline-preserving — audio is copied untouched and total duration is identical, so every downstream timestamp (captions, b-roll windows) stays valid. Runs on the 1080x1920 vertical clip AFTER fill-vertical and BEFORE zoom-punch/broll/burn-subtitles, so cutaways override their own windows and captions burn on top. The visual-change-density lever for sources where b-roll stays sparse.
allowed-tools: Bash
user-invocable: true
---

# jump-cut

Single-camera podcast footage reads as one long static crop between cutaways.
Top short-form editors break that up with frequent hard cuts between framings of
the same speaker — a fake "multi-cam" rhythm that keeps the frame changing even
with no new footage. This skill manufactures that churn deterministically.

## Invoke

```
.claude/skills/jump-cut/jump-cut.sh <in.mp4> <transcript.json> <out.mp4> [seg_secs=3.2]
```

- `in.mp4`: the 1080x1920 vertical clip (post fill-vertical)
- `transcript.json`: the clip-local word-timed transcript (cuts snap to word starts)
- `seg_secs`: target segment length / cut rhythm (default 3.2s)

## How it works

- `plan.py` tiles `[0, dur]` into segments at ~`seg_secs` spacing, each boundary
  snapped to the nearest word start within 0.7s so the cut lands ON speech.
- Segments alternate **base** (full frame, unchanged) and **punch** (a centered
  ~1.11–1.16x reframe biased to the upper third). The cold-open lead (2.6s, the
  title) and the tail (1.5s, the landing) stay base for a stable open/close.
- One ffmpeg pass: `split` → per-segment `trim`+`crop`/`scale` → `concat`. Video
  is concatenated; **audio is mapped straight from the source with `-c:a copy`**,
  so duration and every downstream timestamp are preserved exactly.

## Placement rules

- count = clamp by `seg_secs` rhythm, capped at `JUMP_CUT_MAX` (default 8) cuts
- clips shorter than `JUMP_CUT_MIN` (default 13s) → passthrough (no churn)
- first 2.6s (cold-open title) and last 1.5s excluded
- min 1.6s between cuts after snapping (never seasick)

## Pipeline order

`fill-vertical` → **`jump-cut`** → `zoom-punch` → `chunk-captions` → `broll-pick`
→ `broll-composite` → `burn-subtitles` → …

It must touch only the clean vertical: b-roll cutaways replace the full frame in
their windows (overriding the reframe underneath) and captions burn on top, so
neither warps. Non-fatal (any failure → passthrough), idempotent (`.jcmeta`
mtime+param signature), `JUMP_CUT=0` disables.

## Env

- `JUMP_CUT` — `0` disables (passthrough). Default on.
- `JUMP_CUT_SEG` — cut rhythm in seconds (default 3.2; also positional arg 4).
- `JUMP_CUT_MAX` — max reframe cuts per clip (default 8).
- `JUMP_CUT_MIN` — min clip duration to activate (default 13.0s).
- `JUMP_CUT_LEAD` / `JUMP_CUT_TAIL` — stable open/close reserve (default 2.6 / 1.5).
