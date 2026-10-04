---
name: audio-content-pipeline-review
description: Use when music, voice, SFX, ambience, or middleware content needs review across source ownership, loudness, codec, streaming, looping, localization, routing, memory, concurrency, platform limits, and integration; not for generic performance budgeting.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos, console, mobile, web]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: build
    risk_level: read-only
    packs: [content-production]
    side_effects: none
    artifact: audio-pipeline-review.json
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
# Audio Content Pipeline Review

## Overview
Provide an evidence-first contract for audio source, loudness, codec, streaming, looping, localization, routing, middleware, memory, concurrency, and platform limits.

## When to use
Use only for the trigger conditions in the description and when the requested artifact needs explicit owners, evidence, limitations, and verification.

## When NOT to use
Do not use for broad frame-time budgeting without audio pipeline evidence.

## Required inputs and context discovery
Collect exact project and build identity, requested scope, owners, dependencies, constraints, existing evidence, commands, artifact paths, risks, approvals, rollback or recovery, and unavailable information.

## Safety and risk level
Risk level is `read-only`. Read-only review never authorizes mutation. Any load, rollout, publication, service, database, credential, or external-system action requires explicit human approval and bounded stop conditions.

## Workflow
1. Bind source audio, rights, owner, target event, platform, and middleware version.
   Completion criterion: evidence is recorded and unresolved items are explicit.
2. Check sample rate, channels, loudness, peaks, silence, loops, and edit boundaries.
   Completion criterion: evidence is recorded and unresolved items are explicit.
3. Review codec, quality, streaming, preload, memory, concurrency, ducking, and routing.
   Completion criterion: evidence is recorded and unresolved items are explicit.
4. Trace localization, subtitles, fallback, event references, and generated banks.
   Completion criterion: evidence is recorded and unresolved items are explicit.
5. Return evidence-backed issues with audible reproduction and validation targets.
   Completion criterion: evidence is recorded and unresolved items are explicit.

## Evidence and output contract
Produce `audio-pipeline-review.json` with scope, snapshot, findings, owners, commands and exit codes, artifacts, acceptance criteria, Verified facts, Snapshot assumptions, Unverified hypotheses, BLOCKED items, and next actions.

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
