---
name: developing-gemini-plugins
description: Use when creating, modifying, testing, or releasing Gemini CLI extensions or Antigravity CLI plugins — provides workflows, patterns, and reference for the complete plugin lifecycle on both platforms
metadata:
  last_updated: "2026-06-04"
---

# Developing Gemini CLI Extensions & Antigravity Plugins

## Overview

This skill provides efficient workflows for creating extensions for Gemini CLI and plugins for Antigravity CLI (Google's official next-generation replacement for Gemini CLI). The two formats are closely related — a Gemini CLI extension can be imported into Antigravity automatically via `agy plugin import gemini`.

**Key distinction:** Gemini CLI uses `gemini-extension.json` as the manifest filename. Antigravity CLI uses `plugin.json`. Both support the same SKILL.md skill format and `GEMINI.md`/`AGENTS.md` session context files.

## When to Use

Use this skill when:
- Creating a new Gemini CLI extension or Antigravity plugin from scratch
- Adding components (skills, hooks, MCP servers, slash commands)
- Writing `GEMINI.md` session context files
- Troubleshooting extension or plugin structure issues
- Migrating a Gemini CLI extension to Antigravity CLI
- Understanding patterns and architecture decisions
- Releasing and distributing plugins
- Writing skills that work cross-platform (Claude Code + Codex + Gemini + Antigravity)

**For official docs**, use the `working-with-gemini` skill.

## Quick Reference

| Need to... | Read This |
| --- | --- |
| Understand directory structure | `references/extension-structure.md` |
| Choose a plugin pattern | `references/common-patterns.md` |
| Write skills that trigger reliably | `references/skills-for-gemini.md` |
| Debug plugin/extension issues | `references/troubleshooting.md` |

## Platform Comparison

| Aspect | Gemini CLI | Antigravity CLI |
| --- | --- | --- |
| Manifest file | `gemini-extension.json` | `plugin.json` |
| Workspace skills path | `.gemini/skills/` | `.agents/skills/` |
| Global skills | `~/.gemini/skills/` | `~/.gemini/antigravity-cli/skills/` |
| Session context file | `GEMINI.md` or `AGENTS.md` | `GEMINI.md` or `AGENTS.md` |
| Skill invocation | `activate_skill("name")` | `activate_skill("name")` |
| SKILL.md format | Identical to Claude Code | Identical to Claude Code |
| Extensions dir | `~/.gemini/extensions/<name>/` | `~/.gemini/antigravity-cli/plugins/<name>/` |
| Import from Gemini CLI | — | `agy plugin import gemini` |
| Install from git | `gemini extensions install <url>` | `agy plugin install <url>` |

## Plugin Development Workflow

### Phase 1: Plan

Before writing any files:

1. **Define your plugin's purpose**
   - What problem does it solve?
   - Target platform: Gemini CLI only, Antigravity only, or both?
   - What components will it need? (skills, hooks, MCP servers, slash commands)

2. **Choose your pattern** (read `references/common-patterns.md`)
   - Single skill?
   - Skill collection with GEMINI.md bootstrap?
   - Hook-enhanced workflow?
   - MCP-integrated full plugin?

3. **Decide on cross-platform scope**
   - Skills are portable as-is
   - Provide both `gemini-extension.json` AND `plugin.json` for dual-platform support
   - `GEMINI.md` and `AGENTS.md` both work in both tools

### Phase 2: Create Structure

1. **Create directories** (see `references/extension-structure.md`):
   ```bash
   mkdir -p my-plugin/skills/skill-name
   # For Gemini CLI:
   # gemini-extension.json lives at plugin root
   # For Antigravity CLI:
   # plugin.json lives at plugin root
   ```

2. **Write the manifest** — provide BOTH for dual support:

   **`gemini-extension.json`** (Gemini CLI):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What your plugin does",
     "contextFileName": "GEMINI.md"
   }
   ```

   **`plugin.json`** (Antigravity CLI):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What your plugin does"
   }
   ```

3. **Write `GEMINI.md`** at the plugin root (works in both tools):
   ```markdown
   # Plugin Name

   This session includes skills from `my-plugin`. Invoke them with `activate_skill("name")`:

   - `activate_skill("skill-name")` — When to use this skill
   ```

