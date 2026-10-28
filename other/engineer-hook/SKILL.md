---
name: engineer-hook
description: >-
  Create and configure event hooks/plugins that manage agent behavior — command
  filtering, auditing, automation, script-based blocking of actions. Use when
  you need to create or configure a hook. Works across IDEs (Cursor, Claude
  Code, OpenCode).
---

# Hook / Plugin Creator

## Overview

This skill helps design and implement event hooks (or plugins). Hooks allow intercepting agent actions (command execution, file read/write, tool usage) and applying rules: allow, block (with explanation), request confirmation, or modify input data.

## IDE Detection and Hook Placement

### Hook Paths by IDE

| IDE | User Hooks | Project Hooks | Format |
|-----|-----------|--------------|--------|
| **Cursor** | `~/.cursor/hooks.json` | `.cursor/hooks.json` | JSON config + shell scripts |
| **Claude Code** | `~/.claude/settings.json` | `.claude/settings.json`<br>`.claude/settings.local.json` | JSON config (4 hook types) |
| **OpenCode** | `~/.config/opencode/plugins/*.{js,ts}` | `.opencode/plugins/*.{js,ts}`<br>`opencode.json` `plugin` (npm) | JS/TS modules (event-based) |

### Detection Strategy

1. Check for IDE-specific markers:
   - `.cursor/` directory → Cursor
   - `.claude/` directory → Claude Code
   - `.opencode/` directory or `opencode.json` → OpenCode
2. If multiple detected or none → ask the user

**IMPORTANT**: After detecting the IDE, read ONLY the corresponding reference file. Do not load all references.

## Hook Type Availability Matrix

| Type | Cursor | Claude Code | OpenCode |
|------|--------|-------------|----------|
| **Command** (shell script) | Yes | Yes | No (use plugin code) |
| **Prompt** (LLM-evaluated) | Yes | Yes (8 events) | No |
| **HTTP** (POST to URL) | No | Yes | No |
| **Agent** (multi-turn subagent) | No | Yes (8 events) | No |
| **Programmatic** (JS/TS code) | No | No | Yes |

## Cross-IDE Event Mapping

| Cursor Event | Claude Code Event | OpenCode Equivalent |
|:---|:---|:---|
| `beforeShellExecution` | `PreToolUse` (matcher: `"Bash"`) | `tool.execute.before` |
| `afterShellExecution` | `PostToolUse` (matcher: `"Bash"`) | `tool.execute.after` |
| `preToolUse` | `PreToolUse` | `tool.execute.before` |
| `postToolUse` | `PostToolUse` | `tool.execute.after` |
| `postToolUseFailure` | `PostToolUseFailure` | `event` → `tool.execute.after` |
| `sessionStart` | `SessionStart` | `event` → `session.created` |
| `sessionEnd` | `SessionEnd` | `event` → `session.deleted` |
| `subagentStart` | `SubagentStart` | — |
| `subagentStop` | `SubagentStop` | — |
| `stop` | `Stop` | `event` → `session.idle` |
| `preCompact` | `PreCompact` | `experimental.session.compacting` |
| `afterFileEdit` | `PostToolUse` (matcher: `"Edit\|Write"`) | `event` → `file.edited` |
| `beforeSubmitPrompt` | `UserPromptSubmit` | `chat.message` |
| `beforeMCPExecution` | `PreToolUse` (matcher: `"mcp__.*"`) | `tool.execute.before` |
| `afterMCPExecution` | `PostToolUse` (matcher: `"mcp__.*"`) | `tool.execute.after` |
| `beforeReadFile` | `PreToolUse` (matcher: `"Read"`) | `tool.execute.before` |
| — | `PermissionRequest` | `permission.ask` |
| — | `Notification` | `event` → various |
| — | `TeammateIdle` | — |
| — | `TaskCompleted` | `event` → `todo.updated` |
| — | `ConfigChange` | — |
| — | `InstructionsLoaded` | — |
| — | `WorktreeCreate` / `WorktreeRemove` | — |

## Main Workflow

1. **Detect IDE** using markers above
2. **Read the IDE-specific reference** (see Resources below)
3. **Define the Event**: Choose from the mapping table above
4. **Choose Implementation Type** per availability matrix
5. **Configure**: Add config to the correct location
6. **Implement Logic**: Create the script/plugin
7. **Test**: Verify the hook fires correctly

## Cursor Hooks

JSON config + shell scripts. Two types: `command` and `prompt`.

### Configuration

