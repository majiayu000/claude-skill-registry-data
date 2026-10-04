---
name: switcher
description: "Quickly navigate to any note by name"
source: switcher
---

# Quick Switcher

## Plugin metadata

- **id:** `switcher`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `switcher:open` -- Open quick switcher

Plugin "Quick Switcher" opens a fuzzy-search dialog to jump to any note.

Available commands:
- switcher:open -- Open the quick switcher dialog

Use this skill when the user wants to navigate to a specific note by name. For programmatic navigation, prefer the open_note tool.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/switcher.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/switcher.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/switcher.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/switcher.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
