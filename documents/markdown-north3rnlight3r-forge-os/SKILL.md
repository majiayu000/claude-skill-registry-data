---
name: markdown
description: "Toggle between editing and reading view"
source: markdown
---

# Markdown

## Plugin metadata

- **id:** `markdown`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `markdown:toggle-preview` -- Toggle reading view

Plugin "Markdown" controls the note view mode.

Available commands:
- markdown:toggle-preview -- Toggle between editing mode and reading (preview) mode

Use this when the user wants to switch view modes. Also available as editor:toggle-source.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/markdown.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/markdown.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/markdown.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/markdown.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
