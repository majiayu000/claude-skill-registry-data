---
name: design-game-systems
description: Specify player decisions, core loops, progression, economies, difficulty, and balance hypotheses with measurable playtests. Use when designing or revising a game's rules beyond a single combat action.
engines: [AGNOSTIC]
---

# Design Game Systems

## When to use

- Establishing a core loop, progression model, economy, or difficulty curve.
- Diagnosing dominant strategies, weak choices, stalled progression, or mismatched rewards.
- Turning a player-experience goal into rules that engineering and playtesting can evaluate.

## Workflow

1. State the intended player experience, audience, session length, constraints, and observable decisions. Describe what the player knows, chooses, risks, and learns; theme alone does not establish a decision.
2. Map the moment-to-moment loop and its longer progression loop. Identify entry, success, failure, recovery, and stopping points. Separate optional rewards from mandatory progression gates.
3. Specify resources, sources, sinks, costs, caps, prerequisites, ownership, and persistence. For an economy, trace conservation and inflation risks across representative player paths, including failure and catch-up.
4. Define rules and tuning ranges separately. Document randomness, information visibility, counterplay, exploit boundaries, accessibility, and multiplayer authority where applicable. Keep combat-specific timing with `design-action-gameplay`.
5. Write falsifiable hypotheses: the expected decision or behavior, target audience, test situation, observation method, and revision threshold. A spreadsheet or simulation tests its stated assumptions; it does not establish enjoyment or comprehension.
6. Playtest representative new and experienced players, record observed choices and reasons, compare alternative explanations, and revise the smallest relevant rule. Preserve rejected hypotheses and changes so a later metric does not erase contradictory evidence.
7. For implementation, resolve the project engine and select a compatible feature skill with `resolve-skill.sh`. This agnostic design workflow neither selects an engine nor supplies its APIs.

For explicitly selected chain-owned assets, use `plan-web3-game-assets` to separate wallet control, ownership and game eligibility. Declare mid-match transfer and scarcity/quantity rules; neither token prices nor a supply spreadsheet establishes game balance.

## Output

- A rules specification with loop diagram or concise flow, decisions, state transitions, resources, failure/recovery, and tunable ranges.
- Balance hypotheses with explicit assumptions and representative initial, middle, late, failure, and exploit cases.
- A playtest plan and findings that distinguish measured behavior, player reports, inference, and blocked or untested questions.

## References

- Read `docs/GAMEPLAY_CONCEPTS.md` in the resolved Hephaera baseline (`.hephaera/docs/GAMEPLAY_CONCEPTS.md` from an installed host's root) when a request about game feel, rendering or runtime systems needs more precise vocabulary and an existing implementation owner. Select only relevant entries and resolve the effective engine's compatible skills before using APIs; the index does not prescribe every listed technique.

## Guardrails

- Do not prescribe a universal frame rate, session length, reward schedule, or numerical fun score.
- Do not treat engagement metrics as consent to manipulative purchases or punitive retention mechanics.
- Do not claim balance from one simulated strategy or assume that difficulty and accessibility are the same setting.
- Keep unavailable player research explicit; a completed design document is not a successful playtest.
