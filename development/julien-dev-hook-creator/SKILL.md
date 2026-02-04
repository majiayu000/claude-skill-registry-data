---
name: julien-dev-hook-creator
description: Guide for creating Claude Code hooks - shell commands that execute at specific lifecycle events (SessionStart, SessionEnd, PreToolUse, PostToolUse, etc.). Use when users want to automate actions, add validation, logging, or integrate external tools into Claude Code workflows.
license: Apache-2.0
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "development"
triggers:
  - "create hook"
  - "new hook"
  - "add hook"
  - "hook template"
  - "write hook"
  - "build hook"
  - "créer hook"
  - "nouveau hook"
  - "ajouter hook"
  - "écrire hook"
  - "SessionStart"
  - "SessionEnd"
  - "PreToolUse"
  - "PostToolUse"
  - "UserPromptSubmit"
  - "claude code hook"
  - "automation hook"
---

# Hook Creator

This skill guides the creation of Claude Code hooks - deterministic shell commands or LLM prompts that execute at specific points in Claude's lifecycle.

## What Are Hooks?

Hooks provide **deterministic control** over Claude's behavior. Unlike skills (which Claude chooses to use), hooks **always execute** at their designated lifecycle event.

```
┌─────────────────────────────────────────────────────────────────┐
│                    HOOKS vs SKILLS                              │
├─────────────────────────────────────────────────────────────────┤
│  HOOKS: Deterministic, always run at lifecycle events           │
│  SKILLS: Model-invoked, Claude decides when to use              │
└─────────────────────────────────────────────────────────────────┘
```

## Available Hook Events

| Event | When It Runs | Common Use Cases |
|-------|--------------|------------------|
| `SessionStart` | Session begins/resumes | Load context, sync data, set env vars |
| `SessionEnd` | Session ends | Cleanup, save state, push changes |
| `PreToolUse` | Before tool execution | Validate, block, modify tool input |
| `PostToolUse` | After tool completes | Format output, log, trigger actions |
| `PermissionRequest` | Permission dialog shown | Auto-approve or deny permissions |
| `UserPromptSubmit` | User submits prompt | Add context, validate requests |
| `Notification` | Claude sends notification | Custom alerts |
| `Stop` | Claude finishes responding | Decide if Claude should continue |
| `SubagentStop` | Subagent completes | Evaluate task completion |

## Hook Configuration

Hooks are configured in `~/.claude/settings.json` (global) or `.claude/settings.json` (project).

### Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `matcher` | For tool events | Pattern to match tool names (regex supported) |
| `type` | Yes | `"command"` (shell) or `"prompt"` (LLM) |
| `command` | For type:command | Shell command to execute |
| `prompt` | For type:prompt | LLM prompt for evaluation |
| `timeout` | No | Seconds before timeout (default: 60, max: 300) |

### Matcher Patterns

```json
"matcher": "Write"           // Exact match
"matcher": "Edit|Write"      // OR pattern (regex)
"matcher": "Notebook.*"      // Wildcard pattern
"matcher": "*"               // All tools (or omit matcher)
```

## Hook Input (stdin)

Hooks receive JSON via stdin with context about the event:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  }
}
```

## Hook Output (Exit Codes)

| Exit Code | Behavior |
|-----------|----------|
| `0` | Success - continue normally |
| `2` | **Block** - stderr fed to Claude, action blocked |
| Other | Non-blocking error (shown in verbose mode) |

### Advanced JSON Output (exit 0)

```json
{
  "continue": true,
  "stopReason": "message if continue=false",
  "suppressOutput": true,
  "systemMessage": "warning shown to user"
}
```

### PreToolUse Decision Control

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Reason here",
    "updatedInput": {
      "field": "modified value"
    }
  }
}
```

## Creating a Hook - Step by Step

### Step 1: Identify the Use Case

Ask:
- **When** should this run? (which event)
- **What** should it do? (validate, log, transform, block)
- **Scope**: Global (`~/.claude/settings.json`) or project (`.claude/settings.json`)?

### Step 2: Write the Script

Create script in `~/.claude/scripts/` or `.claude/scripts/`:

```bash
#!/bin/bash
# ~/.claude/scripts/my-hook.sh

# Read input from stdin
INPUT=$(cat)

# Parse with jq
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Your logic here
if [[ "$FILE_PATH" == *".env"* ]]; then
    echo "Blocked: Cannot modify .env files" >&2
    exit 2  # Block the action
fi

exit 0  # Allow the action
```

**Important**: Make executable with `chmod +x`

### Step 3: Configure the Hook

Add to settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/scripts/my-hook.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Step 4: Test

```bash
# Test script directly
echo '{"tool_name":"Write","tool_input":{"file_path":"/test/.env"}}' | bash ~/.claude/scripts/my-hook.sh
echo "Exit code: $?"
```

## Common Hook Patterns

### 1. File Protection (PreToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED=(".env" "package-lock.json" ".git/" "credentials")
for pattern in "${PROTECTED[@]}"; do
    if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Protected file: $pattern" >&2
        exit 2
    fi
done
exit 0
```

### 2. Auto-Format on Save (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$(cat | jq -r '.tool_input.file_path') && npx prettier --write \"$FILE\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 3. Command Logging (PostToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
DESC=$(echo "$INPUT" | jq -r '.tool_input.description // "No description"')
echo "$(date +%Y-%m-%d_%H:%M:%S) | $CMD | $DESC" >> ~/.claude/logs/bash-commands.log
exit 0
```

