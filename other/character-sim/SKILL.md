---
name: character-sim
description: Pressure-test a character by speaking or reasoning strictly from that character's current voice, goals, relationships, emotional pressure, and knowledge boundary without creating canon by accident.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Character Sim

## Workflow

1. Read core contract, `REVIEW_PROTOCOLS.md`, the character bible, canon, and `01_story/story_state.json` if present.
2. Define the exact story moment, character ID, immediate goal, relationship context, pressure, and knowledge boundary.
3. Simulate only from facts the character can know at that moment. Future revelations and narrator-only facts are unavailable.
4. Preserve the character's established vocabulary, rhythm, evasions, habits, contradictions, and pressure behavior.
5. Use the simulation for voice discovery, dialogue testing, relationship pressure, or decision plausibility.
6. If the result suggests a useful new fact, record it as a proposal. Do not silently add it to canon or story state.
7. Save durable tests under `00_project/reviews/` only when future work needs the record.

## Done

The simulation is internally consistent with the character's knowledge and state, and no improvised detail was promoted to canon without an upstream decision.
