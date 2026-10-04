---
name: load-soak-capacity-verification
description: Use when servers or online game services need controlled load, soak, concurrency, capacity, saturation, leak, queue, failover, recovery, and scaling verification with baselines and stop conditions; not for client frame budgets.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos, console, mobile, web]
metadata:
  studio:
    type: gate
    lifecycle_stage: verify
    risk_level: medium
    packs: [production-management]
    side_effects: none
    artifact: load-soak-report.json
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
# Load Soak Capacity Verification

## Overview
Provide an evidence-first contract for load, soak, concurrency, capacity, saturation, queues, leaks, failover, recovery, scaling, baselines, and stop conditions.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use for client FPS budgets or uncontrolled production load testing.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `medium`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Define environment, topology, dataset, traffic model, baseline, SLOs, and abort thresholds.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Verify authorization, isolation, observability, cleanup, and recovery before generating load.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Run stepped load and bounded soak while capturing latency, errors, saturation, queues, and resources.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Test degradation, scaling, failover, recovery, and leak hypotheses against baselines.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return measured capacity, confidence, bottlenecks, artifacts, and BLOCKED gaps.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `load-soak-report.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
