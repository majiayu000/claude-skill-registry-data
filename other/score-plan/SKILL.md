---
name: score-plan
description: Plan a film score as dramatic cues with entry, exit, duration, energy curve, instrumentation, tempo, key, motif rules, hit points, silence, and model targets.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Score Plan

## Workflow

1. Read core contract, style rules, screenplay, director book if present, and edit intent.
2. Define motif rules before individual cue prompts. State where a motif must not appear as clearly as where it should.
3. Write `04_generation/music_cues.jsonl` using stable `MUS-###` IDs.
4. Each cue needs a dramatic job, start and end logic, estimated duration, energy curve, instrumentation, tempo or tempo range, key only if useful, hit points, transition behavior, and avoid list.
5. Choose ACE-Step XL for structured local control or MiniMax Music 3 for a rich musical brief. Stable Audio 3 may be used for instrumental beds or textures.

## Done

Every music cue has a reason to exist and does not duplicate ambience or emotional information the scene already carries by itself.
