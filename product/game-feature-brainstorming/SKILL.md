---
name: game-feature-brainstorming
description: Use when exploring a game feature, mechanic, player experience, or production approach and the team needs two or three options with trade-offs before choosing a design.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: interactive
    lifecycle_stage: define
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: design-options.md
    required_evidence: [player-goal, constraints, trade-off-table]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [obra/superpowers brainstorming pattern Unverified, independent wording]
      copied_text: none
---
# Game Feature Brainstorming

## Overview
Clarify the desired player experience, then compare a small set of meaningfully different options before implementation details harden.

## When to use
Use for new mechanics, progression, combat, economy, social features, tools, UX flows, or technical approaches with real design trade-offs.

## When NOT to use
Do not use when an approved option already needs a formal specification, when the request is a micro-fix, or when safety requires immediate containment rather than ideation.

## Required inputs and context discovery
Collect player goal, target audience, platform, session length, constraints, production budget, content burden, technical limits, accessibility needs, success signals, and non-goals.

## Safety and risk level
Brainstorming is read-only. It does not authorize prototypes, purchases, schema changes, service work, or asset mutation.

## Workflow
1. Frame the player problem and the experience the feature should create.
   Completion criterion: outcome and non-goals are testable statements.
2. Identify constraints and the decisions with the highest downstream cost.
   Completion criterion: technical, content, UX, and production limits are explicit.
3. Propose two or three distinct options rather than cosmetic variants.
   Completion criterion: each option has a different core loop or implementation shape.
4. Compare player value, complexity, risk, tuning leverage, exploit surface, and testability.
   Completion criterion: a trade-off table makes the recommendation inspectable.
5. Recommend one option and list assumptions requiring prototype or playtest evidence.
   Completion criterion: the selected direction can move to `game-feature-to-spec`.

## Evidence and output contract
Produce problem framing, constraints, two or three options, trade-off table, recommendation, rejected alternatives, assumptions, and required prototype/playtest evidence.

## Handoff contract
Record chosen and rejected options, decision rationale, unresolved assumptions, tuning risks, and the prompt for creating the specification.

## Pitfalls and anti-rationalization
- Do not present one real option and two strawmen.
- Do not hide production cost behind player-facing language.
- Do not treat untested fun or retention claims as observed metrics.
- Do not implement before the direction is approved.

## Verification checklist
- [ ] Player goal and non-goals are explicit.
- [ ] Two or three distinct options exist.
- [ ] Trade-offs cover player, technical, and production concerns.
- [ ] Recommendation separates evidence from assumptions.
- [ ] Next step is specification, prototype, or BLOCKED.

## References and scripts
Use product constraints, existing design pillars, telemetry definitions, and technical architecture only as verified inputs.
