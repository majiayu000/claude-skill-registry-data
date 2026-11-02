---
name: nexora-ci-resource-budget
description: "Prevents CI jobs and test suites from exhausting memory, CPU, disk, or execution time as the engine grows."
---

# nexora ci resource budget

## Purpose

Use this workflow for NEXORA-scale engine work when continuous integration resource budgets. Inspect the current code before proposing implementation details; do not assume an unverified subsystem exists.

## Required inputs

- Relevant source files, owning crates/modules, and the current diff or incident.
- Acceptance criteria, compatibility constraints, and known resource budgets.
- Existing tests, logs, fixtures, and reproduction steps where available.
- Explicit unknowns and assumptions requiring confirmation.

## Workflow

1. Measure current job duration and peak resource use.
2. identify expensive tests and duplicated setup.
3. define per-job time and memory budgets.
4. shard only independent deterministic suites.
5. cap parallelism based on runner capacity.
6. cache reproducible artifacts with versioned keys.
7. preserve diagnostics on timeout.
8. test budget enforcement.
9. monitor trend changes.
10. document which checks are required versus advisory.

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

CI completes within declared resource budgets without silently skipping required validation.

Do not mask failures by increasing timeouts indefinitely. Avoid shared mutable fixtures across parallel jobs.

## Trigger examples

- **Positive:** A code change or incident directly involves continuous integration resource budgets and needs reproducible validation.
- **Positive:** Reviewers need explicit invariants, boundary cases, and failure recovery for this subsystem.
- **Negative:** The task is unrelated to this subsystem or asks for speculative changes without source evidence.
- **Negative:** The request is only documentation/content work with no runtime or code behavior impact.
