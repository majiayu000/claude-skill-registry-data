---
name: telemetry-event-contract-review
description: Use when reviewing game analytics or telemetry event names, IDs, required properties, types, versions, privacy classes, producers, consumers, and backward compatibility before instrumentation changes.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [any]
  platforms: [client, server, data-pipeline]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: review
    risk_level: read-only
    packs: [production-design-liveops]
    side_effects: none
    artifact: telemetry-contract-review.json
    required_evidence: [baseline-schema, proposed-schema, producer-consumer-map, privacy-classification]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [registry/capabilities.yaml production catalog, lua-client-server-contract-audit]
      copied_text: none
---
# Telemetry Event Contract Review

## Overview
Treat telemetry as a versioned producer-consumer contract so analytics changes remain compatible, privacy-aware, and testable.

## When to use
Use for new events, renamed properties, type changes, required-field changes, client/server instrumentation, analytics migrations, and dashboard dependency reviews.

## When NOT to use
Do not use to transmit live events, query production player data, deploy collectors, or approve privacy-sensitive collection without the responsible human reviewers.

## Required inputs and context discovery
Collect baseline and proposed schemas, event IDs and names, property types and optionality, versions, producers, consumers, sampling, timestamps, identity fields, privacy classification, retention, consent rules, rollout, and deprecation window.

## Safety and risk level
Read-only contract review. Unknown privacy classification, ambiguous identifiers, missing consent rules, or inaccessible consumer inventories are `BLOCKED` for approval.

## Workflow
1. Normalize event IDs, names, versions, properties, types, and optionality.
   Completion criterion: duplicate IDs and ambiguous aliases are explicit failures.
2. Compare baseline and proposal for additive, breaking, and semantic changes.
   Completion criterion: every change has compatibility classification and affected versions.
3. Trace producers, consumers, dashboards, experiments, and retention dependencies.
   Completion criterion: unknown consumers are `BLOCKED` rather than assumed safe.
4. Review privacy classification, minimization, consent, sampling, and retention.
   Completion criterion: sensitive or unnecessary properties have an owner and disposition.
5. Define rollout, dual-write or migration, validation, and deprecation evidence.
   Completion criterion: backward compatibility and rollback are testable before deployment.

## Evidence and output contract
Produce `telemetry-contract-review.json` with normalized schemas, compatibility findings, producer-consumer impacts, privacy findings, rollout plan, validation cases, verdict, and limitations.

## Handoff contract
Record schema owners, affected producers and consumers, breaking changes, privacy decisions, rollout order, dashboard updates, deprecation deadline, and unresolved gaps.

## Pitfalls and anti-rationalization
- Renaming a property is a breaking change for existing consumers.
- Same type does not guarantee same semantics or units.
- Optional client fields may become effectively required downstream.
- Do not collect identifiers merely because storage exists.

## Verification checklist
- [ ] IDs and names are unique and versioned.
- [ ] Types, units, and optionality are explicit.
- [ ] Producers and consumers are traced.
- [ ] Privacy and retention are reviewed.
- [ ] Rollout and rollback are testable.

## References and scripts
Use the bundled [scripts/telemetry_contract.py](scripts/telemetry_contract.py) for deterministic schema compatibility checks. Live collectors and production datasets remain outside this read-only skill.
