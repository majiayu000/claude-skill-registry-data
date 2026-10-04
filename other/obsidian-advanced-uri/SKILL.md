---
name: obsidian-advanced-uri
description: "Control various aspects through URIs, including opening files, creating new files, and executing commands."
source: obsidian-advanced-uri
---

# Advanced URI

## Plugin metadata

- **id:** `obsidian-advanced-uri`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** false
- **needs-setup:** true

### Commands

- `obsidian-advanced-uri:copy-uri-current-file` -- Advanced URI: Copy URI for file with options
- `obsidian-advanced-uri:copy-uri-current-file-simple` -- Advanced URI: Copy URI for current file
- `obsidian-advanced-uri:copy-uri-current-file-with-format` -- Advanced URI: Copy formatted URI for file with options 
- `obsidian-advanced-uri:copy-uri-current-file-simple-with-format` -- Advanced URI: Copy formatted URI for current file
- `obsidian-advanced-uri:copy-uri-daily` -- Advanced URI: Copy URI for daily note
- `obsidian-advanced-uri:copy-uri-search-and-replace` -- Advanced URI: Copy URI for search and replace
- `obsidian-advanced-uri:copy-uri-command` -- Advanced URI: Copy URI for command
- `obsidian-advanced-uri:copy-uri-block` -- Advanced URI: Copy URI for current block
- `obsidian-advanced-uri:copy-uri-block-with-format` -- Advanced URI: Copy formatted URI for current block
- `obsidian-advanced-uri:copy-uri-workspace` -- Advanced URI: Copy URI for workspace
- `obsidian-advanced-uri:copy-uri-canvas-node` -- Advanced URI: Copy URI for selected canvas nodes
- `obsidian-advanced-uri:copy-uri-canvas-viewport` -- Advanced URI: Copy URI for current canvas viewport

# Advanced URI

**Description:** Control various aspects through URIs, including opening files, creating new files, and executing commands.
**Status:** Enabled
**Plugin ID:** obsidian-advanced-uri

## Setup Required

No settings file found (data.json). Plugin may need initial setup via Obsidian Settings.
Guide the user to configure this plugin via Obsidian Settings if needed.

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `obsidian-advanced-uri:copy-uri-current-file` -- Advanced URI: Copy URI for file with options
- `obsidian-advanced-uri:copy-uri-current-file-simple` -- Advanced URI: Copy URI for current file
- `obsidian-advanced-uri:copy-uri-current-file-with-format` -- Advanced URI: Copy formatted URI for file with options 
- `obsidian-advanced-uri:copy-uri-current-file-simple-with-format` -- Advanced URI: Copy formatted URI for current file
- `obsidian-advanced-uri:copy-uri-daily` -- Advanced URI: Copy URI for daily note
- `obsidian-advanced-uri:copy-uri-search-and-replace` -- Advanced URI: Copy URI for search and replace
- `obsidian-advanced-uri:copy-uri-command` -- Advanced URI: Copy URI for command
- `obsidian-advanced-uri:copy-uri-block` -- Advanced URI: Copy URI for current block
- `obsidian-advanced-uri:copy-uri-block-with-format` -- Advanced URI: Copy formatted URI for current block
- `obsidian-advanced-uri:copy-uri-workspace` -- Advanced URI: Copy URI for workspace
- `obsidian-advanced-uri:copy-uri-canvas-node` -- Advanced URI: Copy URI for selected canvas nodes
- `obsidian-advanced-uri:copy-uri-canvas-viewport` -- Advanced URI: Copy URI for current canvas viewport

## Configuration File

Settings path: `.obsidian/plugins/obsidian-advanced-uri/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/obsidian-advanced-uri/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/obsidian-advanced-uri/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/obsidian-advanced-uri.readme.md")

## Usage

When the user asks for functionality related to Advanced URI:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/obsidian-advanced-uri/data.json). If it does not exist, that is normal -- create it with the required settings
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
