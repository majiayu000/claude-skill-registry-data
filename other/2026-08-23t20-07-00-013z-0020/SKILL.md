---
name: theme
description: "Switch between light and dark mode or change themes"
source: theme
---

# Theme

## Plugin metadata

- **id:** `theme`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `theme:switch` -- Switch theme
- `theme:use-dark` -- Use dark mode
- `theme:use-light` -- Use light mode

Plugin "Theme" controls the visual appearance.

Available commands:
- theme:switch -- Open the theme picker to change the active theme
- theme:use-dark -- Switch to dark color scheme
- theme:use-light -- Switch to light color scheme

Use this when the user asks to change the theme or switch between dark and light mode.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/theme.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/theme.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/theme.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/theme.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
