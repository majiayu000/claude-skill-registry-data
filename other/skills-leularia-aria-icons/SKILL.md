---
name: aria-icons
description: "Use when working with icons in any project. Search 340k+ icons, add them as source files (no giant dependency), migrate existing icon libraries, and run as an MCP server. Commands: `aria-icons search`, `aria-icons add`, `aria-icons get`, `aria-icons migrate`, `aria-icons doctor`."
---

# Aria Icons

Find any icon. Put it directly into the codebase. Let AI use it.

The CLI is tiny — it talks to the Aria Icons API and only downloads the icons you ask for.

## Installation

```bash
npm install -g aria-icons
# or
bun add -g aria-icons
```

Run without installing:

```bash
npx aria-icons search arrow --limit 10
npx aria-icons add house
```

Point at a local API during development:

```bash
ARIA_ICONS_API=http://localhost:3001 aria-icons search house
```

## CLI

```bash
# Search
aria-icons search <query> [--collection lucide] [--style outline] [--limit 32] [--json]

# Get SVG / component source
aria-icons get lucide:house
aria-icons get lucide:house --format react --size 20 --color currentColor

# Add to the project (detects React/Vue/Svelte/Solid/Flutter/RN)
aria-icons add house arrow-up github
aria-icons add lucide:house --out-dir src/components/icons

# Audit + migrate
aria-icons doctor
aria-icons similar lucide:house
aria-icons equivalent lucide:house --to tabler
aria-icons migrate --to lucide --dry-run
aria-icons migrate --to lucide

# MCP for agents
aria-icons setup
aria-icons mcp
```

## Icon IDs

`collection:name` — e.g. `lucide:house`, `tabler:arrow-up`, `mdi:account`, `thesvg:github`.

Aliases: `lucide` → `lucide-icons`, `tabler` → `tabler-icons`, `feather` → `feathers`.

## MCP tools

| Tool | Description |
|------|-------------|
| `search_icons` | Search across all collections |
| `get_icon` | SVG + framework snippets |
| `get_icon_svg` | SVG only |
| `get_icon_component` | One framework |
| `get_icons` | Batch fetch |
| `list_collections` | Browse sets |
| `find_similar_icons` | Other collections / related names |
| `find_equivalent_icon` | Map onto a target collection |
| `add_icon_to_project` | Write a component file |
| `scan_project_icons` | Detect existing icon libraries |

## Project config

`aria-icons init` writes `.aria-icons.json`:

```json
{
  "framework": "react",
  "outDir": "src/components/icons",
  "defaultCollection": "lucide"
}
```
