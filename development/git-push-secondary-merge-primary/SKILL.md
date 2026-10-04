---
name: git-push-secondary-merge-primary
description: Use when committing and pushing a work branch, then merging it into the primary branch and pushing both branches.
---

# Git Push Secondary Merge Primary

## Overview

Execute the standard two-branch handoff: finish work on the secondary branch, push it, merge it into the primary branch, push the primary branch, then return to the secondary branch.

Use "secondary branch" for the branch that contains the current work, such as `dev`, `develop`, or another integration branch. Use "primary branch" for the protected/release branch, such as `main` or `master`.

This workflow is for safe release-sync handoffs where both branches need to be pushed and the primary branch should preserve a clear merge result.

## When to Use

Use this skill when the user asks for:
- Pushing the work branch and then merging into the release branch
- A two-branch release-sync workflow such as `dev` → `main` or `develop` → `master`
- Finishing a feature on a secondary branch and propagating it to the primary branch
- Keeping a clean merge commit on the primary branch while preserving the secondary branch history

## Do Not Use

Do not use this skill for:
- Single-branch commit/push (use a normal commit + push flow)
- Force-pushing, history rewriting, or rebasing operations
- Generating reports from git history (use `git-weekly-report` instead)
- Reviewing code changes (use `code-reviewer` or `frontend-code-review` instead)

## Instructions

Follow the branch detection rules first, then execute the workflow in order. Stop and report the blocker instead of guessing when branch names, merge conflicts, dirty worktrees, or rejected pushes cannot be handled safely.

## Branch Detection

1. Prefer explicit branch names from the user.
2. If the user says `dev` or `main` but the repository uses `develop` or `master`, inspect actual branches before choosing.
3. Detect the primary branch with `git symbolic-ref refs/remotes/origin/HEAD` when available.
4. If remote HEAD is unavailable, prefer an existing `main`, then `master`.
5. Detect the secondary branch from the current branch when it is not the primary branch.
6. If currently on the primary branch and no secondary branch was specified, prefer an existing `dev`, then `develop`.
7. If the branches still cannot be determined safely, ask the user for the primary and secondary branch names.

## Instructions

Follow the workflow below exactly, preserving user changes and stopping on unsafe branch, merge, or push conditions.

## Workflow

1. Inspect repository state.
   - Run `git status --short`, `git branch --show-current`, and `git remote -v`.
   - Ensure the worktree belongs to the intended repository.
   - Never discard or revert user changes.
   - Determine `<secondary_branch>` and `<primary_branch>` using the branch detection rules.

2. Move work onto `<secondary_branch>`.
   - If already on `<secondary_branch>`, continue.
   - If on another branch with a dirty worktree, switch only when Git allows it cleanly; otherwise stop and explain the blocker.
   - If on another clean branch, run `git checkout <secondary_branch>` and `git pull --ff-only origin <secondary_branch>`.

3. Commit `<secondary_branch>` if there are local changes.
   - Stage relevant changes with `git add` unless the user requested a narrower scope.
   - Generate a Conventional Commits message with an English `type(scope):` prefix and a Chinese summary after the colon.
   - Do not use `--no-verify`.
   - If hooks or checks fail, fix the issue before committing.
   - If `<secondary_branch>` has no local changes, skip commit and continue to push.

4. Push `<secondary_branch>`.
   - Run `git push origin <secondary_branch>`.
   - If the push is rejected because the remote moved, fetch and inspect before retrying; do not force-push unless the user explicitly requested it.

5. Merge into `<primary_branch>`.
   - Run `git checkout <primary_branch>`.
   - Run `git pull --ff-only origin <primary_branch>`.
   - Run `git merge --no-ff <secondary_branch> -m "chore(<primary_branch>): merge <secondary_branch> into <primary_branch>"` to preserve a merge commit when `<primary_branch>` does not already contain `<secondary_branch>`.
   - If there are merge conflicts, stop after Git reports them and tell the user which files need resolution.

6. Push `<primary_branch>`.
   - Run `git push origin <primary_branch>`.

7. Return to `<secondary_branch>`.
   - Run `git checkout <secondary_branch>`.
   - Verify with `git status --short` and `git branch --show-current`.
   - The final branch must be `<secondary_branch>`.
   - Report the secondary branch commit SHA, the primary branch merge commit SHA when one was created, the pushed branches, and the final branch.

## Reporting

Keep the final response concise. Include successful branch pushes and commit hashes. If the host app supports Git directives, emit them only after the matching Git action succeeds.
