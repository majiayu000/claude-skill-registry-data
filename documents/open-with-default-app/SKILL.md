---
name: open-with-default-app
description: "Open files in the system default app or file manager"
source: open-with-default-app
---

# Open with Default App

## Plugin metadata

- **id:** `open-with-default-app`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `open-with-default-app:open` -- Open in default app
- `open-with-default-app:show` -- Show in system explorer

Plugin "Open with Default App" opens files outside Obsidian.

Available commands:
- open-with-default-app:open -- Open the active file with the system's default app (e.g., Preview for PDF, browser for HTML)
- open-with-default-app:show -- Reveal the active file in Finder/Explorer

Use this when the user wants to view a file in an external application or locate it in the file system.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/open-with-default-app.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/open-with-default-app.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/open-with-default-app.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/open-with-default-app.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
