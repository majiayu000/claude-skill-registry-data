---
name: animate-image
description: Animate one supplied still into a short video with bounded subject and camera motion while preserving identity and composition. Use for image-to-video motion from a specific source frame; do not use for text-only video generation, talking portraits, full video restyling, or clip editing.
---
# Animate Image

## Catalog

- Display name: Animate Image
- Categories: Video
- Status: Ready
- Route label: Kling 3.0 image-to-video
- Tone: cyan
- Short description: Animate one supplied still with bounded subject and camera motion while preserving identity and composition.

## What this skill does

- Adds controlled motion to a still rather than regenerating an unrelated scene.
- Separates subject, environmental and camera motion to reduce warping.

## How to use

Provide one image, desired motion, camera behavior, duration and audio preference.

#### Example

```text
Animate this still life for 5 seconds: candle flickers, curtain moves slightly, camera locked; preserve every object.
```

## Workflow

1. Map subjects, depth layers, protected geometry and allowed motion per region.
2. Write one primary motion plus subtle secondary motion; avoid conflicting camera instructions.
3. Run the `kling` model route with `modelName: Kling_3_0`, one source image, one result, 5 seconds and audio off by default. Never treat `ai-image-animation` as a model.
4. Inspect identity, edge stability, ending, motion amplitude and added-object errors.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The supplied still brought to life as one shot
- Default layout: User-requested delivery format
- Model policy: `kling` v1.0 with `modelName: Kling_3_0`
- Downstream use: Motion posts and cinematic inserts
