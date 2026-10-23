---
name: video-asset-pipeline
description: Turn owned, stock, generated, Blender, or Remotion footage into optimized website video, posters, mobile variants, loops, and scrub-ready media with provenance.
---

# Video Asset Pipeline

Read:

- `creative-production/pipelines/video-assets.md`
- `creative-production/standards/asset-budgets.md`
- `creative-production/standards/provenance.md`
- the completed hero or cinematic-scene brief

## Required outputs

Unless the page proves otherwise:

- clean master outside the public repo
- desktop MP4
- mobile MP4
- poster
- reduced-motion still
- optional WebM after measured benefit
- manifest

## Edit

- make the focal point deliberate
- grade against the real page copy
- remove unnecessary duration
- build an actual loop when looping
- remove audio unless user-controlled
- create mobile composition, not an accidental crop
- composite VFX before the browser when live blending adds no value

## Encode

Use FFmpeg commands from the pipeline guide. For scroll scrubbing, compare a short-GOP and all-intra export in the target browser.

## Integrate

- explicit dimensions or aspect ratio
- `muted playsinline` for ambient autoplay
- meaningful poster
- preload only what the first scene needs
- warm later video near use
- pause offscreen
- no essential information only in motion
- range-request verification for scrub media

## Verify

Run:

```bash
npm run assets
npm run audit -- path/to/page
npm run smoke
```

Inspect desktop, mobile, reduced motion, slow loading, reverse scroll, and playback failure.

Do not downgrade resolution to hide a seeking problem. Fix the encoding and loading strategy.
