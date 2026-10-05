---
name: git-guardrails
description: Set up Claude Code hooks to block dangerous Git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive Git operations, add Git safety hooks, or block Git push/reset in Claude Code.
---

# Git Guardrails

Sets up a `PreToolUse` hook that intercepts and blocks dangerous Git commands before Claude executes them.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Steps

### 1. Ask Scope

Ask the user's preference: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the Hook script

The bundled script is at: [scripts/block-dangerous-commands.sh](scripts/block-dangerous-commands.sh)

Copy it to the target location based on scope:

-- **Project**: `.claude/hooks/block-dangerous-commands.sh`
-- **Global**: `~/.claude/hooks/block-dangerous-commands.sh`

Make it executable with `chmod +x`.

### 3. Add Hook to Settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-commands.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-commands.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array. Don't overwrite other settings.

### 4. Ask About Customization

Ask the user if they want to add or remove any patterns from the blocked list. Edit the copied script accordingly.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
```

Should exit with code `2` and print a `BLOCKED` message to stderr.
