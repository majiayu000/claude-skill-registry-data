---
name: editorial-package
description: Compile a standalone portable editorial package with timeline events, shot media, dialogue, subtitles, music, sound cues, stems, placeholders, missing media, and interchange-ready records.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Editorial Package

## Workflow

1. Read the standalone contract, editorial package rules, edit plan, shot briefs, generated-media map if present, voice cues, music cues, sound cues, and screenplay dialogue.
2. Write `05_post/editorial_manifest.json`.
3. Map every timeline event to stable scene, shot, voice, music, and sound IDs where applicable.
4. Record placeholders and missing media explicitly rather than inventing files.
5. Create `05_post/subtitles.srt` when dialogue or captions require subtitles and timing is sufficiently known.
6. Update `05_post/cue_sheet.csv` with music and sound placements.
7. Keep paths project-relative.
8. Do not fabricate an editor-private project format. Use `mlt-export` only when standard MLT interchange is requested.
9. If the endpoint is an actual finished film, pass the reconciled editorial state to `audio-master` and `timeline-assembly`.

## Done

A human editor or the native finishing layer can assemble the project from the portable manifest and identify every missing element without consulting the original chat.
