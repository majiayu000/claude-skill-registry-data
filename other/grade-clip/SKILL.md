---
name: grade-clip
description: Per-clip upload-readiness grade (0-99) read off a FINISHED .mp4 plus its persisted sidecar plans — the first skill that inspects a delivered pixel-level artifact, the on-disk proxy for YouTube's VVSA swipe gate. Deterministic retention-proxy floor (frame1_is_face, letterbox_bars, credit_lit_at_open, first_visual_change, first_payoff_offset, longest_static_gap, opening_caption_words, max_residual_silence, terminal_loop_score) with hard caps (letterbox / face_withheld / credit_at_open / blocking_card / dead_tail) that cap grade≤40, plus ONE batched Claude rubric call (hook↔payoff / open-loop / cold-context) skipped when GRADE_SKIP_CLAUDE=1. Runs at the END of the per-span chain (after save-local) AND standalone over the whole output/ backlog (--backlog → output/_triage.json). Emits clip_NN.grade.json per the locked SELECTION-SUITE-CONTRACT schema. Idempotent (.gcmeta), non-fatal (any error → DROSS/empty, exit 0).
allowed-tools: Bash
user-invocable: true
---

# grade-clip

The keystone of the selection/repair/drip suite. The pipeline today is
open-loop and produce-only — `qc-clip` checks only duration/size, `visual-cadence`
is one diagnostic. Nothing ever inspects a *delivered pixel-level artifact* for
upload-readiness. `grade-clip` is that gate: the on-disk translation of YouTube's
un-exportable VVSA ("viewed vs swiped away") front-gate, scored 0-99 off the
finished `.mp4` and its persisted sidecar plans.

```
grade-clip.sh <clip.mp4>                       # single / in-chain (after save-local)
grade-clip.sh --backlog [output_dir=output]    # sweep output/<src>/*.mp4 + _triage.json
```

## Output — `clip_NN.grade.json` (locked SELECTION-SUITE-CONTRACT schema)

```json
{
  "clip": "output/<src>/<title>.mp4",
  "grade": 0,
  "tier": "GOLD|FIXABLE|DROSS",
  "hard_caps": ["letterbox","face_withheld","credit_at_open","blocking_card","dead_tail"],
  "signals": { "frame1_is_face": true, "letterbox_bars": false, "credit_lit_at_open": false,
               "first_visual_change_sec": 1.2, "first_payoff_offset": 2.4,
               "longest_static_gap": 3.1, "opening_caption_words": 5,
               "max_residual_silence": 0.4, "terminal_loop_score": 0.37,
               "claude": {"hook_payoff":7,"open_loop":6,"cold_context":8} },
  "fix_routes": ["broll_open_truncate","shot0_repunch","credit_rerender"],
  "source": "<source-slug>"
}
```

## Algorithm — deterministic retention-proxy floor (no model)

