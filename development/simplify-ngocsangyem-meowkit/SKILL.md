---
name: mk:simplify
description: Post-implementation simplification pass. Reduces complexity without changing behavior. Use after Phase 3 (Build GREEN) and before Phase 4 (Review). Catches dead code, unnecessary abstractions, over-engineering, and redundant patterns. Triggers on "simplify", "clean up", "reduce complexity", "too complex". NOT for style/convention enforcement (see mk:clean-code); NOT for reviewing diffs or PRs (see mk:review).
argument-hint: '[file_or_directory]'
source: local
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Bash
keywords:
  - simplify
  - behavior-preserving
  - refactor
  - reduce-complexity
  - yagni-pass
when_to_use: Use for behavior-preserving simplification passes on existing code. NOT for authoring-time quality enforcement (see mk:clean-code).
user-invocable: true
owner: docs
criticality: medium
status: active
runtime: claude-code
---

# Code Simplification

Runs after implementation, before review. Reduces complexity while preserving behavior.

> For ad-hoc quality review outside the current implementation diff, use `mk:clean-code`. `mk:simplify` is behavior-preserving and scoped to the current diff only.

## Iron Rule

> **Behavior must not change.** Every simplification must pass the exact same tests as before. If tests fail after simplification, the simplification was wrong — revert it.

## What to Look For

### Remove

- **Dead code** — functions never called, variables never read, unreachable branches, import never used
- **Commented-out code** — if it's in git history, delete it from source
- **Unnecessary abstractions** — wrapper that adds no value, interface with one implementation
- **Redundant null checks** — checking null after a guard that already prevents null

### Simplify

- **Deep nesting** — 3+ levels of if/else → extract early returns or guard clauses
- **God functions** — >50 lines → extract focused helpers
- **Duplicate logic** — same pattern in 3+ places → extract shared utility
- **Complex conditions** — `if (a && !b || (c && d))` → extract to named boolean or function

### Don't Touch

- **Working code that's "not how I'd write it"** — style is not complexity
- **Performance-optimized code** — it looks complex for a reason
- **Code outside the current diff** — scope discipline, even for simplification

## Process

1. **Identify** — scan changed files for complexity signals
2. **Propose** — list each simplification with before/after preview
3. **Apply** — make changes one at a time
4. **Verify** — run full test suite after each change (not batched)
5. **Report** — list what was simplified and why

## Gotchas

- **"Just one more cleanup"** — scope creep is the #1 risk. Only simplify code from the current diff
- **Removing "dead" code that's used via reflection/dynamic import** — grep for string references, not just static imports
- **Extracting too early** — 2 copies is not enough to justify a shared utility. Wait for 3
- **Breaking public API** — simplifying internals is fine; changing exported signatures is a breaking change
- **Test-only code** — don't simplify test helpers/fixtures; they prioritize readability over DRY

## Pipeline Position

```
Phase 2 (Test — RED if `--tdd`) → Phase 3 (Build) → [mk:simplify] → Phase 4 (Review)
```

Simplification happens AFTER tests pass but BEFORE review. Reviewer sees the simplified code.
