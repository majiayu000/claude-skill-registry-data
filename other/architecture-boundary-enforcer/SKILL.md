---
name: architecture-boundary-enforcer
description: Define and mechanically enforce architecture boundaries for a repo. Use when a project needs allowed dependency rules, forbidden imports, layer documentation, dependency maps, circular dependency checks, or protection against agent-created architectural drift.
---

# Architecture Boundary Enforcer

## Purpose

Make architecture copyable and enforceable. Agents copy local patterns, so preferred boundaries must be documented and checked mechanically where possible.

## Inspect First

- source tree and module layout
- imports between major directories
- framework conventions
- existing lint rules, dependency-cruiser config, import-linter config, or custom checks
- architecture docs and ADRs

## Procedure

1. Infer current architecture.
   - Identify layers, modules, cross-cutting utilities, and data boundaries.
   - Do not invent a strict model that conflicts with the repo's real structure.

2. Define allowed dependencies.
   - Start with a permissive baseline that catches obvious violations.
   - Document known gaps instead of creating noisy false positives.

3. Add enforcement.
   - TypeScript/JavaScript: prefer dependency-cruiser, ESLint import rules, or a small local script.
   - Python: prefer import-linter or a small local script.
   - Other stacks: prefer existing ecosystem tools before custom checks.

4. Create docs.
   - `docs/architecture/overview.md`
   - `docs/architecture/boundaries.md`
   - ADR for major boundary decisions when useful.

5. Wire validation.
   - Add or update `scripts/check-boundaries`.
   - Scope custom text/import scans to source file extensions only; do not scan docs, generated route trees, or `AGENTS.md` unless the check is explicitly about documentation.
   - Include it in `scripts/validate`.
   - Route recurring boundary review findings to `review-feedback-promoter` so repeated violations become durable checks.

## Boundary Doc Requirements

- List layers or modules.
- State allowed imports.
- State forbidden imports.
- Name approved cross-cutting access patterns.
- Give concrete examples of correct and incorrect placement.
- Explain how to update the boundary when architecture changes.

## Validation

- Run the boundary check.
- Confirm the check catches at least one synthetic or known violation when safe to test.
- Confirm false positives are documented or tuned away.

## Completion Criteria

- Agents know where new code belongs.
- Forbidden dependencies are executable checks, not only prose.
- Architecture docs match the current source tree.
