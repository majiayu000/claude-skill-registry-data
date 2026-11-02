---
name: nexora-audio-voice-budget
description: "Manages simultaneous sound voices under CPU and memory limits without unpredictable priority decisions."
---

# nexora audio voice budget

## Purpose

Use this workflow for NEXORA-scale engine work when audio voice limits and sound prioritization. Inspect the current code before proposing implementation details; do not assume an unverified subsystem exists.

## Required inputs

- Relevant source files, owning crates/modules, and the current diff or incident.
- Acceptance criteria, compatibility constraints, and known resource budgets.
- Existing tests, logs, fixtures, and reproduction steps where available.
- Explicit unknowns and assumptions requiring confirmation.

## Workflow

1. Inventory voice classes and costs.
2. define active and virtualized voice limits.
3. rank by gameplay importance, distance, audibility, and recency.
4. reserve capacity for critical feedback.
5. define fade and virtualization behavior.
6. prevent priority oscillation.
7. test dense combat and ambient scenes.
8. measure voice steals and mixer cost.
9. expose rejection reason codes.

## Validation checklist

- [ ] The invariant and measurable acceptance criteria are explicit.
- [ ] Ownership, lifecycle, and failure handling are documented.
- [ ] Tests cover normal, boundary, repeated, and failure cases.
- [ ] Changes preserve source/plugin byte parity and catalog uniqueness.
- [ ] Focused tests, formatting, and applicable static checks pass; skipped checks are listed.
- [ ] Performance and reliability claims include reproducible evidence.

## Required output

Provide the decision and scope, invariants, code paths reviewed or changed, tests and results, compatibility implications, and unresolved risks.

## Boundaries and failure handling

Voice use stays bounded and priority decisions are observable and stable.

Do not rely only on distance for priority or abruptly cut critical cues without fallback.

## Trigger examples

- **Positive:** A code change or incident directly involves audio voice limits and sound prioritization and needs reproducible validation.
- **Positive:** Reviewers need explicit invariants, boundary cases, and failure recovery for this subsystem.
- **Negative:** The task is unrelated to this subsystem or asks for speculative changes without source evidence.
- **Negative:** The request is only documentation/content work with no runtime or code behavior impact.
