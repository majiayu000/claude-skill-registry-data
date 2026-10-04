---
name: invariant-policy-checker
description: Define and evaluate deterministic invariants and policy checks for DSDS simulations. Use when encoding correctness rules, post-run validation gates, compliance constraints, and safety checks that must hold across scenarios.
---

# Invariant Policy Checker

## Overview
Turn system correctness requirements into explicit simulation checks. Report violations with severity, evidence, and likely causes.

## Workflow

1. Collect invariant candidates
- Identify invariants for idempotency, ordering, consistency, security, and SLOs.
- Convert vague requirements into measurable assertions.

2. Encode check definitions
- Define each check with id, condition, severity, and failure message.
- Map each condition to observable metrics or trace state.

3. Run post-simulation evaluation
- Evaluate checks against output metrics, traces, and events.
- Flag violations with context and impacted scope.

4. Classify and triage
- Separate hard failures from warning-level drift.
- Highlight violations that indicate systemic risk.

5. Recommend remediation
- Suggest configuration or architecture changes linked to each violation.
- Suggest follow-up scenarios to re-test fixes.

## Output format
1. `Invariant set`
2. `Violation report`
3. `Severity-ranked findings`
4. `Remediation plan`
5. `Follow-up validation scenarios`

## References
- Read `references/invariant-catalog.md` for invariant classes and examples.
- Use these repo sources:
- `canonical-catalogue/DSDS Canonical Catalogue - Policies and invariants.csv`
- `planning/IMPLEMENTATION_PLAN.md` (Phase 9.2)
- `schema/complete_simulator_schema.ts` (invariant types)
