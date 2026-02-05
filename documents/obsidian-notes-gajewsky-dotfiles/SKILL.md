---
name: obsidian-notes
description: Use when saving notes to Obsidian vault, creating documentation, capturing knowledge, or logging any information. This skill determines the correct PARA location and applies the appropriate template from the vault.
---

# Obsidian Notes

## Overview

Save notes to a PARA-structured Obsidian vault by selecting the appropriate location and template. Templates are read dynamically from the vault itself.

## Vault Discovery

Obsidian vaults are located in `~/Obsidian/`. A vault is identified by having a `.obsidian/` subdirectory.

**Discovery process:**
1. List directories in `~/Obsidian/`
2. Check each for a `.obsidian/` folder
3. If one vault exists, use it automatically
4. If multiple vaults exist, ask user to choose

## PARA Structure

Vaults follow PARA methodology with numbered prefixes:

```
[vault]/
├── 0.Inbox/      # Quick captures, unsorted notes
├── 1.Projects/   # Active projects with defined outcomes
├── 2.Areas/      # Ongoing responsibilities
│   └── Templates/  # Note templates (fixed location)
├── 3.Resources/  # Reference material, knowledge base
└── 4.Archives/   # Completed/inactive items
```

## Location Decision Tree

To determine where to save a note:

1. **Quick capture with no clear category?** → `0.Inbox/`
2. **Active project with a defined end goal?** → `1.Projects/[project-name]/`
3. **Ongoing area of responsibility?** → `2.Areas/[area-name]/`
4. **Reference material or knowledge?** → `3.Resources/[topic]/`
5. **Completed or inactive item?** → `4.Archives/`

## Template Discovery

Templates are stored in `2.Areas/Templates/` within the vault.

**To find the right template:**
1. List all `.md` files in `2.Areas/Templates/`
2. Read the template frontmatter to identify the `type:` field
3. Match note type to template type
4. If no match, use minimal frontmatter

**Common template types:**
- `issue` - Bug investigations, issue tracking
- `incident` - Incident response notes
- `command` - Useful commands and scripts
- `project` - Project documentation
- `daily` - Daily journal entries
- `reflection` - Self-reflections
- `moc` - Map of Content

## Creating Notes

1. **Discover vault** - Find vault with `.obsidian/` folder in `~/Obsidian/`
2. **Determine location** - Use decision tree to pick PARA folder
3. **Find template** - Read from `2.Areas/Templates/` and match type
4. **Apply template** - Replace placeholders:
   - `{{date}}` → Current date (YYYY-MM-DD)
   - `{{title}}` → Note title
   - `{{time}}` → Current time (HH:MM)
5. **Write file** - Save to determined location

## File Naming

- Use descriptive names: `My Note Title.md`
- Projects may use emoji prefixes: `1.Projects/💻 Project Name/`
- Incidents use slug format: `inc-12345-brief-description.md`
- Daily notes use date: `YYYY-MM-DD.md`

## Minimal Frontmatter

When no template matches, use minimal frontmatter:

```yaml
---
type: note
created: {{date}}
---
```

## Examples

### Quick capture
User: "Save this quick thought about refactoring"

Location: `0.Inbox/Refactoring thought.md`
Template: None (minimal frontmatter)

### Issue tracking
User: "Create a note for the cart bug investigation"

1. Read templates from `2.Areas/Templates/`
2. Find template with `type: issue`
3. Location: `2.Areas/Issues/Cart bug investigation.md`

### Knowledge reference
User: "Save this info about GraphQL pagination"

Location: `3.Resources/GraphQL pagination.md`
Template: None (minimal frontmatter)

## Notes

- Always include YAML frontmatter with at least `type` and `created`
- Use wikilinks `[[]]` for internal links
- Create subfolders as needed within PARA directories
