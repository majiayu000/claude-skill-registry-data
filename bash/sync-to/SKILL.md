---
name: sync-to
description: "Merge current branch into a target branch and return. Use when user says 'sync to', 'merge into', 'push changes to branch', or wants to sync their work branch into another branch without leaving the current branch."
argument-hint: <target-branch>
allowed-tools: Bash(bash *)
---

> **DO NOT auto-invoke this skill.** This merges and pushes to a remote branch. Always ask for user confirmation before proceeding.

# sync-to

Merge the current branch into a specified target branch, push if remote exists, then return to the original branch. The source branch remains intact. The target branch is automatically fetched and updated from the remote before merging to avoid stale-branch issues.

## Usage

Run the bundled script:

```bash
bash $HOME/.claude/skills/sync-to/scripts/sync-to.sh $ARGUMENTS
```

Report the script output to the user verbatim. Do not add extra commentary unless there was an error.

## Conflict handling

If the script exits with a merge conflict error, immediately stop and ask the user to use `/sync-force-to` instead. Do not attempt to resolve conflicts manually.
