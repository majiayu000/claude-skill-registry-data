---
name: production-risk-and-dependency-review
description: Use when a production plan needs a read-only dependency risk review covering critical path, ownership gaps, blocked handoffs, mitigation, escalation, and schedule exposure; not for creating the baseline production schedule.
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
    lifecycle_stage: plan
    risk_level: read-only
    packs: [production-management]
    side_effects: none
    artifact: production-risk-review.json
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
# Production Risk and Dependency Review

## Overview
Provide an evidence-first contract for critical-path dependencies, ownership, probability, impact, mitigations, triggers, and escalation.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use to create the baseline schedule or silently accept missing owners.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Load the approved production plan and current workstream snapshots.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Trace dependency chains and identify single points of failure or owner gaps.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Score probability, impact, detectability, and schedule exposure with stated evidence.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Assign mitigation, contingency, trigger, owner, and escalation date.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return PASS, FAIL, or BLOCKED per gate without changing the plan.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `production-risk-review.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
