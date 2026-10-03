---
name: rebase-onto-main
description: Rebase the current branch onto main with guardrails. Manual command — run with /rebase-onto-main when the user asks to rebase the current branch on main.
disable-model-invocation: true
---

# Rebase Onto Main

Rebase the current branch onto the latest `main` safely.

1. **Branch + cleanliness checks**
   - Run `git branch --show-current`; abort if on `main`/`master`.
   - Run `git status --short`.
   - If the working tree is dirty, stop and ask whether to commit or stash first.

2. **Fetch latest main**
   - Run `git fetch origin main`.
   - If the default branch isn't `main`, detect it (`git remote show origin`) and use that instead throughout.

3. **Rebase**
   - Run `git rebase origin/main`.

4. **Conflict handling (mandatory)**
   - If a conflict occurs:
     - Run `git status --short` and report conflicted files.
     - Stop and ask the user whether to continue resolving, abort (`git rebase --abort`), or take a narrower scope.

5. **Post-rebase verification**
   - Run `git status`.
   - Run `git log --oneline -5` for a quick verification summary.
   - If the branch was previously pushed, note that the next push requires `--force-with-lease` — never plain `--force`.
