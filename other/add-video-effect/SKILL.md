---
name: add-video-effect
description: Add one specified visual effect to supplied video at a defined time and region while preserving the underlying footage. Use for localized glow, particles, weather, light, impact, or transition effects; do not use for whole-video restyling, color correction, footage assembly, or removing overlays.
---
# Add Video Effect

## Catalog

- Display name: Add Video Effect
- Categories: Video
- Status: Ready
- Route label: MiniMax H3 localized video edit
- Tone: pink
- Short description: Add one specified effect to a supplied video at a defined time and region while preserving underlying footage.

- Similar skills: correct-video-color, restyle-video, upscale-video
## What this skill does

- Adds a bounded effect such as glow, particles, flare, weather or speed treatment.
- Anchors timing, target, duration and interaction so the effect does not become a full restyle.

## How to use

Provide video, exact effect, target, start and end time, intensity and protected content.

#### Example

```text
Add a subtle golden particle trail behind the skateboard from 00:02–00:04; preserve rider, board and camera.
```

## Workflow

1. Locate effect interval, tracked target, occlusions and protected regions.
2. Specify onset, evolution, interaction, intensity and exit as one bounded effect.
3. Run MiniMax H3, the cataloged source-video editing model, with bounded temporal and regional instructions.
4. Inspect frames before, during and after for tracking, spill, timing and preservation.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The source clip with one time-bounded visual effect
- Default layout: User-requested delivery format
- Model policy: MiniMax H3 for source-video editing; stop when the required tracking/edit contract is unavailable
- Downstream use: Creative post-production
