---
name: dxb
description: |
  Build and manage DXPR Builder pages via drush dxb:* commands.
  Write Bootstrap 5 HTML: the builder parses it into drag-and-drop
  editable elements. Use when asked to "create a page", "build a
  landing page", "edit page markup", "list templates", "update page
  layout", "create a reusable section", "scaffold content from a
  template", or any DXPR Builder content/layout task.
---

# DXPR Builder Drush Commands

<!-- PROMPT_RULES_START (auto-generated from prompt.js; do not edit manually) -->
## HTML Content Rules

DXPR Builder parses standard Bootstrap 5 HTML into drag-and-drop
editable elements. Follow these rules when generating markup:

### Layout

- Use Bootstrap grid system and responsive design patterns
- Row columns must total exactly 12 (e.g. col-6 + col-6, col-4 + col-4 + col-4). Do NOT use col-auto or col without a size: each column must have an explicit number (col-1 through col-12)
- Avoid nested containers
- Sections contain content directly - no empty wrapper divs:
- But only use a container-fluid when appropriate for the type of content
- CRITICAL: NEVER use Bootstrap flexbox utility classes (d-flex, d-inline-flex, gap-*, flex-row, flex-column, flex-wrap, justify-content-*, align-items-*) for layouts. These classes are FORBIDDEN.
- For ANY horizontal arrangement of elements (buttons, links, cards, icons, etc.), you MUST use the Bootstrap grid: wrap elements in div.row containing div.col-N children that total 12

### Styling

- The content will be part of a custom themed Bootstrap 5 page
- Use Bootstrap classes for their intended purpose, e.g. do not use .warning or .success just for styling
- DO NOT use CSS background colors or gradients unless the user explicitly requests them
- DO NOT include style tags

### Images

- Every IMG tag needs src and alt attributes
- Place images between content blocks, not inline with text
- Format src as: https://promptahuman.com/600x400@2x?bg_color=[HEX]&text_color=[HEX+333333]&title=[file_name.png]&prompt=[Creative Brief in plain text, emoji allowed.]
<!-- PROMPT_RULES_END -->

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `dxb:element:list` | `dxpr-el` | List available elements (blocks, views) |
| `dxb:template:list` | `dxpr-tl` | List page templates |
| `dxb:page:create` | `dxpr-pc` | Create entity from template (`type` and `template_id` are arguments) |
| `dxb:page:get` | `dxpr-pg` | Read builder markup |
| `dxb:page:update` | `dxpr-pu` | Update builder markup with BS5 HTML |
| `dxb:user-template:list` | `dxpr-utl` | List reusable user templates |
| `dxb:user-template:create` | `dxpr-utc` | Save reusable template |
| `dxb:setup-ai` | `dxpr-sa` | Install AI skill files to project root |

Run `drush <command> --help` for full options.

## Workflow

1. **Discover**: `template:list`, `element:list`
2. **Create**: `page:create` from template or create entity then `page:update`
3. **Edit**: `page:get` to read, modify, `page:update` to save
4. **Reuse**: `user-template:create` to save sections

Write Bootstrap 5 HTML following the rules above.
The builder parses it into drag-and-drop components automatically.
