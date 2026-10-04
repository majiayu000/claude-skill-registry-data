---
name: workspace
description: "Native workspace operations: PDF export, tab/pane management, file paths"
source: workspace
---

# Workspace

## Plugin metadata

- **id:** `workspace`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** FULL
- **has-settings:** true

### Commands

- `workspace:export-pdf` -- Export current note to PDF
- `workspace:close` -- Close current tab
- `workspace:split-horizontal` -- Split horizontally
- `workspace:split-vertical` -- Split vertically
- `workspace:new-tab` -- New tab
- `workspace:copy-path` -- Copy file path
- `workspace:copy-url` -- Copy Obsidian URL
- `workspace:edit-file-title` -- Rename file
- `workspace:toggle-pin` -- Toggle pin

Plugin "Workspace" provides core Obsidian workspace operations.

Available commands:
- workspace:export-pdf -- Export the currently open note to PDF using Obsidian's built-in renderer
- workspace:close -- Close the currently active tab
- workspace:split-horizontal -- Split the current pane horizontally
- workspace:split-vertical -- Split the current pane vertically
- workspace:new-tab -- Open a new empty tab
- workspace:copy-path -- Copy the active file's vault-relative path to clipboard
- workspace:copy-url -- Copy an obsidian:// URL for the active file
- workspace:edit-file-title -- Rename the active file inline
- workspace:toggle-pin -- Pin or unpin the active tab (pinned tabs stay open)

workspace:export-pdf is a native Obsidian command -- zero external dependencies, always available.
It renders the note exactly as Obsidian displays it (theme, CSS, plugins applied).
Note: Opens an export dialog. The user must confirm settings and save location.

Use workspace:export-pdf for quick PDF exports. For advanced conversion (custom LaTeX templates, bibliography, DOCX): use execute_recipe with Pandoc instead.

## Configuration File

Settings path: `.obsidian/workspace.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/workspace.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/workspace.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Current Configuration

```
main:
  id: ac84c8dee480a2db
  type: split
  children: [1 items]
  direction: vertical
left:
  id: 088448aa21f5bb97
  type: split
  children: [1 items: {...}...]
  direction: horizontal
  width: 300
right:
  id: bf52afa4a769ef37
  type: split
  children: [1 items: {...}...]
  direction: horizontal
  width: 300
left-ribbon:
  hiddenItems:
    switcher:Open quick switcher: false
    graph:Open graph view: false
    canvas:Create new canvas: false
    daily-notes:Open today's daily note: false
    templates:Insert template: false
    command-palette:Open command palette: false
    bases:Create new base: false
    markdown-importer:Open format converter: false
    workspaces:Manage workspace layouts: false
    agent-client:Open agent client: false
    webpage-html-export:Export as HTML: false
    obsidian-shellcommands:Shell commands: Custom variables: false
    open-gate:North3rnLight3r.com: false
    vault-ai-chat:Open AI vault memory: false
    agentcairn:Agentcairn memory: false
    nexus:Open chat: false
    vault-operator:Vault Operator: false
    table-editor-obsidian:Advanced Tables Toolbar: false
    obsidian-git:Open Git source control: false
    vscode-editor:Create Code File: false
active: 8b32ea1d242d3d32
lastOpenFiles: [Nexus/data/tasks, Nexus/data/conversations, README.md, session/README.md, Dev_Notes/Forge_updates.md, Nexus/data/workspaces/ws_default/shard-000001.jsonl, Nexus/data/workspaces/ws_default, Nexus/data/workspaces, Nexus/data, Nexus]
```

For full settings, read: `.obsidian/workspace.json`

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/workspace.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
