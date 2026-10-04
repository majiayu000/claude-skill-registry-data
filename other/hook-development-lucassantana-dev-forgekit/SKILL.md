---
name: hook-development
description: Use when creating hooks for Claude Code plugins. Covers hook events, configuration, exit codes, and stdin/stdout contracts. Hooks execute in response to events to validate operations and enforce policies.
---

# Hook Development for Claude Code Plugins

Hooks are event-driven scripts that validate operations, enforce policies, and add context.

## Hook Types

**Prompt-based** (LLM reasoning): Use for complex validation. Recommended.
```json
{"type": "prompt", "prompt": "Validate write safety. Check for: system paths, secrets, path traversal.", "timeout": 30}
```

**Command** (bash): Use for deterministic checks, fast operations.
```json
{"type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh", "timeout": 60}
```

## Hook Events

| Event | When | Use |
|-------|------|-----|
| PreToolUse | Before tool | Approve/deny/modify calls |
| PostToolUse | After tool | React to results, log |
| UserPromptSubmit | User prompt | Add context, validate |
| Stop | Agent stopping | Verify completion |
| SubagentStop | Subagent done | Ensure task complete |
| SessionStart | Session begins | Load context, env vars |

## Configuration

**Plugin:** `hooks/hooks.json` (with `"hooks"` wrapper)
```json
{"hooks": {"PreToolUse": [...]}}
```

**User settings:** `.claude/settings.json` (direct, no wrapper)
```json
{"PreToolUse": [...]}
```

## Exit Codes

- **0** — Success; stdout in transcript
- **2** — Block; stderr to Claude (halt)

Prompt hooks return JSON: `{decision: approve|block|ask}`

## stdin/stdout Contract

Input JSON includes `tool_name`, `tool_input` (PreToolUse), `user_prompt` (UserPromptSubmit), etc.

Output JSON:
```json
{"continue": true, "systemMessage": "..."}
```

## Example: Write Validation

```json
{
  "PreToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{"type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/validate.sh"}]
  }]
}
```

Script:
```bash
#!/bin/bash
input=$(cat)
file=$(echo "$input" | jq -r '.tool_input.file_path')

[[ "$file" == *".."* ]] && echo '{"decision":"deny"}' >&2 && exit 2
[[ "$file" == *".env"* ]] && echo '{"decision":"deny"}' >&2 && exit 2

echo '{"decision":"approve"}'
```

## Critical Rules

- Quote all bash variables: `"$var"` not `$var`
- Use `${CLAUDE_PLUGIN_ROOT}` for portability
- Set timeouts: command 60s, prompt 30s
- Validate all inputs
- Hooks load at session start — restart to apply changes

---

**See REFERENCE.md for:** full event catalog, matcher patterns, testing, environment variables.
