---
name: stash
description: Git stash + session linking
---

# Stash Session

Save git changes to stash with Claude Code session ID for later retrieval and session continuity.

## Purpose

Link git stash entries to Claude Code sessions. When resuming work, find the exact stash associated with a previous conversation.

## Message Format

```
claude:[session_id] [user_message]
```

Example: `claude:abc123de My feature work in progress`

## Operations

### Save (Default)

Stash current changes with session ID tag.

#### Workflow

1. Call AskUserQuestion to collect Session ID:
   - Prompt: "Enter the Session ID from your statusline (e.g., abc123de):"
   - User copies value from Claude Code statusline

2. Call AskUserQuestion to collect stash message:
   - Prompt: "Enter a description for this stash (optional):"
   - Default to "WIP" if empty

3. Execute stash:
   ```bash
   git stash push -m "claude:[session_id] [message]"
   ```

4. Confirm success with stash reference.

### List

Show stash entries for a specific session or all claude-tagged stashes.

#### Workflow

1. Call AskUserQuestion:
   - Prompt: "Enter Session ID to filter (leave empty for all claude stashes):"

2. Execute based on input:
   ```bash
   # All claude stashes
   git stash list | grep "claude:"

   # Specific session
   git stash list | grep "claude:[session_id]"
   ```

3. Present results as table:
   | Index | Session ID | Message | Date |

### Pop

Restore stash by session ID.

#### Workflow

1. Call AskUserQuestion:
   - Prompt: "Enter the Session ID to restore:"

2. Find matching stash:
   ```bash
   git stash list | grep "claude:[session_id]"
   ```

3. If multiple matches, call AskUserQuestion with options list.

4. If single match, apply:
   ```bash
   git stash pop stash@{n}
   ```

5. Report restored files.

### Drop

Remove stash by session ID (irreversible).

#### Workflow

1. Call AskUserQuestion:
   - Prompt: "Enter the Session ID to drop:"

2. Find and display matching stash.

3. Call AskUserQuestion for confirmation:
   - Prompt: "Confirm drop stash@{n}? (yes/no)"

4. Execute only on explicit "yes":
   ```bash
   git stash drop stash@{n}
   ```

## Session ID Location

Users find Session ID in Claude Code statusline (bottom of terminal). Format: short hash (e.g., `abc123de`).

## Notes

- Stash includes untracked files by default (`-u` flag available)
- Multiple stashes per session allowed
- Empty working directory: stash command will fail gracefully
- Session ID validation: 8+ alphanumeric characters expected
