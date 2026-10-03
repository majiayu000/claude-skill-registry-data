---
name: plan-critic
description: >-
  Challenge a proposed implementation plan before execution: scope, dependency
  order, PR slicing, risk, test adequacy, operational readiness. Use when the
  user asks to review, critique, or stress-test a plan, or after plan-from-rfc
  when a second pass is wanted.
---

# Plan Critic

Challenge an implementation plan before anyone executes it.

## Input collection

If missing, ask for:

1. Plan text to review (required)
2. Source document (RFC URL/path) if available
3. Constraints (time, risk tolerance, no-behavior-change, testing limits)

## Review checklist

Evaluate and report on:

1. Scope clarity (in/out, non-goals, hidden expansion risk)
2. Dependency order (technical and process dependencies)
3. PR slicing quality (too broad, too coupled, conflict-prone)
4. Risk coverage (runtime regressions, migration risk, rollback viability)
5. Test adequacy (targeted tests, hotspot checks, missing integration/E2E)
6. Decision traceability (explicit decisions vs assumptions)
7. Operational readiness (release approach, feature flags, observability/support)
8. Contract safety (does any step change an externally consumed surface without the `contract-guard` treatment?)

## Output format (exact order)

1. **Verdict** (`Go`, `Go with changes`, or `No-go`)
2. **Critical Gaps** (must-fix)
3. **Important Improvements** (should-fix)
4. **Revised PR Sequence** (if needed)
5. **Minimum Test Gate**
6. **Approval Questions**

## Rules

- Be direct and evidence-based.
- Prefer minimal changes to make the plan executable.
- Flag assumptions explicitly.
- If the plan is already solid, say so and keep only minor improvements.
