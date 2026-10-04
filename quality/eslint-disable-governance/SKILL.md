---
id: quality.eslint.eslint-disable-governance
name: ESLint Disable Governance
description: >
  Governs eslint-disable usage by classifying justified versus unjustified suppressions, requiring technical justification, and cleaning up unnecessary rule disables without changing behavior.
stack:
  - JavaScript
  - TypeScript
category: eslint
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - eslint disable governance
  - eslint-disable
  - ts-ignore
  - ts-expect-error
  - lint suppression
  - disable comments
compatibility:
  runtime:
    browser: true
    node: true
---

# ESLint Disable Governance

## Purpose

Use this skill to control `eslint-disable` and similar suppressions.

Suppressions are debt. They may be justified, but they must be visible, explained, and periodically re-evaluated.

The core rule is simple:

```txt
Every suppression needs a reason and an expiry path.
```

## When to Use

Use this skill when:

- the repo has many lint suppressions
- `eslint-disable` is hiding debt
- `ts-ignore` or `ts-expect-error` needs triage
- a cleanup pass is needed before harder lint rules

## Do

Locate:

- `eslint-disable`
- `eslint-disable-next-line`
- `ts-ignore`
- `ts-expect-error`

Classify each suppression:

- justified
- temporary
- unnecessary
- suspicious

Require a technical reason for keeping it.

## Do Not

Avoid removing suppressions blindly when they protect a known issue.

Avoid allowing suppressions with no comment or ticket path when governance expects one.

Avoid changing behavior accidentally while removing a disable.

## Review Checklist

- [ ] Suppressions are found and classified.
- [ ] Justifications are technical, not cosmetic.
- [ ] Unnecessary suppressions are removed.
- [ ] Behavior is preserved.

## Expected Output

1. Inventory suppressions.
2. Classify their legitimacy.
3. Remove unnecessary disables.
4. Preserve behavior.
5. Record remaining suppressions clearly.
