---
name: shooting-script
description: Compile screenplay lines, performance blocking, shot briefs, scene state, and dialogue timing into a portable machine-readable shooting script with positions, moves, actions, camera coverage, exact dialogue, and timing sources.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Shooting Script

## Workflow

1. Read core contract, `HIERARCHICAL_PRODUCTION_PLANNING.md`, `VISIBLE_DIALOGUE_SYNC.md`, `SHOOTING_SCRIPT.md`, screenplay, line manifest, blocking, shot briefs, voice cues when present, continuity, and production capabilities.
2. Work one approved scene or sequence at a time.
3. Write `03_preproduction/shooting_script.json`. Preserve exact dialogue and stable IDs.
4. For every unit, record current positions, moves, actions, covering shot IDs, constraints, and timing source.
5. For visibly spoken dialogue, compile the matching `lip_sync` record and ensure at least one covering shot carries the same exact line and speaker requirement.
6. Keep movement separate from non-locomotion actions.
7. If measured voice duration exists, propagate it into visible-dialogue timing and use it instead of an estimate where it controls shot/action/subtitle timing.
8. Never rewrite dialogue or choose a new story beat to fit a technical limit. Route the conflict upstream or split the production unit.
9. Run `production-coverage` after compiling the requested scope.

## Done

The approved scope can be executed or translated into generation tasks without reconstructing performer state, dialogue, camera coverage, or timing from chat.
