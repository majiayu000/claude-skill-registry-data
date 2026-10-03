---
name: refactor
description: Safely restructure existing code to improve clarity, reduce duplication, or modernize patterns — without changing external behavior. Use when the user says "clean this up", "modernize", "refactor", "reduce duplication", or "simplify".
allowed-tools: Read, Grep, Glob, Bash
---

# Safe Refactoring

Read `learnings.md` beside this file before starting; append an entry when a "safe step" turned out not to be.

## Governing Principle

> **Refactoring is behavior-preserving transformation.** The external contract (inputs, outputs, side effects) must not change. If behavior needs to change, that's a feature — design it first with `/system-design`.

## Procedure

1. **Discover** — read the code to be refactored AND all its consumers. Map:
   - What calls this code? (grep for imports, function calls)
   - What does this code call? (dependencies, services, DB)
   - What is the public contract? (parameters, return type, side effects)
   - Are there tests? If yes, run them first to establish the green baseline.

2. **Diagnose** — name the specific debt being addressed:
   | Debt type | Signal |
   |---|---|
   | **Duplication** | Same logic in 2+ places with minor variations |
   | **Wrong abstraction** | A "shared" module that requires `if/else` for each caller |
   | **Boundary violation** | Logic in the wrong layer (DB query in a component, UI logic in a service) |
   | **Dead code** | Unused exports, commented-out blocks, unreachable branches |
   | **Pattern drift** | Code written before the current conventions were established |
   | **Complexity** | Function does too many things; long parameter lists; deep nesting |

3. **Decompose** — break the refactor into the smallest safe steps. Each step must independently leave the code in a working state. Order by dependency (extract first, then replace callers).

4. **Scaffold** — for each step:
   - Write the new structure following the project's current patterns (`/patterns`)
   - Migrate one consumer at a time
   - **Validate** after each step (lint + typecheck at minimum)
   - Never have both old and new code "live" for more than one step

5. **Instrument** — after all steps:
   - Run full lint + typecheck
   - Run tests if they exist
   - Grep for any remaining references to the old structure
   - Verify no new `any` types were introduced as shortcuts

## Constraints

- **No behavior changes.** If you discover a bug during refactoring, fix it in a separate, explicit step and note it.
- **No new dependencies.** Refactoring should reduce complexity, not add libraries.
- Preserve all existing comments and docstrings that describe intent (not implementation).
- If the refactor touches more than 5 files, present the plan before executing.

## Handoffs

- Refactor reveals an architectural problem → `/system-design`.
- New code must follow established patterns → `/patterns`.
- User wants to understand why code was structured this way → `/teach`.
- Refactor complete → `/full-review` to validate.
