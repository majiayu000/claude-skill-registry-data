---
name: aisolve
description: Use when asked to resolve one tractable TODO or XXX comment from a codebase; selects, implements, and verifies a real fix.
version: 1.0.0
license: MIT
---

# Solve One TODO

Read the repository's `AGENTS.md` and preserve unrelated work.

## Workflow

1. Run `git grep -nE 'TODO|XXX'` and exclude generated, vendored, fixture, and dependency trees.
2. Choose one bounded comment whose intended behavior can be established from nearby code, callers, tests, history, or documentation. Do not select randomly when candidates differ materially in risk.
3. Trace the affected path end to end. State the behavior the comment requires and one observable success check.
4. Add or identify a focused regression test when the comment represents missing behavior or a bug.
5. Implement the smallest complete fix. Remove or update the comment only when its obligation is actually satisfied.
6. Run the focused test, the nearest relevant broader check, and `git diff --check`.
7. Inspect the final diff to confirm that only the selected TODO and its required test/support changes are included.

## Completion Gate

- The selected comment's obligation is implemented, not hidden or reworded.
- The relevant verification passes after the final edit.
- Remaining TODOs are untouched.
- The receipt names the resolved location, changed files, commands run, and observed results.
