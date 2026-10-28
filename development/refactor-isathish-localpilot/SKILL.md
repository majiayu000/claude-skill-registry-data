---
name: refactor
description: Restructure code safely without changing behaviour — simplify, extract, rename, remove duplication or dead code, modernise — guarded by tests, types and diagnostics at every step. USE WHEN the user says "refactor", "clean up", "simplify", "extract", "rename", "split this file", "reduce duplication", "this is messy", "tech debt", "modernise/upgrade this code".
---

# Refactor

Goal: identical observable behaviour, clearer code, verified by the same tests passing before and after.

## 1. Establish the safety net
- Find and run the relevant tests before touching anything (`run_command`); note the baseline (N passed). If coverage of the area is thin, add characterisation tests first that pin current behaviour (see the `test` skill) — including the odd edge cases you intend to preserve.
- `get_diagnostics` baseline on the files involved. Commit or stash state is the user's call; don't run `git stash`/`reset` yourself.

## 2. Understand before moving
- Read the whole file(s) and every caller: `find_references` on each symbol you will change; `grep_search` for string-based references (dynamic imports, config, templates, docs).
- Identify the smells you're fixing: long function, duplication, deep nesting, god module, primitive obsession, boolean parameters, leaky abstraction, dead code, inconsistent naming. Name them in your plan so the change stays targeted.

## 3. Refactor in small, verified steps
- One transformation at a time (extract function → run tests → rename → run tests → move file → fix imports → run tests). Never combine a refactor with a behaviour change; if you find a bug, note it and fix it separately after.
- Prefer language-server-safe moves (rename via consistent edits across all references found; update exports/imports/barrels, types, tests, docs).
- Keep public APIs stable unless the user asked otherwise; when they must change, add a thin compatibility shim or update every caller in the same step.
- Simplification targets: early returns over nesting · pure functions with I/O at edges · replace comments that explain *what* with clearer names · delete dead code (confirm with `find_references` + grep) · consolidate duplicates into one well-named helper only when there are ≥ 3 copies or they must change together.
- Don't "improve" by adding abstraction layers, generic helpers for one call site, or speculative configuration.

## 4. Verify
- After each step and at the end: `get_diagnostics` on all touched files, the test suite (same count passing, no skipped), lint/typecheck/build. For UI, a quick `browser_inspect` of the affected screen.
- Diff review: `run_command` `git diff --stat` and skim the diff for accidental behaviour changes (changed conditions, defaults, error messages, ordering).

## 5. Report
- What was restructured and why (smell → remedy), file moves/renames list, proof (tests before/after, diagnostics clean), and anything you deliberately left alone or found that deserves its own task.
