---
name: golden-pattern-extractor
description: Identify preferred local implementation patterns and encode them for agents to copy. Use when a repo has inconsistent patterns, needs canonical examples, templates, or docs/quality/golden-patterns.md updates.
---

# Golden Pattern Extractor

## Purpose

Find the best examples already in a repo and turn them into copyable guidance so agents replicate good patterns instead of accidental ones.

## Inspect First

- repeated implementations across source directories
- architecture docs, tests, lint rules, technical debt docs, and recent reviews
- examples of both preferred and deprecated patterns

## Procedure

1. Find candidate patterns.
   - Look for repeated handlers, services, components, migrations, errors, tests, and config modules.
   - Prefer examples that are simple, tested, and aligned with architecture docs.

2. Choose golden examples.
   - Document why each example is preferred.
   - Mark deprecated or risky alternatives clearly.

3. Encode patterns.
   - Update `docs/quality/golden-patterns.md`.
   - Add templates only when the pattern is frequently repeated and stable.
   - Recommend lint or boundary checks when misuse is common.

4. Coordinate cleanup.
   - Use `entropy-auditor` for broad drift findings.
   - Use `agent-reviewer` to check pattern migrations.

## Validation

- Confirm each golden pattern points to a real source path.
- Confirm examples are current and tested where feasible.
- Confirm deprecated patterns have a replacement.

## Completion Criteria

- Agents know exactly which local examples to copy and which to avoid.
