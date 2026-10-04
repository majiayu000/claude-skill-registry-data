---
name: studio-production-planning
description: Use when a game milestone needs production planning across schedule, staffing, workstreams, dependencies, delivery forecast, scope, and milestone acceptance; not for decomposing one approved feature into work packets.
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
    lifecycle_stage: plan
    risk_level: low
    packs: [production-management]
    side_effects: none
    artifact: production-plan.json
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
# Studio Production Planning

## Overview
Provide an evidence-first contract for milestone scope, staffing, schedule, dependencies, critical path, confidence, and delivery forecast.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use for one feature breakdown, detailed task assignment, or release go/no-go.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `low`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Bind the plan to a milestone goal, scope, constraints, and target date.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Map workstreams, owners, capacity, dependencies, and integration points.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Build a critical path with confidence ranges and explicit schedule assumptions.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Define milestone gates, change control, escalation thresholds, and reporting cadence.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Publish a forecast with blockers, decisions, and next review date.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `production-plan.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
