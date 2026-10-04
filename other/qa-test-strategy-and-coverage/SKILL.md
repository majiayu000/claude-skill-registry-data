---
name: qa-test-strategy-and-coverage
description: Use when a game project, milestone, or feature needs a QA test strategy and coverage matrix across risk, test levels, platforms, environments, ownership, automation, regression, evidence, and exit criteria; not for one playtest session.
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
    lifecycle_stage: verify
    risk_level: read-only
    packs: [production-management]
    side_effects: none
    artifact: qa-strategy.json
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
# QA Test Strategy and Coverage

## Overview
Provide an evidence-first contract for risk-based QA strategy, coverage matrix, unit, integration, gameplay, platform, regression, automation, ownership, and exit criteria.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use to summarize one playtest or merely run an existing test command.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Define scope, quality risks, supported platforms, environments, and release gates.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Map risks to unit, integration, gameplay, network, data, performance, security, and compatibility coverage.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Assign owners, fixtures, automation candidates, evidence artifacts, and triage policy.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Define regression selection, entry criteria, exit criteria, waivers, and BLOCKED handling.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Publish gaps and a prioritized implementation roadmap without inventing coverage.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `qa-strategy.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
