---
name: cpp-server-crash-triage
description: Use when triaging a C++ game server crash, dump, access violation, segmentation fault, stack trace, symbols, or build identity into a stable signature and ranked root-cause plan.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic]
  versions: [cpp17+]
  platforms: [windows, linux]
metadata:
  studio:
    type: diagnostic
    lifecycle_stage: verify
    risk_level: read-only
    packs: [cpp-lua-mmorpg]
    side_effects: none
    artifact: cpp-crash-triage.json
    required_evidence: [build-id, crash-signature, stack-frames]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-08
    provenance:
      derived_from: none
      patterns_from: [evidence-first-debugging, registry/capabilities.yaml domain catalog]
      copied_text: none
---
# Cpp Server Crash Triage

## Overview
Turn a crash dump or stack trace into a build-bound stable signature, symbol state, first application frame, ranked hypotheses, and next discriminating experiment.

## When to use
Use for access violations, segmentation faults, aborts, corrupted stacks, watchdog crashes, or repeated server dump signatures.

## When NOT to use
Do not use for static packet schema drift, ordinary log errors without a crash, or live service control.

## Required inputs and context discovery
Collect build ID, executable hash, platform, compiler, dump/core path, exception or signal, thread, raw frames, symbol paths, recent changes, reproduction state, and protected production paths.

## Safety and risk level
Read-only triage. Do not restart production, attach invasive debuggers, upload private dumps, or modify symbol stores without authorization.

## Workflow
1. Bind the dump and symbols to an exact build snapshot.
   Completion criterion: mismatched or missing symbols are explicit.
2. Normalize volatile addresses into a stable crash signature.
   Completion criterion: equivalent stacks group without hiding frame differences.
3. Identify the first application-owned frame and relevant thread context.
   Completion criterion: source blame is not assigned to runtime frames alone.
4. Rank hypotheses using exception type, frames, logs, and recent changes.
   Completion criterion: each hypothesis has supporting and counter evidence.
5. Define the smallest safe reproduction, instrumentation, or symbol action.
   Completion criterion: service-control work remains BLOCKED pending approval.

## Evidence and output contract
Produce `cpp-crash-triage.json` with build identity, signature, normalized frames, symbol state, ranked hypotheses, limitations, and next experiment.

## Handoff contract
Record build/dump paths, signature, first application frame, symbol gaps, attempted reproductions, suspect paths, and next action owner.

## Pitfalls and anti-rationalization
- Raw addresses are not stable signatures.
- A top frame without matching symbols is not a root cause.
- Do not upload dumps that may contain credentials or player data.
- An unreproduced crash remains Snapshot or Unverified.

## Verification checklist
- [ ] Dump matches the recorded build.
- [ ] Frames are normalized without losing order.
- [ ] Symbol limitations are explicit.
- [ ] Hypotheses cite evidence.
- [ ] Next action is safe and bounded.

## References and scripts
Read [references/commands.md](references/commands.md) for Windows and Linux symbolization commands. Use the bundled [scripts/crash_triage.py](scripts/crash_triage.py) for normalized fixtures and project-specific debugger tooling for authorized dump inspection.
