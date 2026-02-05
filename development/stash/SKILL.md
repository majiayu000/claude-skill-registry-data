---
name: stash
description: |
  This skill should be used when the user asks to "stash with session", "save work for later session", "link stash to session", "find stash by session ID", or "restore session stash". Saves git changes associated with Claude Code session ID for later retrieval.
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

Stash current changes with current session ID tag.

**Current Session ID**: `${CLAUDE_SESSION_ID}`

#### Workflow

1. Call AskUserQuestion to collect stash message:
   - Prompt: "Enter a description for this stash (optional):"
   - Default to "WIP" if empty

2. Execute stash:
   ```bash
   git stash push -m "claude:${CLAUDE_SESSION_ID} [message]"
   ```

3. Confirm success with stash reference.

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

## Session ID Format

- **Save**: Uses `${CLAUDE_SESSION_ID}` (full UUID, e.g., `02349458-8910-4228-b931-ac9f0c83081e`)
- **List/Pop/Drop**: Accepts both full UUID and short hash (first 8 characters)

## Notes

- Stash includes untracked files by default (`-u` flag available)
- Multiple stashes per session allowed
- Empty working directory: stash command will fail gracefully
- Full UUID enables direct matching with session files in `~/.claude/projects/`
