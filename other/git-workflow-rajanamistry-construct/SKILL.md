---
name: git-workflow
description: Safely inspect Git state, stage and commit focused changes, manage branches, rebase or cherry-pick authorized local work, resolve conflicts and plan recovery. Use for Git operations or commit-history review. Preserves existing work and never assumes permission to commit, rewrite history or push.
argument-hint: "<inspect | commit | branch | rebase | cherry-pick | recover | push> [target]"
---

# Git workflow

Status: Draft. Instructions reviewed; not yet verified end to end in a documented example.

Load `construct` and the project's Git conventions first. This skill supplies a procedure, not permission or extra tools. Respect the calling workflow's read-only scope. Inspect by default; ask when the operation, target or authorization is unclear. A request to create a skill is not permission to commit it.

## 1. Inspect before acting

```sh
git status --short --branch
git diff --stat
git diff --cached --stat
git worktree list
git log -5 --oneline
```

Confirm the repository, current branch or detached HEAD, intended base, remote owner/repository, upstream and any operation already in progress. Inspect remote URLs locally but do not expose embedded credentials or private addresses in output. Do not assume the base is `main`, the remote is `origin`, or a branch belongs only to the user.

Read relevant diffs, including staged and untracked files, before editing or staging. Treat unfamiliar changes as user work. Do not mix unrelated changes, unstage someone else's files or resume an existing merge/rebase/cherry-pick without agreement. A read-only history check needs no fetch or checkout.

Before integrating remote work, confirm the remote and fetch the specific branch when network access is allowed. Inspect ahead/behind commits and divergence; fetch updates remote-tracking refs, not the working branch. Choose an explicit integration method instead of a blind `git pull`.

Before remote Git or forge CLI access, follow [tool preflight](../../../docs/tool-preflight.md): check availability, existing authentication and the intended host/account. Git transport authentication and forge API authentication are separate. Reuse the suitable existing method; if it is missing or unclear, ask for the method and target without requesting secrets. Offline inspection does not authorize a network authentication check.

## 2. Branches and work preservation

1. Follow project naming and branching conventions. Confirm the starting revision before creating or switching a branch. Use an agreed worktree for isolated work where useful; never remove or force-switch an occupied worktree.
2. If local changes could be affected, stop and agree how to preserve them. A backup ref protects committed history, not uncommitted or untracked files. Do not rely on reflog to recover files Git never recorded.
3. Stash only with permission. Record the original branch/revision and the exact stash object ID, including whether untracked files were included. Ignored files are not included by `-u`; do not sweep them up with `-a` without specific approval.
4. Restore to the recorded context, inspect current changes, then apply the exact recorded stash. Verify contents before asking to drop it. On conflicts, keep the stash and stop; never guess, clear all stashes or discard new work to make restoration succeed.
5. Helpers may have weaker bookkeeping. Inspect their state and refusal conditions before use; do not treat a stash message alone as unique identity or a successful script exit as proof that all local work was restored.

## 3. Focused commits

Commit only when the assignment authorizes it. Confirm what is already staged, then stage named paths or selected hunks, not a blanket `git add .`. Keep one coherent concern per commit; tests and necessary generated artifacts travel with the behavior. Inspect new files and metadata as well as modifications.

```sh
git diff --cached --check
git diff --cached --stat
git diff --cached
```

Review the complete staged diff for secrets and private information before committing. Report suspected secrets by path and type only, and stop until resolved. Run relevant checks; never bypass hooks, signing or project policy to get a commit through. If a hook changes files, inspect them and restage deliberately rather than repeatedly committing blindly.

Follow the project's commit-message convention. Without one, use a short imperative subject under 72 characters, a blank line and a body explaining why when useful. Do not impose Conventional Commits or invent issue IDs, trailers or authorship claims. Use `pre-push-review` for description and message drafting in a branch self-review.

```text
Preserve task input after a failed save

Keep the draft available so a transient error does not erase user input.
```

After committing, inspect `git show --stat HEAD` and the commit diff, then check status. Report the actual commit ID and remaining changes. Do not include unrelated user work merely because it was already staged.

## 4. Rebase, amend and cherry-pick

Rebase, amend, squash and interactive history editing rewrite commit IDs. Require explicit authorization for the particular operation and range. Confirm whether commits have been shared; a local rewrite is not permission to rewrite the remote. Prefer a follow-up commit on shared work unless the user and project explicitly permit another approach.

1. Record the original branch tip, agreed base and intended commit range. Ensure a clean operation workspace and create an agreed unique backup ref for committed history before rewriting. Never overwrite an existing backup or include unrelated work.
2. Rebase only the selected branch onto the agreed revision. Cherry-pick only identified commits in the intended order; inspect prerequisites and duplicates. A cherry-pick adds commits but can duplicate behavior already present. Avoid automatic merge-commit picks when the intended mainline is unclear.
3. On conflicts, inspect `git status`, the conflicting files and both intents. During rebase, ours refers to the upstream plus replayed history and theirs to the commit being replayed, unlike an ordinary merge. Do not select an entire side without understanding the result. Regenerate derived files with project tooling rather than hand-editing generated output.
4. Resolve only the conflict, stage named resolved paths and inspect the staged resolution before `--continue`. An empty commit or unclear product decision is a stop: ask before skipping, dropping or choosing behavior. Use the operation's `--abort` only after inspecting whether work added during the operation could be lost; do not replace it with a hard reset.
5. Compare the new history with the recorded original tip (for example with `git range-diff` for a rebased series), inspect the final diff and run affected tests. Report changed commit IDs, conflicts, evidence and remaining risks. Keep the backup until recovery is no longer needed and its deletion is approved.

## 5. Recovery and publication

For recovery, stop mutations and inspect `git status`, the operation state, named backups and local `git reflog`. Identify the wanted revision and propose a recovery branch or isolated worktree to inspect it before moving any existing branch. Reflogs are local, expire and are not backups. A revert creates new history and can conflict; it also needs authorization for the intended commits.

Never run `git reset --hard`, `git clean`, forced checkout, branch deletion or blanket restore to clear an obstacle. Any destructive recovery needs explicit approval for the exact scope and prior preservation of affected work. Do not change global configuration, credentials, hooks or protection rules.

Push only with explicit authorization in the current message. Verify the destination remote, source and target branch, fetch and inspect unexpected remote changes, review the outgoing commits and privacy checks, then use an ordinary push with explicit targets. Do not automatically push all branches or tags. Verify the published commit against the remote afterward; a local commit or successful-looking message is not synchronization evidence.

Never use plain `--force`. Even `--force-with-lease` rewrites remote history: it is not a default or a remedy for divergence. Where a different project's policy permits it, require explicit rewrite approval and a lease pinned to the reviewed remote branch and SHA. **Construct forbids force-pushing**, including force-with-lease; stop and use an ordinary push or reviewed pull request under `construct.md`.

Return the branch and before/after revisions, actions actually performed, checks run, preserved work/backup references and exact next action. Do not report an inspection as a completed operation.

## References

- [Git rebase](https://git-scm.com/docs/git-rebase), [cherry-pick](https://git-scm.com/docs/git-cherry-pick) and [range-diff](https://git-scm.com/docs/git-range-diff)
- [Git stash](https://git-scm.com/docs/git-stash) and [reflog](https://git-scm.com/docs/git-reflog)
- [Git push](https://git-scm.com/docs/git-push) and [commit](https://git-scm.com/docs/git-commit)
