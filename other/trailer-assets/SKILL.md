---
name: trailer-assets
description: Plan and generate trailer-specific pickup plates, title cards, voiceover, music, SFX, and other marketing assets while preserving film canon and media approval state.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Trailer Assets

## Workflow

1. Read trailer manifest, reference assets, canon, generation adapters, and media registry.
2. Write `06_release/trailers/assets.jsonl` with one stable source/group identity per required asset.
3. Reuse approved film material when it performs the trailer job cleanly.
4. Generate a pickup only when the trailer plan identifies a concrete missing function.
5. Use existing image/video/audio adapters and ComfyUI execution when rendering is requested.
6. Route every candidate through media QC where applicable and `asset-approval`.
7. Trailer-only material must not silently become film canon.

## Done

Every trailer asset requirement points to approved existing media or a traceable generated candidate group.
