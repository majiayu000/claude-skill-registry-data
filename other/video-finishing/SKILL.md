---
name: video-finishing
description: Normalize or deliberately reframe selected picture media for edit and delivery, with optional approved AI-upscale routing and new media identities for every finished derivative.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Video Finishing

## Workflow

1. Read `../../references/VIDEO_FINISHING.md`, selections, media QC, media registry, and target timeline settings.
2. Decide whether a selected take needs no separate finish, conventional normalization, or an approved generative upscale.
3. For conventional finishing, write `05_post/video_finish.jsonl` and use `scripts/video_finish.py`.
4. For an AI upscale, route through the declared production capability and matching model adapter. Preserve the original selected take.
5. Register every derivative as a new media candidate.
6. Re-run media QC after generative or materially destructive processing.

## Done

Every picture file entering the final timeline either satisfies the timeline contract directly or has a traceable finished derivative.
