---
name: review-swarm
description: Use when reviewing a known change set through parallel read-only code, architecture, test, safety, or product lanes with disjoint concerns and one integrator verdict.
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
    lifecycle_stage: review
    risk_level: read-only
    packs: [studio-core]
    side_effects: none
    artifact: review-verdict.md
    required_evidence: [lane-findings, affected-paths, integrator-verdict]
    owner: HoaTV Studio
    reviewer: null
    maturity: beta
    last_reviewed: 2026-08-07
    provenance:
      derived_from:
        repo: Dimillian/Skills
        path: review-swarm/SKILL.md
        commit: 05ba982bfeb0d77d3c97d4542b0ee15034d05f84
        license: MIT
      patterns_from: [AGENTS.md multi-agent ownership]
      copied_text: none
---
# Review Swarm

## Overview
Parallelize independent review questions, never write ownership. Reviewers remain read-only and the integrator owns deduplication and the final verdict.

## When to use
Use for a known diff, pull request, generated output, architecture change, safety review, or release candidate that benefits from independent lenses.

## When NOT to use
Do not use when the failure is unknown and needs hypothesis discovery; route that work to `bug-hunt-swarm`. Do not use when lanes would need to edit the same files.

## Required inputs and context discovery
Require the exact change set, repository snapshot, review questions, lane boundaries, affected paths, applicable contracts, severity model, and integrator owner.

## Safety and risk level
All lanes are read-only. Reviewers may inspect files and run non-mutating checks but may not edit, commit, start services, import data, or alter generated state.

## Workflow
1. Freeze the review target and define non-overlapping lane questions.
   Completion criterion: every concern has one lane and no lane owns writes.
2. Give each lane the minimum repository context and exact evidence format. Add one optional independent dependency/impact lane when a fresh provider is available; the lane stays read-only, owns graph blast-radius findings, owns source disagreements and missing coverage, and cannot issue runtime PASS.
   Completion criterion: lane reports cite affected paths and concrete evidence.
3. Run lanes independently without sharing conclusions mid-review.
   Completion criterion: findings are not contaminated by another lane’s verdict.
4. Integrate, deduplicate, calibrate severity, and record counterevidence.
   Completion criterion: each retained finding is actionable and source-backed.
5. Issue PASS, NEEDS WORK, or BLOCKED and assign fixes to a separate write owner.
   Completion criterion: reviewers still have no write scope.

## Evidence and output contract
Produce lane reports, affected locations, evidence, counterevidence, severity, recommended next step, and one integrator verdict.

## Handoff contract
Record target revision, lane assignments, commands run, findings accepted or rejected, unresolved disagreements, and exact write-owner follow-ups.

## Pitfalls and anti-rationalization
- More lanes do not improve quality when concerns overlap.
- Reviewers may not “quickly fix” issues they discover.
- A clean static review does not prove runtime behavior.
- Duplicate findings must not inflate severity.
- Graph extraction, inferred semantics, and runtime behavior are separate evidence classes; stale or unsupported graph data is BLOCKED.
- A BLOCKED graph lane never becomes a clean dependency finding; source review continues independently.

## Verification checklist
- [ ] Target revision is fixed.
- [ ] Lanes are independent and read-only.
- [ ] Findings cite paths and evidence.
- [ ] Integrator verdict handles duplicates and counterevidence.
- [ ] Any fixes have separate ownership.

## References and scripts
Use repository diffs and native static checks as read-only evidence sources. The kit-maintenance helpers `scripts/validate.py` and `scripts/secret_scan.py` are available only in a full repository clone.
