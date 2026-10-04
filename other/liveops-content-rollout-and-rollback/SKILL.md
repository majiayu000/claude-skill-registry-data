---
name: liveops-content-rollout-and-rollback
description: Use when a live game content update needs a governed rollout and rollback plan across cohort, canary, configuration, dependencies, monitoring, approvals, triggers, recovery, communication, and post-rollout verification; not for incident response after failure.
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
    lifecycle_stage: operate
    risk_level: high
    packs: [product-analytics]
    side_effects: none
    artifact: liveops-rollout-plan.json
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
# LiveOps Content Rollout and Rollback

## Overview
Provide an evidence-first contract for live content rollout, cohort, canary, configuration, dependencies, monitoring, approvals, rollback triggers, recovery, and verification.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use as incident response after an outage or to publish without approval.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `high`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Bind content identity, dependencies, environment, owner, approvals, and player impact.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Define cohort, canary stages, timing, compatibility, migration, and configuration controls.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Specify dashboards, guardrails, stop conditions, rollback triggers, and decision authority.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Verify rollback artifacts, data recovery, cache behavior, support, and communication drafts.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Produce a reviewed plan; execution remains blocked until explicit human authorization.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `liveops-rollout-plan.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
