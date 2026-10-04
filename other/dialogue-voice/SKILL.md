---
name: dialogue-voice
description: Create a reusable voice bible and exact dialogue cue list from screenplay lines, including character voice identity, delivery intent, language, timing, and continuity across scenes.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Dialogue Voice

## Workflow

1. Read core contract, `CHARACTER_PROFILE.md`, style rules, screenplay, `02_screenplay/line_manifest.jsonl` when present, character bible, canon, and continuity.
2. Assign one `VOICE-###` identity per recurring voice. Use the canonical speech signature for cadence, habitual delivery behavior, and language style, while keeping acoustic timbre/accent/reference-audio identity in the voice bible.
3. Write `04_generation/voice_bible.md` with vocal age range, register, texture, cadence, accent or dialect only when decided, speech habits, emotional range, and forbidden drift.
4. Write `04_generation/voice_cues.jsonl` with the originating `LINE-###`, exact screenplay text, scene, speaker, language, delivery intent, timing target if known, measured duration when available, and target model.
5. Do not rewrite dialogue merely to make TTS easier without updating the screenplay.

## Done

Every spoken `LINE-###` in scope maps to one voice identity and exact text source, and measured speech duration is available to the shooting script when generated.
