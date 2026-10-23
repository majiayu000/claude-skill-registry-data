---
name: merge-worktree
description: "Use when only part of a worktree needs to come back into the current branch: selective merge (file, patch, cherry-pick, multi-worktree) and the post-merge cleanup. Complements finish."
---

# merge-worktree

Brings the work from one or several worktrees back into the current branch when a full merge
isn't the right fit (we only want part of the content, or we want to review before validating).
Sits at step 11 of `WORKFLOW.md`, just upstream of `finish`: here we choose *what* to
bring back, `finish` then tidies away the worktree that has become useless.

## When

- A single feature, a single file to retrieve from a worktree.
- A worktree contains several changes and only some of them are ripe.
- The content needs reviewing before validating the merge (no automatic commit).
- Several worktrees have to converge into a single integration branch.

## Steps

1. **Spot the active worktrees**: `git worktree list`, check the path and branch of each one
   before doing anything. Know where you stand: when `git rev-parse --git-dir` and `git rev-parse
   --git-common-dir` differ, you are inside a linked worktree and not in the main checkout. A detached HEAD
   is a state to resolve before removing or merging anything, never a branch to delete from under.
2. **Choose the strategy according to the need**:
   - **Targeted file(s)**: we know exactly what to retrieve, everything else is ignored:
     `git checkout <worktree-branch> -- path/file`
   - **Interactive patch**: we want to pick hunk by hunk within a file:
     `git checkout -p <worktree-branch> -- path/file`
   - **Cherry-pick without commit**: a specific commit from the worktree, but we want to drop
     some files from the commit before validating:
     `git cherry-pick --no-commit <sha>` then `git restore --staged path/file-to-exclude`
   - **Merge under review**: all of the branch's content, but a last look before committing:
     `git merge --no-commit --no-ff <worktree-branch>` then re-read the staged diff
     (`git diff --staged`) before `git commit`.
   - **Multi-worktree**: several branches have to converge into a single integration branch:
     repeat the merge-under-review per branch, one at a time, resolving conflicts before moving
     on to the next.
   - **Neighbouring branches that overlap**: when it is unclear which branch should be the base or in what order
     they fold in, decide that first, read-only, before any merge command: `references/01-consolidating-branches.md`.
3. **Validate**: commit once the content has been checked (never an automatic commit on a
   cherry-pick/merge until the staged diff has been re-read).
4. **Clean up**: list the remaining worktrees (`git worktree list`), remove the one(s) that have
   become useless (`git worktree remove <path>`), then `git worktree prune` if orphan entries
   remain (worktree deleted by hand, external drive unplugged…). Remove only worktrees this task created or that
   the operator named; one made by a tool or by someone else is left in place and mentioned. Never remove the
   worktree you are standing in from inside it.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Consolidating neighbouring branches: roster, shared read-only plan file, one reader per branch, rounds, conclusion | several branches overlap and the base and order are not decided | [`01-consolidating-branches.md`](./references/01-consolidating-branches.md) |

## Output / checkpoint

The targeted content merged into the current branch, the source worktree(s) removed cleanly.
If the step chains into `finish`, that block takes over for the task's main worktree and updates
the integration base.

## Guardrails

- Never a `git merge`/`cherry-pick` without `--no-commit` when there's any doubt about the
  content: always re-read the staged diff before validating.
- Don't confuse it with `finish`: `finish` closes a whole task after the MR has been merged by a
  human; `merge-worktree` is used *during* development, for selective or multi-source merges.
- Merge conflict: resolve file by file, never `git checkout --theirs`/`--ours` en masse without
  re-reading: it silently overwrites the other side.
- Files modified locally on top of the worktree: stash or commit before merging, otherwise the
  merge can fail or mix in unwanted changes.
- Stale worktree (path gone, branch deleted on the remote): `git worktree prune` before taking
  it over again, don't force a `remove` on an already-broken entry without checking
  `git worktree list` first.

## Origin

Idea taken from: a market context-engineering kit,
plugins/git/skills/git-worktrees/SKILL.md, "How to Merge Worktree" section. Mechanism rewritten
our way (mentis template, articulation with `finish`).

The consolidation of overlapping branches (§1) is the mechanism of the `standup` skill of `claude-mem`
(Apache-2.0, read 2026-10-02): a read-only shared room, one agent per branch, rounds driven by a facilitator, a
conclusion written by the facilitator. Rewritten in our words and without its helper scripts, since a plain file
and a lock are enough; no text copied, so the NOTICE obligations do not apply. The worktree-detection and
removal-scope rules of step 1 and step 4 come from the `using-git-worktrees` and
`finishing-a-development-branch` skills of `superpowers` (MIT, same date), rewritten.
