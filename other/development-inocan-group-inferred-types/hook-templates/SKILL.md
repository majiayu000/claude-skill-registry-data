---
name: hook-templates
description: Comprehensive Claude Code hook patterns for automation, state management, and external integration. Use when implementing hooks for validation, workflow gates, MCP integration, or state machines.
allowed-tools: ["Read", "Write", "Bash", "Grep", "Glob"]
---

# Hook Patterns

Production-tested patterns for Claude Code hooks (1.0.40+).

## Hook Roles (Beyond Just Validation)

| Role | Hook Event | Example |
|------|------------|---------|
| **Gate** | PreToolUse | Block dangerous commands, require prerequisites |
| **Side Effect** | PostToolUse | Auto-format, auto-commit, lint |
| **State Manager** | PostToolUse | Create/delete state files, track workflow phase |
| **External Integrator** | Any | MCP calls, HTTP APIs, WebSocket |
| **Context Injector** | SessionStart | Load project context, activate services |

## Event Reference

| Event | Trigger | Can Block | Use For |
|-------|---------|-----------|---------|
| SessionStart | Session begins | No | Context loading, service activation |
| UserPromptSubmit | User sends message | Yes | Prompt validation, skill suggestion |
| PreToolUse | Before tool | **Yes** | Validation, workflow gates |
| PostToolUse | After tool | No | State updates, side effects |
| Stop | Claude stops | Yes | Quality gates, cleanup |
| SubagentStop | Subagent stops | Yes | Subagent quality gates |

## Exit Codes

| Code | PreToolUse/Stop | Others |
|------|-----------------|--------|
| 0 | Allow | Continue |
| 2 | **Block** (stderr→Claude) | Logged |
| 1, 3+ | **Block** | Logged |

## JSON Response (Advanced)

```json
{
  "decision": "approve|block",
  "reason": "Shown to user/Claude",
  "continue": true,
  "suppressOutput": false
}
```

## Quick Registration

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "script.sh", "timeout": 5 }]
    }]
  }
}
```

## Pattern Selection

| Need | Pattern | Reference |
|------|---------|-----------|
| **Force skill/agent activation** | Orchestration | [orchestration-templates.md](references/orchestration-templates.md) |
| Block dangerous actions | Gate Pattern | [gate-patterns.md](references/gate-patterns.md) |
| Auto-format/lint/commit | Side Effect Pattern | [side-effect-patterns.md](references/side-effect-patterns.md) |
| Full working examples | Examples | [full-examples.md](references/full-examples.md) |

## Orchestration Patterns (NEW)

Hook-based skill/agent activation with reliability stats:

| Pattern | Success | Use Case |
|---------|---------|----------|
| Forced Evaluation | **84%** | Force Claude to evaluate and use skills |
| Agent Router | **100%** | Route to plugin agents via Task tool |
| Context Injection | 100% | Load project context at session start |

See [orchestration-templates.md](references/orchestration-templates.md) for templates.

## Debugging

Common issues and solutions in [debugging-guide.md](references/debugging-guide.md).

Quick checklist:
- Hook executable? (`chmod +x`)
- Using `INPUT=$(cat)` to read stdin?
- Using `exit 2` for blocking (not exit 1)?
- Debug to stderr (`>&2`), output to stdout?
- New session after settings.json change?

## Common Mistakes

- Missing nested `hooks` array
- Missing `"type": "command"`
- Using exit 1 instead of exit 2 for blocking
- Object matcher (not supported) - use script parsing instead
