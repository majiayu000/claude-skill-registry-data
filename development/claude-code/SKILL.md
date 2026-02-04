---
name: claude-code
description: "Claude Code expert guidance - features, configuration, hooks, plugins, MCP servers, IDE integration, and enterprise deployment"
---

# Claude Code Expert Skill

This skill provides guidance on using Claude Code, Anthropic's agentic coding tool.

## When to Use

Activate when users need help with:
- Understanding Claude Code features
- Setting up hooks, plugins, or MCP servers
- Working with slash commands
- Troubleshooting issues
- Best practices

## Core Concepts

**Claude Code** is an agentic coding tool in your terminal that:
- Autonomously plans, executes, and validates tasks
- Supports plugins, skills, and MCP servers for extensibility
- Integrates with VS Code and JetBrains IDEs

### Key Components

| Component | Purpose |
|-----------|---------|
| **Slash Commands** | User operations like `/fix`, `/plan`, `/commit` |
| **Skills** | Modular capabilities in `.claude/skills/` |
| **Hooks** | Shell commands on events (PreToolUse, PostToolUse) |
| **MCP Servers** | External tool integrations via `.mcp.json` |
| **Plugins** | Packaged collections of commands/skills/hooks |

## Common Workflows

```bash
# Feature implementation
/cook implement user authentication

# Bug fixing
/fix the login button is not working

# Planning
/plan implement payment integration

# Git operations
/commit
```

## Quick Setup

### MCP Server
```json
// .mcp.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your_token" }
    }
  }
}
```

### Hook Example
```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": ["./scripts/format.sh"]
    }]
  }
}
```

## References

For detailed documentation:
- `references/slash-commands.md` - Full command reference
- `references/skills-plugins.md` - Creating skills and plugins
- `references/mcp-hooks.md` - MCP and hooks configuration
- `references/troubleshooting.md` - Debugging and best practices

## IDE Integration

**VS Code / JetBrains**: Install "Claude Code" extension, authenticate, use inline chat and code actions.

## Essential Commands

```bash
/help                  # Show available commands
/clear                 # Clear conversation
/memory                # View stored context
/compact               # Summarize conversation
/plugins               # List installed plugins
```
