---
name: daily-notes
description: "Create and navigate daily journal notes"
source: daily-notes
---

# Daily Notes

## Plugin metadata

- **id:** `daily-notes`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `daily-notes:open` -- Open today's daily note
- `daily-notes:goto-next` -- Open next daily note
- `daily-notes:goto-prev` -- Open previous daily note

Plugin "Daily Notes" provides date-based note creation and navigation.

Available commands:
- daily-notes:open -- Open or create today's daily note
- daily-notes:goto-next -- Navigate to the next daily note
- daily-notes:goto-prev -- Navigate to the previous daily note

Use this skill when the user asks about daily notes, journals, today's note, or date-based note navigation. The daily note format and folder are configured in Obsidian settings.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/daily-notes.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/daily-notes.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/daily-notes.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/daily-notes.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
