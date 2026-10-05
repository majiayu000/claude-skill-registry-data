---
name: git-workflow
description: Use for branching, committing, history repair, and release hygiene. Covers atomic commits, rebase versus merge, bisect, reflog recovery, and undoing mistakes safely.
metadata:
  category: development
  version: 1.0.0
  tags: [git, version-control, rebase, bisect, workflow]
---

# Git Workflow

## Purpose

Keep history readable and recoverable. A good history is a debugging tool: it lets you bisect, revert, and explain. A bad one is a wall of "fix", "fix again", "wip".

## When to Use

- Structuring commits before opening a pull request.
- Recovering from a bad rebase, reset, or force-push.
- Bisecting to find the commit that introduced a regression.
- Cleaning up a branch's history.
- Deciding a team branching strategy.

## Capabilities

- Atomic commit construction, including interactive staging.
- History rewriting: interactive rebase, squash, fixup, autosquash.
- Recovery: reflog, `ORIG_HEAD`, `git restore`, cherry-pick.
- Bisection, including automated bisection with a test script.
- Conflict resolution and `rerere`.

## Inputs

- The repository state and the branch's relationship to its base.
- Whether the branch has been pushed and whether others have based work on it.

## Outputs

- A branch whose commits each build, pass tests, and do one thing.
- Commit messages that explain why, not what.
- A rebase or merge that preserves the ability to revert cleanly.

## Workflow

1. **Commit atomically** — One logical change per commit. Use `git add -p` to split a messy working tree.
2. **Write the message for the future** — Subject in the imperative under 72 characters; body explaining why the change was needed.
3. **Clean before review** — `git rebase -i` to squash fixups and reorder. Reviewers should read the story, not the process.
4. **Rebase private branches, merge shared ones** — Rewriting history that others have pulled is how you lose their work.
5. **Recover with reflog** — Almost nothing is truly lost. `git reflog` shows every position HEAD has held.

## Best Practices

- Never `git push --force` to a shared branch. Use `--force-with-lease`, which refuses if someone else has pushed.
- A commit that does not build is a commit that breaks bisect. Keep every commit green.
- `git commit --fixup <sha>` plus `git rebase -i --autosquash` makes review-response commits disappear cleanly.
- Do not commit generated files, secrets, or large binaries. Removing them later requires rewriting history for everyone.
- `git bisect run ./test.sh` finds the offending commit automatically. It is the fastest regression hunt available.
- Enable `rerere` — Git will remember how you resolved a conflict and reapply it next time.

## Examples

**Automated bisection:**

```bash
git bisect start
git bisect bad HEAD             # current commit is broken
git bisect good v2.14.0         # this release was fine

# Any script exiting 0 for good, non-zero for bad.
git bisect run pytest tests/test_checkout.py::test_total

# Git prints the first bad commit, then:
git bisect reset
```

**Recovering a branch destroyed by a bad reset:**

```bash
git reflog                       # find the sha from before the reset
# 8a3f1c2 HEAD@{3}: commit: add proration handling
git reset --hard 8a3f1c2         # branch is back
```

**Splitting a messy working tree into reviewable commits:**

```bash
git add -p                       # stage hunks belonging to the first change
git commit -m "Extract proration calculator"
git add -p                       # stage the next logical change
git commit -m "Fix double-charge on mid-cycle upgrade"
```

## Notes

- The reflog is local and expires (90 days by default). It will not save you from a force-push that only ever existed on someone else's machine.
- Merge commits make `git log --oneline` noisy but preserve the true topology. On a team that reviews by PR, squash-merging to main and keeping the branch history in the PR is a reasonable middle ground.
- If a secret is committed, rotating it is mandatory and rewriting history is optional. Assume it is compromised the moment it is pushed.
