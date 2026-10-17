---
name: plugin-creator
description: This skill should be used when creating, modifying, or managing Claude Code plugins and plugin marketplaces. Trigger when working with plugin manifests (plugin.json, marketplace.json), creating plugin directory structures, adding plugin components (commands, skills, agents, hooks), version bumping, or when discussing plugin development workflows.
disable-model-invocation: true
---

# Plugin Creator

Official docs: <https://code.claude.com/docs/en/plugins.md>, <https://code.claude.com/docs/en/plugins-reference.md>, <https://code.claude.com/docs/en/plugin-marketplaces.md>. Fetch when unsure about manifest schema, distribution, or recent features.

## Overview

Create and manage Claude Code plugins with proper structure, manifests, and marketplace integration. This skill provides workflows, automation scripts, and reference documentation for plugin development.

## Prerequisites

- `python3` for the bundled scripts

## When to Use This Skill

Trigger this skill when:

- Creating new plugins for a marketplace
- Adding or modifying plugin components (commands, skills, agents, hooks)
- Updating plugin versions
- Working with plugin or marketplace manifests
- Setting up local plugin testing
- Publishing plugins to marketplaces

## Quick Start

### Creating a New Plugin

Use the `create_plugin.py` script to generate plugin structure:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/create_plugin.py plugin-name \
  --marketplace-root /path/to/marketplace \
  --author-name "Your Name" \
  --author-email "your.email@example.com" \
  --description "Plugin description" \
  --keywords "keyword1,keyword2" \
  --category "productivity"
```

This automatically:

- Creates plugin directory structure
- Generates `plugin.json` manifest
- Creates README template
- Updates `marketplace.json`

### Bumping Plugin Version

Use `bump_version.py` to update versions in both manifests:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/bump_version.py plugin-name major|minor|patch \
  --marketplace-root /path/to/marketplace
```

Semantic versioning rules:

- **major**: Breaking changes (1.0.0 → 2.0.0)
- **minor**: New features, refactoring (1.0.0 → 1.1.0)
- **patch**: Bug fixes, docs only (1.0.0 → 1.0.1)

## Plugin Development Workflow

### 1. Create Plugin Structure

Manual approach if not using `create_plugin.py`:

```bash
mkdir -p plugins/plugin-name/.claude-plugin
mkdir -p plugins/plugin-name/commands
mkdir -p plugins/plugin-name/skills
```

### 2. Create Plugin Manifest

File: `plugins/plugin-name/.claude-plugin/plugin.json`

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### 3. Register in Marketplace

Update `.claude-plugin/marketplace.json` by adding to `plugins` array:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Plugin description",
  "version": "0.1.0",
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

### 4. Add Plugin Components

Create components in their respective directories:

**Commands:** `commands/` - Markdown files with frontmatter
**Skills:** `skills/` - Subdirectories containing `SKILL.md`
**Agents:** `agents/` - Markdown agent definitions
**Hooks:** `hooks/hooks.json` - Event handler configurations
**MCP Servers:** `.mcp.json` - External tool integrations

### 5. Local Testing

```bash
# Add marketplace
/plugin marketplace add /path/to/marketplace-root

# Install plugin
/plugin install plugin-name@marketplace-name

# After changes: uninstall, reinstall, restart Claude Code
/plugin uninstall plugin-name@marketplace-name
/plugin install plugin-name@marketplace-name
```

## Plugin Structure Patterns

### Framework Plugin

For framework-specific guidance (React, Vue, Nuxt):

```
plugins/framework-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── framework-name/
│       ├── SKILL.md              # Quick reference
│       └── references/           # Library patterns
├── commands/
│   └── prime/
│       ├── components.md
│       └── framework.md
└── README.md
```

### Utility Plugin

For tools and commands:

```
plugins/utility-name/
├── .claude-plugin/plugin.json
├── commands/
│   ├── action1.md
│   └── action2.md
└── README.md
```

### Domain Plugin

For domain-specific knowledge:

```
plugins/domain-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── domain-name/
│       ├── SKILL.md
│       ├── references/
│       │   ├── schema.md
│       │   └── policies.md
│       └── scripts/
│           └── automation.py
└── README.md
```

## Command Naming Convention

Commands use subdirectory-based namespacing with `:` separator:

- File: `commands/namespace/command.md` → `/namespace:command`
- File: `commands/simple.md` → `/simple`

Examples:

- `commands/prime/vue.md` → `/prime:vue`
- `commands/docs/generate.md` → `/docs:generate`

## Version Management

**Critical:** Always update version in BOTH locations:

1. `plugins/<name>/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json` (matching entry)

Use `bump_version.py` to automate this.

## Git Workflow

Use conventional commits:

```bash
git commit -m "feat: add new plugin"
git commit -m "fix: correct plugin manifest"
git commit -m "docs: update plugin README"
git commit -m "feat!: breaking change to plugin API"
```

## Resources

This skill includes detailed reference documentation:

### references/plugin-structure.md

Complete plugin directory structure, manifest schema, component types, and path requirements.

### references/marketplace-schema.md

Marketplace manifest format, plugin entry schema, source specifications, and team distribution setup.

### references/workflows.md

Step-by-step workflows for creating plugins, version bumping, local testing, publishing, and common plugin patterns.

### scripts/create_plugin.py

Automates plugin creation with proper structure and manifest generation.

### scripts/bump_version.py

Updates version in both plugin.json and marketplace.json simultaneously.

## Key References

When Claude needs detailed information about specific aspects:

- **Plugin structure details**: Read `references/plugin-structure.md`
- **Marketplace schema**: Read `references/marketplace-schema.md`
- **Development workflows**: Read `references/workflows.md`

These references provide comprehensive information without cluttering the main skill context.
