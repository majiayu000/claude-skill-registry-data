---
name: balance-data-change-review
description: Use when numeric game tuning data such as damage, price, cooldown, drop rate, or progression has a before/after diff that must stay within approved min/max bounds.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [any]
metadata:
  studio:
    type: workflow
    lifecycle_stage: review
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: balance-change-review.json
    required_evidence: [baseline-data, proposed-data, declared-bounds, design-intent]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, review-swarm]
      copied_text: none
---
# Balance Data Change Review

## Overview
Review balance changes as data contracts with intent, bounds, dependencies, and rollback conditions rather than approving isolated numbers by feel.

## When to use
Use for stat tables, abilities, cooldowns, drop rates, XP curves, encounter tuning, rewards, crafting values, and configuration-driven balance patches.

## When NOT to use
Do not use to write generated tables directly, deploy live configuration, or replace playtest and telemetry evidence.

## Required inputs and context discovery
Collect source-of-truth path, generated outputs, baseline and proposed rows, design intent, allowed bounds, formulas, dependent systems, segment impact, test evidence, rollout scope, and rollback owner.

## Safety and risk level
Read-only review. Source data may be changed only by its named owner through the project generation pipeline; generated outputs are never hand-edited.

## Workflow
1. Verify source ownership, generation path, schema, and baseline snapshot.
   Completion criterion: the canonical editable source and generated consumers are identified.
2. Compute field-level deltas and compare them with declared bounds.
   Completion criterion: every changed value has old, new, absolute, relative, and bound status.
3. Trace formulas, dependencies, breakpoints, and player-segment effects.
   Completion criterion: hidden multipliers and downstream consumers are documented or `BLOCKED`.
4. Review design evidence, exploit risk, and rollback conditions.
   Completion criterion: intent is testable and rollback restores the exact baseline.
5. Issue a review verdict and required validation plan.
   Completion criterion: approval is withheld for unexplained, out-of-bound, or untestable changes.

## Evidence and output contract
Produce `balance-change-review.json` with source identity, deltas, bound violations, dependency impacts, evidence, risks, rollback data, verdict, and required tests.

## Handoff contract
Record canonical source, generation command, affected systems, unresolved dependencies, review owner, validation build, rollout scope, and rollback snapshot.

## Pitfalls and anti-rationalization
- A small scalar change can cross a systemic breakpoint.
- Percentage deltas need context for zero or tiny baselines.
- Generated data is not the source of truth.
- Design intent without a measurable criterion is not sufficient evidence.

## Verification checklist
- [ ] Canonical source and baseline are exact.
- [ ] Every delta is normalized and bounded.
- [ ] Dependencies and formulas are traced.
- [ ] Validation and rollback are concrete.
- [ ] No generated or live data was modified during review.

## References and scripts
Use the bundled [scripts/balance_review.py](scripts/balance_review.py) for normalized data-delta and bound checks. Use project-specific generators only after owner approval.
