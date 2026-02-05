---
name: claude-code-cli
description: Build and run AI agents using Claude Code CLI. Use when developing autonomous agents, multi-agent systems, CI/CD automation, or scripting Claude for programmatic tasks. Covers authentication, headless mode (-p), JSON output parsing, tool restrictions, subagents, and orchestration patterns.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Claude Code Agent Development

Build autonomous agents using Claude Code CLI. Language-agnostic patterns for agent orchestration and programmatic integration.

## Quick Reference

| Task | Command |
|------|---------|
| Basic agent | `claude -p "prompt"` |
| JSON output | `claude -p --output-format json "prompt"` |
| Streaming | `claude -p --output-format stream-json "prompt"` |
| Autonomous | `claude -p --dangerously-skip-permissions "prompt"` |
| Budget limit | `claude -p --max-budget-usd 5 "prompt"` |
| Restrict tools | `claude -p --tools "Read,Edit" "prompt"` |
| Structured output | `claude -p --output-format json --json-schema '{...}' "prompt"` |

## Authentication

### API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### OAuth Token (Pro/Team Subscription)

```bash
claude setup-token  # Interactive setup
export CLAUDE_CODE_OAUTH_TOKEN="your-token"
```

## Running Agents

### Headless Mode (`-p`)

```bash
# Basic prompt
claude -p "Implement a REST API"

# Piped input
echo "Fix the bug" | claude -p

# Full autonomy (sandboxed environments only)
claude -p --dangerously-skip-permissions "Build the feature"
```

### Output Formats

| Format | Flag | Use Case |
|--------|------|----------|
| `text` | default | Simple scripts |
| `json` | `--output-format json` | Programmatic parsing |
| `stream-json` | `--output-format stream-json` | Real-time UI |

**For detailed parsing examples**: See [references/response-parsing.md](references/response-parsing.md)

### Structured Output

```bash
echo "What is 2+2?" | claude -p --output-format json \
  --json-schema '{"type":"object","properties":{"answer":{"type":"number"}},"required":["answer"]}'
```

Result: `{"type": "result", "structured_output": {"answer": 4}, ...}`

## Tool Restrictions

```bash
# Read-only agent
claude -p --tools "Read,Glob,Grep" "Analyze code"

# Specific bash commands only
claude -p --allowed-tools "Bash(npm:*) Bash(git:*)" "Build project"

# Deny dangerous operations
claude -p --disallowed-tools "Bash(rm:*)" "Clean up"
```

**For project configuration**: See [references/configuration.md](references/configuration.md)

## Multi-Agent Patterns

### Sequential Pipeline

```bash
analysis=$(claude -p --output-format json "Analyze codebase")
claude -p "Implement based on: $analysis"
```

### Parallel Agents

```bash
claude -p "Review auth/" > auth.txt &
claude -p "Review api/" > api.txt &
wait
claude -p "Summarize: $(cat *.txt)"
```

### Specialist Agents

```bash
claude --agents '{"security": {"prompt": "You are a security expert"}}' \
  --agent security -p "Review auth"
```

**For complete orchestration patterns**: See [references/orchestration.md](references/orchestration.md)

## Session Management

```bash
# Persistent session
claude --session-id "task-123" -p "Start feature"
claude --session-id "task-123" -c -p "Continue"

# Stateless
claude -p --no-session-persistence "One-off task"
```

## Project Configuration

### `.claude/settings.json`

```json
{
  "permissions": {
    "allow": ["Bash(npm:*)", "Edit", "Read"],
    "deny": ["Bash(rm -rf:*)"]
  }
}
```

### `CLAUDE.md`

Project instructions auto-loaded by Claude.

**For CI/CD and MCP**: See [references/configuration.md](references/configuration.md)

## Parsing JSON Output

### Quick jq Examples

```bash
# Get result
claude -p --output-format json "prompt" | jq -r '.[-1].result'

# Check success
claude -p --output-format json "prompt" | jq '.[-1].is_error'

# Get cost
claude -p --output-format json "prompt" | jq '.[-1].total_cost_usd'
```

### Message Types

| Type | Description |
|------|-------------|
| `system` | Init with tools, model, session |
| `assistant` | Claude's response |
| `user` | Tool results |
| `result` | Final status and cost |

**For complete parsing guide**: See [references/response-parsing.md](references/response-parsing.md)

## Best Practices

1. **Budget limits**: Always `--max-budget-usd` for autonomous agents
2. **Tool restrictions**: Minimal toolset with `--tools`
3. **Structured output**: `--json-schema` for reliable parsing
4. **Sandboxing**: `--dangerously-skip-permissions` only in isolated environments
5. **Error handling**: Check `is_error` and exit codes
