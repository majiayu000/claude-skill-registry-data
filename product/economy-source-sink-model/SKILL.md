---
name: economy-source-sink-model
description: Use when modeling a game economy's currencies, item faucets, sinks, exchange rates, player segments, inflation risk, progression affordability, or live-operations reward assumptions.
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
    lifecycle_stage: define
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: economy-source-sink-model.json
    required_evidence: [currency-definitions, source-rates, sink-rates, player-segments]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, game-feature-to-spec]
      copied_text: none
---
# Economy Source Sink Model

## Overview
Make economy assumptions explicit by balancing normalized sources and sinks per currency, player segment, and time horizon.

## When to use
Use for progression economies, reward calendars, crafting costs, vendor pricing, inflation reviews, currency conversions, and monetization-adjacent design analysis.

## When NOT to use
Do not use to change live prices, grant currency, purchase items, or claim player behavior without telemetry or playtest evidence.

## Required inputs and context discovery
Collect currency and item definitions, source and sink events, rates, caps, exchange rules, player segments, session cadence, progression targets, telemetry window, and uncertainty ranges.

## Safety and risk level
Read-only modeling. Real-money pricing, regulated loot systems, or live economy changes require legal, product, and human review outside this skill.

## Workflow
1. Normalize currencies, items, sources, sinks, and conversion edges.
   Completion criterion: every flow has a unit, direction, frequency, and owning system.
2. Define representative player segments and time horizons.
   Completion criterion: assumptions and evidence sources are explicit for each segment.
3. Calculate net flow, stock accumulation, affordability, and sink coverage.
   Completion criterion: observed inputs are separate from forecast values and uncertainty.
4. Identify inflation, starvation, dead-currency, and exploit risks.
   Completion criterion: each risk cites the flows or conversion loop that causes it.
5. Propose bounded tuning experiments and telemetry needs.
   Completion criterion: no live value changes occur and every proposal has a measurable outcome.

## Evidence and output contract
Produce `economy-source-sink-model.json` with definitions, segments, normalized flows, net values, affordability, risks, assumptions, sensitivity ranges, and proposed experiments.

## Handoff contract
Record model version, input sources, uncertain assumptions, high-risk loops, proposed owners, telemetry gaps, and approval needs for any live change.

## Pitfalls and anti-rationalization
- Forecasts are not observed telemetry.
- Total sources and sinks hide segment-specific starvation.
- Conversion loops can duplicate value even when each edge looks safe.
- A balanced spreadsheet does not prove the economy is fun.

## Verification checklist
- [ ] Every flow has a unit and direction.
- [ ] Segments and time horizons are explicit.
- [ ] Forecasts and observations are separated.
- [ ] Conversion loops are reviewed.
- [ ] Live changes remain outside this read-only model.

## References and scripts
Use the bundled [scripts/economy_model.py](scripts/economy_model.py) for deterministic normalized-flow checks. Connect real telemetry only through project-approved sanitized exports.
