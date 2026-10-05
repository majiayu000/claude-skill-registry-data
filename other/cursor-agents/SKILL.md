---
name: cursor-agents
description: Configure and manage Cursor IDE agents for parallel AI-assisted development. Use when asked about Cursor agent mode, background agents, cloud agents, or multi-agent workflows.
---

# Cursor Agents

## Repository Pattern

Store agent configs in `agents/` directory, symlink to activate:

```
agents/
├── code-reviewer.md
├── test-writer.md
└── refactor-agent.md

# Activate in target project:
ln -s /path/to/agents/code-reviewer.md .cursor/agents/code-reviewer.md
```

## Agent Capabilities

- Run up to 8 agents in parallel on a single prompt
- Each agent operates in isolated codebase copy (git worktrees or remote)
- Cloud agents: 99.9% reliability, instant startup

## Agent Modes

| Mode | Description |
|------|-------------|
| Normal | Standard agent with confirmations |
| YOLO | Auto-approve actions (use with caution) |
| Cloud | Run agents on Cursor's infrastructure |

## Workflow

1. Create agent config in `agents/<name>.md`
2. Symlink to project's `.cursor/agents/` to activate
3. Remove symlink to deactivate (config remains in repo)

## CLI Commands

```bash
/models    # List available models
/rules     # Manage rules
/mcp       # Manage MCP servers
```

Combine with `rules/` for consistent agent behavior across projects.
