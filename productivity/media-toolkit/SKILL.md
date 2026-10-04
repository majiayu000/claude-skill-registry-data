---
name: media-toolkit
description: Route deterministic media editing and manipulation through installed FFmpeg, FFprobe, MLT/melt, and ImageMagick runtimes with runtime capability discovery, portable manifests, safe argv execution, and reproducible evidence.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Media Toolkit

## Workflow

1. Read `../../references/FFMPEG_TOOLKIT.md`, `../../references/MLT_TOOLKIT.md`, and `../../references/IMAGEMAGICK_TOOLKIT.md`.
2. Determine whether the task is primarily moving-image/audio/subtitle/container work, MLT service-graph/timeline work, or still-image/image-sequence work.
3. Read the matching specialist: `ffmpeg`, `mlt`, or `imagemagick`.
4. Discover the installed runtime before relying on optional codecs, filters, delegates, MLT modules, or hardware acceleration.
5. Prefer an existing domain-specific helper when it exactly fits. Otherwise use `scripts/media_toolkit.py`.
6. Preserve source media unless in-place modification is explicitly requested.
7. Verify outputs rather than treating a zero-error plan as completed media.

## Done

The requested deterministic manipulation is either completed and verified, or blocked with the exact missing runtime/capability identified.
