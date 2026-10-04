---
name: game-feature-to-spec
description: Use when an approved, chosen, or selected game mechanic direction must become a testable specification with acceptance criteria, state transitions, inputs, outputs, edge cases, tuning, telemetry, and playtest criteria.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: plan
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: feature-spec.md
    required_evidence: [approved-option, edge-case-table, acceptance-criteria]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from: none
      patterns_from: [Product-Manager-Skills pattern-only; no copied content]
      copied_text: none
---
# Game Feature to Spec

## Overview
Convert an approved direction into an implementation-neutral contract that design, engineering, QA, art, data, and production can test.

## When to use
Use after a feature option is selected and before tasks, code, content production, or schema changes begin.

## When NOT to use
Do not use to choose among competing feature directions or to split an existing specification into ownership packets.

## Required inputs and context discovery
Require approved option, player goal, non-goals, system boundaries, platform constraints, dependencies, persistence/network authority, content needs, tuning ownership, telemetry expectations, and playtest audience.

## Safety and risk level
Specification writes are low-risk. Do not invent engine, backend, analytics, or database contracts; mark unresolved authority and schema decisions BLOCKED.

## Workflow
1. State purpose, player outcome, scope, and non-goals.
   Completion criterion: stakeholders can identify what is explicitly not being built.
2. Define inputs, outputs, state transitions, authority, persistence, and failure behavior.
   Completion criterion: the feature can be represented as deterministic scenarios.
3. Enumerate edge cases, abuse/exploit cases, accessibility, localization, and offline/network behavior.
   Completion criterion: risky branches have expected outcomes or BLOCKED owners.
4. Define tuning levers, defaults, ownership, migration needs, and telemetry events.
   Completion criterion: designers can tune without hidden code changes where intended.
5. Write acceptance and playtest criteria tied to observable behavior.
   Completion criterion: QA can derive tests without guessing product intent.

## Evidence and output contract
Produce `feature-spec.md` with purpose, non-goals, I/O, states, authority, edge cases, tuning, telemetry, content, acceptance criteria, playtest criteria, dependencies, and open decisions.

## Handoff contract
Record approved version, owners of open decisions, affected systems, required prototypes, schema risks, and the prompt for work-packet decomposition.

## Pitfalls and anti-rationalization
- Do not bake one implementation into a product requirement without reason.
- Do not omit failure, offline, or exploit behavior.
- Do not use target KPIs as observed results.
- Do not hide unresolved authority behind “implementation detail.”

## Verification checklist
- [ ] Purpose and non-goals are clear.
- [ ] States, I/O, authority, and failures are specified.
- [ ] Edge cases and tuning levers exist.
- [ ] Acceptance and playtest criteria are observable.
- [ ] Open decisions have owners or BLOCKED labels.

## References and scripts
Use the approved brainstorming artifact, architecture contracts, data schemas, and existing telemetry vocabulary as inputs.
