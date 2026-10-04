---
name: shot-list
description: Compile approved shot briefs into a practical CSV shot list with source line IDs, setups, framing, angle, movement, action, audio, duration, continuity, and production notes.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Shot List

## Workflow

1. Read core contract, film grammar, and all shot briefs in scope.
2. Write `03_preproduction/shot_list.csv` with the columns in `OUTPUT_TEMPLATES.md`.
3. Group shots by efficient setup only if doing so does not obscure story order. Preserve scene, shot, and source `LINE-###` IDs.
4. Keep generation duration estimates synchronized with shot briefs.
5. Flag shots that require exact first or last frames, reference media, lip sync, or complex transitions.

## Done

Every approved shot appears exactly once, every row maps to one scene, and duration totals can be reconciled against the edit plan.
