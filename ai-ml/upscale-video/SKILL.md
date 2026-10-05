---
name: upscale-video
description: Increase supplied video resolution and clarity while preserving timing, content, grain intent, and natural detail. Use for resolution enhancement and restrained restoration of existing footage; do not use for reframing, restyling, frame interpolation, content repair, or generating replacement scenes.
---
# Upscale Video

## Catalog

- Display name: Upscale Video
- Categories: Video
- Status: Ready
- Route label: WeShop AI Video Enhancer
- Tone: green
- Short description: Increase supplied video resolution and clarity while preserving timing, content, grain intent and natural detail.

- Similar skills: add-video-effect, correct-video-color, restyle-video
## What this skill does

- Upscales one video to requested resolution with temporal consistency.
- Rejects invented facial, text or texture detail and separates upscale from restyling.

## How to use

Provide video, target resolution, priority regions, denoise and sharpening limits and codec.

#### Example

```text
Upscale this supplied 720p clip to 4K; mild denoise only; preserve faces, film grain and exact duration.
```

## Workflow

1. Probe source resolution, frame rate, codec, duration, interlace and damage.
2. Choose ai-video-enhancer or free-4k-video-upscaler by target and source.
3. Poll the WeShop run to terminal success and download the file.
4. Compare matched timestamps for inventions, halos, waxy faces, text corruption, flicker, timing and resolution.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The same video at the requested higher resolution
- Default layout: User-requested delivery format
- Model policy: WeShop AI Video Enhancer
- Downstream use: Archival and delivery enhancement
