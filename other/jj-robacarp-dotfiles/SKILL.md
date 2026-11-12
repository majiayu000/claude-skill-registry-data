---
name: jj
description: Use when performing version control operations in repositories that use jj (Jujutsu) instead of git. Detected by the presence of a .jj directory.
disable-model-invocation: false
user-invocable: false
allowed-tools: Bash
---

# Jujutsu (jj) Version Control

When a `.jj` directory is present, use `jj` instead of `git` for all version control operations.

## Command mapping from git to jj:

| git | jj |
|-----|-----|
| `git status` | `jj status` or `jj st` |
| `git log` | `jj log` |
| `git diff` | `jj diff` |
| `git diff --staged` | `jj diff` (no staging concept) |
| `git add` | not needed — all changes are automatically tracked |
| `git commit` | `jj describe` to set the message on `@`, then `jj new` to start the next change |
| `git commit --amend` | `jj describe` (edits message on `@`) or `jj squash` (folds into parent) |
| `git branch` | `jj bookmark` |
| `git push` | `jj git push` |
| `git pull` / `git fetch` | `jj git fetch` |
| `git rebase` | `jj rebase` |
| `git stash` | not needed — just `jj new` and come back later |
| `git checkout` | `jj edit <change>` to resume work on a change |

## Key concepts:

- The working copy (`@`) is always a commit — don't abandon it even if empty
- There is no staging area — all file changes are part of the working copy commit
- Use `jj new` to start a new change on top of the current one
- Use `jj new --before @` to insert a commit before the working copy
- Use `jj squash --from <source> --into <target>` to move changes between commits
- Create a new commit any time the subject matter changes — it's far easier to merge two commits than to split one

## Commit messages:

- Use present active tense in the body: "Updates ...", "Adds ...", "Changes ..."
- Set the message with `jj describe -m "message"`

## Rebase:

- `jj rebase -s <rev> -d <dest>` — rebases a revision **and all its descendants** onto a new destination. Use this for moving a whole branch.
- `jj rebase -r <rev> -d <dest>` — rebases only a **single revision**, reparenting its children to its former parent. This orphans descendants from the moved commit.
- When rebasing a branch onto master, always use `-s` (source subtree), not `-r` (single revision).

## Squashing changes into specific commits:

- `jj squash --from @ --into <target> -- <file1> <file2>` — moves specific file changes from working copy into a target commit. Descendant commits are automatically rebased.
- `jj squash` (no args) — squashes the working copy into its parent.

## Viewing diffs and history:

- `jj diff -r <rev> --stat` — summary of changes in a revision
- `jj diff -r <rev> -- <file>` — diff for a specific file in a revision
- `jj show -r <rev>` — full diff of a revision. Note: does NOT accept `--` file path arguments; use `jj diff -r <rev> -- <file>` instead.
- `jj log -r 'parents(<rev>)'` — see what a commit is based on
- `jj log -r '<ancestor>::<descendant>'` — see a range of commits
- `jj log -r 'roots(<rev>::<rev>)'` — find the base of a branch

## Pushing and GitHub PRs:

Push the current change and auto-create a bookmark in one command:

```
jj git push --change @
```

jj names the bookmark after the change ID (e.g. `push-abc123`). The command prints the bookmark name on success. Since jj leaves git in a detached HEAD state, `gh pr create` cannot auto-detect the current branch — always pass `--head` and `--base` explicitly:

```
gh pr create --head <bookmark-name> --base main --title "..." --body "..."
```

## Divergent commits — always clean up immediately:

Divergence happens when two commits share the same change ID. jj marks them as `(divergent)` in `jj log` and `jj st`. This typically occurs when a PR is merged and the local working copy still has a version of the same change on top.

**Divergence must always be resolved before doing further work.** Do not push, create PRs, or build on top of a divergent change.

### How to detect:
```
jj log  # shows (divergent) next to affected commits
jj st   # shows (divergent) in the working copy line
```

### How to resolve after a PR is merged:

The most common case: `master@origin` was updated with a merged version of our change, but `@` still carries a divergent copy.

1. Check what's different between the two divergent versions:
   ```
   jj diff --git --from '<change_id>/1' --to '<change_id>/0'
   ```
   (jj numbers divergent copies as `/0`, `/1`, etc.)

2. If `@` has NEW work on top of what was merged (e.g. compile fixes), that work should become a **fresh commit** on top of master — not a divergent copy of the merged change:
   ```
   # Save the diff of what you want to keep (already in the files)
   jj new master@origin -m "Description of the new fixes"
   # Files already have the right content; jj tracks them automatically
   jj describe -m "Your message"
   jj git push --change @
   ```

3. If `@` has NO new work (just stale divergence after a merge), clean it up:
   ```
   jj edit master@origin   # switch working copy to the merged commit
   jj abandon <divergent_change_id>/0   # abandon the stale local copy
   ```

4. After resolving, verify with `jj log` that no `(divergent)` entries remain.

### Why rebasing a divergent `@` onto master creates conflicts:
`jj rebase -r @ -d master@origin` when `@` is divergent with master will produce a 3-way conflict because the "base" of the rebase includes the full original change on both sides. Prefer creating a fresh `jj new` commit over rebasing in this situation.

### Stale working copy from a shared `.jj` store (no workspace hooks):

If a repo's `EnterWorktree`/`ExitWorktree` hooks aren't installed for jj, worktrees fall back to plain `git worktree add`, which shares the *same* `.jj` store with every other session working in that repo. Concurrent jj activity elsewhere (another agent, another worktree, the user) can leave a workspace stale:

```
Error: The working copy is stale (not updated since operation ...).
```

Running `jj workspace update-stale` resolves it, but can itself produce a `(divergent)` commit and a `(conflicted)` bookmark if the edit you were mid-way through wasn't committed anywhere else yet — the resolution picks up whatever state existed at the last known-good operation, which can be older than your most recent edit.

**Fix forward, don't archaeology-dig.** Don't try to reconstruct the lost edit from `jj diff --git --from <rev>/0 --to <rev>/1` — just re-read the current file, re-apply the intended change directly, then collapse the bookmark conflict onto your working copy and push:

```
jj workspace update-stale
# re-apply the edit with Read + Edit, not by diffing divergent copies
jj bookmark set <bookmark-name> -r @
jj git push --bookmark <bookmark-name>
jj abandon <other-divergent-copy>   # e.g. <change_id>/1, once confirmed unneeded
```

Only inspect a divergent copy's content first if there's a real risk it holds unrelated work you'd lose (check `jj diff -r <rev> --stat` for surprising files) — otherwise this is a fast, low-stakes fix.

## Diff format:

jj uses **color-words** diff format by default, NOT the unified diff format that git uses. The output looks different:

- Changed lines show the file path, then the before/after content inline with word-level granularity
- Added content and removed content appear on the same line, distinguished by color (not +/- prefixes)
- The format is: `filename:line: <before text><after text>` with removed words and added words marked inline

When reading `jj diff` output, don't expect `+` and `-` line prefixes. Instead look for the word-level changes shown inline. To get git-style unified diffs if needed, use `jj diff --git`.
