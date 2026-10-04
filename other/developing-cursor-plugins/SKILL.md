---
name: developing-cursor-plugins
description: Use when working on Cursor plugins (creating, modifying, testing, releasing, or maintaining) - provides streamlined workflows, patterns, and examples for the complete Cursor plugin lifecycle
metadata:
  last_updated: "2026-06-05"
---

# Developing Cursor Plugins

## Overview

This skill provides efficient workflows for creating Cursor plugins. Use it to make plugin development fast and correct — it synthesizes official docs into actionable steps and covers Cursor-specific patterns like `.mdc` rules, plugin manifests, and MCP integration.

## When to Use

Use this skill when:
- Creating a new Cursor plugin from scratch
- Adding components to an existing plugin (rules, skills, commands, agents, hooks, MCP servers)
- Writing `.cursor/rules/*.mdc` rule files
- Setting up a local development environment for plugin testing
- Troubleshooting plugin structure or loading issues
- Understanding plugin architecture and component choices
- Releasing or distributing a plugin (Cursor Marketplace, cursor.directory, team marketplace)

**For comprehensive official documentation**, use the `working-with-cursor` skill to access full docs.

## Quick Reference

| Need to... | Read This | Official Docs |
|-----------|-----------|---------------|
| Understand directory structure | `references/plugin-structure.md` | `plugins.md` |
| Choose a component pattern | `references/common-patterns.md` | `plugins.md` |
| Write .cursor/rules/*.mdc files | `references/cursor-rules-guide.md` | `context-rules.md` |
| Debug plugin issues | `references/troubleshooting.md` | Various |

## Plugin Development Workflow

### Phase 1: Plan

Before writing anything:

1. **Define your plugin's purpose**
   - What problem does it solve?
   - Who will use it — personal, team, or public?
   - Which components are needed?

2. **Choose your pattern** (read `references/common-patterns.md`)
   - Rules only (lightweight context injection)?
   - Rules + skills (guidance + reusable workflows)?
   - MCP integration (external tool access)?
   - Full-featured platform (all component types)?

3. **Review installed plugins** at `~/.cursor/plugins/` for examples

### Phase 2: Create Structure

1. **Create directories**:
   ```bash
   mkdir -p my-plugin/.cursor-plugin
   mkdir -p my-plugin/rules my-plugin/skills my-plugin/commands
   ```

2. **Create the manifest** `.cursor-plugin/plugin.json`:
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What this plugin does",
     "author": { "name": "Your Name" }
   }
   ```

3. **Add components** (see `references/plugin-structure.md` for full layout)

### Phase 3: Develop

**Rules** (`.cursor/rules/*.mdc`) — unique to Cursor, read `references/cursor-rules-guide.md` first:
```yaml
---
description: When to apply this rule (used by AI for auto-discovery)
globs: ["**/*.ts", "**/*.tsx"]
alwaysApply: false
---
# Rule content here
```

**Skills** (`skills/skill-name/SKILL.md`):
```yaml
---
name: skill-name
description: What this skill does and when to invoke it
---
# Skill content
```

**MCP servers** (`.cursor/mcp.json` at plugin root):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-package"]
    }
  }
}
```

### Phase 4: Test Locally

1. **Link plugin** for live iteration:
   ```bash
   ln -s $(pwd)/my-plugin ~/.cursor/plugins/local/my-plugin
   ```

2. **Reload Cursor** via `Developer: Reload Window` in command palette

3. **Verify loading** — check that rules appear, skills are discoverable, MCP tools connect

4. **Test each component**:
   - Rules: open a file matching the glob, confirm AI applies guidance
   - Skills: invoke via `/skill-name` in agent chat
   - MCP: check tool availability in agent context

### Phase 5: Release

**Distribution options:**
- **Cursor Marketplace** — official, reviewed, open-source: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish)
- **cursor.directory** — community platform for plugins and MCP servers
- **Team Marketplace** — internal GitHub repo, configured in Cursor team settings
- **Direct GitHub** — users install manually via local symlink

**Version bump:** Update `version` in `.cursor-plugin/plugin.json`, tag the release.

## Critical Rules

### `.cursor-plugin/` Contains ONLY the Manifest

❌ WRONG:
```
.cursor-plugin/
├── plugin.json
└── skills/          ← skills here
```

✅ CORRECT:
```
.cursor-plugin/
└── plugin.json      ← manifest only
skills/              ← components at plugin root
```

### Rules Live in `rules/` at Plugin Root

Rules bundled with a plugin go in `rules/*.mdc` at the plugin root. They are installed into `.cursor/rules/` when the plugin is activated — users should NOT hand-edit the installed copies.

### Use `.mdc` Extension for Rules

Rules in `.cursor/rules/` **must** use the `.mdc` extension. Plain `.md` files in that directory are ignored by Cursor.
