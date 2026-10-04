---
name: cut-filler
description: Apply a trim-filler keeps.json to a clip's video. Reads the kept time ranges and re-encodes the clip with ffmpeg select/aselect so kept ranges are concatenated and removed spans (filler, trail-offs, digressions) disappear. Output aligns with the trimmed transcript trim-filler wrote, so downstream subtitle / caption / title skills stay in sync.
allowed-tools: Bash
user-invocable: true
---

# cut-filler

Video-side companion to `trim-filler`. Takes the clip-local `keeps.json` (a list of `[t0, t1]` ranges to keep) plus the input clip, and re-encodes a new clip containing only the kept ranges, concatenated in order.

## Invoke

```
.claude/skills/cut-filler/cut-filler.sh <in_clip> <keeps.json> <out_clip>
```

- `in_clip` — clip-local mp4 (post `cut-clip + rebase`, pre `tighten-pace`)
- `keeps.json` — emitted by `trim-filler`
- `out_clip` — written mp4 with filler ranges removed

## How

Builds a single `select` / `aselect` filter expression over the keep ranges and re-encodes once with libx264 + AAC. If `keeps` covers the entire clip (nothing to cut), the input is copied through unchanged.

Idempotent via `<out>.cfmeta` (clip mtime + keeps mtime).

## Pairs with

- `trim-filler` — produces the `keeps.json` this skill consumes.

## Caveats

- Always re-encodes (ffmpeg `select` cannot stream-copy).
- The trimmed transcript is written by `trim-filler`, not by this skill — downstream skills consume it directly.