### Phase 3: Add Components

Use TodoWrite to track component creation. For each component:

- **Skills**: create `skills/skill-name/SKILL.md` (see `references/skills-for-gemini.md`)
- **Hooks**: create `hooks/hooks.json` + scripts (see `references/extension-structure.md`)
- **MCP servers**: add `mcpServers` to `gemini-extension.json` (see official `docs-mcp-server.md`)
- **Slash commands**: create `.toml` files in `commands/` directory

### Phase 4: Test Locally

**Gemini CLI:**
```bash
gemini extensions install --path=./my-plugin
gemini                         # start session, test activate_skill("name")
gemini extensions uninstall my-plugin   # clean up
```

**Antigravity CLI:**
```bash
agy plugin install --path=./my-plugin
agy                            # start session, test activate_skill("name")
agy plugin uninstall my-plugin
```

Test checklist:
- Skills: invoke explicitly with `activate_skill("skill-name")`
- Hooks: trigger the relevant events and check output
- GEMINI.md: verify it loads at session start
- Slash commands: run `/your-command`
- MCP servers: verify tools appear in session

### Phase 5: Debug and Refine

Start with `references/troubleshooting.md`. Use `gemini doctor` (or `agy doctor`) to validate the installation first.

Common issues:
- Manifest name doesn't match install directory name
- `contextFileName` in manifest doesn't match actual file
- Hook script not executable (`chmod +x`)
- Skill not auto-triggering — see `references/skills-for-gemini.md` for description writing
- GEMINI.md path wrong — must be at plugin root, not in a subdirectory

### Phase 6: Release and Distribute

1. **Bump version** in both `gemini-extension.json` and `plugin.json`

2. **Commit and tag**:
   ```bash
   git commit -m "Release v1.2.0: [description]"
   git tag v1.2.0
   git push origin main --tags
   ```

3. **Distribution**:

   **Gemini CLI:**
   ```bash
   gemini extensions install https://github.com/your-org/your-plugin
   ```

   **Antigravity CLI:**
   ```bash
   agy plugin install https://github.com/your-org/your-plugin
   ```

   **Import Gemini CLI extension into Antigravity:**
   ```bash
   agy plugin import gemini    # imports all installed Gemini extensions
   ```

## Critical Rules

1. **Manifest name must match the install directory name** — `"name": "my-plugin"` installs to `~/.gemini/extensions/my-plugin/`. Mismatch causes silent failures.

2. **Provide both `gemini-extension.json` and `plugin.json`** for dual-platform support — they can have identical content for basic plugins.

3. **`GEMINI.md` goes at the plugin root** — the `contextFileName` field in `gemini-extension.json` tells Gemini CLI which file to load; default is `GEMINI.md`.

4. **Use `activate_skill()` in GEMINI.md, not `skill()`** — Codex uses `skill()`, Gemini/Antigravity uses `activate_skill()`. Write platform-specific invocation syntax in each bootstrap file.

5. **Workspace skills live in `.agents/skills/`** for Antigravity (`.gemini/skills/` for Gemini CLI). Use `.agents/skills/` if you want one path that works in both after migration.

6. **Hook scripts must be executable** — `chmod +x hooks/*.sh`; commit with `git update-index --chmod=+x`.

## Resources in This Skill

- **`references/extension-structure.md`** — Directory layout, manifest schemas, component formats for both platforms
- **`references/common-patterns.md`** — Pattern decision matrix with examples
- **`references/skills-for-gemini.md`** — `activate_skill()`, SKILL.md authoring, GEMINI.md bootstrap patterns, Antigravity caveats
- **`references/troubleshooting.md`** — Debug guide for Gemini CLI and Antigravity, migration footguns

## Cross-References

For official documentation, use the `working-with-gemini` skill:
- `docs-creating-skills.md` — Official skill authoring guide
- `docs-skills-best-practices.md` — Trigger reliability, description quality
- `docs-writing-extensions.md` — Extension development guide
- `docs-writing-hooks.md` — Hook authoring
- `docs-gemini-md.md` — GEMINI.md format
- `docs-troubleshooting.md` — Official troubleshooting
