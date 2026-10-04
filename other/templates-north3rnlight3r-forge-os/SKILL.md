---
name: templates
description: "Insert predefined note templates"
source: templates
---

# Templates

## Plugin metadata

- **id:** `templates`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `templates:insert-template` -- Insert template

Plugin "Templates" inserts template content into the current note.

Available commands:
- templates:insert-template -- Opens a picker to insert a template from the configured templates folder

Use this skill when the user asks to apply a template to a note. The template folder is configured in Obsidian settings. Note: If Templater is installed, prefer that for dynamic templates.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/templates.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/templates.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/templates.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/templates.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
