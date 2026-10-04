---
name: tighten-pace
description: Remove dead air from a clip by collapsing any inter-word gap > gap_max (default 0.18s). Gaps collapse to collapse_to (default 0.08s), or sentence_beat (default 0.15s) when the preceding word ends with . ? or !. Re-emits the clip and a re-timed transcript so downstream subtitle / chunk / title skills align. Use right after cut-clip + rebase to keep pacing punchy.
allowed-tools: Bash
user-invocable: true
---

# tighten-pace

Podcast clips die on dead air. This skill walks a word-timed transcript,
finds any silence longer than `gap_max`, and collapses that silence to a
short floor — either `collapse_to` (mid-sentence) or `sentence_beat` (after
a `.`, `?`, or `!` so a beat is preserved between thoughts). Output is a
new clip plus a transcript whose timestamps reflect the tightened timeline,
so chunk-captions, burn-subtitles, and title-transition all align correctly.

## Invoke

```
.claude/skills/tighten-pace/tighten-pace.sh <input_clip> <input_transcript> <out_clip> <out_transcript> [gap_max=0.18] [sentence_beat=0.15] [collapse_to=0.08]
```

- `input_clip` — clip-local mp4 (post cut-clip + rebase)
- `input_transcript` — clip-local word-timed transcript JSON
- `out_clip` — written mp4 with silences collapsed
- `out_transcript` — written transcript JSON with shifted t0/t1
- `gap_max` — silence threshold in seconds; only gaps strictly greater are collapsed
- `sentence_beat` — target gap (sec) at sentence boundaries
- `collapse_to` — target gap (sec) elsewhere

Env overrides: `TIGHTEN_GAP`, `TIGHTEN_SENTENCE_BEAT`, `TIGHTEN_COLLAPSE_TO`.

## How

`plan.py` walks word pairs. When `nxt.t0 - prev.t1 > gap_max`, the kept
ranges are split: the previous range ends at `prev.t1 + target/2` and the
next starts at `nxt.t0 - target/2`, so the residual silence after ffmpeg
`select`+`aselect` is exactly `target` seconds. `target` is `sentence_beat`
when `prev.w` ends with `.`, `?`, or `!`; otherwise `collapse_to`.

## Caveats

- Always re-encodes (select filter cannot stream-copy).
- Idempotent via `<out>.tpmeta` (input + transcript mtimes + all three params).
- If the transcript has fewer than 2 words, the input is copied through.
