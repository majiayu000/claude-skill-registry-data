---
name: pr-discipline
description: |
  Use this skill when ready to open a pull request or merge to main. Triggers include:
  "open a PR", "create pull request", "ready to merge", "let's review",
  "ship this", "time to merge", "submit for review", "let's get this into main".
  Always apply before invoking gh pr create or merging.
---

# PR Discipline

Enforces a clean PR workflow: up-to-date branch, green checks, full description, cross-model review,
README/TODO sync. **Nothing reaches `main` except via an approved, squash-merged PR.**

## Pre-PR checks (run before opening)

1. **Branch up to date with main:**
   ```bash
   git checkout main && git pull --ff-only && git checkout - && git rebase main
   ```
   Resolve conflicts, then `git push --force-with-lease` if rebased.

2. **All quality checks green:** `make grade` (ruff + format + mypy + tests + scanners). If any fail —
   STOP, fix, commit, push. Don't open the PR yet.

3. **README current:** any user-visible change reflected — but remember the **README is the report**
   and stays honest (no claims of results that aren't measured yet).

4. **TODO current:** tick every checkbox this branch completes, in the relevant commit.

5. **Self-review the diff** on GitHub compare view: every intended file present, no stray files
   (`.DS_Store`, IDE configs, **model weights**), no debug `print()`, no hardcoded values, tests cover
   new logic + edge cases.

## Opening the PR

```bash
gh pr create --base main --head <branch>
```
The PR template loads automatically — fill **every** section: summary (user-facing), linked PRD/PLAN
ids + TODO items, concrete changes list, checklists. End the PR body with the Claude Code trailer.

## After opening

- **Wait for CI.** Red CI → read the failure, fix locally, push (PR auto-updates). Never merge red.
- **Cross-model review is a real gate** (not optional). A separate model family reviews the PR and
  posts findings as comments. Address each: evaluate honestly (accept/reject with reasoning), apply
  fixes on the branch, and **reply on the thread** documenting the resolution. See
  `docs/REVIEW_PROCESS.md`.

## Merging

- **Squash-merge** is the default (one meaningful commit per concern; clean history).
- `gh pr merge <n> --squash --delete-branch`, then `git checkout main && git pull --ff-only`.

## Post-merge

Update `docs/PROMPTS.md` with a brief, truthful entry for the shipped work (driver, reviewer, outcome).
Only log work that is actually committed.

## Anti-patterns to refuse

Open a PR without rebasing · skip `make grade` · merge with a vague description · merge red CI ·
force-push to `main` · merge before the cross-model review is addressed.
