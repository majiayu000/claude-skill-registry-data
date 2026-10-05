---
name: power-finish
description: Use when implementation is complete, tests pass, and the work needs integrating - merging, opening a pull request, or being left in place
---

# Finish a Branch

Never push, merge, or open a pull request unless the human asked in this session; read
[safety](../../references/safety.md) before Step 5 and Step 6.

## Step 1 — Green first

Run the full suite. If it fails, report it and stop. **The menu below does not appear until the
suite is green** — offering integration options over a red suite invites choosing one.

## Step 2 — Capture the environment

Record `WORKTREE_PATH` and the current branch **now**, before any step changes directories.
Step 5 moves you, and a path captured after the move points at the wrong place.

## Step 3 — Confirm the base

Ask which branch this integrates into. Do not assume `main`; do not read it from a config and
proceed silently.

## Step 4 — The menu

Present exactly these, and wait:

1. **Merge locally** into the base branch.
2. **Push and open a pull request.**
3. **Leave it as is** — keep the branch and the worktree.

In detached HEAD, only options 2 and 3 apply; say why.

Discarding is not on the menu. If the human asks to discard, require them to type the word
`discard`, and confirm what will be lost first.

## Step 5 — Execute

**Merge locally**: merge **before** removing anything, then run the suite again **on the merged
result**. Two branches that each pass can fail together, and that failure belongs to whoever
merged them.

**Pull request**: push, open it, and **keep the worktree**. Review feedback gets fixed there,
and a removed worktree means recreating it in an hour.

**Leave it**: record where it is and what state it is in, so the next session does not rediscover
it.

## Step 6 — Cleanup

Only remove worktrees under `.worktrees/` or `worktrees/`, and only ones this work created.

```bash
git worktree remove <path>
git worktree prune
```

If removal is refused because of uncommitted files, **do not add `--force` on your own
initiative.** Show `git status --porcelain -uall` and offer: commit them, stash them, or leave
the worktree in place. The refusal is git protecting work that someone may want.
