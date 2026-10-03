---
name: code-review
description: Review code for correctness, security, and maintainability with severity-ranked findings. Use when reviewing pull requests, diffs, local changes, or when the user asks for a code review.
---

# Code review

## Quick start

1. Determine scope: uncommitted diff, branch vs base, or named files/PR.
2. Prefer `git status`, `git diff`, and (if needed) `git log` / PR view via `gh`.
3. Review for correctness, edge cases, security, and maintainability against project conventions and `.specify/memory/constitution.md` when present.
4. Report findings only; do not rewrite code unless the user asks.

## Checklist

- [ ] Logic correct; edge cases and error paths handled
- [ ] No obvious security issues (injection, authz gaps, secret leakage)
- [ ] Matches existing style and architecture
- [ ] Changes scoped; no unrelated churn
- [ ] Tests cover behavior changes (or gap called out)
- [ ] Spec Kit tasks/spec still accurate if this is feature work

## Feedback format

- Critical: must fix before merge
- Suggestion: should improve
- Nice to have: optional

For each finding: location, why it matters, concrete fix direction.
If nothing material: say so briefly.

## Over-engineering

For a delete-list focused on unnecessary abstractions, deps, or boilerplate, prefer
`/ponytail-review` (diff) or `/ponytail-audit` (whole repo) instead of this skill.
