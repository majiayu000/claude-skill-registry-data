---
name: cc-plugin-extensions
description: This skill should be used when the user asks to "install a plugin", "extend a plugin", "create a .local.md file", "add project context for a plugin", "customize plugin for this project", or mentions project-specific paths, conventions, or workflows that relate to an installed plugin. Covers the .local.md extension pattern for bridging general plugin skills to specific codebases.
---

# Plugin Extension Pattern

Extend marketplace plugins with project-specific context using `.local.md` files. These files bridge general plugin skills to a specific codebase.

## When to Use This Skill

Apply this skill when:
- Installing a marketplace plugin in a project
- A plugin skill is generic but project-specific guidance is needed
- Documenting project-specific file paths, conventions, or workflows that relate to a plugin
- Setting up a new project that uses existing plugins

### Key Distinction
`.local.md` files are **agent context** (for Claude), not human documentation (like READMEs or guides). Treat them like CLAUDE.md in purpose.

## The Pattern

### File Location and Naming

```
.claude/<plugin-name>.local.md
```

Examples:
- `.claude/cc-governance-skills.local.md`
- `.claude/fvtt-skills.local.md`

### Structure

```markdown
---
plugin: <plugin-name>
project: <project-name>
---

# <Plugin Name> - Project-Specific Context

This file extends the `<plugin-name>` plugin with <project>-specific information.

## <Section relevant to plugin's skills>

<Project-specific details>
```

### YAML Frontmatter

| Field | Purpose |
|-------|---------|
| `plugin` | Name of the marketplace plugin being extended |
| `project` | Name of the current project |

## What Belongs in Extension Files

### DO Include

1. **File paths** - Where plugin patterns are implemented in this project
   ```markdown
   | Skill | Implementation Files |
   |-------|---------------------|
   | `fvtt-performance-safe-updates` | `scripts/lib/update-queue.js`, `scripts/hooks.js` |
   ```

2. **Project conventions** - How general patterns apply here
   ```markdown
   ### Actor Types
   - `character` - Player characters
   - `crew` - Crew sheets
   ```

3. **Workflows** - Project-specific processes
   ```markdown
   ### Git Workflow
   - Feature branches → PR to `upstream/rc-1.1.0`
   - Use `--head ImproperSubset:branch-name` for cross-fork PRs
   ```

4. **Build commands** - Project-specific tooling
   ```markdown
   ## Build Commands
   npm run build:css         # Compile SCSS
   npm run lint:css          # Stylelint
   ```

5. **Reminders** - Project-specific gotchas related to plugin skills
   ```markdown
   ### Multi-Client Development
   Every update handler MUST have:
   1. Ownership guard
   2. No-op check
   3. Batched updates
   ```

### DON'T Include

- Content that should be in the plugin itself (general patterns)
- Personal preferences (those stay gitignored in `settings.local.json`)
- Information unrelated to the plugin's skills

## Version Control

### Check In (Project Context)
Commit extension files containing project-specific context to the repository. This ensures all contributors using the plugins get the enhanced context.

```gitignore
# .gitignore - DON'T ignore project context
# .claude/*.local.md  <-- Remove this line
```

### Gitignore (Personal Preferences)
Gitignore only personal settings:

```gitignore
# .gitignore
.claude/settings.local.json
```

## Example: Complete Extension File

```markdown
---
plugin: fvtt-skills
project: my-foundry-module
---

# FVTT Skills - Project-Specific Context

This file extends the `fvtt-skills` plugin with my-foundry-module-specific information.

## File Paths

| Skill | Implementation Files |
|-------|---------------------|
| `fvtt-performance-safe-updates` | `scripts/lib/update-queue.js` |
| `fvtt-version-compat` | `scripts/compat.js` |

## Project Conventions

### Document Types
- `character` - Player characters
- `npc` - Non-player characters

### Flag Namespace
```javascript
actor.getFlag("my-foundry-module", "flagName")
```

## Build Commands
```bash
npm run build    # Build module
npm run test     # Run tests
```
```

## When NOT to Create Extension Files

- Plugin is used without project-specific customization
- Information belongs in CLAUDE.md (not plugin-specific)
- Content is personal preference (use `settings.local.json`)
