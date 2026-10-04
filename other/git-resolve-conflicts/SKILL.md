---
name: git-resolve-conflicts
description: Resolve Git merge, rebase, cherry-pick, or PR branch conflicts against a fetched remote base branch. Use when a user asks to fix conflicts, update a branch onto its remote base, make a branch mergeable, resolve GitHub PR conflicts, continue an interrupted conflict operation, or prepare a conflicted branch for merge without pushing automatically.
---

# Git Resolve Conflicts

Use this as a safety protocol for risky Git conflict resolution. Do not use it as a general guide to interpreting code conflicts.

## Required Protocol

1. Collect Git state with the bundled read-only script. Treat it as the deterministic source for conflict-state collection.

   ```bash
   <python> <skill-dir>/scripts/git_conflict_preflight.py --repo .
   ```

2. Stop if unrelated dirty worktree files, staged changes, or untracked files make conflict resolution ambiguous. Ask before stashing, committing, discarding, or moving them.

3. Confirm the remote base by fetching and resolving the fetched ref:

   ```bash
   git fetch --prune <remote>
   git rev-parse --verify <remote>/<base>
   <python> <skill-dir>/scripts/git_conflict_preflight.py --repo . --base-ref <remote>/<base>
   ```

4. Before starting a new merge or rebase attempt, create a backup ref:

   ```bash
   git branch backup/conflict-resolution/<branch-name> HEAD
   ```

5. If a Git operation is already in progress, continue that operation. Otherwise use the user-requested operation; when unspecified, prefer rebasing onto the fetched remote base:

   ```bash
   git rebase <remote>/<base>
   ```

6. When conflicts occur, rerun preflight before editing. Use standard Git inspection commands only as needed for path-level detail.

7. Before asking about or resolving any non-mechanical conflict, read `references/interview-gate.md`.

8. Treat semantic, product, API, data, security, ownership, and deletion-retention conflicts as mandatory stop conditions. Interview the user before resolving them.

9. After each resolution batch, stage resolved files and continue the active operation:

   ```bash
   git add <paths>
   git rebase --continue
   git merge --continue
   git cherry-pick --continue
   ```

10. After completion, verify with preflight, Git checks, and identifiable project checks:

   ```bash
   <python> <skill-dir>/scripts/git_conflict_preflight.py --repo . --base-ref <remote>/<base>
   git status --short --branch
   git diff --check
   ```

   Run relevant tests, typecheck, lint, or build commands when the project makes them discoverable.

11. Report the base ref and SHA, conflict files resolved, user interview decisions, verification commands, and remaining risk.

## Push Rule

Do not push automatically. If the user explicitly asks to update a remote branch after conflict resolution, use `git push --force-with-lease`, never plain `--force`.

## Rebase Terminology

During a rebase conflict, `ours` means the already-rebased side and `theirs` means the topic commit being replayed. Explain this mapping before using `--ours`, `--theirs`, or those labels with the user.
