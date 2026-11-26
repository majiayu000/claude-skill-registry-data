---
name: refactoring
description: >-
  Changes code structure without changing behaviour. Use when the user asks to refactor, clean up, restructure, extract, rename across files, reduce duplication, or improve the architecture. Not for features, bug fixes or reviews.
license: Apache-2.0
metadata:
  level: "method"
  uses: "tdd"
  agents: ""
  tokens: "542"
---

Restructure code in small steps with the tests green after each one, so behaviour stays identical.

Uses: foma-skills:tdd (add a characterisation test when coverage is missing).

Path: a rename or extract inside one file → steps 1, 2, 4, 5; a change across modules, public interfaces or many call sites → all steps, and confirm the plan with the user before step 4. Say which path in one line.

## Steps
1. Read the CLAUDE.md conventions and test/lint/build commands, and match existing patterns and names. Scope: the user's target; with none, start from files that change often (`git log --oneline --name-only`).
2. Run the suite first and note the result as the baseline. Already-failing tests stay the baseline: the refactor may not change that set. If they fail in the code you are about to change, stop and report.
3. No tests around the code to change: write characterisation tests that pin current behaviour (including odd behaviour) through foma-skills:tdd, and see them pass before touching the code.
4. Plan (full path): list the steps, each small and independently green, with the end shape. Prefer deleting a shallow wrapper or merging scattered logic behind one interface (deletion test: does removing it concentrate complexity or just move it?). Skip changes that contradict a recorded decision (`docs/decisions.md`, ADRs) unless the friction is real; say so.
5. Apply one step, run the tests (the targeted ones; the whole suite after the last step), then the typecheck or lint. Repeat. Remove dead code your steps made unused.

## Rules
- Never mix a behaviour change into a refactor; a bug or missing feature you notice goes into the report, unfixed.
- A step that turns red is reverted, not patched forward; if it stays red after one retry, stop and report.
- Never change a test's expectations to get green; only move or rename tests with the code.
- Do not refactor beyond the request; list tempting extras as ideas.
- Rename or move public API only after the user agrees.

## Report
- What changed structurally, files touched, path taken.
- Evidence: tests and typecheck before and after.
- Noticed but not changed: bugs, extras.
- Not checked: <…>
