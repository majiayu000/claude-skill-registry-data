---
name: claude-code-plugin-dev
description: "Comprehensive guide for building, testing, and distributing Claude Code plugins including slash commands, Agent Skills, subagents, MCP servers, and hooks. Use this when the user asks about creating plugins, writing slash commands, implementing skills, building MCP tools, configuring hooks, plugin architecture, marketplace distribution, or debugging plugin components. Covers 2025 schema with tool permissions, version tracking, and activation triggers."
version: "1.0.0"
tags: ["plugin", "development", "skills", "commands", "mcp", "hooks", "agents", "marketplace", "tools", "claude-code", "sdk"]
allowed-tools: "Read(*), Write(*), Edit(*), Bash(mkdir:*, git:*, npm:*, node:*, python:*, jq:*), Glob(**/*.md, **/*.json, **/*.ts, **/*.py)"
---

# Claude Code Plugin Development Skill

Expert knowledge for building Claude Code plugins with up-to-date 2025 standards.

## When Claude Should Use This Skill

Activate this skill automatically when the user:
- Asks to create/build a Claude Code plugin
- Wants to write slash commands or Agent Skills
- Needs to implement MCP servers or custom tools
- Wants to configure hooks or event handlers
- Asks about plugin architecture or structure
- Needs help with plugin.json manifest
- Wants to publish to a marketplace
- Asks about debugging plugin components
- Mentions keywords: plugin, skill, command, MCP, hook, marketplace, subagent

## Quick Overview

Claude Code plugins consist of **five component types** that extend functionality:

1. **Slash Commands** - User-triggered shortcuts (`/command`)
2. **Agent Skills** - Model-invoked capabilities (auto-activated)
3. **Subagents** - Specialized task handlers
4. **MCP Servers** - External tool/data integrations
5. **Hooks** - Event-driven automations

## Documentation Structure

This skill is organized into focused modules for easy reference:

### Core References

- **[Plugin Structure](reference/plugin-structure.md)** - Architecture, file organization, component types, scope hierarchy
- **[Plugin Manifest](reference/plugin-manifest.md)** - plugin.json schema, validation, configuration
- **[Slash Commands](reference/slash-commands.md)** - Command creation, arguments, tool permissions, namespacing
- **[Agent Skills](reference/agent-skills.md)** - 2025 schema, activation patterns, descriptions that work
- **[MCP Servers](reference/mcp-servers.md)** - Custom tools, TypeScript/Python implementations, tool naming
- **[Hooks](reference/hooks.md)** - Event handlers, available events, matchers, environment variables

### Practical Guides

- **[Development Workflow](guides/development-workflow.md)** - Local testing, debugging, validation checklist
- **[Publishing & Distribution](guides/publishing.md)** - GitHub setup, versioning, marketplace creation
- **[Best Practices](guides/best-practices.md)** - Security, performance, maintainability, design principles

### Examples & Troubleshooting

- **[Complete Plugin Examples](examples/complete-plugins.md)** - Full working examples for common use cases
- **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions

## Getting Started

### For First-Time Plugin Creators

1. Read **[Plugin Structure](reference/plugin-structure.md)** to understand architecture
2. Create **[Plugin Manifest](reference/plugin-manifest.md)** (required `.claude-plugin/plugin.json`)
3. Choose component type(s) to implement:
   - Commands? → See **[Slash Commands](reference/slash-commands.md)**
   - Skills? → See **[Agent Skills](reference/agent-skills.md)**
   - Tools? → See **[MCP Servers](reference/mcp-servers.md)**
   - Automation? → See **[Hooks](reference/hooks.md)**
4. Follow **[Development Workflow](guides/development-workflow.md)** for local testing
5. Use **[Publishing Guide](guides/publishing.md)** to distribute

### For Specific Tasks

**"I want to create a slash command"**
→ See [Slash Commands](reference/slash-commands.md)

**"How do I make a skill that auto-activates?"**
→ See [Agent Skills](reference/agent-skills.md) - especially the "Activation Patterns" section

**"I need to build custom tools/MCP server"**
→ See [MCP Servers](reference/mcp-servers.md)

**"How do I auto-format code after edits?"**
→ See [Hooks](reference/hooks.md) - PostToolUse event

**"My skill isn't activating"**
→ See [Troubleshooting Guide](troubleshooting.md) - "Skills Not Activating" section

**"What are the best practices?"**
→ See [Best Practices](guides/best-practices.md)

## Quick Reference

### Minimal Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # REQUIRED
├── commands/                    # Optional
│   └── my-command.md
├── skills/                      # Optional
│   └── my-skill/
│       └── SKILL.md
├── mcp/                         # Optional
│   └── server.ts
└── README.md
```

### Essential Commands

```bash
# Local testing
/plugin marketplace add ~/.claude/marketplaces/local
/plugin install my-plugin

# Management
/plugin list
/plugin update my-plugin
/help | grep my-command

# Validation
jq . .claude-plugin/plugin.json
```

### Key 2025 Updates

- ✅ `allowed-tools` field for tool permissions in skills
- ✅ Version tracking required
- ✅ Enhanced activation triggers with specific keywords
- ✅ 240+ community plugins available

## When to Reference Each Module

| User Question | Read This |
|--------------|-----------|
| "How do I structure a plugin?" | [Plugin Structure](reference/plugin-structure.md) |
| "What goes in plugin.json?" | [Plugin Manifest](reference/plugin-manifest.md) |
| "Create a command that..." | [Slash Commands](reference/slash-commands.md) |
| "Build a skill that activates when..." | [Agent Skills](reference/agent-skills.md) |
| "Implement custom tools/API integration" | [MCP Servers](reference/mcp-servers.md) |
| "Auto-run something after tool use" | [Hooks](reference/hooks.md) |
| "How do I test locally?" | [Development Workflow](guides/development-workflow.md) |
| "How do I publish my plugin?" | [Publishing](guides/publishing.md) |
| "My plugin component isn't working" | [Troubleshooting](troubleshooting.md) |
| "Show me a complete example" | [Examples](examples/complete-plugins.md) |

## Important Notes

- **2025 Schema**: All documentation follows the latest 2025 plugin schema
- **Activation Keywords**: Skill descriptions must be specific with file types, actions, and tools
- **Tool Permissions**: Use `allowed-tools` to restrict access appropriately
- **Testing First**: Always test locally before publishing
- **No Secrets**: Never commit API keys or credentials

## Additional Resources

- Official docs: https://code.claude.com/docs/en/plugins
- Community marketplace: https://claudecodemarketplace.com
- 240+ plugins: https://github.com/jeremylongshore/claude-code-plugins-plus

---

**Next Steps**: Based on what the user is trying to build, direct them to the appropriate reference guide above. For comprehensive understanding, recommend reading in this order: Plugin Structure → Plugin Manifest → specific component type → Development Workflow → Publishing.
