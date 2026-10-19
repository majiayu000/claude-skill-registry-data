---
name: git-pro
description: Advanced Git — rebasing, history surgery, bisecting, and recovery — use when Git gets complicated or things go wrong.
category: git
---

## Overview

Everyday Git (commit, push, pull) is easy; the power — and the danger — lies in
history manipulation, debugging with bisect, and recovering from mistakes.
This skill covers the workflows that turn Git from a save button into a
precision instrument, plus how to undo nearly anything.

## When to use

- Rebasing, squashing, or reordering commits cleanly
- Finding which commit introduced a bug (`git bisect`)
- Recovering deleted branches, lost commits, or bad resets (`reflog`)
- Resolving complex merges and understanding merge strategies
- Managing submodules, large files (LFS), and monorepo-scale histories

## Core concepts

**The commit graph is the truth.** Branches and tags are just movable pointers
to commits. Internalizing this makes rebase (replay commits onto a new base),
reset (move a pointer), and reflog (history of where pointers were) intuitive
instead of magical.

**Rebase for private history, merge for shared history.** Rewrite commits that
only exist on your machine freely (`rebase -i` to squash/fixup/reword/reorder).
Never rewrite commits others have based work on — that rule prevents 90% of
Git disasters. `pull --rebase` keeps local history linear without rewriting
anyone else's work.

**Bisect is binary search over history.** `git bisect start`, mark a bad commit
and a known-good commit, and Git checks out the midpoint; you test and say
good/bad (or automate with `git bisect run <test-command>`). Logarithmic time
to the culprit commit — the fastest debugging tool most developers underuse.

**The reflog is your safety net.** `git reflog` records every position HEAD and
branches have pointed to — deleted branches, bad resets, and "lost" commits are
recoverable for ~90 days (default) via `git checkout <sha>` or
`git branch recovery <sha>`. Almost nothing is truly lost until GC runs.

**Staging is a feature.** The index lets you craft precise commits: stage hunks
(`git add -p`), split work into logical commits, and keep unrelated changes
apart. Atomic commits (one logical change each) make revert, bisect, and
review dramatically easier.

## Practical workflow

1. **Keep history clean as you go:** commit atomically with imperative,
   specific messages ("Add retry with backoff to payment client", not
   "fix stuff"); use `git add -p` to separate concerns.
2. **Before sharing:** `git rebase -i main` to squash fixups, reword vague
   messages, and drop debug commits — present a reviewable story.
3. **To find a regression:** `git bisect start`, `git bisect bad`,
   `git bisect good <old-sha>`, then `git bisect run npm test` (or manual
   good/bad); `git bisect reset` when done.
4. **To undo:** uncommitted mess → `git restore` / `git stash`; bad last
   commit (unpushed) → `git reset --soft HEAD~1`; bad pushed commit →
   `git revert` (adds a new commit, safe for shared history).
5. **To recover:** `git reflog` → find the sha → `git branch <name> <sha>` or
   `git reset --hard <sha>`; for truly deleted remote branches, check other
   clones, CI artifacts, or the hosting provider's reflog/events API.
6. **For big repos:** shallow clones (`--depth`) for CI, partial clone/sparse
   checkout for monorepos, and Git LFS for large binaries — don't commit
   500MB datasets to regular history.

## Common pitfalls

- **Rewriting shared history** — `push --force` on a collaborative branch
  strands teammates; use `--force-with-lease` and only on personal branches.
- **`git reset --hard` without checking status** — destroys uncommitted work
  permanently; `git stash` or commit first when in doubt.
- **Committing secrets** — once pushed, a secret is compromised even if you
  later remove it (history retains it); rotate the secret and purge history
  with filter-repo, then force-push with team coordination.
- **Merge commits for every PR** vs rebasing everything — pick a team policy
  (merge, squash, or rebase) and stay consistent; mixed strategies confuse
  history.
- **Huge files in history** — they bloat every clone forever; LFS from the
  start for binaries, and migrate early if missed.
- **Bisecting with a flaky test** — non-deterministic tests send bisect to
  the wrong commit; ensure the repro is reliable before automating.
