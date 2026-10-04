---
name: tag-pane
description: "Browse all tags used in the vault"
source: tag-pane
---

# Tags

## Plugin metadata

- **id:** `tag-pane`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `tag-pane:open` -- Open tags pane

Plugin "Tags" shows a browsable list of all tags used across vault notes.

Available commands:
- tag-pane:open -- Open the tags pane in the sidebar

Use this skill when the user wants to browse or explore tags. For programmatic tag searching, prefer the search_by_tag tool.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/tag-pane.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/tag-pane.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/tag-pane.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/tag-pane.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
