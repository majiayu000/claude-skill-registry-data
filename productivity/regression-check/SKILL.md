---
name: regression-check
description: Plan regression checks for bug fixes, features, refactors, and release candidates. Use when Codex is asked to identify regression risk, define a regression test plan, verify a fix, choose smoke tests, or decide what must be retested after a code change.
license: MIT
---

# Regression Check

## Core Workflow

1. Identify the changed behavior, affected surfaces, dependencies, and user
   journeys.
2. Map the change to known invariants, prior bugs, adjacent workflows, and
   compatibility requirements.
3. Start with targeted checks for the changed behavior and required repository
   gates. Add broader regression tests for plausible side effects; do not
   require every coverage type for a small change.
4. Separate automated coverage from manual, exploratory, visual, accessibility,
   performance, or data checks.
5. Specify test data, environment, permissions, feature flags, and observability
   needed for verification.
6. Stop after relevant checks pass unless new changes, failures, or unresolved
   risks justify more testing. State residual risk and, when requested, the
   release gate recommendation.

## Safety Rules

- Do not treat tests as passed unless output or evidence is available.
- Do not rely only on happy-path checks for auth, billing, data, migrations, or
  customer-facing workflows.
- Escalate when there is no reproducible baseline, missing test data, unclear
  owner, or high-risk production dependency.

## Deliverable Shape

For regression work, cover the applicable items below; combine them for small
changes and do not invent a release ceremony for a local fix:

- Changed surface
- Regression risk areas
- Direct verification tests
- Broader regression tests
- Automation versus manual coverage
- Test data and environment needs
- Release gate recommendation
- Residual risk

## References

- Read `references/regression-check-checklist.md` when planning or reviewing
  regression coverage.
