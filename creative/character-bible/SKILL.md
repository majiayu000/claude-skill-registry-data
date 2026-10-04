---
name: character-bible
description: Create a compact character bible focused on behavior under pressure, goals, contradictions, relationships, speech, appearance, wardrobe, and continuity facts that affect story or production.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Character Bible

## Workflow

1. Read core contract, `CHARACTER_PROFILE.md`, style rules, brief, story architecture, existing canon, and current story state when present.
2. Assign stable `CHAR-###` IDs. Work one consequential character at a time when the cast or context is large.
3. Resolve story function before biography. Record objective, fear or limit, contradiction, pressure behavior, private knowledge, and only backstory that changes present behavior.
4. Build canonical identity with physical identifiers, `must_preserve`, explicit `must_not_be` exclusions when useful, and `may_vary` scene-state traits.
5. Keep speech, movement, and stillness as separate performance signatures. Do not turn acoustic TTS settings into a speech-writing profile.
6. Record recurring pair behavior as canonical `relationship_baselines`. Put chronology-specific trust, hostility, power, knowledge, injury, possession, and other current state in `story_state.json` instead.
7. Preserve strong user wording. If a consequential creative fact is unresolved, keep it open or use `decision-tree-interview`; do not invent detailed canon to fill a template.
8. Write `01_story/characters.md` and update `00_project/canon.json` with only locked identity, performance, relationship-baseline, and continuity facts.
9. Run `scripts/character_profiles.py <project>` and the project validator.

## Done

Every recurring character can be recognized by durable identity and behavior, current story state remains separate from baseline canon, and downstream writing/directing/generation work can use the saved profile without reconstructing it from chat.
