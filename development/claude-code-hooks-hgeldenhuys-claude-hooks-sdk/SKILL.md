---
name: claude-code-hooks
description: Guide for implementing Claude Code hooks - automated scripts that execute at specific workflow points. Use when building hooks, understanding hook events, or troubleshooting hook configuration.
---

# Claude Code Hooks Implementation Guide

Implement automated hooks that execute bash commands or TypeScript scripts in response to Claude Code events.

## Quick Reference

### 9 Available Hook Events

1. **PreToolUse** - Before tool execution (validation, blocking)
2. **PostToolUse** - After tool success (formatting, testing)
3. **Notification** - On Claude notifications
4. **UserPromptSubmit** - Before processing user input (context injection)
5. **Stop** - When main agent finishes responding
6. **SubagentStop** - When subagent completes
7. **PreCompact** - Before context compaction
8. **SessionStart** - Session begins
9. **SessionEnd** - Session ends

### Hook Input (stdin JSON)

```json
{
  "session_id": "...",
  "transcript_path": "...",
  "cwd": "/current/working/dir",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "...", "content": "..."},
  "tool_response": "..."
}
```

### Hook Output Mechanisms

**Exit Codes:**
- `0` - Success (stdout → transcript, or context if UserPromptSubmit)
- `2` - Blocking error (stderr → Claude feedback)
- Other - Non-blocking error (shown to user)

**JSON Output (stdout):**
```json
{
  "continue": true,
  "stopReason": "optional message",
  "suppressOutput": true,
  "decision": "allow|deny|ask",
  "hookSpecificOutput": {}
}
```

## Recommended: Use claude-hooks-sdk for TypeScript

For TypeScript hooks, use the SDK for type safety and utilities:

```bash
bun add claude-hooks-sdk
```

```typescript
#!/usr/bin/env bun
import { HookManager, success, block, createLogger } from 'claude-hooks-sdk';

const logger = createLogger('my-hook');

const manager = new HookManager({
  logEvents: true,
  clientId: 'my-hook',
  trackEdits: true,
});

manager.onPreToolUse(async (input) => {
  if (input.tool_name === 'Bash' && input.tool_input.command.includes('rm -rf /')) {
    logger.warn('Blocked dangerous command');
    return block('Dangerous command blocked');
  }
  return success();
});

manager.run();
```

## Common Use Cases

### 1. Code Formatting (PostToolUse)

**Configuration** (`.claude/settings.json`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Script** (`.claude/hooks/format-code.sh`):
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$FILE_PATH" =~ \.(ts|tsx|js|jsx)$ ]]; then
  npx prettier --write "$FILE_PATH" 2>&1
  echo "✓ Formatted: $FILE_PATH"
fi

exit 0
```

### 2. Security Validation (PreToolUse)

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Block dangerous patterns
if [[ "$COMMAND" =~ (rm\ -rf\ /|\.\./) ]]; then
  echo '{"decision": "deny", "continue": false}' | jq
  echo "❌ Blocked: Dangerous command" >&2
  exit 2
fi

echo '{"decision": "allow", "continue": true}' | jq
exit 0
```

### 3. Context Injection (UserPromptSubmit)

**Using SDK (recommended)**:
```typescript
#!/usr/bin/env bun
import { createUserPromptSubmitHook } from 'claude-hooks-sdk';

// ONE LINE - injects session ID and name into Claude's context
createUserPromptSubmitHook();
```

### 4. Environment Setup (SessionStart)

```bash
#!/bin/bash
if [ ! -d "node_modules" ]; then
  bun install
fi

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo "export NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
fi

echo "✓ Environment ready"
exit 0
```

## Configuration Patterns

### Project-Specific Hooks

Store in `.claude/settings.json` (project root):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh"}
        ]
      }
    ]
  }
}
```

### Global Hooks

Store in `~/.claude/settings.json` (user home).

## Troubleshooting

### Hook Not Executing
1. Check matcher pattern (case-sensitive)
2. Verify script permissions: `chmod +x script.sh`
3. Enable debug mode: `claude --debug`

### Hook Blocking Execution
1. Exit code 2 blocks, other codes don't
2. `{"decision": "deny"}` blocks PreToolUse

## Resources

- [Official Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [claude-hooks-sdk on npm](https://www.npmjs.com/package/claude-hooks-sdk)
- [claude-hooks-sdk on GitHub](https://github.com/hgeldenhuys/claude-hooks-sdk)
