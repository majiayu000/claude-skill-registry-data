---
name: phase-implement
description: Implement exactly one selected phase from an authoritative repository plan. Use when a named phase or equivalent scoped implementation unit must be completed without later-phase work.
---

# Phase Implementation

Own phase scope and orchestrate only the work required to implement it.

Before writing, stop at the first option that holds: the behavior is not needed, the codebase already has it, the standard library or platform does it, an installed dependency does it, or it fits in one clear line. Otherwise write the minimum that works in the fewest files, deleting before adding. Never cut trust-boundary validation, data-loss handling, security, accessibility, or anything explicitly requested.

## Workflow

1. Read the selected phase, applicable repository instructions, and the minimum local evidence needed to identify files, patterns, and required checks.
2. Confirm phase boundaries, prerequisites, acceptance criteria, and unchanged behavior.
3. Use `plan-update` for proven plan-mechanics defects and `spec-update` for non-plan semantic contract defects.
4. Use `behavior-implement` for product behavior. For tooling or infrastructure, implement directly and prove the change with the native checks, such as linters, validators, dry runs, or plans; use `behavior-implement` only when those checks cannot show behavior that matters.
5. Implement only the phase and prerequisites required for it to work.
6. Run phase-required and focused checks, fixing only scoped implementation failures.
7. Report what changed, what was deliberately left out and the condition that would justify adding it, checks and alternative evidence, and remaining blockers.

Do not perform independent post-implementation validation, structural review, final closeout, commits, pushes, releases, later phases, or unrelated cleanup. Those remain separate gates unless the user explicitly requests them.

Finish at implementation evidence when the selected phase is complete, required checks pass or are explicitly blocked, and no later-phase work was introduced.
