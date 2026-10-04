---
name: broll-composite
description: Hard-cut full-frame B-roll cutaways onto a 1080x1920 clip per broll_plan.json. During each [t0,t1] the entire frame is replaced by the cutaway (instant in/out, no crossfade/zoom); 16:9 source is scale-to-cover + SUBJECT-cropped to 1080x1920 with no bars — the slack-axis offset is chosen subject-first (MediaPipe face -> pose person -> thresholded multi-frame saliency, reusing fill-vertical's engine), so the crop sits on the actual subject instead of drifting to background texture. No transition SFX by default (BROLL_SFX=1 re-enables a short synthesized whoosh on each cutaway in/out); the podcast audio stays continuous underneath (amix'd, never replaced). Zero valid picks -> passthrough copy. Pure ffmpeg.
allowed-tools: Bash
user-invocable: true
---

# broll-composite

Applies the cutaways chosen by broll-pick. For each pick `[t0,t1]` the whole
1080×1920 frame is replaced by the B-roll (hard cut, no transition). The 16:9
source is scaled to COVER and SUBJECT-cropped to 1080×1920 — full-bleed, never
letterboxed (same philosophy as fill-vertical). The crop offset on the slack
axis follows the cutaway's subject (a face if present, else a person, else the
thresholded multi-frame saliency mass), so the subject reads centered instead of
sliced off to one side. The podcast audio stays
continuous for the whole clip; B-roll audio is dropped. No transition SFX by
default — audio stays pure stream-copy. `BROLL_SFX=1` re-enables a 0.3s
synthesized whoosh (make_whoosh.py, ~-15dBFS under speech) that sweeps up into
each cutaway and down out of it. Runs BEFORE
burn-subtitles so karaoke captions render on top of the cutaways.

## Invoke

```
.claude/skills/broll-composite/broll-composite.sh <in_clip.mp4> <broll_plan.json> <out.mp4>
```

- `in_clip`: the vertical 1080×1920 clip (from fill-vertical)
- `broll_plan.json`: from broll-pick
- `out`: composited clip

## Behavior

- Zero picks, or every `clip_path` missing → copy-passthrough, exit 0.
- A pick whose `clip_path` no longer exists is skipped; remaining picks apply.
- ffmpeg failure → falls back to passthrough (never blocks the pipeline).

## Idempotency

Caches on in_clip+plan mtimes + BROLL_SFX via `<out>.compmeta`.

## Notes

- Subject-cover crop reuses fill-vertical's framing engine (`build_filter.py`
  imports `fill_vertical` for face/pose detection): per cutaway it samples 5
  frames and picks the slack-axis offset face -> person -> thresholded
  multi-frame saliency. Still COVER (no extra punch-in) — only WHERE the crop
  sits changes. Degrades to a centered crop when MediaPipe/cv2 are unavailable.
- Whole video is re-encoded (overlay can't partial stream-copy); audio is
  amix'd with the whoosh bed to AAC 192k (or `-c:a copy` when BROLL_SFX=0 /
  no picks). Uses `_lib/encode.sh` (VideoToolbox/x264) + thread caps.
