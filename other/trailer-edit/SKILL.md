---
name: trailer-edit
description: Build an executable trailer timeline from approved movie material and trailer pickups with deliberate pacing, spoiler control, title-card placement, dialogue selection, and source traceability.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Trailer Edit

## Workflow

1. Read `../../references/TRAILER_SYSTEM.md`, one `TRL-###` plan, approved trailer assets, film selections, and spoiler policy.
2. Create `06_release/trailers/TRL-###/timeline.json` using the executable timeline schema.
3. Create the matching trailer `audio_mix.json` with approved score, dialogue, VO, and SFX.
4. Preserve source IDs on every event.
5. Check planned duration against target and tolerance.
6. Re-read the spoiler policy after the cut is assembled.
7. Validate timeline and promo manifests before mastering.

## Done

The trailer is represented as a complete executable picture and audio edit with no unresolved required event.
