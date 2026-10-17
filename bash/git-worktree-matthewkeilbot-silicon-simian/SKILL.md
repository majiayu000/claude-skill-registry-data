---
name: git-worktree
description: Enforce safe git worktree workflow for coding tasks so agents do not modify the main checkout or protected branches by accident. Use when implementing code changes in an existing git repo, creating a feature branch, delegating work to sub-agents, or when the user explicitly asks to use git worktrees / protect main / avoid contaminating unstable.
---

# Git Worktree

Use this skill to keep coding work out of the primary checkout.

## Core rules

1. Never edit, commit, checkout, or reset from the main repo directory.
2. Every task gets its own sibling worktree.
3. Pass `workdir`/`cwd` explicitly on every tool or sub-agent call.
4. Verify location before any git command.
5. Refuse to push from protected branches like `main`, `master`, or `unstable`.
6. Prefer merging base into the feature branch over rebasing when bots are involved.

## Workflow

### 1) Inspect the repo and base branch

From the main checkout, verify the repo root and choose the protected base branch (`unstable`, `main`, or repo-specific default).

```bash
git rev-parse --show-toplevel
git branch --show-current
git fetch origin
```

If the current checkout is dirty in a way that matters, stop and tell the user before creating a worktree.

### 2) Create a dedicated worktree

Create a sibling directory named after the repo and task.

```bash
git worktree add ../<repo>-<feature> -b <feature> origin/<base>
```

Example:

```bash
git worktree add ../lodestar-fix-peer-id -b feat/fix-peer-id origin/unstable
```

After creation, all coding work happens only inside that worktree.

### 3) Run a pre-flight check before git operations

Before any status/add/commit/push/merge command, verify both path and branch.

```bash
pwd
git rev-parse --show-toplevel
BRANCH=$(git branch --show-current)
[[ "$BRANCH" == "main" || "$BRANCH" == "master" || "$BRANCH" == "unstable" ]] && { echo "ON PROTECTED BRANCH"; exit 1; }
```

If this check fails, stop immediately.

### 4) Delegate safely

When spawning sub-agents or running shell commands:

- set `cwd`/`workdir` to the worktree path every time
- say explicitly: `You are working in a git worktree. Do not cd to the main checkout.`
- require the first command to be `pwd`

If a sub-agent needs to inspect the base branch, prefer:

```bash
git show origin/<base>:<path>
```

Do not jump back into the primary checkout just to read a file.

### 5) Commit and update safely

Commit from the worktree only.

When the base branch has moved, update the feature branch with a merge:

```bash
git fetch origin
git merge origin/<base>
```

Default to merge, not rebase, so bot-generated review history stays stable and does not require force-push.

### 6) Push and open the PR

Push from the worktree branch only after the protected-branch check passes.

```bash
git push -u origin <feature>
```

Then open the PR using the repo's normal workflow.

### 7) Clean up after merge

Once the PR is merged and the worktree is no longer needed:

```bash
git worktree remove ../<repo>-<feature>
git branch -d <feature>
```

## Failure modes to guard against

- Agent drifts back into the main checkout and forgets to return.
- Sub-agent ignores inherited cwd and defaults to the parent repo.
- Push happens from `main`/`master`/`unstable`.
- Stale worktrees pile up and create confusion.
- Relative-path scripts break because the worktree is a sibling directory.
- Hooks, dependencies, or build artifacts are missing in the new worktree.
- Bot rebases, force-pushes, and wrecks reviewer history.

## Naming guidance

Use predictable feature branch and worktree names so cleanup is obvious.

- branch: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`
- worktree dir: `../<repo>-<topic>`

## Response pattern

When using this skill, tell the user:

- which repo is the protected primary checkout
- which base branch you selected
- the exact worktree path you created
- that all further work will happen only in that worktree
