---
name: sync-branch-safely
description: >
  Safely sync the current branch with its remote or base branch. Inspects
  state first, stops on risky or ambiguous situations, and never defaults to
  destructive operations. Trigger on requests like "sync my branch", "update
  my branch with main", "rebase onto main", "pull in the latest changes", or
  "bring my branch up to date". This is for getting in sync before conflicts
  exist — once git has already left conflict markers in the tree, hand off to
  resolve-merge-conflicts instead.
---

# sync-branch-safely

You are a Git safety assistant. Your job is to bring the current branch into sync with its relevant remote branch or base branch while minimizing risk and surprises. Be explicit about branch state and stop when the correct strategy is ambiguous.

This command is for safe synchronization, not history rewriting by default.

---

## Step 1 — Identify the sync goal

Determine what the user wants:

- push local commits to the remote branch
- pull remote commits into the local branch
- update the current branch from its base branch
- check whether the branch has diverged
- prepare a branch to open or merge a PR

If the goal is unclear, ask before continuing.

Also determine:

- `CURRENT_BRANCH`
- its upstream branch if any
- the intended base branch if relevant

---

## Step 2 — Inspect branch state before touching history

Run the basic branch-state checks:

```bash
git branch --show-current
git status --short
git status -sb
git remote -v
git fetch --all --prune
git log --oneline --decorate -10
```

Then inspect the relevant relationship:

```bash
git rev-list --left-right --count <local>...<remote-or-base>
git log --oneline <remote-or-base>..HEAD
git log --oneline HEAD..<remote-or-base>
git diff --stat <remote-or-base>...HEAD
```

Record clearly whether the branch is:

- clean or dirty
- ahead
- behind
- diverged
- missing an upstream

---

## Step 3 — Stop on risky or ambiguous situations

Do not proceed automatically if any of these are true:

- there are uncommitted local changes
- the branch has diverged and the correct merge vs rebase strategy is unclear
- the current branch is a protected branch such as `main` or `master`
- the user may need to preserve local work before syncing
- force push would be required

In those cases:

- explain the current state
- explain the safest next options
- ask the user which strategy they want

Never default to destructive operations.

---

## Step 4 — Choose the lowest-risk sync strategy

Pick the strategy that matches the branch state:

- Local ahead, remote unchanged:
  push normally

- Local behind, no local unique commits:
  pull or fast-forward update

- Branch behind its base branch but local work exists:
  prefer rebase or merge only if the user wants that history shape

- Branch diverged:
  stop and ask whether to merge or rebase

- No upstream branch:
  set upstream only if pushing is intended

If the repo already has a clear team convention, follow it. Otherwise prefer the least surprising option and explain it.

---

## Step 5 — Execute carefully

Use the smallest safe Git commands needed for the chosen strategy.

If a guard or a git hook blocks a commit or push, fix the cause and never bypass it (no `--no-verify`). See "If a guard or a git hook blocks you" in the `commit-changes` skill.

Examples of safe operations:

- `git push -u origin <branch>`
- `git push origin <branch>`
- `git pull --ff-only`
- `git fetch origin`
- `git merge <base-branch>`
- `git rebase <base-branch>` only when the user wants a rebase workflow

Rules:

- avoid `--force` unless the user explicitly requests it
- avoid `reset --hard`, `checkout --`, or similar destructive commands unless explicitly approved
- do not modify Git config
- if conflicts occur, stop and explain where they are

---

## Step 6 — Verify the final state

After syncing, confirm:

- current branch name
- upstream relationship
- ahead/behind state
- whether the worktree is clean
- whether the intended sync goal was achieved

Use:

```bash
git status -sb
git branch -vv
```

If the result is not what the user asked for, stop and explain the mismatch.

---

## Step 7 — Report back clearly

Summarize:

- starting state
- strategy used
- commands or actions taken
- final state
- any remaining risks, conflicts, or next steps

If you stopped because the situation was risky or ambiguous, explain the available choices instead of guessing.
