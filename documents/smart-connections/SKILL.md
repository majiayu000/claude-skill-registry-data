---
name: smart-connections
description: "AI link discovery copilot. See related notes as you write. Lookup using semantic (vector) search across your vault. Zero-setup local model for embeddings, no API keys, private."
source: smart-connections
---

# Smart Connections

## Plugin metadata

- **id:** `smart-connections`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `smart-connections:smart-connections-getting-started` -- Smart Connections: Show: Getting started slideshow
- `smart-connections:smart-connections-random` -- Smart Connections: Open: Random note from connections
- `smart-connections:smart-connections-view` -- Smart Connections: Open: Connections view
- `smart-connections:toggle-footer-connections` -- Smart Connections: Toggle: Footer connections
- `smart-connections:insert-connections-codeblock` -- Smart Connections: Insert: Connections codeblock
- `smart-connections:browse-smart-plugins` -- Smart Connections: Browse Smart Plugins
- `smart-connections:env-status-view` -- Smart Connections: Open Environment Status View
- `smart-connections:release-notes` -- Smart Connections: Open: Release Notes

# Smart Connections

**Description:** AI link discovery copilot. See related notes as you write. Lookup using semantic (vector) search across your vault. Zero-setup local model for embeddings, no API keys, private.
**Status:** Enabled
**Plugin ID:** smart-connections

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `smart-connections:smart-connections-getting-started` -- Smart Connections: Show: Getting started slideshow
- `smart-connections:smart-connections-random` -- Smart Connections: Open: Random note from connections
- `smart-connections:smart-connections-view` -- Smart Connections: Open: Connections view
- `smart-connections:toggle-footer-connections` -- Smart Connections: Toggle: Footer connections
- `smart-connections:insert-connections-codeblock` -- Smart Connections: Insert: Connections codeblock
- `smart-connections:browse-smart-plugins` -- Smart Connections: Browse Smart Plugins
- `smart-connections:env-status-view` -- Smart Connections: Open Environment Status View
- `smart-connections:release-notes` -- Smart Connections: Open: Release Notes

## Configuration File

Settings path: `.obsidian/plugins/smart-connections/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/smart-connections/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/smart-connections/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
last_version: 4.7.2
```

For full settings, read: `.obsidian/plugins/smart-connections/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/smart-connections.readme.md")

## Usage

When the user asks for functionality related to Smart Connections:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/smart-connections/data.json). If it does not exist, that is normal -- create it with the required settings
3. Configure the plugin by writing data.json with the values needed for the task
4. Execute the task using the appropriate tool:
   - For Obsidian-native commands (including file export): use execute_command
   - For CLI-based conversion needing Pandoc/LaTeX: use execute_recipe
   - For data queries: use call_plugin_api
5. If a command opens a UI dialog, tell the user what to click.

CRITICAL RULES:
- Prefer native Obsidian commands over external tools when both can accomplish the task.
- NEVER create fake output files. If the user asks for a PDF/DOCX/image export, use execute_recipe -- do NOT write content to a .pdf file yourself.
- If a dependency is missing (e.g. Pandoc), tell the user what to install.
IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