### 4. Session Sync (SessionStart/SessionEnd)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash ~/.claude/scripts/sync-marketplace.sh",
          "timeout": 30
        }]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [{
          "type": "command",
          "command": "bash ~/.claude/scripts/push-marketplace.sh",
          "timeout": 30
        }]
      }
    ]
  }
}
```

### 5. Add Context to Prompts (UserPromptSubmit)

```bash
#!/bin/bash
# stdout is added as context to the prompt
echo "Current git branch: $(git branch --show-current 2>/dev/null || echo 'not a git repo')"
echo "Node version: $(node -v 2>/dev/null || echo 'not installed')"
exit 0
```

### 6. LLM-based Stop Decision (Stop)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [{
          "type": "prompt",
          "prompt": "Review if all tasks are complete. Check: 1) All todos marked done 2) Tests passing 3) No pending questions. Respond with decision: approve (stop) or block (continue).",
          "timeout": 30
        }]
      }
    ]
  }
}
```

## Best Practices

### Do's
- ✅ Always quote shell variables: `"$VAR"` not `$VAR`
- ✅ Use absolute paths for scripts
- ✅ Handle errors gracefully (exit 0 if non-critical)
- ✅ Set appropriate timeouts
- ✅ Test scripts independently before configuring
- ✅ Use `tr -d '\r'` for Windows CRLF compatibility

### Don'ts
- ❌ Don't block critical operations without good reason
- ❌ Don't use long timeouts (blocks Claude)
- ❌ Don't trust input blindly - validate paths
- ❌ Don't expose secrets in logs
- ❌ Don't use interactive commands (no stdin available)

## Debugging Hooks

```bash
# Run with debug output
bash -x ~/.claude/scripts/my-hook.sh

# Test with sample input
echo '{"tool_name":"Write","tool_input":{"file_path":"/test/file.txt"}}' | bash ~/.claude/scripts/my-hook.sh

# Check hook errors in Claude Code
# Look for "hook error" messages in the UI
```

For detailed troubleshooting of common errors (timeout, CRLF, jq not found, etc.), see `references/troubleshooting.md`.

## Environment Variables

Available in hooks:
- `CLAUDE_PROJECT_DIR` - Current project directory
- `CLAUDE_CODE_REMOTE` - Remote mode indicator
- `CLAUDE_ENV_FILE` - (SessionStart only) File path for persisting env vars

## File Locations

| Location | Scope |
|----------|-------|
| `~/.claude/settings.json` | Global (all projects) |
| `.claude/settings.json` | Project-specific |
| `.claude/settings.local.json` | Local overrides (not committed) |
| `~/.claude/scripts/` | Global scripts |
| `.claude/scripts/` | Project scripts |

## Quick Reference

```
Event Flow:
SessionStart → UserPromptSubmit → PreToolUse → [Tool] → PostToolUse → Stop → SessionEnd

Exit Codes:
0 = Success (continue)
2 = Block (stop action, feed stderr to Claude)
* = Non-blocking error

Matcher:
"Write"        = exact match
"Edit|Write"   = OR
"Notebook.*"   = regex
"*" or omit    = all tools
```

## 🔗 Skill Chaining

### Skills Required Before
- Aucun (skill autonome)
- Optionnel: Connaissance de base de bash/shell scripting

### Input Expected
- **Use case description**: Quel événement déclencher, quelle action effectuer
- **Scope decision**: Global (`~/.claude/settings.json`) ou project (`.claude/settings.json`)
- **Prerequisites**: `jq` installé pour parsing JSON

### Output Produced
- **Format**:
  - Script bash dans `~/.claude/scripts/` ou `.claude/scripts/`
  - Configuration JSON dans `settings.json`
- **Side effects**:
  - Création/modification de fichiers scripts
  - Modification de settings.json
  - Hooks actifs au prochain événement
- **Duration**: 2-5 minutes pour un hook simple

### Compatible Skills After
**Recommandés**:
- **sync-personal-skills**: Si le hook modifie des fichiers du marketplace
- **skill-creator**: Si création d'un skill qui intègre des hooks

**Optionnels**:
- Git workflow: Committer les scripts et settings

### Called By
- Direct user invocation: "Crée un hook pour...", "Je veux automatiser..."
- Part of skill/workflow development

### Tools Used
- `Read` (lecture settings.json existant)
- `Write` (création scripts bash)
- `Edit` (modification settings.json)
- `Bash` (test du hook, chmod +x)

### Visual Workflow

```
User: "Je veux protéger les fichiers .env"
    ↓
hook-creator (this skill)
    ├─► Step 1: Identify event (PreToolUse)
    ├─► Step 2: Write script (protect-files.sh)
    ├─► Step 3: chmod +x script
    ├─► Step 4: Configure settings.json
    └─► Step 5: Test with sample input
    ↓
Hook active ✅
    ↓
[Next: Test in real session]
```

### Usage Example

**Scenario**: Créer un hook de logging des commandes bash

**Input**: "Log toutes les commandes bash exécutées"

**Process**:
1. Event identifié: `PostToolUse` avec matcher `Bash`
2. Script créé: `~/.claude/scripts/log-bash.sh`
3. Settings.json mis à jour avec hook config
4. Test avec sample JSON input

**Result**:
- Script logging actif
- Commandes loguées dans `~/.claude/logs/bash-commands.log`
