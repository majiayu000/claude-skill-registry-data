---
name: developing-codex-plugins
description: Use when working on Codex plugins (creating, modifying, testing, releasing, or maintaining) - provides streamlined workflows, patterns, and reference for the complete Codex plugin lifecycle
metadata:
  last_updated: "2026-06-04"
---

# Developing Codex Plugins

## Overview

This skill provides efficient workflows for creating Codex CLI plugins. Use it to make plugin development fast and correct — it synthesizes patterns and structure into actionable steps with working examples.

## When to Use

Use this skill when:
- Creating a new Codex plugin from scratch
- Adding components to an existing plugin (skills, hooks, commands)
- Troubleshooting plugin structure issues
- Understanding Codex plugin architecture and patterns
- Releasing a plugin (versioning, tagging, distribution)
- Publishing updates or maintaining existing plugins

**For comprehensive official documentation**, use the `working-with-codex` skill to access full docs.

## Quick Reference

| Need to... | Read This |
|-----------|-----------|
| Understand directory structure | `references/plugin-structure.md` |
| Choose a plugin pattern | `references/common-patterns.md` |
| Write skills that trigger reliably | `references/skills-for-codex.md` |
| Debug plugin issues | `references/troubleshooting.md` |

## Plugin Development Workflow

### Phase 1: Plan

Before writing any files:

1. **Define your plugin's purpose**
   - What problem does it solve?
   - Who will use it?
   - What components will it need?

2. **Choose your pattern** (read `references/common-patterns.md`)
   - Single skill plugin?
   - Skill collection?
   - Hook-enhanced workflow?
   - Full-featured platform?

3. **Review existing plugins**
   - Installed plugins in `~/.codex/plugins/`
   - Agent skills repo: `skills/` directory

### Phase 2: Create Structure

1. **Create directories** (see `references/plugin-structure.md` for details):
   ```bash
   mkdir -p my-plugin/.codex-plugin
   mkdir -p my-plugin/skills
   # Add other component directories as needed
   ```

2. **Write `.codex-plugin/plugin.json`** (required):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What your plugin does",
     "author": {"name": "Your Name"},
     "skills": "./skills/"
   }
   ```
   See `references/plugin-structure.md` for complete format.

3. **Write `AGENTS.md`** at the plugin root (Codex session bootstrap):
   ```markdown
   # Plugin Name

   This session has access to the following skills:

   - `skill("my-skill")` — Brief description of when to use it
   ```

### Phase 3: Add Components

Use TodoWrite to track component creation:

**Example:**
```
- Create skill: main-workflow
- Configure hooks
- Write AGENTS.md bootstrap
- Write README
- Test locally
```

For each component type, see `references/plugin-structure.md` for format and syntax.

### Phase 4: Test Locally

1. **Load for testing**:
   ```bash
   codex --plugin-dir ./my-plugin
   # or in an existing session:
   # add the plugin directory to config
   ```

2. **Test each component**:
   - Skills: Ask for tasks matching skill descriptions, or invoke directly with `skill("name")`
   - Hooks: Trigger relevant events (file write, session start, etc.)
   - AGENTS.md: Check that context loads at session start

3. **Iterate** — update files and reload to pick up changes.

### Phase 5: Debug and Refine

Start with `references/troubleshooting.md` if something doesn't work. Common issues:

- Wrong directory structure (see `references/plugin-structure.md`)
- `plugin.json` paths not matching actual file locations
- Skill descriptions not triggering reliably (see `references/skills-for-codex.md`)
- `AGENTS.md` not loading (check file location and format)
- Missing executable permissions on hook scripts

### Phase 6: Release and Distribute

1. **Write README** with:
   - What the plugin does
   - Installation instructions
   - Usage examples
   - Component descriptions

2. **Version your release** using semantic versioning:
   - Update `version` in `.codex-plugin/plugin.json`
   - Example: `"version": "1.2.1"` (major.minor.patch)

3. **Commit and tag**:
   ```bash
   git add .
   git commit -m "Release v1.2.1: [brief description]"
   git tag v1.2.1
   git push origin main --tags
   ```

4. **Choose distribution method**:

   **Option A: Direct GitHub distribution**
   - Users install via: `codex plugin install github:your-org/your-plugin-repo`
   - Your `.codex-plugin/plugin.json` serves as the manifest

   **Option B: Marketplace distribution** (see `references/plugin-structure.md`)
   - Register in a marketplace repository

## Critical Rules

**Always follow these** (from `references/plugin-structure.md`):

1. **`.codex-plugin/` contains ONLY manifests** (`plugin.json`)
   - ❌ Don't put skills, hooks, or other components inside it
   - ✅ Put them at plugin root

2. **Use the `skills` field in `plugin.json`** to point to the skills directory
   - Example: `"skills": "./skills/"`

3. **AGENTS.md belongs at the plugin root**, not inside `.codex-plugin/`
   - This is the session bootstrap Codex reads at start

4. **Make hook scripts executable**
   - `chmod +x hooks/my-hook.sh`

## Resources in This Skill

- **`references/plugin-structure.md`** — Directory layout, plugin.json schema, component formats
- **`references/common-patterns.md`** — When to use each plugin pattern, decision matrix
- **`references/skills-for-codex.md`** — Skill authoring, trigger reliability, AGENTS.md patterns
- **`references/troubleshooting.md`** — Debug guide for common plugin issues

## Cross-References

For deep dives into official documentation, use the `working-with-codex` skill to access:
- `plugins.md` — Plugin development overview
- `skills.md` — Complete skill authoring guide
- `hooks.md` — Hook system reference
- `configuration.md` — AGENTS.md and session configuration
- `README.md` — Getting started and CLI reference

## Best Practices

1. **Start simple** — Begin with one skill, add complexity when needed
2. **Test frequently** — Add → test → modify → repeat
3. **Write a good AGENTS.md** — This is how users discover your skills in a session
4. **Document skill triggers** — Clear descriptions are how Codex finds your skills
5. **Version properly** — Use semantic versioning (major.minor.patch)

## Workflow Summary

```
Plan → Choose pattern, define purpose
Create → Make structure, write manifests + AGENTS.md
Add → Build components (skills, hooks, etc.)
Test → Load via --plugin-dir, invoke skills
Debug → Use troubleshooting guide
Release → Version, tag, distribute
```

**The correct path is the fast path.** Use references, follow patterns, test frequently.
