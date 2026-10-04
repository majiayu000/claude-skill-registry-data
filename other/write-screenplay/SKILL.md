---
name: write-screenplay
description: Write a complete Fountain screenplay, scene manifest, and stable line manifest from an approved scene plan or adaptation map, using filmable action, character-specific dialogue, and traceable scene/line IDs.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Write Screenplay

## Workflow

1. Read core contract, `CHARACTER_PROFILE.md`, style rules, screenplay craft, canon, brief, `01_story/characters.md`, `01_story/world.md` when present, current story state, and scene outline or adaptation map.
2. Write `02_screenplay/screenplay.fountain` in present tense and filmable language.
3. Keep action paragraphs short and dialogue character-specific. Use speech signatures and current relationship state without turning profile notes into exposition.
4. Create `02_screenplay/scene_manifest.json` with one object per `SCN-###`: heading, location ID, time, characters, purpose, outcome, source beat, and approximate runtime.
5. Create `02_screenplay/line_manifest.jsonl` with stable `LINE-###` records for production-relevant dialogue, action, movement, and transitions. Preserve exact dialogue text, scene ID, order, speaker ID where applicable, and whether the unit is audible, on screen, or needs blocking.
6. Keep scene IDs in the manifest rather than cluttering screenplay dialogue or headings unless the user wants visible IDs.
7. Update `story-state` with screenplay scene order and mutable state changes that differ from the source plan or adaptation.
8. Run `scripts/screenplay_consistency.py <project>` before checkpointing. Do not write an ad hoc dialogue parser and do not hardcode character names into a verification command.
9. Run the style checker.

## Done

The screenplay is complete through FADE OUT or an equivalent ending, scene manifest, line manifest, and story-state scene order agree, `screenplay_consistency.py` passes, and mutable narrative facts remain traceable.
