---
name: plugins
description: How to create, install, and manage Claude Code plugins and plugin marketplaces. Use when user asks about plugins, plugin creation, plugin distribution, or plugin marketplaces.
---

# Claude Code Plugins

## Overview

Plugins extend Claude Code with custom functionality including commands, agents, hooks, Skills, and MCP servers. They can be shared across projects and teams through marketplaces.

## Quick Start

### Basic Structure
A plugin requires:
- **Plugin manifest** (`.claude-plugin/plugin.json`) - metadata
- **Commands directory** (`commands/`) - custom slash commands
- **Optional components** - agents, skills, hooks, MCP servers

### Creating Your First Plugin

1. **Setup directories**
```bash
mkdir test-marketplace/my-first-plugin
cd my-first-plugin
mkdir .claude-plugin commands
```

2. **Create plugin manifest** (`.claude-plugin/plugin.json`)
```json
{
  "name": "my-first-plugin",
  "description": "A simple greeting plugin",
  "version": "1.0.0",
  "author": {"name": "Your Name"}
}
```

3. **Add command** (`commands/hello.md`)
Contains: "Greet the user warmly and ask how you can help them today."

4. **Create marketplace manifest** (`.claude-plugin/marketplace.json`)
Lists your plugins with their source paths and descriptions.

5. **Install locally**
```
/plugin marketplace add ./test-marketplace
/plugin install my-first-plugin@test-marketplace
```

## Plugin Components

### Commands
Markdown files in `commands/` directory defining custom slash commands that Claude can invoke.

### Agents
Agent definitions in `agents/` directory for specialized task automation.

### Skills
`SKILL.md` files in `skills/` directory that extend Claude's autonomous capabilities. Model-invoked based on task context.

### Hooks
`hooks.json` for event handling and workflow automation.

### MCP Servers
`.mcp.json` configuration for external tool integration.

## Managing Plugins

**Add marketplace**: `/plugin marketplace add your-org/claude-plugins`

**Browse/install**: `/plugin` opens interactive menu

**Direct install**: `/plugin install formatter@org-name`

**Control**: Enable, disable, or uninstall plugins as needed

**Verify**: Run `/help` to see newly available commands

## Team Setup

Configure plugins at repository level via `.claude/settings.json`. When team members trust the folder, marketplaces and plugins install automatically.

## Development Workflow

1. Create local development marketplace
2. Organize plugins in subdirectories
3. Test changes iteratively
4. Uninstall and reinstall to verify updates
5. Document with README and semantic versioning

## Distribution

- Add comprehensive documentation
- Use semantic versioning in `plugin.json`
- Create or use existing marketplaces
- Test with team members before wider release

## Plugin Marketplaces

Plugin marketplaces are JSON-based catalogs that distribute Claude Code extensions. They enable centralized discovery, version management, and team distribution of plugins across multiple sources.

### Key Features

- **Centralized discovery**: Browse plugins from multiple sources in one location
- **Version management**: Track and automatically update plugin versions
- **Team distribution**: Share required plugins across organizations
- **Flexible sources**: Support git repositories, GitHub repos, local paths, and package managers

### Adding Marketplaces

**GitHub Repositories:**
```
/plugin marketplace add owner/repo
```

**Git Repositories:**
```
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**Local Development:**
```
/plugin marketplace add ./my-marketplace
/plugin marketplace add ./path/to/marketplace.json
/plugin marketplace add https://url.of/marketplace.json
```

### Creating a Marketplace

Create `.claude-plugin/marketplace.json` in your repository:

```json
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "[email protected]"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0"
    }
  ]
}
```

### Plugin Sources

**Relative Paths:**
```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

**GitHub:**
```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

**Git Services:**
```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

## Team Configuration

Specify marketplaces in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

## Management Commands

```
/plugin marketplace list          # Show all marketplaces
/plugin marketplace update name   # Refresh metadata
/plugin marketplace remove name   # Remove marketplace
```

## Best Practices

- Establish clear versioning policies
- Provide comprehensive README documentation
- Maintain active community engagement
- Review plugins for security before distribution
- Document all marketplace contents
