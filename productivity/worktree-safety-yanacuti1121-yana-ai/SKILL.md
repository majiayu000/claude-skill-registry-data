---
name: worktree-safety
description: "Use when starting a new feature task, before making experimental changes, or when user says 'try this', 'experiment with', 'test out'. Ensures work happens on a branch, not directly on main."
---

# Worktree Safety Skill

Experimental or risky work should never happen directly on main. This skill ensures
a branch exists before any code changes are made.

## When to use this skill

- Starting a new feature or task that will take more than one commit
- User says "try this", "experiment", "test out an idea"
- About to make changes that are hard to reverse
- Working on something that might break existing tests

Do NOT use for: reading files, running read-only commands, answering questions.

## Workflow

### Step 1 — Check current branch

```bash
git branch --show-current
git status --short
```

If already on a feature branch (not `main` or `master`): report branch name and skip to Step 3.
If on `main` or `master`: proceed to Step 2.

### Step 2 — Create branch

Ask the user for a branch name OR suggest one based on the task:

```bash
git checkout -b task/<suggested-name>
```

Naming convention: `task/<short-slug>` — e.g., `task/fix-scope-guard`, `task/add-plan-skill`.

Verify:
```bash
git branch --show-current
```

### Step 3 — Baseline test

```bash
bash core/tests/hooks/run-hook-tests.sh 2>&1 | tail -3
```

Report:
- If tests pass: "Baseline: N tests passing. Safe to proceed."
- If tests fail: "Baseline failing before changes — investigate first. List failures."

Do not proceed with changes if baseline is failing. Ask user whether to continue.

### Step 4 — Confirm ready

Report:
```
Branch: <branch-name>
Baseline: [N tests passing | FAILING — list]
Safe to proceed: [YES | NO]
```

## Constraints

- Never create a branch named `main`, `master`, `develop`, or `release/*`.
- Never skip the baseline test — you need to know what was already broken.
- If the repo has no test suite, report that explicitly and proceed.
- If `git worktree` is available and the user wants isolation, suggest it:
  `git worktree add .worktrees/<branch-name> -b <branch-name>`
