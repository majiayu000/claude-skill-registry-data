---
name: graph
description: "Visualize note connections as a graph"
source: graph
---

# Graph View

## Plugin metadata

- **id:** `graph`
- **source:** core
- **plugin-type:** core
- **status:** enabled
- **class:** PARTIAL
- **has-settings:** true

### Commands

- `graph:open` -- Open graph view
- `graph:open-local` -- Open local graph

Plugin "Graph View" visualizes connections between notes.

Available commands:
- graph:open -- Open the full vault graph view
- graph:open-local -- Open a local graph showing connections of the active note

Use this when the user wants to visualize note relationships or explore the knowledge graph.

## Configuration File

Settings path: `.obsidian/graph.json`

To configure this plugin programmatically:
1. Read the config: read_file(".obsidian/graph.json")
2. Understand the settings structure and modify values as needed
3. Write changes: write_file(".obsidian/graph.json", updatedJSON)

Do NOT ask the user to open Settings UI. Modify config directly.

## Current Configuration

```
collapse-filter: false
showTags: true
showAttachments: true
hideUnresolved: true
showOrphans: true
collapse-color-groups: false
collapse-display: false
showArrow: false
textFadeMultiplier: 0
nodeSizeMultiplier: 1
lineSizeMultiplier: 1
collapse-forces: true
centerStrength: 0.518713248970312
repelStrength: 10
linkStrength: 1
linkDistance: 250
scale: 1.2069946451410882
close: false
```

For full settings, read: `.obsidian/graph.json`

## Documentation

For detailed documentation:
read_file(".vault-operator/data/skills/graph.readme.md")

IMPORTANT: After reading this file, ALWAYS take action or respond. Never end silently.
