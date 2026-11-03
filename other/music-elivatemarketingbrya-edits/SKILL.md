---
name: music
description: >
  Step 6 of the content pipeline, optional. Adds a flat music bed under
  the already-polished dialogue in a single mix pass — no ducking
  automation, no per-segment adjustments. Use only when the user asks
  for background music.
---

# Music (optional)

Skip this entirely unless the user wants a music bed. When they do:

## 1. Get the track

If the user supplies a file, use it. If they need one sourced or
generated, that's `/media-use` (BGM resolution/generation) — come back
here once you have a local audio file.

## 2. Mix it in, once

```bash
.claude/skills/music/scripts/mix_music_bed.sh <job-name> <music-file> [bed_db_below_dialogue]
```

Default is 18dB under the dialogue. This is deliberately a **flat**
bed — one static volume offset for the whole track, mixed once against
whatever the job's furthest-along render is (captioned > graphics >
rough cut). No ducking curve, no per-segment volume automation — those
would violate the "never per-segment audio FX" lock and reintroduce the
click/pump risks that lock exists to avoid. If a scene genuinely needs
the music to duck under a specific line, that's a deliberate creative
call to make with `/hyperframes-audio`'s automation envelopes inside the
HyperFrames composition itself (before this flattening mix), not a patch
applied here.

Writes `outputs/<job>-music.mp4` with dialogue untouched and the mix
re-encoded at AAC 256k (matches, never drops below, the polish pass's
bitrate).

## 3. Continue

Straight to `/export`.
