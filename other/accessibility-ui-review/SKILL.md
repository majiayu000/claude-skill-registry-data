---
name: accessibility-ui-review
description: "Reviews UI accessibility: keyboard, focus, semantics, labels, contrast, motion, forms, dialogs, tables, and screen readers."
---

# Accessibility UI Review

Review accessibility as part of UI quality.

## Workflow

1. Read `ui-qa`.
2. Inspect semantic structure, labels, focus order, keyboard operation, visible
   focus, color contrast, reduced motion, error states, and ARIA usage.
3. Prefer actual browser checks when possible.
4. Report actionable issues with affected files or components.

## Output

- issues by severity
- evidence
- affected components
- recommended fix
- validation gaps

## Rule

Do not add ARIA to compensate for incorrect native elements when native
semantics can solve the issue.
