---
name: "HUD: Worktrees"
description: "Map every worktree in this repo in plain language: where each one is, what state it is in and whether it is safe to touch"
when_to_use: "When the user asks what worktrees exist, seems confused about which checkout they're in or a worktree-related git error appears; worktrees are easy to get wrong, which is why this skill exists. Creating or removing one is branch-worktree's job."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: hud
disable-model-invocation: false # confusion about worktrees is exactly when it should appear; read-only, so no gate is needed
allowed-tools: ["Bash(git worktree list:*)", "Bash(~/.claude/library/scripts/worktree-state.sh:*)", "Bash(gh pr list:*)", "Bash(gh pr view:*)", "Read", "Glob"]
argument-hint: "(no arguments: shows the map)"
---

# HUD: Worktrees

Worktrees go wrong in predictable ways: removing the one you're standing in, creating a duplicate branch because one already existed, forgetting a worktree exists and wondering why a branch won't delete. This skill's job is to make the current state impossible to misread. It changes nothing: creating a worktree, moving the session into one and removing them all live in `branch-worktree`.

## Always start with the map

Gather first:

1. `git worktree list --porcelain`: every worktree, its path, branch, HEAD.
2. For each worktree: `~/.claude/library/scripts/worktree-state.sh <path> origin/main`, which prints `dirty` (changed and untracked files), `ahead` and `behind` as JSON; it exits 2 when the base does not resolve, so use `worktree-state.sh <path>` (its upstream, or null counts when it has none) for a branch with no remote base. Never call `git -C` directly: a permission rule loose enough for any path also lets `-c` options through. When the branch has an open PR whose base isn't main (`gh pr view <branch> --json baseRefName,number`), it's a stacked layer: count against `origin/<baseRefName>` instead and say so in the sentence; counting a stacked child against main folds the parent's commits into its ahead-count and misreads the layer.
3. `pwd`: establish **which worktree you are standing in right now**. This drives every safety check below.

Render as a table plus one plain-English sentence per worktree: what it is, what state it's in, whether it's safe to touch:

```markdown
| Worktree | Branch | State | You are here |
|---|---|---|---|
| ~/code/app (main checkout) | main | clean, up to date | |
| ~/code/app-worktrees/feat/search | feat/search | 2 uncommitted files, 3 ahead | ◀ |
```

Group the table in two sections, both always shown: **deliberate worktrees** (the main checkout plus paths following the project's worktree convention, e.g. the sibling `../<repo>-worktrees/<branch>` layout) first, then **machine-made worktrees** (session- or tool-created: paths under temp directories or `.claude`, or generated names following no human convention). When provenance is unclear, treat it as deliberate.

Then a **Suggestions** line naming anything that deserves attention: a worktree whose branch's PR has merged (or, un-PR'd, is merged to main; candidate for cleanup), a dirty worktree untouched for weeks, a branch checked out in a worktree that someone might try to check out elsewhere. An abandoned machine-made worktree (clean, branch merged or never pushed) is a first-class cleanup candidate here. When several worktrees form a stack (each branch the PR base of the next), say so plainly: "these three are one stack, bottom to top", since removing or rebasing them out of order is the trap.

Stop here; the map is the output. When the Suggestions line names something to act on, point at the skill that does it: `/branch-worktree new <branch>` to work on a branch in a worktree and `/branch-worktree prune` to clear redundant ones.

## Red flags

**Never:** run a command that changes a worktree or a branch from here (no `git worktree add|remove|prune`, no `git branch -d|-D`); tell the user a worktree is safe to remove without having read its dirty state and its PR.
