---
name: burn-subtitles
description: Burn karaoke-style word-timed subtitles into a video. Takes a transcript JSON with word timestamps and a video, emits a new video with subtitles rendered in. Renders text as a PNG overlay sequence (the local ffmpeg build has no libass/drawtext).
allowed-tools: Bash
user-invocable: true
---

# burn-subtitles

Word-timed subtitle burn-in for shorts. Highlights the current word, no manual sync.

## Invoke

```
.claude/skills/burn-subtitles/burn-subtitles.sh <input> <transcript.json> <out> [style] [font_size]
```

- `input`: video path
- `transcript`: path to JSON. For `style=chunks` (default) this is a `chunks.json` from the `chunk-captions` skill. For other styles it's a `transcribe` output JSON.
- `out`: output video path
- `style` (optional): `chunks` (default) | `line` | `word-karaoke` | `selective`
- `font_size` (optional): default `72`

## Output

mp4 with subtitles burned in. Same dimensions, audio stream-copied. Prints the
output path to stdout. Idempotent: skips work if `out` is newer than both inputs.

## Styles

- `chunks` (default): consumes a `chunks.json` from the `chunk-captions`
  skill. Each chunk is shown as a complete phrase for its `[t0, t1]` window;
  the currently-spoken word is rendered cyan, all other words white. Chunks
  hard-cut between each other — no scrolling, no fade. Kills the per-word
  slide-up that made the legacy `word-karaoke` style hard to read.
- `line`: one plain line per transcript segment.
- `word-karaoke` (legacy): rolling window of up to 4 words, tied to word
  timestamps. Each word slides up 8px over 80ms at its own `t0` and hard-cuts
  off when bumped or after a >0.6s speech gap. Deprecated for shorts —
  feedback showed the constant scroll was hard to follow.
- `selective`: only burns segments overlapping high-RMS-energy seconds.

## Brand preset (deliberate, not default)

This is the project's caption identity — keep it consistent:

- **Font**: Impact (`/System/Library/Fonts/Supplemental/Impact.ttf`) — chunky
  condensed sans, distinct from the CapCut/Submagic/Opus default of Arial.
- **Accent (active word)**: Sapphire Glow `#2E6BFF` — the C0BALT CUT brand
  accent (brand/BRAND.md), chosen against the ubiquitous MrBeast-yellow
  `#FFD633`.
- **Context (earlier visible words)**: off-white `#F5F5F0`.
- **Position**: upper-third (top of first line at ~22% of frame height) — not
  the default lower-third.
- **Animation**: 8px slide-up over 80ms (linear) on entry; hard-cut on exit.
  No ease-out-back pop, no scale animation.
- **Stroke**: thick black outline (font_size / 10), for legibility over any
  background without falling back to white-on-black bars.

## How

The local ffmpeg build ships without `libass`, `subtitles`, or `drawtext`
filters. So `burn_subtitles.py` renders a transparent PNG per video frame with
PIL using the brand preset above, hardlinking duplicate frames for speed.
`burn-subtitles.sh` then composites the sequence onto the source with ffmpeg's
`overlay` filter and re-encodes video (libx264 veryfast crf18); audio is copied.

## Status

Works. Tested on a 6.7s 720x1280 clip (say-synthesized speech, 19 words):
- word-karaoke: 20 unique states, frame at t=3.2s shows 16130 white + 5616
  accent (highlighted-word) pixels in the lower third.
- line: 27049 white pixels, 0 accent. Dimensions and duration preserved,
  audio stream-copied (aac).
