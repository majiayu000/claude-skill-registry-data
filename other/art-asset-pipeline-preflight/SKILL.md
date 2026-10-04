---
name: art-asset-pipeline-preflight
description: Use when source art or game assets need preflight across naming, ownership, DCC export, scale, pivots, materials, textures, LOD, collision, compression, import settings, budgets, and delivery; not for GUID-only audits.
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
    lifecycle_stage: build
    risk_level: read-only
    packs: [content-production]
    side_effects: none
    artifact: art-asset-preflight.json
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
# Art Asset Pipeline Preflight

## Overview
Provide an evidence-first contract for source art ownership, naming, export, scale, pivot, material, texture, LOD, collision, compression, import, and budget.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use for a narrow Unity GUID/meta integrity check or bulk reimport.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Bind assets to source files, owners, target platforms, engine version, and budget.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Check naming, hierarchy, scale, pivots, transforms, topology, UVs, and material slots.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Verify export settings, texture channels, color space, compression, LOD, and collision.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Review import presets, generated outputs, dependencies, licensing, and rollback.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return per-asset PASS, FAIL, or BLOCKED with exact remediation owners.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `art-asset-preflight.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