In `.cursor/hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [{ "command": ".cursor/hooks/format.sh" }],
    "beforeShellExecution": [
      { "command": ".cursor/hooks/guard.sh", "matcher": "rm " }
    ]
  }
}
```

### Implementation Types

1. **Command-based**: Shell script receiving JSON via stdin, returning JSON via stdout. Exit 0 = success, 2 = deny.
2. **Prompt-based**: LLM-evaluated condition.
   ```json
   { "type": "prompt", "prompt": "Is this command safe?", "timeout": 10 }
   ```

### Full Reference

For events list, input/output schemas, env vars, matcher values: see [hooks_api.md](references/hooks_api.md).

### Example: Blocking Dangerous Commands

**guard.sh**:
```bash
#!/bin/bash
input=$(cat)
command=$(echo "$input" | jq -r '.command')
if [[ "$command" == *"rm -rf"* ]]; then
  echo '{"permission": "ask", "user_message": "Are you sure?", "agent_message": "rm -rf requires confirmation."}'
else
  echo '{"permission": "allow"}'
fi
```

## Claude Code Hooks

JSON config in `settings.json`. Four types: `command`, `http`, `prompt`, `agent`.

### Configuration

In `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/guard.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Note the **nested structure**: each event maps to an array of matcher groups, each containing a `hooks` array.

### Implementation Types

1. **Command**: Shell script. Exit 0 = allow, exit 2 = block (stderr = reason).
2. **HTTP**: POST event data to URL. Response body parsed as JSON.
3. **Prompt**: Single-turn LLM evaluation with `$ARGUMENTS` placeholder.
4. **Agent**: Multi-turn subagent verification with tool access (up to 50 turns).

Prompt/agent types only available for 8 events: `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `UserPromptSubmit`.

### Full Reference

For all 18 events, input/output schemas, env vars, exit code behavior per event: see [claude_code_hooks_api.md](references/claude_code_hooks_api.md).

### Example: Blocking Dangerous Commands

**guard.sh** (same script works for both Cursor and Claude Code):
```bash
#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
tool_input=$(echo "$input" | jq -r '.tool_input.command // empty')
if [[ "$tool_input" == *"rm -rf"* ]]; then
  echo "Blocked: rm -rf requires manual confirmation" >&2
  exit 2
fi
exit 0
```

## OpenCode Plugins

JS/TS modules returning a `Hooks` object. No JSON config — all logic is code.

### Plugin Structure

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export default (async ({ project, client, $, directory, worktree }) => {
  return {
    "tool.execute.before": async (input) => {
      // inspect/modify tool arguments
      return input
    },
    event: async (event) => {
      // handle any system event
    },
  }
}) satisfies Plugin
```

### Distribution

- Local: `.opencode/plugins/*.ts`
- npm: `opencode.json` → `"plugin": ["package-name"]`

### Full Reference

For all hooks, events, `tool()` helper, examples: see [opencode_plugins_api.md](references/opencode_plugins_api.md).

### Example: Blocking Dangerous Commands

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export default (async ({ client }) => ({
  "tool.execute.before": async (input) => {
    if (input.tool === "bash" && input.args?.command?.includes("rm -rf")) {
      client.app.log({ body: { level: "warn", message: "Blocked rm -rf" } })
      return { ...input, args: { command: "echo 'Blocked: rm -rf not allowed'" } }
    }
    return input
  },
})) satisfies Plugin
```

## Resources

- [hooks_api.md](references/hooks_api.md) — Cursor: full event list, I/O formats, env vars
- [claude_code_hooks_api.md](references/claude_code_hooks_api.md) — Claude Code: 18 events, 4 hook types, settings.json format
- [opencode_plugins_api.md](references/opencode_plugins_api.md) — OpenCode: plugin API, hooks, events, tool() helper
- `assets/hook_template.sh` — Bash script template for command-type hooks

## Tips

- **All IDEs**: Paths in hook configs are relative to project root
- **Cursor**: Use `matcher` so hooks only fire for relevant commands
- **Cursor**: Debug via "Hooks" tab in settings or "Hooks" output channel
- **Cursor**: Set `failClosed: true` for security-critical hooks
- **Claude Code**: Use `claude --debug` or `Ctrl+O` for verbose hook logging
- **Claude Code**: Interactive `/hooks` menu available for managing hooks
- **Claude Code**: Check `stop_hook_active` in Stop hooks to prevent infinite loops
- **Claude Code**: `PermissionRequest` hooks don't fire in non-interactive mode (`-p`)
- **OpenCode**: Plugin dependencies go in `.opencode/package.json` (Bun auto-installs)
- **OpenCode**: Plugin tools override built-in tools with matching names
