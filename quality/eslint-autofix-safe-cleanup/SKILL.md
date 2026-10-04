---
id: quality.eslint.eslint-autofix-safe-cleanup
name: ESLint Autofix Safe Cleanup
description: >
  Applies ESLint autofix only when the fixes are mechanical and safe, keeping the change small, reviewable, and separated from semantic refactors.
stack:
  - JavaScript
  - TypeScript
category: eslint
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - eslint autofix
  - safe cleanup
  - lint fix
  - auto fix
  - mechanical fix
compatibility:
  runtime:
    browser: true
    node: true
---

# ESLint Autofix Safe Cleanup

## Purpose

Use this skill to apply ESLint autofix only when the changes are mechanical and safe.

The goal is to avoid turning `eslint --fix` into a semantic refactor disguised as formatting.

The core rule is simple:

```txt
Autofix only what you can review as mechanical.
```

## When to Use

Use this skill when:

- lint errors are auto-correctable
- the diff can stay small
- formatting and semantics are separable
- cleanup needs to be incremental

## Do

Review the diff before accepting it.

Keep format, refactor, and logic changes separate.

Validate with the project checks after the fix.

## Do Not

Avoid accepting a massive autofix without inspection.

Avoid mixing semantic and mechanical changes.

Avoid using autofix when the rule change is ambiguous.

## Review Checklist

- [ ] The fix is mechanical.
- [ ] The diff is small.
- [ ] Behavior is unchanged.
- [ ] Validation passed.

## Expected Output

1. Decide whether autofix is safe.
2. Apply only mechanical changes.
3. Review the diff.
4. Validate the result.
5. Keep the refactor bounded.
