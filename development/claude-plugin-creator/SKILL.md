---
name: claude-plugin-creator
description: Claude Code plugin creation guide. Use when creating new plugins, adding commands/skills/hooks/MCP servers to plugins, or setting up marketplace distribution. Triggers on "create plugin", "add command", "add skill", "add hook", "plugin structure".
---

# Claude Code Plugin Creator

Guide for creating Claude Code plugins with correct structure and components.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata
├── commands/                 # Optional: Slash commands
│   └── my-command.md
├── skills/                   # Optional: Agent skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Optional: Event handlers
│   └── hooks.json
└── .mcp.json                # Optional: MCP servers
```

## Quick Start

### 1. Create Plugin Directory

```bash
mkdir -p my-plugin/.claude-plugin
```

### 2. Create plugin.json

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

### 3. Add Components

- **Commands**: See [commands.md](references/commands.md)
- **Skills**: See [skills.md](references/skills.md)
- **Hooks**: See [hooks.md](references/hooks.md)
- **MCP Servers**: See [mcp.md](references/mcp.md)

## Adding to Marketplace

For this repository, add plugin to `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./my-plugin",
      "description": "Plugin description"
    }
  ]
}
```

## Validation

Run validation script before committing:

```bash
./validate-plugin.sh my-plugin
```

## Component Reference

| Component | Location | Format | Trigger |
|-----------|----------|--------|---------|
| Commands | `commands/*.md` | Markdown + frontmatter | User: `/command` |
| Skills | `skills/*/SKILL.md` | Markdown + frontmatter | Auto (context) |
| Hooks | `hooks/hooks.json` | JSON | Events |
| MCP | `.mcp.json` | JSON | Auto |
