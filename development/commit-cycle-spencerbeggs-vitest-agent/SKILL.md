---
name: commit-cycle
description: Use when reaching any TDD phase transition — spike close, red→green, green→refactor, or discard — required before exiting the phase so each cycle lands as a discrete, greppable commit in git history.
---

# Commit at every TDD phase transition

Each accepted phase transition is a checkpoint. Commit at:

- **spike**: exploratory work before writing a failing test. Commit message:
  `tdd(<goalId>:spike): <imperative summary of exploration>`
- **red→green**: test passes after the production fix. Commit message:
  `tdd(<goalId>:green): <imperative summary>`
- **green→refactor**: cleanup done, all tests still pass. Commit message:
  `tdd(<goalId>:refactor): <what changed>`
- **discard (red)**: goal or behavior abandoned with uncommitted production code in the working tree. Commit message:
  `tdd(<goalId>:red): discard — <reason>`

`<goalId>` is the bare numeric DB id returned by `tdd_goal (action: create)` (e.g., `7`).

**Examples:**

```text
tdd(7:spike): explore lifecycle.ts shape before writing test
tdd(7:green): implement sum() to pass failing assertion
tdd(7:refactor): extract add-three helper
tdd(8:green): handle negative inputs in sum()
tdd(8:red): discard — step too large, re-decomposing
```

## Rules

1. Never commit during `red` itself — by definition the suite is failing. The `red` state is for discard only: commit after abandoning the goal or behavior with uncommitted production code still in the tree.
2. If no refactor is needed after green, skip the `refactor` commit and move on.
3. The post-commit hook captures the commit hash and writes a `commits` row to the DB. It records changed files against the most-recent test run — no message-tag parsing.

## Squash after the goal is complete

After the main agent runs the seven-step audit, squash all `tdd(<goalId>:*)` commits for the goal into a single conventional commit whose type (`fix`, `feat`, `refactor`, `test`) reflects what the goal actually delivered:

```text
fix(playground): sum handles negative inputs and off-by-one

Signed-off-by: ...
```
