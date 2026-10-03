---
name: github-branch
description: Safely create, adopt, publish, or clean up an issue-backed non-primary Git branch without force-pushing or absorbing ambiguous work
type: operations
version: v0.1
argument-hint: "<ensure|adopt|publish|cleanup|status> [issue-number] [branch-name]"
---

# GitHub Branch

Use this low-freedom subskill to own branch selection, dirty-tree adoption, commits, push, and cleanup. Follow the canonical `docs/github-delivery-contract.md` when available.

## Commands

- `ensure`: create or reuse the one non-primary work branch for an issue.
- `adopt`: move explicitly owned uncommitted work from primary or another branch onto the resolved work branch without losing unrelated work.
- `publish`: push the resolved work branch with an upstream, never with force.
- `status`: report primary, current branch, issue link, upstream, divergence, dirty paths, and open pull request.
- `cleanup`: delete an already-merged work branch only after proving safety and receiving separate confirmation.

## Prompt History Termination

Prompt history is metadata, not work that initiates this lifecycle. Never create or adopt a branch, commit, or push solely to ship a prompt-history record. These lifecycle commands create no prompt file when it would be their only tracked mutation; when another user-invoked skill produces substantive tracked changes, its prompt record travels with that same work.

## Ensure And Adopt

1. Detect the repository primary branch from remote metadata. Never assume `main` or `master` when it can be discovered.
2. Require one resolved open issue from `github-issue ensure`. Search local and remote branches for that issue number and task slug before creating anything.
3. Reuse a branch only when its issue, task scope, base, owner, and commit history are compatible. Stop on multiple candidates or conflicting work.
4. New names use a repository convention when documented; otherwise use `<type>/<issue-number>-<short-kebab-slug>`, with a stable type such as `feat`, `fix`, `docs`, or `chore`.
5. Before switching or adopting, inspect all tracked and untracked paths, staged changes, worktrees, upstream state, and recent commits. Enumerate the exact task-owned paths. Stop if ownership overlaps or is ambiguous.
6. Preserve unrelated changes in place. Do not stash, reset, clean, overwrite, or stage them implicitly. If safe movement cannot be proven, report the blocker.

## Commit And Publish

- Commit only explicit intended paths after inspecting the staged diff and running proportionate validation and secret checks.
- Refuse commits on the detected primary branch. Refuse direct pushes to primary, force-pushes, history rewrites, and `--force-with-lease`.
- Fetch before publish. Stop on unexpected remote divergence or a remote branch owned by different work.
- Push only the current resolved branch and set its upstream. Report the exact local and remote refs plus commit SHA.
- If GitHub or authentication is unavailable, keep safe local commits on the non-primary branch and report the blocker; never fall back to primary.

## Cleanup

Cleanup requires proof that the linked pull request merged, the branch has no unique commits, the branch is not checked out in any worktree, and ownership is unambiguous. Show local and remote deletion targets and obtain explicit confirmation immediately before deletion. Never delete an unmerged branch.

## Output

Report issue, primary, branch, upstream, head SHA, dirty-tree ownership decision, publication state, pull-request link when present, and any blocker.
