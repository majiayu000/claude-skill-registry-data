---
name: scene-outline
description: Convert beats into executable scenes with stable scene IDs, location, time, characters, goal, conflict, turn, outcome, and causal handoff to the next scene.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Scene Outline

## Workflow

1. Read core contract, story craft, beat sheet, characters, world, and brief.
2. Assign stable `SCN-###` IDs.
3. Use the scene template in `OUTPUT_TEMPLATES.md`.
4. Give each scene one primary dramatic job.
5. Enter late enough to avoid dead setup and leave after the turn has landed.
6. Check that the scene outcome causes or constrains what follows.
7. Save `01_story/scene_outline.md`.
8. When the outline is approved, run `story-state` to initialize `scene_order` and any explicit audience questions or promises that already exist in the plan. Do not invent ledger items merely to populate the file.

## Done

Every scene changes story state, every recurring character and location ID resolves, and the outline covers the complete ending.
