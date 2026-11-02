---
name: hyperframes-video
description: Create local HTML, SVG, Canvas and GSAP videos with HyperFrames. Use for interface demos, motion typography, animated diagrams and layered explainers.
priority: P0
category: media
status: builtin-guidance
---

# HyperFrames Video

Choose HyperFrames for browser-native motion: typography, glass interfaces, SVG paths, diagrams, dashboards and timed overlays. Use Remotion when the brief benefits from React scene composition or an established Three.js camera workflow; follow an explicitly requested engine.

## Device and permission gates

Use an authorized user device and writable task workspace. Read video-creator for the shared local-rendering workflow, source handling and verification. Ordinary HyperFrames, browser and FFmpeg dependencies may be prepared automatically within that media request and current permissions, after disclosing download source, approximate size and destination. All rendering stays local. Qwen TTS and ACE-Step downloads still require size-aware installation consent.

## Execute

This package includes the same hashed scripts/local-media.mjs as video-creator. Materialize it with prepare_skill in Arc or chunked read_skill resource reads in Connect.

    node "<skill>/scripts/local-media.mjs" ensure --workspace "<workspace>" --components hyperframes
    node "<skill>/scripts/local-media.mjs" render --workspace "<workspace>" --engine hyperframes --project "<project>" --output "<new film>.mp4"

Use the installed pinned CLI's documentation. In index.html provide composition dimensions, data-fps, data-duration and a window.__timelines entry. Register paused, seekable GSAP timelines. Give every timed media element a stable id, local src and correct duration. Bundle fonts and scripts locally. Canvas particles must be deterministic functions of the seek time; do not use wall-clock loops or fresh randomness.

Animate the explanation itself: let a path carry an order, make a queue react to a sell order, or transform data into a new view. Use music-derived edit points when requested, preserve reading time, and update subtitle timing when retiming scenes. Test forward and backward seeks before full rendering.

## Verify and deliver

Resolve lint errors, including missing media IDs and unregistered timelines. Check actual captured frames, scene boundaries, text layout, particles, audio throughout the film and the final frame. Verify the finished MP4 with ffprobe and full decode. Deliver that file and editable HTML/JS sources; a preparation receipt alone is not a video.
