---
name: active-rebaser
description: Use when local main has just been updated — pulled, fast-forwarded, merged a PR, or reset — and the other branches and worktrees are now behind it. Also use when asked to "rebase everything", "catch the branches up", or "run the active rebaser".
---

# Active rebaser

Rebase every local branch and worktree onto the new `main`, one at a time, then report and ask which rebased branches to push. Never push anything without explicit per-branch approval, and never push with anything other than `--force-with-lease`.

## Enumerate

```bash
git rev-parse --abbrev-ref HEAD          # remember where to return
git branch --format='%(refname:short)'   # every local branch except main
git worktree list --porcelain            # which branch is checked out where
```

Record each branch's pre-rebase SHA (`git rev-parse <branch>`) before touching it — that SHA is the undo button.

Skip a branch and mark it **up to date** when `git merge-base --is-ancestor main <branch>` succeeds.

## Rebase, one branch at a time

- A branch checked out in a **worktree** is rebased inside that worktree: `git -C <worktree-path> rebase main`. A dirty worktree is skipped and reported — never stash someone's work-in-progress.
- Any other branch is rebased in the primary worktree with `git rebase main <branch>` if it is clean, or in a throwaway `git worktree add` under the scratchpad if it is not. Return to the original branch when the loop ends.

## Conflicts: resolve small, abort big

A conflict is **simple** only when every conflicted file (2 files at most) is one of:

- a lockfile or generated file — regenerate it instead of merging text
- both sides added independent lines to the same list (imports, exports, table rows) — keep the union
- a version or date bump — keep the newer value
- one side is a strict superset of the other — keep the superset

Anything else — overlapping logic edits, a moved function, 3+ conflicted files, or any doubt at all — is **huge**: `git rebase --abort`, record the conflicted paths for the report, move to the next branch. Never write new code inside a conflict hunk; resolution picks between what the two sides already wrote.

After any hand-resolved rebase, run `bun run system-check` on that branch. If it fails, `git reset --hard <pre-rebase SHA>` and report the branch as restored, with the failing output.

## Report

When the loop finishes, show one table — every branch appears, no silent skips:

| Branch | Result                       | Details                          |
| ------ | ---------------------------- | -------------------------------- |
| foo    | rebased clean                | 3 commits replayed               |
| bar    | rebased — conflicts resolved | lockfile regenerated; check pass |
| baz    | aborted — conflict too big   | `src/data/progress.ts` + 4 more  |
| qux    | up to date                   | already contains main            |

## Approval, then push

Ask which successfully rebased branches to push (one multi-select question listing only the rebased ones — aborted and up-to-date branches are not offered). Then, for each approved branch only:

```bash
git push --force-with-lease origin <branch>
```

A `--force-with-lease` rejection means the remote moved since the last fetch — report it and stop; do not retry with `--force`.

## Common mistakes

| Mistake                                          | Consequence                                                           |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| Pushing without asking, or batching approval     | The whole point of the report is per-branch consent. Ask first.       |
| `--force` after a `--force-with-lease` rejection | Overwrites remote work the lease just protected. Report instead.      |
| "This conflict is only medium-sized"             | The simple list is exhaustive. Not on it → abort. There is no medium. |
| Inventing code to satisfy a conflict hunk        | That is authoring changes nobody reviewed. Abort instead.             |
| Stashing a dirty worktree to force the rebase    | Someone's WIP is not yours to shelve. Skip and report.                |
| Losing the pre-rebase SHA                        | No clean undo when system-check fails. Record it before every rebase. |
