---
name: plugin-manager
description: This skill should be used when the user asks about Claude Code plugins, including listing installed plugins, checking plugin status (enabled/disabled), verifying if a specific plugin exists, or getting plugin information in different formats (table, JSON, list). Use when queries mention "list plugins", "installed plugins", "plugin status", "is plugin X installed", or related plugin management tasks.
---

# Plugin Manager Skill

## Purpose

This skill provides functionality to list, check, and manage Claude Code plugins using the settings.json file. Since the `claude plugin list` command does not exist, this skill uses direct JSON file access with jq or a Python helper script to retrieve plugin information.

## When to Use This Skill

Use this skill when the user requests information about:
- Listing all installed Claude Code plugins
- Checking if a specific plugin is installed
- Viewing plugin status (enabled/disabled)
- Getting plugin information in different formats (table, JSON, simple list)
- Counting total installed plugins

## Platform Detection

**Current Environment:** Windows (MINGW64_NT-10.0-26100)

**For detailed command reference, see:**
- **Windows (Git Bash/MINGW64)**: `docs/windows-guide.md` ← USE THIS
- Unix/Linux/Mac: `docs/unix-guide.md`

## Quick Start (Cross-Platform)

The Python script works on all platforms:

```bash
# List all plugins with status
python scripts/list_plugins.py

# Table format
python scripts/list_plugins.py --format table

# JSON format
python scripts/list_plugins.py --format json

# Check specific plugin
python scripts/list_plugins.py --check "plugin-name@marketplace-name"

# Count plugins
python scripts/list_plugins.py --count
```

## Platform-Specific Commands

For jq commands and advanced usage, **read your platform-specific guide:**

- **Windows users**: See `docs/windows-guide.md` for correct path syntax
- **Unix/Mac users**: See `docs/unix-guide.md` for bash commands

## Key Information

- **No `claude plugin list` command**: This command does not exist in Claude Code CLI
- **Settings location**:
  - Windows: `$USERPROFILE/.claude/settings.json`
  - Unix/Mac: `~/.claude/settings.json`
  - Project-specific: `./.claude/settings.json`
- **Plugin format**: Plugins are named as `plugin-name@marketplace-name`
- **Status values**: `true` (enabled) or `false` (disabled)
- **Alternative discovery**: Use `/plugin` interactive menu to manage plugins

## Important: Path Syntax

**Windows (Git Bash/MINGW64):**
- ✓ Use forward slashes: `scripts/list_plugins.py`
- ✓ Use `$USERPROFILE`: `$USERPROFILE/.claude/settings.json`
- ✗ Never use backslashes: `scripts\list_plugins.py`
- ✗ Never use `~` on Windows: `~/.claude/settings.json`

**Unix/Mac:**
- ✓ Use forward slashes: `scripts/list_plugins.py`
- ✓ Use tilde: `~/.claude/settings.json`

## Error Handling

**Common issues:**
1. Settings file not found → Ensure Claude Code is installed and has run at least once
2. Path errors on Windows → See `docs/windows-guide.md` for correct syntax
3. Empty plugin list → Check that plugins have been installed via `/plugin` menu

## Architecture

```
plugin-manager/
├── SKILL.md              # This file - main entry point
├── docs/
│   ├── windows-guide.md  # Windows-specific commands (Git Bash/MINGW64)
│   └── unix-guide.md     # Unix/Mac-specific commands
└── scripts/
    └── list_plugins.py   # Cross-platform Python script
```

## Notes

- **Recommended approach**: Use the Python script for simplicity and cross-platform compatibility
- **Advanced usage**: Use jq commands from your platform-specific guide
- **All commands are non-interactive**: Suitable for automation and scripting
- **Python script handles paths automatically**: Works on Windows, Unix, Mac, and Linux
