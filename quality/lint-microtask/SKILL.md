---
name: lint-microtask
description: Validate that a code file complies with the ≤50 effective lines micro-task rule
version: 2.0.0
tags: [validation, microtask, pdca-t, phase-4, phase-7]
trigger_keywords: [lint, microtask, validate, lines, split]
requires_approval: false
estimated_duration: 2-5 seconds
---

# Skill: Lint Microtask

## Purpose

Validate that a source code file complies with the ≤50 effective lines micro-task constraint. "Effective lines" excludes blank lines, comment-only lines, and import/using lines.

## When to use

- After implementing any micro-task in Phase 4
- During the **Check** step of the PDCA-T cycle (Plan → Do → **Check** → Act → Test)
- Before marking a micro-task as complete
- When a file appears to exceed the 50-line budget

## How to run

```bash
# Single file
node packs/enterprise-microtask-planner-pack/validators/microtask-linter/src/index.ts \
  --task=src/payments/domain/money.ts

# All files in a directory
node packs/enterprise-microtask-planner-pack/validators/microtask-linter/src/index.ts \
  --dir=src/payments/ --recursive

# Custom line limit
node packs/enterprise-microtask-planner-pack/validators/microtask-linter/src/index.ts \
  --task=src/file.ts --max-lines=40
```

## Supported languages

- TypeScript (`.ts`, `.tsx`)
- JavaScript (`.js`, `.mjs`, `.cjs`)
- Python (`.py`)

## Output interpretation

**PASS:**
```
✓ src/payments/domain/money.ts — PASS (38 effective lines)
```

**FAIL with split suggestions:**
```
✗ src/payments/application/authorize-payment.ts — FAIL (67 effective lines > 50)
  Breakdown: 89 total | 67 code | 12 comments | 8 imports | 2 blank

  Suggested split (3 units):
    ├── extract: unit-1()  [lines 1–28]    ~22 effective lines
    ├── extract: unit-2()  [lines 29–55]   ~24 effective lines
    └── extract: unit-3()  [lines 56–89]   ~21 effective lines

  Result: 3 micro-tasks of ~22 lines each
```

## Action on FAIL

1. Review the split suggestions
2. Extract each suggested unit into its own file
3. Re-run the linter on each new file to confirm all pass
4. Update the micro-task backlog to reflect the split
5. Continue with the Act step of PDCA-T

## Gate rule

A micro-task that exceeds 50 effective lines cannot be marked as complete until it is split.
