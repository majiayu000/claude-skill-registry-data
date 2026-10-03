---
name: plan-from-rfc
description: >-
  Generate a phased implementation plan from an RFC, design doc, or spec (URL
  or file). Use when the user provides an RFC/design document and wants an
  implementation plan, migration plan, or execution-ready PR breakdown from it.
---

# Plan From RFC

Turn an RFC or design document into a phased, executable delivery plan.

## Input collection

If any input is missing, ask the user first:

1. RFC source (URL or workspace file path)
2. Goal (`implement`, `refactor`, `migrate`, or `review`)
3. Constraints (timeline, risk tolerance, no-behavior-change, testing scope)
4. Output depth (`high-level` or `execution-ready PR breakdown`)

If the RFC source cannot be accessed, ask the user to paste key sections (goal, scope, constraints, decisions, risks), then continue with explicit assumptions.

## Analysis steps

1. Extract: problem statement, goals and non-goals, constraints, accepted decisions, dependencies.
2. Identify ambiguities and missing information.
3. Convert into a phased delivery plan with small, low-risk increments.
4. Keep behavior-preserving constraints explicit when requested.

## Output format (exact order)

1. **Context Summary**
2. **Assumptions**
3. **Scope In / Scope Out**
4. **Implementation Plan** — phased steps, per-step dependencies, rollback notes
5. **PR Breakdown** — one bullet per PR with intent, likely files/areas touched, and risk
6. **Test Strategy** — targeted tests first; broader checks only where risk justifies
7. **Risks and Mitigations**
8. **Open Questions for Approval**

## Rules

- Prefer small PRs over broad multi-domain PRs.
- Highlight hotspot/conflict-prone files when likely.
- Do not invent undocumented architecture decisions; mark them as open questions.
- If the user asked for a plan only, do not implement code.
- Keep commands aligned with the repo's package scripts when possible.
- To stress-test the resulting plan, follow with the `plan-critic` skill.
