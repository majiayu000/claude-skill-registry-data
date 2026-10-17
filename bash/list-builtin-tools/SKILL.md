---
name: list:builtin-tools
description: List all built-in Claude Code tools
disable-model-invocation: true
---

## Context

Claude Code has a set of built-in tools that are always available, separate from MCP server tools. Users may want to see what built-in tools are available for reference.

Tools denied via `permissions.deny` in settings are removed from the session entirely — they never appear in the tool list, not even as deferred tools. So the live tool list alone under-reports what the harness ships: a denied tool looks identical to a tool that doesn't exist. Read the settings files to tell the two apart.

## Your task

1. Read the `permissions.deny` array from each settings file that applies, in order: `~/.claude/settings.json`, `.claude/settings.json`, `.claude/settings.local.json`. Collect bare tool-name entries (e.g. `NotebookEdit`); ignore scoped ones like `Bash(rm -rf /*:*)`, which gate arguments rather than the tool.
2. List all built-in Claude Code tools (excluding MCP tools that start with `mcp__`) — both the ones available this session and the ones denied by those settings.

For each tool, provide:

- Tool name in backticks
- Brief description (one line)
- `— disabled (deny: <settings file>)` suffix if it was denied

Organize by category:

- File Operations
- Execution & Shell
- Web Access
- Task Management
- Integration

Deferred tools (schemas loaded on demand via `ToolSearch`) are available — list them normally, not as disabled.

Use compact format with minimal formatting.
