---
name: simple-check
description: Pre-ship review of the change just made, ending with a ship verdict. Use after finishing a feature or fix, or when the user asks to check, verify, or sanity-check changes. Reports only.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Check

Evaluate the change that was just made, not the whole codebase. Scope is the current diff (`git diff` and `git diff --staged`), or the files changed in this session if there is no diff.

## Criteria

1. The change is logically correct and does what was intended
2. Existing functionality is intact, with no regressions, broken flows, or side effects
3. Related code is updated too, such as call sites, types, tests, and docs
4. Naming, structure, and patterns follow the repo's conventions
5. Nothing is left behind, such as debug logs, commented-out code, TODOs, or secrets

## Rules

- Read the surrounding code and usages, not just the diff.
- Run the project's build, type check, lint, or tests when available. If you cannot, say what was not run.
- Report only real issues you can point to. Do not pad with nitpicks.
- Report only. Do not change code unless the user asks.

## Output

- Issues found, each with `file:line` and what to fix
- Verdict: ready to ship, or not, and the blockers