- **`frame1_is_face`** — decode frame 0, MediaPipe face detection (reuses
  fill-vertical's `face_landmarker.task`); TRUE if a face spans >~2% of frame
  area. If `.vert.fillplan.json` is present, factor `shots[0].kind != "face"` as
  the face-withheld signal. `face_withheld` hard-cap fires when no face in frame0
  (or fillplan shot0 kind != face). Policy is A/B-able via `GRADE_FACE_OPEN`:
  `face` (default, legacy) keeps the hard cap; `broll` inverts it (opening ON a
  talking head takes a soft -8 penalty, no cap, no `broll_open_truncate` route —
  the 2026-07-07 perf-style analysis found opens_on_face ranked -0.94 against
  likes/1k); `off` disables the frame1 judgment entirely.
- **`letterbox_bars`** — sample top/bottom + left/right edge bands; flag a
  near-constant / very-low-variance band (black bars / blurred pillarbox). A
  correct full-bleed punch-in has high variance everywhere. `letterbox` hard-cap
  (structural → `rerun_recommended`).
- **`credit_lit_at_open`** — edge density in the top ~12% banner at t≈0.6s; flag
  a dense text strip in the first ~1s (the source credit should appear only in
  the final `CREDIT_TAIL`). Approximate. `credit_at_open` hard-cap → `credit_rerender`.
- **`first_visual_change_sec`** — in-chain: min over (first broll pick t0, first
  caption swap = chunk0 t1); backlog: first ffmpeg scene-detect change. null if none.
- **`first_payoff_offset`** — in-chain: lexical-overlap match of the title's key
  noun/verb against `.chunks.json` → t0 of the best-matching chunk; backlog: null.
- **`longest_static_gap`** — read `.cadence.json` `max_gap`; backlog: compute via
  scene-detect (visual-cadence logic).
- **`opening_caption_words`** — word count of chunk0 within the swipe window; backlog: null.
- **`max_residual_silence`** — longest `ffmpeg silencedetect` silence (sec).
- **`terminal_loop_score`** — frame0 vs last-frame normalized-histogram
  correlation → 0-1 (the >100%-retention loop lever).
- **`dead_tail` hard-cap** — trailing silence in the last ~1.5s AND a static
  final ~1s (low frame delta) → `dead_tail` (no clean fix route on its own).

**Hard caps** (`letterbox`, `face_withheld`, `credit_at_open`, `blocking_card`,
`dead_tail`) any present → grade clamped ≤40. Each maps to a `fix_routes` entry:
`letterbox → rerun_recommended`, `face_withheld → shot0_repunch`,
`credit_at_open → credit_rerender`, `blocking_card → card_rerender`. A
`broll_plan.picks` window overlapping `[0, GRADE_OPEN_GUARD_SEC]` adds
`broll_open_truncate` (only under `GRADE_FACE_OPEN=face`).

**Grade formula** (explicit + commented in `grade.py`): start near 99, subtract
documented penalties for the soft signals (large static gap, late/None
first_payoff_offset, high residual silence, weak terminal-loop, too-few opening
caption words, no visual change before 3s), then apply the Claude rubric (when
present), THEN clamp ≤40 if any hard cap.

**`tier`**: GOLD = grade ≥ `GRADE_MIN_UPLOAD` (60) & no hard caps; FIXABLE = has
hard caps but ALL map to a non-`rerun_recommended` route; DROSS otherwise.

## Algorithm — one batched Claude call (the only model use)

When `GRADE_SKIP_CLAUDE` is unset/0 AND a transcript is available, ONE
`run_claude_step` call rates hook↔payoff coherence + open-loop strength +
cold-viewer context, each 0-10, on the opening transcript (first ~10s) + title
(`build_prompt.py` → `run_claude_step` → `parse_reply.py`, neutral-5 fallback on
unparseable reply). Result lands under `signals.claude`. `GRADE_SKIP_CLAUDE=1`
skips entirely. **Backlog mode defaults proxy-only** — it does NOT call Claude
unless `GRADE_SKIP_CLAUDE=0` is explicitly set.

## Backlog triage

`--backlog` sweeps every `output/<src>/*.mp4` (skips `_preview/`, `source/`,
`_toupload/`), writes `<clip>.grade.json` next to each, and an aggregate
`output/_triage.json` = `{generated, n, gold:[...], fixable:[{clip,defect}],
dross:[{clip,reason}], by_source:{...}}`. Finished output clips usually have NO
co-located sidecars, so backlog mode is PROXY-ONLY by direct pixel/ffprobe reads.

## Knobs

`GRADE_MIN_UPLOAD` (default 60), `GRADE_SKIP_CLAUDE` (1 = proxy-only; backlog
default), `GRADE_OPEN_GUARD_SEC` (2.2), `GRADE_FIRST_CHANGE_SEC` (3.0),
`GRADE_PAYOFF_SEC` (3.0), `GRADE_STATIC_GAP_SEC` (5.0), `GRADE_SILENCE_SEC` (0.8),
`GRADE_MIN_CAPTION_WORDS` (3), `GRADE_SILENCE_DB` (-30dB), `GRADE_SCENE` (0.3).

Idempotent — mtime+param `.gcmeta` signature over the clip + every sidecar that
exists. Non-fatal — any error emits a DROSS/empty verdict and exits 0; it never
hard-fails the pipeline.
