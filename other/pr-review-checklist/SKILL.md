---
name: pr-review-checklist
description: 'Applies a structured, repo-aware pull request review checklist with objective pass/fail gates'
---

# PR Review Checklist

Use this skill before creating or approving a PR.

## Checklist Gates

### 1) Correctness

- Change implements intended behavior.
- Edge cases and null/undefined paths handled.
- No obvious regressions in touched flows.

### 2) Type and Build Safety

- TypeScript compiles for changed scope.
- No newly introduced diagnostics in touched files.
- Imports/exports are valid and consistent.

### 3) Testing

- Existing tests updated where behavior changed.
- New critical logic has at least focused test coverage.
- Manual validation steps are documented when tests are absent.

### 4) Security and Privacy

- Sensitive routes/actions include auth + permission checks.
- No secret/token leakage.
- Input validation/sanitization remains intact.

### 5) Maintainability

- Naming and structure follow repository conventions.
- Changes are cohesive and not unnecessarily broad.
- Comments/docs updated where behavior changed.

## Output Format

- **PASS** / **CONDITIONAL PASS** / **BLOCKED**
- Bullet list of blockers with file references
- Quick remediation list (ordered by impact)

## Handoff

Include:

- files reviewed
- validations run
- unresolved risks (if any)

<!-- Inspired by awesome-copilot reviewer/checklist conventions -->
