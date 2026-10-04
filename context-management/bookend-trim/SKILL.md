---
name: bookend-trim
description: Snap each picked segment's [t0, t1] to a sentence boundary so shorts begin and end on full thoughts instead of mid-sentence. Claude reads ±extend seconds of context per span and picks clean sentence-completing endpoints from whisper transcript-line boundaries. Runs after verify-coherence, before cut-clip.
allowed-tools: Bash
user-invocable: true
---

# bookend-trim

Picked segments tend to begin or end mid-sentence because `pick-segments` and
`verify-coherence` choose by topic, not prosody. This skill nudges each span's
`[t0, t1]` to the nearest clean sentence boundary so the resulting short feels
like a complete thought.

## Invoke

```
.claude/skills/bookend-trim/bookend-trim.sh <segments.json> <transcript.json> <out.json> [extend=6.0] [dmin=20]
```

- `segments`: output of `verify-coherence` (or `pick-segments`)
- `transcript`: full-source transcript (whisper output with `segments[]`)
- `out`: same shape as input, with `t0` / `t1` adjusted and a `bookend_note`
- `extend`: max seconds Claude may push outward in either direction (default 6.0)
- `dmin`: min surviving duration; an adjustment that collapses below this is rejected

## How

This project's `transcribe` skill runs whisper.cpp with `--max-len 1
--split-on-word`, which strips punctuation. So a pure
ends-with-`.`/`?`/`!` snap finds nothing and inter-word gaps are also
collapsed. Instead we delegate to Claude:

1. For each span, build a context window: every whisper transcript line
   (`segments[]`, each ~5s of speech) within `±extend` of `[t0, t1]`.
2. Ask Claude (single batched `claude -p` call across all spans) to pick a
   new `t0` that starts at a sentence start and a new `t1` that lands on a
   sentence end. New values must be transcript-line boundaries within the
   window.
3. Cache on input mtimes; out-of-window or too-short adjustments are
   rejected and the original `[t0, t1]` is kept.

Per-span `bookend_note` records `Δt0` / `Δt1` and Claude's reason. Pairs
well with `tighten-pace` downstream, which removes dead air inside the
re-bookended clip.
