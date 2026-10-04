---
name: checkpoint
description: Git-level WIP safety net. Stashes uncommitted work, tags, and pushes to remote
triggers:
  - checkpoint
  - save wip
  - safety save
  - wip backup
  - stash backup
---

# Checkpoint

Create a recoverable snapshot of in-progress work via git stash, tag, and optional remote push.

## Usage

```bash
checkpoint
```

Stashes all uncommitted changes (including untracked files), creates a timestamped tag, and pushes to origin if remote exists. Output shows the stash ID and tag for recovery.

## What It Does

1. Runs `git stash push -u -m "checkpoint-<unix-ts>"`
2. Creates `git tag checkpoint/<unix-ts>` pointing to current HEAD
3. Attempts `git push origin refs/tags/checkpoint/<unix-ts>` (silent if no remote)
4. Prints recovery commands for later use

## Recovery

- **From stash**: `git stash apply stash@{0}` or `git stash pop stash@{0}`
- **From tag**: `git checkout checkpoint/<unix-ts>` (creates detached HEAD, safe to inspect)
- **List all checkpoints**: `git tag -l "checkpoint/*"`

## Exit Conditions

- **Success**: "Checkpoint <ts> saved" + recovery command printed
- **No git repo**: Warns "not a git repo", exits with code 1
- **Stash empty**: Warns "no uncommitted changes", exits with code 0
- **No remote**: Tags locally only, no push attempt
- **Push fails**: Warns "remote push failed but local checkpoint saved"
- **User abort**: Ctrl+C exits cleanly, does not stash

## Safety Notes

- Tags are lightweight, no additional refs needed
- Stash ID changes after git operations — use tags for stable recovery
- Tags persist even after `git gc`
- Useful alongside `context-save` for manual checkpoints between auto-saves
