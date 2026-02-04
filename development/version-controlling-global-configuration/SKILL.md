---
name: Version Controlling Global Configuration
description: Use when user asks about version controlling ~/.claude directory or syncing Claude Code settings across machines. Provides git setup instructions and .gitignore patterns to track only portable settings while excluding logs, session data, and machine-specific plugin metadata. Invoke before initializing git in ~/.claude to prevent committing non-portable data.
---

# Version Controlling Claude Code Global Configuration

Use this skill when users want to version control their `~/.claude` directory to sync settings across machines.

## Critical Understanding

The `~/.claude` directory contains both portable settings and machine-specific data. **Not everything should be version controlled.**

### Safe to Version Control

- `CLAUDE.md` - Global instructions
- `settings.json` - User preferences (only contains enabled plugin names)
- Documentation files you create (README, PLUGINS.md)

### NEVER Version Control

- `plugins/installed_plugins.json` - Contains absolute paths and timestamps
- `plugins/known_marketplaces.json` - Contains absolute paths and timestamps
- `plugins/config.json` - Machine-specific configuration
- `plugins/marketplaces/` and `plugins/repos/` - Downloaded plugin data
- `debug/`, `file-history/`, `history.jsonl` - Logs and session data (may contain sensitive info)
- `projects/`, `session-env/`, `shell-snapshots/`, `todos/` - Session-specific cache
- `statsig/` - Analytics cache

## Why Plugin Metadata Shouldn't Be Versioned

The plugin metadata files contain:
1. **Absolute paths** specific to each machine (e.g., `/Users/username/...`)
2. **Timestamps** that cause unnecessary merge conflicts
3. **Git commit SHAs** from local repositories

These files are **automatically regenerated** by Claude Code when plugins are installed. You don't need to preserve them.

## Standard .gitignore Template

```gitignore
# Session data and logs
debug/
file-history/
history.jsonl
session-env/
shell-snapshots/
todos/

# Project-specific cache
projects/

# Analytics and telemetry
statsig/

# Plugin metadata (machine-specific paths and timestamps)
plugins/installed_plugins.json
plugins/known_marketplaces.json
plugins/config.json
plugins/marketplaces/
plugins/repos/

# Any log files
*.log

# Temporary files
*.tmp
*.swp
*~

# OS-specific files
.DS_Store
Thumbs.db
```

## Recommended Workflow

### Initial Setup

1. Examine the `~/.claude` directory to understand what's there
2. Create `.gitignore` with the template above
3. Create `PLUGINS.md` to document which plugins to install:

```markdown
# Installed Plugins

## Marketplaces
- **marketplace-name**: `https://github.com/user/repo`

## Plugins
From `marketplace-name`:
- `plugin-name` - Brief description

## Installation on New Machine
1. Clone/install marketplaces listed above
2. Use Claude Code to install plugins
3. Copy `settings.json` and `CLAUDE.md` from this repo
```

4. Create `README.md` explaining what the repo contains and setup process
5. Initialize git: `git init`
6. Verify with `git status` - should only show safe files
7. Commit the initial setup

### Cross-Machine Sync

On a new machine:
1. Clone the config repo to `~/.claude`
2. Manually install marketplaces and plugins per `PLUGINS.md`
3. Claude Code will regenerate all machine-specific metadata automatically

## Validation Steps

After creating `.gitignore`:
1. Run `git status` to see what will be tracked
2. Verify NO plugin metadata files appear
3. Verify NO log or session files appear
4. Should only see: `.gitignore`, `CLAUDE.md`, `settings.json`, and any docs you created

If plugin metadata appears in `git status`, the `.gitignore` is incorrect.

## Common Mistakes to Avoid

- **Don't** version control the entire `plugins/` directory
- **Don't** try to preserve absolute paths across machines
- **Don't** commit `history.jsonl` (contains conversation history, potentially sensitive)
- **Don't** assume plugin metadata needs to be preserved

## When to Use This Skill

Trigger this skill when users:
- Ask about version controlling `~/.claude`
- Want to sync Claude settings across machines
- Ask what's safe to commit from their Claude directory
- Question whether plugin files should be in git
