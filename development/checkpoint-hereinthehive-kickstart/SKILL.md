---
description: Save a recoverable snapshot of the current working tree via git stash. Triggered by /checkpoint or "save a checkpoint" / "snapshot this".
disable-model-invocation: true
allowed-tools: Read Bash
---

You are the `/checkpoint` skill. Save a recoverable snapshot before something risky.

## Triggers

- Slash form: `/checkpoint [optional description]`
- Natural language: "save a checkpoint", "snapshot this", "before we do that, save where we are"

## Step 1: Hard refusals (check first)

- **No git repo.** `git rev-parse --is-inside-work-tree 2>/dev/null` — if not, tell user the safety net wasn't activated; abort.
- **Merge in progress.** `git rev-parse --verify MERGE_HEAD 2>/dev/null` — if exits 0:
  > "Something's mid-merge here — let's not checkpoint until that's resolved."

## Step 2: Infer a description

If the user passed a description, use it. Otherwise, infer one from recent activity:
- The last 1-2 things you helped with (e.g., "before refactoring login form").
- Fall back to a timestamp if nothing distinctive: "checkpoint at <time>".

## Step 3: Stash with the description

```
git stash push -u -m "checkpoint: $(date -u +%Y-%m-%dT%H:%M:%SZ) <description>"
```

## Step 4: Log it

Append to `.claude/checkpoints.log` (create if missing):

```
<ISO timestamp> | <description> | <stash ref returned by git stash list -1>
```

## Step 5: Confirm

> "Saved a checkpoint: '<description>'. If you want to come back to this exact state, just say 'restore the checkpoint' or pop the stash."

## Restoration

Triggered by "restore the checkpoint" or "go back to the checkpoint":

If multiple checkpoints exist (read `.claude/checkpoints.log`), list and ask which.

```
git stash apply stash@{N}
```

Note: use `apply` rather than `pop` so the checkpoint stays available for repeated restoration.

## Hard rules

- Never overwrite a checkpoint silently. Always create a new stash entry.
- Never delete a checkpoint without explicit user confirmation.
- The `.claude/checkpoints.log` is append-only from this skill's perspective.
