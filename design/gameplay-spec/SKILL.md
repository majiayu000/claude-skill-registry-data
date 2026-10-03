---
name: gameplay-spec
description: Produce an implementation-ready gameplay specification covering player goal, rules, states, inputs, feedback, tunable data, interactions, failure, edge cases, and validation without dictating unnecessary code structure.
---
# Gameplay Specification

Use when an approved mechanic or game system must be handed to engineering, level design, UI, audio, and QA.

## Procedure
1. State the intended player experience, supported modes, system boundaries, and relationship to the core loop.
2. Define inputs, preconditions, rules, state transitions, outputs, costs, rewards, failure, cancellation, and persistence behavior.
3. Specify feedback requirements across visuals, UI, audio, animation, camera, haptics, or world response where relevant.
4. List tunable parameters with meaning, units, allowed range, initial values, and who owns later balancing.
5. Map interactions with other gameplay systems and identify ordering, concurrency, multiplayer, AI, save or load, and networking concerns that affect behavior.
6. Document edge cases and invalid states explicitly, including repeated actions, interruptions, disconnected players, scene transitions, and resource boundaries as applicable.
7. Define content or data requirements separately from implementation architecture so designers can tune without code changes where intended.
8. Provide acceptance and playtest criteria that prove the player-facing rules rather than private implementation details.

## Decision rules
- A gameplay spec defines behavior and data contracts, not an engineering class diagram.
- Tunable values should carry semantic meaning and units.
- Important failure and interruption states belong in the spec.
- Cross-system interactions need explicit ownership before parallel implementation.

## Quality gate
The specification is ready when every material player-facing state and rule is unambiguous, tunable data and feedback are defined, cross-system dependencies and edge cases are visible, and engineering and QA can implement and validate the same intended behavior.