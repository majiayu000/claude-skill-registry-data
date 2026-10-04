---
name: watermark
description: Overlay the persistent @C0BALT_CUT channel watermark at the BOTTOM of a finished short — the vertical opposite of source-credit's top banner. Renders the handle as a transparent PNG via PIL (Impact, Platinum #E8ECF1 with the slashed-zero in Sapphire Glow #2E6BFF, semi-transparent); ffmpeg composites it for the whole clip duration. Runs after source-credit and before loudnorm in the per-span chain.
allowed-tools: Bash
user-invocable: true
---

# watermark

Persistent channel branding. "@C0BALT_CUT" in Impact at ~2% of frame
height, Platinum white with the `0` in Sapphire Glow (brand/BRAND.md
palette), thin black stroke, semi-transparent (alpha ≈200) so it reads
without competing with captions. Same renderer pattern as `source-credit`
(PIL PNG, ffmpeg overlay) because the local ffmpeg has no libass/drawtext.

## Invoke

```
.claude/skills/watermark/watermark.sh <input> <out>
```

- `input`: video to overlay onto (any aspect ratio; designed for 1080x1920)
- `out`: output mp4

## Output

mp4, same dimensions and duration as the input, video re-encoded, audio
stream-copied. Cache: skip rebuild when `out` is newer than `input`.
Prints the output path to stdout.

## Geometry

Mark is bottom-anchored at y = 97.5% of frame height, centered
horizontally — for a 1080x1920 short the text baseline sits around
y=1830. Captions live in the lower third (≈y=1344) and the source credit
is a top chyron (y≈77), so the mark collides with neither. The CTA
overlay (last ~4s) composites AFTER this skill in the chain, so it
covers the mark briefly — intended, the CTA is the louder ask.
