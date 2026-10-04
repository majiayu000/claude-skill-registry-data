---
name: git-ops
description: Use when Sam asks Claude Code to create, rename, compare, commit, push, merge, promote, or clean up Git branches. Covers Sam's feature branch naming convention, safe Git pre-checks, JetBrains DontCommit handling, commit-message defaults, push and release promotion verification, branch rename upstream cleanup, branch sync comparison, and submodule/gitlink handling.
---

# Git Ops

## Scope

Use this skill for Git operation tasks. Keep project-specific runtime, build, API, environment, and release-policy details in the repo's `AGENTS.md`; keep reusable Git behavior here.

Do not expand scope silently. If Sam only asks to inspect, report findings. If Sam asks to commit/push/merge, carry that operation through verification unless blocked.

## Safety Rules

Before any Git write operation:

```bash
git status --short --branch
```

Rules:

- Treat existing uncommitted changes as user work unless proven otherwise.
- Do not run destructive commands such as `git reset --hard`, `git checkout -- <file>`, `git clean -fd`, `git push --delete`, or force-push without explicit written confirmation.
- Use `git clean -fdn` before any real clean operation and report what would be removed.
- Prefer `rg`, `git diff`, `git status`, `git branch -vv`, `git log`, and `git show-ref` for inspection before acting.
- For remote cleanup wording, say `stale local remote-tracking refs` or `本地 origin/* 缓存`; `git fetch --prune origin` does not delete remote branches.

## Feature Branch Naming

When Sam says "功能分支" or asks to create a feature branch, use:

```text
feature/<YYYYMMDD>/<需求编码>_<功能简介>
```

Example:

```text
feature/20260521/MR2026052182911_xiaomei
```

Rules:

- The first path segment is always `feature`.
- The second segment is the date as `YYYYMMDD`.
- Sam usually provides the date. If the date is missing, ask before creating the branch.
- If Sam provides `MMDD` only, normalize it to `YYYYMMDD` using the clearly applicable year from the task context. If the year is ambiguous, ask.
- The third segment is `<需求编码>_<功能简介>`.
- Do not invent a requirement code. If missing, ask.
- Keep `功能简介` short and branch-safe. Prefer lowercase ASCII slugs such as `hyde`, `xiaomei`, `rrl_auth`.

Given:

```text
需求编码: MR2026051590006
date: 0528
功能简介: hyde
```

Create:

```text
feature/20260528/MR2026051590006_hyde
```

## Create Branch

Before creating a branch:

1. Run `git status --short --branch`.
2. Check whether the base branch and target branch exist.
3. If the worktree has unrelated changes, ask whether to use a separate worktree, stash, or keep the current state.
4. Refresh the remote base when network access is available.

Preferred feature-from-master flow:

```bash
git fetch origin master
git switch --no-track -c feature/YYYYMMDD/MRxxxx_short_desc origin/master
git status --short --branch
```

Use `--no-track` so a new feature branch does not accidentally track `origin/master`.

If Sam explicitly says to use local `master`, create from local `master`:

```bash
git switch --no-track -c feature/YYYYMMDD/MRxxxx_short_desc master
```

## JetBrains DontCommit

Before `git add` / `git commit`, inspect `.idea/workspace.xml` if it exists:

```bash
rg -n "ChangeListManager|DontCommit|DoNotCommit" .idea/workspace.xml
```

Rules:

- Files in `DontCommit` / `DoNotCommit` changelists must not be committed.
- If such files are already staged, unstage only those files.
- Override only if Sam explicitly asks to include them.
- If the main worktree has DontCommit or unrelated local files, prefer a temporary `git worktree` for release promotion.

## Commit And Push

When Sam says "提交推送吧" after implementation, treat commit and push as part of the task.

Before commit:

```bash
git status --short --branch
git diff --check
```

Rules:

- Stage only intended files.
- Keep unrelated user changes unstaged.
- Default `git commit` messages to Chinese. Code identifiers, module names, commands, paths, and proper nouns may stay in English.
- If independent topics are mixed and Sam says "拆两个", split commits by topic.
- After push, verify branch state with `git status --short --branch` and, when useful, `git branch -vv --list <branch>`.

## Release Promotion

When Sam explicitly asks to merge/push into `release/sit`, `release/uat`, or a dated release branch, perform the full requested merge and push path unless blocked.

Default flow:

```bash
git fetch origin <target-branch>
git switch <target-branch>
git merge --ff-only <feature-branch>
git push origin <target-branch>
```

If `--ff-only` fails:

- Inspect divergence first.
- Explain why fast-forward is impossible.
- Use `git merge --no-ff -m "<中文合并信息>" <feature-branch>` only when that matches the requested promotion.

For multi-branch promotion:

- Keep the sequence explicit.
- Verify each local and remote branch tip.
- Use temporary `git worktree` when the main workspace has unrelated local changes.

## Rename Branch

For branch rename requests, change the visible branch identifier exactly. Do not add code edits or content merges.

Reliable flow:

```bash
git branch -m <old> <new>
git branch --unset-upstream <new>
git push -u origin <new>
git branch -vv --list <new>
git ls-remote --heads origin <new> <old>
```

Rules:

- After `git branch -m`, always check for stale upstream metadata.
- Do not delete the old remote branch unless Sam explicitly asks.
- If deleting a remote branch is requested, verify the old and new refs point to the expected content first.

## Compare Branches

Do not judge sync from commit message shape alone. Compare content and ancestry:

```bash
git rev-list --left-right --count <left>...<right>
git rev-parse <ref>^{tree}
git diff --name-status <left>..<right>
git log --oneline --ancestry-path <left>..<right>
```

Notes:

- `release/sit` may carry extra merge history while still being content-identical to `release/uat` or a feature branch.
- Tree hash plus `git diff --name-status` is the most direct content-sync check.

## Submodules

When a repo contains submodules or gitlinks:

- A `160000` entry is a parent-repo pointer, not normal file content.
- If submodule source changed, commit and push inside the submodule first, then commit the parent pointer.
- Branch switching can leave an untracked submodule working tree on disk. Inspect it as submodule state; do not delete it as noise without confirmation.

## Finish

Always report the final Git state:

- current branch
- start point or target branch used
- commit hash / merge hash when created
- push result when pushed
- verification commands run
- whether `git status --short --branch` is clean
- skipped files, especially `DontCommit` / `DoNotCommit`
