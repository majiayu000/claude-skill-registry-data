---
name: open-gate
description: "Embed any website to Obsidian, you have anything you need in one place. You can browse website and take notes at the same time. e.g. Ask ChatGPT and copy the answer directly to your note."
source: open-gate
---

# Open Gate

## Plugin metadata

- **id:** `open-gate`
- **source:** vault-native
- **plugin-type:** community
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `open-gate:open-gate-aHR0cHM6Ly93d3cubm9ydGgzcm5saWdodDNyLi5jb20=` -- Open Gate: Open gate North3rnLight3r.com
- `open-gate:open-gate-YWJvdXQ6Ymxhbms=` -- Open Gate: Open gate Temp Gate
- `open-gate:open-gate-create-new` -- Open Gate: Create new gate
- `open-gate:open-list-gates-modal` -- Open Gate: List Gates

# Open Gate

**Description:** Embed any website to Obsidian, you have anything you need in one place. You can browse website and take notes at the same time. e.g. Ask ChatGPT and copy the answer directly to your note.
**Status:** Enabled
**Plugin ID:** open-gate

## Available Commands

Available command IDs (use execute_command for Obsidian-native commands):
- `open-gate:open-gate-aHR0cHM6Ly93d3cubm9ydGgzcm5saWdodDNyLi5jb20=` -- Open Gate: Open gate North3rnLight3r.com
- `open-gate:open-gate-YWJvdXQ6Ymxhbms=` -- Open Gate: Open gate Temp Gate
- `open-gate:open-gate-create-new` -- Open Gate: Create new gate
- `open-gate:open-list-gates-modal` -- Open Gate: List Gates

## Configuration File

Settings path: `.obsidian/plugins/open-gate/data.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/plugins/open-gate/data.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/plugins/open-gate/data.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify data.json directly.

## Current Configuration

These are the plugin's current settings (sensitive values redacted):

```
uuid: 1dszu4d2h27q5xrdxrirnp
gates:
  aHR0cHM6Ly93d3cubm9ydGgzcm5saWdodDNyLi5jb20=:
    id: aHR0cHM6Ly93d3cubm9ydGgzcm5saWdodDNyLi5jb20=
    title: North3rnLight3r.com
    icon: ~/home/North3rnLight3r/Projects/AIFRED/apps/website/assets/artwork/aifred-mascot.jpg
    hasRibbon: true
    position: right
    profileKey: open-gate
    url: https://www.north3rnlight3r..com
    zoomFactor: 1
    userAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
```

For full settings, read: `.obsidian/plugins/open-gate/data.json`

## Documentation

For detailed plugin documentation (commands, options, dependencies):
read_file(".vault-operator/data/skills/open-gate.readme.md")

## Usage

When the user asks for functionality related to Open Gate:
1. Read the plugin documentation (.readme.md) to understand capabilities and dependencies
2. Read the config file (.obsidian/plugins/open-gate/data.json). If it does not exist, that is normal -- create it with the required settings
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
