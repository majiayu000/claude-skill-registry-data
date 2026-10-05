---
name: claude-agents
description: Create and configure Claude Code subagents for task-specific workflows. Use when creating new agents, updating agent configurations, or understanding agent best practices.
---

# Claude Code Subagents

Create specialized AI subagents that handle specific types of tasks with isolated context, custom tools, and focused system prompts.

## File Structure

Subagents are Markdown files with YAML frontmatter stored in:
- `.claude/agents/` - Project-level (check into version control)
- `~/.claude/agents/` - User-level (available in all projects)

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase letters and hyphens only |
| `description` | Yes | When Claude should delegate (include "use proactively" for automatic use) |
| `tools` | No | Tools to allow (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` (default: inherit) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | No | Skills to preload into subagent context |
| `hooks` | No | Lifecycle hooks for this subagent |

## Available Tools

Read-only: `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`
Modification: `Write`, `Edit`, `NotebookEdit`
Execution: `Bash`, `Task`
Other: `AskUserQuestion`, `Skill`, `mcp__*` (MCP tools)

## Template

```markdown
---
name: my-agent
description: Brief description of purpose. Use proactively when [trigger conditions].
tools: Read, Glob, Grep, Bash
model: sonnet
skills:
  - relevant-skill-name
---

You are a [role] responsible for [responsibilities].

## When Invoked

1. [First step]
2. [Second step]
3. [Continue as needed]

## Key Practices

- [Practice 1]
- [Practice 2]

## Output Format

[Describe expected output structure]
```

## Best Practices

1. **Focus on one task** - Each subagent should excel at a specific purpose
2. **Write detailed descriptions** - Claude uses this to decide when to delegate
3. **Limit tool access** - Grant only necessary permissions for security
4. **Preload relevant skills** - Use `skills` field for domain knowledge
5. **Include trigger phrases** - Add "use proactively" for automatic delegation
6. **Specify model wisely** - Use `haiku` for fast/cheap, `sonnet` for balanced, `opus` for complex

## Model Selection

| Model | Use When |
|-------|----------|
| `haiku` | Fast exploration, simple validation, high-volume operations |
| `sonnet` | Balanced capability and speed, code analysis, most tasks |
| `opus` | Complex reasoning, architecture decisions, nuanced analysis |
| `inherit` | Match parent conversation model |

## Tool Restriction Patterns

### Read-only Agent
```yaml
tools: Read, Glob, Grep, Bash
disallowedTools: Write, Edit
```

### Code Modification Agent
```yaml
tools: Read, Write, Edit, Bash, Glob, Grep
```

### Research Agent
```yaml
tools: Read, Glob, Grep, WebFetch, WebSearch
```

## Hooks

Subagents can define hooks in frontmatter:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
```

## Common Patterns

### Isolate Verbose Output
Delegate test runs, log analysis, or documentation fetching to subagents to keep main context clean.

### Parallel Research
Spawn multiple subagents for independent investigations, then synthesize results.

### Chain Subagents
Use subagents in sequence: reviewer → optimizer → validator.
