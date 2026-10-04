---
name: platform-device-compatibility-matrix
description: Use when a game needs a platform and device compatibility matrix across OS, hardware, GPU, memory, resolution, input, network, storefront, certification, test evidence, and support policy; not for store metadata preparation.
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
    risk_level: read-only
    packs: [production-management]
    side_effects: none
    artifact: compatibility-matrix.json
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
# Platform Device Compatibility Matrix

## Overview
Provide an evidence-first contract for platform, device, OS, CPU, GPU, memory, resolution, input, network, storefront, certification, and support evidence.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use only to prepare store screenshots, metadata, or submission forms.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Define supported platforms, minimum and recommended tiers, regions, and support policy.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Enumerate representative devices, OS versions, hardware, display, input, and network conditions.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Bind each matrix cell to build identity, scenario, command, artifact, and freshness.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Record certification, storefront, accessibility, peripheral, and degradation risks.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return supported, unsupported, conditional, or BLOCKED verdicts without extrapolation.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `compatibility-matrix.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
