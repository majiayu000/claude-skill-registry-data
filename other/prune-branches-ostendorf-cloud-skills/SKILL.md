---
name: prune-branches
description: "Lists merged and stale branches, locally and on origin, and deletes the merged local ones without asking. Use when the branch list has grown or after merging several pull requests."
---

# Prune branches

Remove the branches that are done. Keep everything that still holds work.

## When to use

- After merging pull requests.
- The local or remote branch list has become unreadable.

## Steps

1. Update the view: `git fetch --prune`.
2. List candidates and classify them:
   - merged into the default branch: `git branch --merged <default>`
   - gone on the remote: `git branch -vv` showing `[origin/... : gone]`
   - stale but unmerged: no commit for several weeks and not merged
3. Never touch the default branch or the branch currently checked out. Switch to the default
   branch first if a local candidate is checked out elsewhere.
4. Drop a candidate that has an open pull request, whichever side it is on.
5. For an unmerged, stale candidate, check whether its commits exist anywhere else. If not,
   report it and leave it alone without asking.
6. Delete every merged local branch with `git branch -d`, without asking first.
7. Report the stale and unmerged candidates, local and remote separately, and ask before
   deleting any of them, and before any remote deletion of any kind.
8. Delete a remote branch only after that explicit confirmation, with
   `git push origin --delete <branch>`.
9. Report what was deleted and what was kept, with the reason for each kept branch.

## Guardrails

- Never delete the default branch or the branch currently checked out.
- Never delete a branch that has an open pull request.
- A merged local branch is deleted without asking. Every remote deletion and every stale or
  unmerged local branch needs an explicit yes first.
- Never force delete (`-D`) a branch whose commits exist nowhere else.

## Config

- `pr.base`: the branch candidates are measured against. Default: the repository default branch.

## References

- `git-conventions` for why a branch is deleted once its pull request is merged.
