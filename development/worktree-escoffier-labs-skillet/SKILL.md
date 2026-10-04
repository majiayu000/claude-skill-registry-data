---
name: worktree
version: 0.1.0
license: MIT
description: Use when starting feature work that needs isolation from the current branch, or before executing a plan or fanning out parallel stations - sets up an isolated workspace using the harness's native worktree tool, falling back to a git worktree. Triggers on "worktree", "isolate this work", "don't touch my branch", "work on a copy".
---

# worktree

A cook does not prep on the same board the plates are leaving from. A clean station is the first move of service, not an afterthought: it keeps the work in front of you from contaminating what is already plated. This skill sets up that clean station for code, an isolated workspace where a feature or a risky change can be built without touching the branch the user is standing on.

**Core principle:** detect existing isolation first, then prefer the harness's native worktree tool, then fall back to git. Never fight the harness by stacking a manual worktree on top of one it already gave you.

## Step 0: are you already isolated?

Before creating anything, check. Stacking a worktree inside a worktree is the most common mistake.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
git rev-parse --show-superproject-working-tree 2>/dev/null   # non-empty = submodule, not a worktree
```

If `GIT_DIR != GIT_COMMON` and you are not in a submodule, you are already in a linked worktree. Report the path and branch, skip to Step 2. If they are equal (or you are in a submodule), you are in a normal checkout: continue.

## Step 1: get consent, then create

If the user's instructions already declare a worktree preference, honor it without asking. Otherwise ask once: "Want me to set up an isolated worktree so your current branch stays untouched?" If they decline, work in place and skip to Step 2.

**1a. Native tool first (preferred).** If the harness gives you a worktree mechanism, a tool named something like `EnterWorktree` or `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag, use it and skip to Step 2. Native tools own directory placement, branch creation, and cleanup; a hand-rolled `git worktree add` on top of them leaves phantom state the harness cannot see.

**1b. Git fallback (only when no native tool exists).** Pick the directory by priority: explicit user preference, then an existing `.worktrees/` (wins) or `worktrees/`, else default to `.worktrees/` at the repo root. For a project-local directory, verify it is ignored before creating anything (`git check-ignore -q .worktrees`); if not, add it to `.gitignore` and commit that first, or the worktree contents get tracked. Then:

```bash
git worktree add ".worktrees/$BRANCH" -b "$BRANCH"
cd ".worktrees/$BRANCH"
```

If creation fails on a permission or sandbox denial, say so plainly, work in the current directory, and run setup in place.

## Step 2: setup and a clean baseline

Install dependencies for whatever the repo is (`npm install`, `cargo build`, `pip install -r requirements.txt` / `poetry install`, `go mod download`), then run the suite once so you start from a known-green floor ([check](../check/SKILL.md)). If the baseline is already red, report it and ask before building on top: you cannot tell your new bug from a pre-existing one otherwise.

Report: the worktree path, the branch, and the baseline result.

## Pairs with

- [stations](../stations/SKILL.md): concurrent stations that write to the same files each get their own worktree so they do not collide in one tree.
- [fire](../fire/SKILL.md): execute a plan inside the isolated workspace, not on the user's working branch.

## Common mistakes

- Creating a worktree when Step 0 already found one. Detect before you build.
- Reaching for `git worktree add` when the harness has a native tool. If you have it, use it; the git path is the fallback, not the default.
- Skipping the ignore check, so the worktree's files land in `git status` and eventually in a commit.
- Building on a red baseline, then being unable to separate your change's failures from the ones that were already there.
- Guessing the directory instead of following the priority order; the inconsistency bites the next session that looks for the worktree.
