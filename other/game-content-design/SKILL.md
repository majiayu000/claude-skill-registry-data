---
name: game-content-design
description: Create, structure, balance, and review game content. Use when Codex is asked to design levels, missions, quests, encounters, enemies, items, rewards, progression, tutorials, puzzles, biomes, factions, economies, live-ops content, design docs, or playable content plans.
license: MIT
---

# Game Content Design

## Core Workflow

1. Identify the genre, target audience, session length, platform, progression model, content budget, and intended player fantasy.
2. Define the content's job: teach, test, reward, surprise, escalate, relax, branch, gate, reveal, or create mastery.
3. Establish constraints before authoring: available mechanics, enemy roster, verbs, locations, assets, pacing target, difficulty range, and production limits.
4. Think compositionally about content when useful: combine reusable mechanics, enemy capabilities, modifiers, objectives, rewards, and environmental constraints instead of inventing bespoke one-off content every time.
5. Build content around player decisions. Avoid sequences that only ask the player to follow instructions unless the goal is onboarding or atmosphere.
6. Use escalation deliberately: introduce, combine, twist, pressure, resolve. Track what the player has learned before asking for mastery.
7. Specify rewards, failure recovery, replay value, and telemetry or playtest signals where relevant.

## Content Types

- Levels: define route, landmarks, gates, loops, shortcuts, sightlines, encounter spaces, traversal tests, secrets, and reset/retry points.
- Quests and missions: define objective chain, motivation, stakes, optional branches, fail states, handoff points, reward logic, and world-state changes.
- Encounters: define enemy composition, terrain, timing, spawn rules, pressure pattern, counterplay, resource drain, and exit condition.
- Items and rewards: define acquisition source, rarity, power budget, tradeoffs, upgrade path, economy impact, and player-facing explanation.
- Progression: define unlock cadence, mastery curve, difficulty ramp, build diversity, catch-up mechanics, and anti-grind safeguards.
- Tutorials: teach one concept at a time, provide safe practice, then require use in a real context.

## Compositional Content Design

Use modular content pieces when designing variants:

- Enemy variants can be composed from movement, attack, defense, perception, status, and reward capabilities.
- Encounters can be composed from terrain pressure, enemy roles, resource constraints, objective pressure, timing, and escape/retry rules.
- Items can be composed from stat changes, verbs, tradeoffs, proc effects, restrictions, rarity, and upgrade hooks.
- Levels can be composed from traversal tests, combat spaces, landmarks, gates, loops, secrets, and rest points.
- Quests can be composed from motivations, objectives, complications, choices, rewards, and world-state consequences.

Keep the design modular without making it generic. A strong content composition still needs a clear fantasy, authored pacing, and a reason the selected pieces belong together.

## Deliverable Shape

For new content, produce compact specs that a designer, engineer, or level builder can act on:

- Goal and player experience
- Required mechanics and assets
- Step-by-step flow
- Tuning values or ranges
- Edge cases and fail states
- Rewards and progression impact
- Playtest questions

## References

- Read `references/content-design-checklist.md` when planning or reviewing levels, quests, encounters, progression, or reward structures.
