---
name: managing-plugins
description: Create and maintain Claude Code plugins. Use when editing ANY file in the plugins/ directory (commands, skills, hooks, subagents, or config), bumping plugin versions, registering plugins in marketplace.json, creating or modifying subagents, or asking about plugin structure and best practices.
---

# Managing Plugins

This skill provides guidance for creating and maintaining Claude Code plugins.

**Before creating or modifying plugin components**, use `@agent-claude-code-guide`
to look up best practices and understand your options.

## Plugin Structure

Every plugin lives in `plugins/<plugin-name>/` with this structure:

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json    # Plugin metadata and configuration
├── changelog/         # Plugin changelog (managed by tenzir-changelog)
├── README.md          # User-facing documentation (required)
├── skills/            # See [skills.md](./skills.md)
├── commands/          # See [commands.md](./commands.md)
├── hooks/             # See [hooks.md](./hooks.md)
└── agents/            # See [subagents.md](./subagents.md)
```

## Plugin Metadata

The `plugin.json` file defines the plugin:

```json
{
  "name": "plugin-name",
  "version": "0.0.0",
  "description": "Brief description of what this plugin does",
  "author": {
    "name": "Tenzir",
    "email": "engineering@tenzir.com",
    "url": "https://github.com/tenzir"
  },
  "homepage": "https://github.com/tenzir/claude-plugins",
  "repository": "https://github.com/tenzir/claude-plugins",
  "license": "Apache-2.0"
}
```

For MCP servers, add:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name"]
    }
  }
}
```

## README Template

Every plugin **must** have a `README.md`. See
[readme-template.md](./readme-template.md) for the exact structure.

## Marketplace Registration

After creating a plugin, register it in `.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "description": "What this plugin does",
  "source": "./plugins/plugin-name"
}
```

**Note**: The `description` must be duplicated in both `plugin.json` and
`marketplace.json`. The marketplace does not read descriptions from
`plugin.json`—it needs its own copy for plugin discovery.

Keep plugins sorted alphabetically by name.

## Versioning

Plugins **must start at version `0.0.0`**. This allows the first release to use
standard bump flags (`--patch`, `--minor`, `--major`) to produce typical initial
versions like `0.0.1`, `0.1.0`, or `1.0.0`.

Follow SemVer when updating plugins:

- **Patch** (0.0.0 → 0.0.1): Bug fixes, typo corrections
- **Minor** (0.0.0 → 0.1.0): New features, backward-compatible enhancements
- **Major** (0.0.0 → 1.0.0): Breaking changes, production-ready
