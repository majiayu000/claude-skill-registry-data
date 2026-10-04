---
name: product-analytics-experiment-review
description: Use when a game product experiment or A/B test needs review across hypothesis, population, assignment, metrics, guardrails, instrumentation, segmentation, sample size, significance, novelty, ethics, and decision rules; not for telemetry schema alone.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos, console, mobile, web]
metadata:
  studio:
    type: workflow
    lifecycle_stage: operate
    risk_level: read-only
    packs: [product-analytics]
    side_effects: none
    artifact: experiment-review.json
    required_evidence: [scope, owners, commands, artifacts, blockers]
    owner: HoaTV Studio
    reviewer: Producer
    maturity: beta
    last_reviewed: 2026-08-18
    provenance:
      derived_from: none
      patterns_from: [full-studio capability gap review]
      copied_text: none
---
# Product Analytics Experiment Review

## Overview
Provide an evidence-first contract for experiment hypothesis, population, assignment, metrics, guardrails, instrumentation, segmentation, sample size, significance, novelty, ethics, and decisions.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use only to define telemetry event fields or to launch an experiment.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. State the product decision, falsifiable hypothesis, unit of randomization, and population.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Define primary metric, guardrails, segments, attribution window, and instrumentation evidence.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Review sample size, power, duration, peeking, novelty, interference, and data quality.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Check player harm, fairness, privacy, rollback, and operational stop conditions.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return approve, revise, reject, or BLOCKED with pre-registered decision rules.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `experiment-review.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

## Handoff contract
Record repository and path, goal, owned scope, do-not-touch scope, decisions, files changed, commands, exit codes, artifacts, restore information, blockers, next owner, and reactivation prompt.

## Pitfalls and anti-rationalization
- Missing evidence is `BLOCKED`, never PASS.
- A plan or review does not authorize production execution.
- Compile success, screenshots, or anecdotes do not prove broader coverage.
- Preserve unrelated work and generated-source ownership.

## Verification checklist
- [ ] Scope, identity, owners, and exclusions are explicit.
- [ ] Every verdict cites observed evidence or is labeled Unverified/BLOCKED.
- [ ] Risks have mitigations, triggers, owners, and dates.
- [ ] No unauthorized mutation, publication, deployment, or destructive action occurred.
- [ ] Handoff names the next bounded action.

## References and scripts
No bundled runtime helper is required. Use project-owned plans, evidence, runbooks, schemas, and validation commands; repository governance tools remain full-clone-only.
