---
name: qa-matrix
description: Create QA matrices for features, releases, platforms, browsers, devices, roles, permissions, and risk areas. Use when Codex is asked to organize test coverage, release QA, compatibility checks, or risk-based validation into a matrix.
license: MIT
---

# QA Matrix

## Core Workflow

1. Identify feature scope, users, platforms, roles, risk areas, release gates,
   and supported environments.
2. Define matrix dimensions: scenarios, browsers, devices, APIs, roles,
   permissions, data states, locales, accessibility, and performance.
3. Prioritize coverage by risk and user impact.
4. Mark required, optional, automated, manual, blocked, and out-of-scope cells.
5. Add evidence needed for each required row.
6. Summarize release recommendation and gaps.

## Safety Rules

- Do not treat a matrix as passed without evidence.
- Do not expand scope so broadly that critical risks become hard to see.
- Escalate uncovered high-risk rows before release.

## Deliverable Shape

For QA matrices, provide:

- Scope and assumptions
- Matrix dimensions
- Required coverage table
- Priority and owner
- Evidence needed
- Gaps and blockers
- Release recommendation

## References

- Read `references/qa-matrix-checklist.md` when building or reviewing a QA
  matrix.
