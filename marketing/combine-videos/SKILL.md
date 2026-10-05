---
name: combine-videos
description: Combine supplied clips into one ordered video with intentional trims, transitions and audio handling; do not regenerate footage.
---
# Combine Videos

## Catalog

- Display name: Combine Videos
- Categories: Video
- Status: Ready
- Route label: Deterministic timeline assembly
- Tone: blue
- Short description: Combine supplied clips into one ordered video with intentional trims, transitions and audio handling; do not regenerate footage.

- Similar skills: edit-social-video, make-beat-synced-video, make-music-video
## What this skill does

- Builds one timeline from multiple clips with explicit order and cut points.
- Preserves source pixels between edits and applies only requested transitions and audio rules.

## How to use

Provide clips, order or narrative goal, runtime, ratio, transitions and audio policy.

#### Example

```text
Combine these three supplied clips in upload order; trim dead starts, use straight cuts, normalize to 16:9, keep audio.
```

## Workflow

1. Probe each clip for duration, frame rate, dimensions, audio and rotation.
2. Create an edit decision list with in/out points, order, transitions and audio treatment.
3. Assemble deterministically; generative models may create inserts but never replace requested clips.
4. Review export for order, cut frames, sync, aspect, black frames, peaks and duration.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: All requested source clips in one verified timeline
- Default layout: User-requested delivery format
- Model policy: Deterministic timeline assembly
- Downstream use: Basic editorial assembly
