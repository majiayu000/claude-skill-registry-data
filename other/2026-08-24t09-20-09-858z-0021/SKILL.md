---
name: window
description: "Window controls: zoom and always-on-top"
source: window
---

# Window

## Plugin metadata

- **id:** `window`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `window:zoom-in` -- Zoom in
- `window:zoom-out` -- Zoom out
- `window:reset-zoom` -- Reset zoom
- `window:toggle-always-on-top` -- Toggle always on top

Plugin "Window" controls the Obsidian window.

Available commands:
- window:zoom-in -- Increase the UI zoom level
- window:zoom-out -- Decrease the UI zoom level
- window:reset-zoom -- Reset zoom to default (100%)
- window:toggle-always-on-top -- Keep the Obsidian window above all other windows

Use this when the user asks to change zoom level or keep the window on top.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/window.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/window.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/window.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/window.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
