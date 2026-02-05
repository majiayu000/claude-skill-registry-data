---
name: manage-hooks
description: MUST INVOKE this skill when working with hooks, setting up event listeners, validating commands, automating workflows, adding notifications, or understanding hook types (PreToolUse, PostToolUse, Stop, SessionStart, UserPromptSubmit, etc). Expert guidance for creating, configuring, and using AI agent hooks (Claude Code-specific).
---

## Objective

Hooks are event-driven automation for Claude Code that execute shell commands or LLM prompts in response to tool usage, session events, and user interactions. This skill teaches you how to create, configure, and debug hooks for validating commands, automating workflows, injecting context, and implementing custom completion criteria.

Hooks provide programmatic control over Claude's behavior without modifying core code, enabling project-specific automation, safety checks, and workflow customization.

## Context

Hooks are shell commands or LLM-evaluated prompts that execute in response to Claude Code events. They operate within an event hierarchy: events (PreToolUse, PostToolUse, Stop, etc.) trigger matchers (tool patterns) which fire hooks (commands or prompts). Hooks can block actions, modify tool inputs, inject context, or simply observe and log Claude's operations.

## Quick Start

### Workflow

1. **Create Hook Directory**:
   ```bash
   mkdir -p .claude/hooks/scripts
   ```

2. **Use the [create-new-hook workflow](workflows/create-new-hook.md)** to:
   - Define hook purpose (event, tools, action)
   - Create hook script (Python with error handling)
   - Generate hooks.json configuration
   - Test the hook

3. **Test with** `claude --debug`

### Example: File Protection Hook

**Generated Structure:**
```
.claude/hooks/
├── hooks.json              # Hook configuration
└── scripts/
    └── protect-files.py    # Hook script
```

**hooks.json:**
```json
{
  "description": "File protection and security checks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/.claude/hooks/scripts/protect-files.py"
          }
        ]
      }
    ]
  }
}
```

This hook:
- Fires before (`PreToolUse`) every `Edit` or `Write` tool use
- Executes a Python script
- Warns about edits to sensitive files

See references/hook-examples.md for more working examples.

## Hook Types

| Event | When it fires | Can block? |
|-------|---------------|------------|
| **PreToolUse** | Before tool execution | Yes |
| **PostToolUse** | After tool execution | No |
| **UserPromptSubmit** | User submits a prompt | Yes |
| **Stop** | Claude attempts to stop | Yes |
| **SubagentStop** | Subagent attempts to stop | Yes |
| **SessionStart** | Session begins | No |
| **SessionEnd** | Session ends | No |
| **PreCompact** | Before context compaction | Yes |
| **Notification** | Claude needs input | No |

Blocking hooks can return `"decision": "block"` to prevent the action. See [references/hook-types.md](references/hook-types.md) for detailed use cases.

## Hook Anatomy

### Command Hook

**Type**: Executes a shell command

**Use when**:

- Simple validation (check file exists)
- Logging (append to file)
- External tools (formatters, linters)
- Desktop notifications

**Input**: JSON via stdin
**Output**: JSON via stdout (optional)

```json
{
  "type": "command",
  "command": "/path/to/script.sh",
  "timeout": 30000
}
```

### Prompt Hook

**Type**: LLM evaluates a prompt

**Use when**:

- Complex decision logic
- Natural language validation
- Context-aware checks
- Reasoning required

**Input**: Prompt with `$ARGUMENTS` placeholder
**Output**: JSON with `decision` and `reason`

```json
{
  "type": "prompt",
  "prompt": "Evaluate if this command is safe: $ARGUMENTS\n\nReturn JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
}
```

## Matchers

Matchers filter which tools trigger the hook:

```json
{
  "matcher": "Bash",           // Exact match
  "matcher": "Write|Edit",     // Multiple tools (regex OR)
  "matcher": "mcp__.*",        // All MCP tools
  "matcher": "mcp__memory__.*" // Specific MCP server
}
```

No matcher: Hook fires for all tools

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [...]  // No matcher - fires on every user prompt
      }
    ]
  }
}
```

## Input/Output

Hooks receive JSON via stdin with session info, current directory, and event-specific data. Blocking hooks can return JSON to approve/block actions or modify inputs.

Example output (blocking hooks):

```json
{
  "decision": "approve" | "block",
  "reason": "Why this decision was made"
}
```

See [references/input-output-schemas.md](references/input-output-schemas.md) for complete schemas for each hook type.

## Environment Variables

Available in hook commands:

| Variable | Value |
|----------|-------|
| `$CLAUDE_PROJECT_DIR` | Project root directory |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin directory (plugin hooks only) |
| `$ARGUMENTS` | Hook input JSON (prompt hooks only) |

Example:

```json
{
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.sh"
}
```

## Common Patterns

Desktop notification when input needed:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

Block destructive git commands:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if this command is destructive: $ARGUMENTS\n\nBlock if it contains: 'git push --force', 'rm -rf', 'git reset --hard'\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}"
          }
        ]
      }
    ]
  }
}
```

Auto-format code after edits:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_PROJECT_DIR",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

Add context at session start:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": \"Current sprint: Sprint 23. Focus: User authentication\"}}'"
          }
        ]
      }
    ]
  }
}
```

## Debugging

Always test hooks with the debug flag:

```bash
claude --debug
```

This shows which hooks matched, command execution, and output. See [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions.

## Reference Guides

Hook types and events: [references/hook-types.md](references/hook-types.md)

- Complete list of hook events
- When each event fires
- Input/output schemas for each
- Blocking vs non-blocking hooks

Command vs Prompt hooks: [references/command-vs-prompt.md](references/command-vs-prompt.md)

- Decision tree: which type to use
- Command hook patterns and examples
- Prompt hook patterns and examples
- Performance considerations

Matchers and patterns: [references/matchers.md](references/matchers.md)

- Regex patterns for tool matching
- MCP tool matching patterns
- Multiple tool matching
- Debugging matcher issues

Input/Output schemas: [references/input-output-schemas.md](references/input-output-schemas.md)

- Complete schema for each hook type
- Field descriptions and types
- Hook-specific output fields
- Example JSON for each event

Working examples: [references/examples.md](references/examples.md)

- Desktop notifications
- Command validation
- Auto-formatting workflows
- Logging and audit trails
- Stop logic patterns
- Session context injection

Troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

- Hooks not triggering
- Command execution failures
- Prompt hook issues
- Permission problems
- Timeout handling
- Debug workflow

## Security Checklist

Critical safety requirements:

- Infinite loop prevention: Check `stop_hook_active` flag in Stop hooks to prevent recursive triggering
- Timeout configuration: Set reasonable timeouts (default: 60s) to prevent hanging
- Permission validation: Ensure hook scripts have executable permissions (`chmod +x`)
- Path safety: Use absolute paths with `$CLAUDE_PROJECT_DIR` to avoid path injection
- JSON validation: Validate hook config with `jq` before use to catch syntax errors
- Selective blocking: Be conservative with blocking hooks to avoid workflow disruption

Testing protocol:

```bash
# Always test with debug flag first
claude --debug

# Validate JSON config
jq . .claude/hooks.json
```

## Success Criteria

A working hook configuration has:

- Valid JSON in `.claude/hooks.json` (validated with `jq`)
- Appropriate hook event selected for the use case
- Correct matcher pattern that matches target tools
- Command or prompt that executes without errors
- Proper output schema (decision/reason for blocking hooks)
- Tested with `--debug` flag showing expected behavior
- No infinite loops in Stop hooks (checks `stop_hook_active` flag)
- Reasonable timeout set (especially for external commands)
- Executable permissions on script files if using file paths
