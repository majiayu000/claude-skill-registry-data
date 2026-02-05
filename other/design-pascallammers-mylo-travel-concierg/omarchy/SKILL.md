---
name: omarchy
description: Expert guide for Omarchy Linux system management. Use when user asks about Omarchy commands, updates, migrations, configuration, or how Omarchy works. Inspects the local Omarchy installation at ~/.local/share/omarchy to provide accurate answers.
---

# Omarchy Expert Guide

## Purpose
This skill helps users understand and work with their Omarchy Linux installation by inspecting the actual Omarchy codebase installed at `~/.local/share/omarchy`.

## Instructions

When a user asks about Omarchy:

1. **Locate the Installation**
   - Main installation: `~/.local/share/omarchy/`
   - Configuration: `~/.config/omarchy/`
   - State files: `~/.local/state/omarchy/`

2. **Understand Their Question**
   - Identify if they're asking about:
     - Commands/scripts (check `~/.local/share/omarchy/bin/`)
     - Migrations (check `~/.local/share/omarchy/migrations/`)
     - Configuration (check `~/.config/omarchy/`)
     - Updates and system management
     - Themes, hooks, or customization

3. **Inspect the Source**
   - Read relevant scripts in `~/.local/share/omarchy/bin/` to understand functionality
   - Check migration files to understand installation history
   - Look at configuration files to understand current setup
   - Examine the actual code to provide accurate, specific answers
   - Check the official Omarchy documentation:
     - Official site: https://omarchy.org
     - Manual: https://learn.omacom.io/2/the-omarchy-manual

4. **Provide Specific Guidance**
   - Show actual commands from the Omarchy installation
   - Explain what the scripts do by reading their source
   - Reference specific file paths: `~/.local/share/omarchy/bin/command-name`
   - Provide examples based on the user's actual setup

5. **Common Tasks to Help With**
   - **Updates**: Explain `omarchy-update` and what it does
   - **Migrations**: Show how to create and run migrations
   - **Commands**: List and explain available `omarchy-*` commands
   - **Package management**: How Omarchy handles system packages
   - **Customization**: Themes, hooks, and configuration

## Available Tools
Use these tools to inspect the Omarchy installation:
- `Read` - Read Omarchy scripts and configuration files
- `Grep` - Search for patterns in Omarchy code
- `Glob` - Find Omarchy files matching patterns
- `Bash` - List directories, check commands
- `WebFetch` - Fetch official documentation from omarchy.org when needed

## Examples

### Example 1: User asks "How do I update with Omarchy?"
1. Read `~/.local/share/omarchy/bin/omarchy-update`
2. Read `~/.local/share/omarchy/bin/omarchy-update-system-pkgs`
3. Explain the update process step-by-step
4. Show the command: `omarchy-update`

### Example 2: User asks "What Omarchy commands are available?"
1. List files in `~/.local/share/omarchy/bin/`
2. Identify `omarchy-*` commands
3. Group by category (update, install, theme, etc.)
4. Offer to explain specific commands

### Example 3: User asks "How do migrations work in Omarchy?"
1. Check `~/.local/share/omarchy/migrations/` for migration files
2. Read the migration runner script
3. Explain the timestamp-based system
4. Show user's existing migrations

## Important Notes
- Always inspect the actual installation - don't assume how Omarchy works
- Omarchy is installed system-wide at `~/.local/share/omarchy/`
- Commands are in `bin/`, migrations are timestamped shell scripts
- The system uses pacman/yay for package management
- Read the source code to give accurate answers
