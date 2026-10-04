---
name: sweep
description: "Two-phase code quality skill: (1) review codebase for structural smells — file LOC, method LOC, accidental complexity, test readability — producing a structured report, then (2) fix all smells via provable refactorings with ACN micro commits and green-bar-at-all-times discipline. Use this skill when the user says 'sweep', 'code review', 'find code smells', 'check method lengths', 'review for complexity', 'tidy up the codebase', 'refactor smells', or asks about long methods, test readability, or accidental complexity. Also trigger when users ask to 'clean up' or 'improve code quality' across multiple files."
metadata:
  context: fork
---

# Sweep

Two-phase code quality workflow: **Review** structural smells, then **Refactor** them away with provable safety.

The philosophy: see clearly first, then cut precisely. Every commit is provably safe. The tests never go red.

## Arguments

Accepts optional focus areas as arguments. When provided, narrow the review to those areas only:
- `readability` — naming, magic numbers, dense logic
- `method LOC` or `method-loc` — methods over 25 lines
- `file LOC` or `file-loc` — large files
- `accidental complexity` or `complexity` — unnecessary nesting, duplication, unclear flow
- `test readability` or `tests` — helper functions, non-coder readability, duplicated setup

When no arguments are given, review all areas.

## Phase 1: Review

Launch up to 2 Explore sub-agents in parallel to scan the codebase:

**Agent 1 — Source scan**: Read all source files. For each file report:
- File LOC
- Every method/function over 25 lines: file, method name, line range, exact line count
- Accidental complexity: unnecessary nesting, duplicated logic, parallel switch statements, unclear flow
- Readability issues: magic numbers without named constants, unclear naming, dense conditional logic

**Agent 2 — Test scan**: Read all test files. For each file report:
- Are there helper functions (factories, builders, assertion helpers)?
- Could a non-coder understand each test from its description and structure?
- Is there duplicated setup that should be extracted?
- Are test names descriptive enough?
- Any tests that are too long or do too many things?

### Report Format

Present findings as a structured report with these sections:

```
## File LOC (top offenders)
| File | LOC | Concern |

## Methods Over 25 Lines
| File | Method | Lines | Severity |
(Severity: Critical >60, High 40-60, Medium 30-40, Low 25-30)

## Accidental Complexity
Numbered list with file, description, and what's duplicated/nested/unclear.

## Test Readability
| File | Lines | Score /10 | Issue |

## What's Good
Acknowledge what's already clean — this matters for morale.
```

After the report, ask:
> **Would you like me to refactor all identified smells?**

Do NOT proceed to Phase 2 until the user confirms.

## Phase 2: Refactor

When the user confirms, execute refactorings using provable safety discipline.

### Step 0: Test Runner Script

Create `bin/check.sh` — a silent test runner that only outputs on failure:

```bash
#!/usr/bin/env bash
set -euo pipefail
output=$(flutter test --reporter compact 2>&1) || {
  echo "$output"
  exit 1
}
```

Adapt the test command to the project's stack:
- Flutter: `flutter test --reporter compact`
- Dart: `dart test`
- Node/JS: `npm test`
- Python: `pytest -q`
- Go: `go test ./...`
- Rust: `cargo test`

Run it once to verify green, then commit: `t - add silent test runner script`

### Refactoring Order

This order exists because each phase makes the next safer:

**1. Test helpers first** — Factory functions, state builders, assertion helpers. These reduce boilerplate and make tests more readable, but more importantly they make the test suite more resilient to the source refactorings that follow.

**2. Source code extractions** — Extract method, extract variable. Break long methods into composed pieces. Each extraction is one commit.

**3. Accidental complexity** — Deduplicate patterns, replace magic numbers with named constants, extract shared logic. These are often enabled by the extractions in step 2.

### Provable Refactorings

Only use refactorings that are provably behavior-preserving:

| Refactoring | What it does |
|---|---|
| **Extract method** | Move lines into a new method, call it from the original site |
| **Extract variable** | Name a sub-expression |
| **Inline** | Replace a call/variable with its definition |
| **Rename** | Change a name everywhere |
| **Extract constant** | Replace magic number/string with a named constant |
| **Move** | Relocate code to a better home |

If a change cannot be proven safe by inspection alone, use **parallel change**: add the new version alongside the old, migrate all callers, then remove the old version. Each step is its own commit.

### Arlo's Commit Notation (ACN)

Every commit message starts with a prefix that communicates intent and risk:

| Prefix | Meaning | Risk |
|---|---|---|
| `t` | Test-only change | Known safe |
| `r` | Provable refactoring | Provably safe |
| `e` | Extract (method, class, variable) | Provably safe |
| `R` | Rename | Provably safe |
| `F` | Feature (new behavior) | Requires review |
| `B` | Bugfix | Requires review |

Format: `<prefix> - <description>`

Examples:
- `t - add mealRecord() helper to meal_summary_test`
- `r - extract _playIfNotMuted from _executeEffects`
- `e - extract _buildMuteButton from MealScreen.build`
- `R - rename processResult to mealTransition`

### Green Bar Protocol

This is non-negotiable. After every single commit:

1. Run `bin/check.sh`
2. If it fails: fix the issue, do NOT commit the broken state
3. Only commit when green

After all commits are done, run the project's static analyzer (`flutter analyze`, `eslint`, `mypy`, etc.) and fix any warnings introduced.

### Execution Pattern

For each smell from the review:

1. Read the file (if not already in context)
2. Make the extraction/change
3. Run `bin/check.sh` — silent means green
4. Commit with ACN prefix
5. Move to next smell

Keep commits small. One extraction = one commit. Do not batch multiple changes.

### Verification Sub-Agent

After all refactoring commits are done, launch a review sub-agent to double-check:
- All tests still pass
- Static analysis is clean
- No methods over 25 lines were introduced
- No new smells were created during refactoring
- Commit messages follow ACN notation

Report the final commit log with all ACN-prefixed messages as a summary.

## Principles

These guide judgment calls throughout the workflow:

- **"Make the change easy, then make the easy change"** (Kent Beck) — test helpers before source refactors
- **Provable over plausible** — if you can't prove a refactoring preserves behavior, use parallel change
- **Micro commits** — small commits are reviewable, revertable, and tell a story
- **Green bar at all times** — broken tests mean stop and fix before continuing
- **Skip what's clean** — not every smell is worth fixing. If extracting a method just moves code without improving clarity, skip it and say why
