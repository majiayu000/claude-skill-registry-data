---
name: edit-plan
description: Create a post-production edit plan and cue sheet from screenplay, shot list, generated clip durations, dialogue, music, and SFX, including transitions, pickups, and continuity risks.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Edit Plan

## Workflow

1. Read core contract, screenplay, scene manifest, shot list, continuity, music cues, SFX cues, and known generated durations.
2. Write `05_post/edit_plan.md` scene by scene with intended cut order, pacing, transitions, audio bridges, and pickup alternatives.
3. Write `05_post/cue_sheet.csv` mapping shot, dialogue, voice, music, SFX, and ambience IDs to timeline intent.
4. Flag duration mismatches instead of hiding them with arbitrary slow motion or repeated footage.
5. Keep a pickup list for missing inserts, reactions, establishing material, or clean audio.

## Done

The planned cut can be assembled from named assets or clearly listed pickups, with no unidentified clip or cue dependency.
