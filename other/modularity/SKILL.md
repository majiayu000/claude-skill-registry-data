---
name: modularity
description: "Enforce module contracts and boundaries: frontend/backend separation, repo guardrails. Smallest safe change in existing code."
---

# modularity

Contracts with checks: every module boundary names its enforcement, or it isn't a boundary.

## Activate when

- Placing new code, splitting modules, fixing cycles, or reviewing dependency direction.

## Do NOT activate for

- Language mechanics of the split (see language-modularity); framework layering (see frameworks/*).

## Structuring pipeline position

Upstream: `../../core/repository-understanding/` (map first) → language/framework identification → this skill (boundaries) + `../language-modularity/` (language mechanics) → `../../core/implementation/` → re-verify dependency direction here → `../../core/code-review/`.

## Inspection

Map modules, their public surfaces, import directions, and existing boundary checks (lint rules, CODEOWNERS, workspace edges). Find cycles, god modules, and leaked internals.

## Decision rules

- One module, one responsibility cluster; public surface minimal and versioned where external.
- Dependencies point toward stability; cycles are defects to break, not patterns to document.
- Frontend/backend (and domain/infra) separation enforced by tooling, not convention prose.
- New module only with a second consumer or a proven isolation need; otherwise a folder suffices.

## Procedure

1. State the boundary (what's inside, what's exposed, direction of deps) before moving code.
2. Move the smallest slice proving the seam; wire the check (import lint, workspace rule, or contract test).
3. Prove the check bites (violate on purpose in a scratch branch, watch it fail, revert).
4. Verify: cycles gone (tool output), surface diff reviewed, dependent tests green, check gating in CI.

## Failure modes

- Boundaries declared but unchecked; premature packages with one consumer; cycles "temporarily" tolerated; splitting without moving the coupling (same mess, more files).

## Escalation

Language specifics → language-modularity; cross-service seams → distributed/systems.

## References

- Related: `../language-modularity/`, `../cohesion-coupling/`, `../../core/repository-understanding/`.
