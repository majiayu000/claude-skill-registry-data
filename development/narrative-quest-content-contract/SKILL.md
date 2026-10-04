---
name: narrative-quest-content-contract
description: Use when narrative, quest, dialogue, objective, state, reward, localization, cinematic, and implementation teams need one explicit content contract; not for general story brainstorming or protocol review.
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
    packs: [content-production]
    side_effects: none
    artifact: narrative-quest-contract.json
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
# Narrative Quest Content Contract

## Overview
Provide an evidence-first contract for quest state, objectives, dialogue, conditions, rewards, failure, localization, telemetry, and implementation authority.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use for general story ideation, packet protocols, or live content publication.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `low`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Define player intent, narrative purpose, entry conditions, and authority.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Model states, objectives, branches, failure, recovery, rewards, and completion.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Bind dialogue, cinematic, localization, audio, UI, data, and telemetry contracts.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Identify save compatibility, replay, sequencing, and content dependency risks.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Produce implementation acceptance criteria and unresolved decisions.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `narrative-quest-contract.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
