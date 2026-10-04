---
name: continuity-check
description: Audit canon, story, screenplay, production documents, and generation prompts for identity, wardrobe, prop, geography, knowledge, time, lighting, audio, and dialogue continuity conflicts.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Continuity Check

## Workflow

1. Read core contract and `CONTINUITY_RULES.md`.
2. Determine the requested scope and read every authoritative artifact, approved reference record, and the relevant entries from `01_story/story_state.json` when present.
3. Write `03_preproduction/continuity.md` with sections: locked facts, approved reference versions, current scene states, conflicts, resolutions, unresolved questions.
4. For each conflict, cite the two project artifacts by path and stable ID.
5. Resolve by authority order. Never quietly pick the more convenient prompt.
6. Update canon when the user or an authoritative upstream edit settles a fact. Use `story-state` when the change is chronological or mutable rather than permanent canon.
7. Run the project validator for deterministic ordering checks, then separately review motivation, performance, and dramatic logic that a structural validator cannot prove.

## Done

There are zero unresolved contradictions that would cause a character, prop, location, action, dialogue line, or audio cue to change identity across adjacent production artifacts.
