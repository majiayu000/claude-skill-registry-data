---
name: slides
description: "Present notes as slideshows using --- separators"
source: slides
---

# Slides

## Plugin metadata

- **id:** `slides`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `slides:start` -- Start presentation

Plugin "Slides" turns notes into presentations.

Available commands:
- slides:start -- Start a slideshow presentation of the current note

Notes are split into slides by horizontal rules (---). Use this when the user wants to present a note as a slideshow.

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.

## Configuration File

Settings path: `.obsidian/slides.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/slides.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/slides.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/slides.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
