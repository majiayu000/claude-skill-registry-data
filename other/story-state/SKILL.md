---
name: story-state
description: Maintain the machine-readable narrative state ledger for character life and knowledge, prop state, open questions, promises and payoffs, scene order, and chronology-sensitive appearances.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Story State

Use after a chapter or screenplay scene settles, or when a revision changes chronology or state.

## Workflow

1. Read the core contract, `NARRATIVE_STATE.md`, canon, and the changed chapter or scene.
2. Read only the ledger entries and adjacent scenes affected by the change.
3. Update `01_story/story_state.json` with changed character, relationship, prop, question, promise, scene-order, and event state. Use the object relationship form from `NARRATIVE_STATE.md` for new relationship changes.
4. Keep canonical speech, movement, stillness, physical identity, and baseline ensemble behavior in canon. Current trust, hostility, allegiance, knowledge, injury, possession, location, and other chronology-sensitive conditions belong here.
5. Keep possibilities out of the ledger until the upstream story or screenplay adopts them.
6. Use `mentions` for non-active appearances such as memories, recordings, references, or posthumous material when that distinction matters.
7. Run `validate_story_project.py` after chronology, setup/payoff, death, or selection state changes.

## Done

The ledger matches the approved narrative scope, every changed state has a traceable scene, and deterministic ordering checks pass.
