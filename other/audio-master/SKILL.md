---
name: audio-master
description: Build and render a synchronized full-program audio master from approved dialogue, voiceover, ambience, Foley, SFX, score, and music using an explicit project-relative mix manifest.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Audio Master

## Workflow

1. Read `../../references/AUDIO_MASTERING.md`, the edit plan, voice/music/SFX cues, media registry, and approvals.
2. Write or update `05_post/audio_mix.json` with exact timeline starts, source trims, durations, gain, pan, and fades.
3. Reject unresolved or missing required media before final rendering.
4. Use `scripts/audio_master.py PROJECT --manifest 05_post/audio_mix.json` for the actual master.
5. Verify the output exists and preserve the renderer report.
6. Run `asset-approval` to register the rendered master.
7. Run `delivery-qc` when the master has delivery constraints.

## Weak-model rule

Do not estimate a rendered waveform path. Do not treat cue descriptions as audio. Do not stretch exact dialogue merely to fill a picture gap.

## Done

The project has a reproducible mix manifest and, when rendering was requested and FFmpeg succeeded, an actual synchronized audio master file.
