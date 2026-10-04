---
name: studio-handoff
description: Use when pausing, transferring, or reactivating game-studio work and a durable handoff must capture branch, goal, scope, files, commands, Verified Snapshot Unverified BLOCKED facts, failures, decisions, next actions, and a reactivation prompt.
version: 0.1.0
author: GameStudio-CodexKIT
license: MIT
compatibility:
  engines: [engine-agnostic, unity]
  versions: [any]
  platforms: [windows, linux, macos]
metadata:
  studio:
    type: workflow
    lifecycle_stage: operate
    risk_level: low
    packs: [studio-core]
    side_effects: files
    artifact: HANDOFF.md
    required_evidence: [git-status, command-summary, changed-file-list]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from:
        repo: mattpocock/skills
        path: skills/productivity/handoff/SKILL.md
        commit: 84fdeffd12f2ee307994d1eb6feb48173b6e0502
        license: MIT
      patterns_from: [sanitized studio handoff fixture]
      copied_text: none
---
# Studio Handoff

## Overview
Create a restartable state transfer that distinguishes verified work from snapshots, hypotheses, and blockers.

## When to use
Use when a session ends, ownership changes, work becomes blocked, a subsystem crosses teams, or another agent must continue without repeating discovery.

## When NOT to use
Do not create a handoff as a substitute for running available verification or resolving a small task that can be completed safely now.

## Required inputs and context discovery
Collect repository/path, branch, goal, owned and excluded scope, current Git state, files touched, commands run, artifacts, decisions, failures, open hypotheses, dependencies, and next actions.

## Safety and risk level
Writing a handoff is low-risk. Preserve existing project handoff conventions, never expose credentials, and never rewrite unrelated history or other sessions’ ownership.

## Workflow
1. Re-read the task packet, applicable instructions, and current Git status.
   Completion criterion: the handoff reflects current state rather than memory.
2. List files touched and commands run with exact results.
   Completion criterion: every PASS claim maps to fresh evidence.
3. Separate Verified, Snapshot, Unverified, and BLOCKED facts.
   Completion criterion: no hypothesis appears under Verified.
4. Record failures, decisions, ownership boundaries, and do-not-touch paths.
   Completion criterion: the next session can avoid conflicting or unsafe work.
5. Provide three to seven ordered next actions and a reactivation prompt.
   Completion criterion: another session can start with one bounded command or inspection.

## Evidence and output contract
Produce `HANDOFF.md` with repository/path, branch, goal, scope ownership/do-not-touch, files touched, commands/tests, Verified results, Snapshot assumptions, Unverified hypotheses, BLOCKED items, failures, decisions, next actions, and Reactivation prompt.

## Handoff contract
The output is the handoff contract. Keep exact paths, symbols, ports, error strings, and commands intact; sanitize secrets and raw credentials.

## Pitfalls and anti-rationalization
- Do not say “tests pass” without the command and fresh output.
- Do not omit dirty or untracked files.
- Do not bury blockers in prose.
- Do not prescribe next actions that require unavailable permissions without labeling them BLOCKED.

## Verification checklist
- [ ] Repository, branch, goal, and scope are current.
- [ ] Files and commands are exact.
- [ ] Verified, Snapshot, Unverified, and BLOCKED are separate.
- [ ] Failures and decisions are explicit.
- [ ] Three to seven next actions and a Reactivation prompt exist.

## References and scripts
Follow the project's existing `HANDOFF.md` and `.agents/CONTRACT.md` when present; otherwise use the handoff contract in `AGENTS.md`.
