---
name: revise-screenplay
description: Review and revise a screenplay for structure, scene purpose, filmability, staging, dialogue, runtime, and page economy while keeping its scene manifest synchronized.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Revise Screenplay

## Workflow

1. Read core contract, `CHARACTER_PROFILE.md`, style rules, screenplay craft, canon, `01_story/characters.md`, current story state, full screenplay, scene manifest, and line manifest when present.
2. Diagnose in this order: structure, scene necessity, scene turn, filmability, staging, dialogue, character-voice drift, line-level economy.
3. Fix scenes that do not change state before polishing dialogue.
4. Remove action that cannot be filmed or convert it into behavior or sound.
5. Check entrances, exits, props, knowledge, and relationships after every scene move.
6. Update the scene manifest and `02_screenplay/line_manifest.jsonl` immediately after screenplay changes. Preserve existing `LINE-###` IDs for surviving units; retire or remove deleted units and assign new IDs only to genuinely new production units.
7. Mark downstream preproduction and generation artifacts stale in state.

8. Run `scripts/screenplay_consistency.py <project>` after screenplay or line-manifest edits. Do not verify dialogue with a hand-written list of character names.
9. Apply the `project-impact` procedure after accepted screenplay changes and mark affected production artifacts stale.

## Done

Screenplay, scene manifest, and line manifest agree, `screenplay_consistency.py` passes, accepted notes are resolved, and no stale production artifact is still marked approved.
