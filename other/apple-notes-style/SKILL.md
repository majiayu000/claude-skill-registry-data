---
name: apple-notes-style
description: Use this skill when the user wants to create content following the formatting style of an existing Apple Notes note. Trigger when the user says things like "siga o padrão da minha nota", "formate igual ao Apple Notes", "use o estilo de [nome da nota]", "crie seguindo o formato de [nota]", or passes a note name as reference.
---

# Apple Notes Style Mirror

Replicate the formatting pattern of an existing Apple Notes note when creating new content.

## How to invoke

```
/apple-notes-style <note-name> [folder]
```

- `<note-name>` — name of the reference note in Apple Notes
- `[folder]` — optional folder (e.g. Work). If omitted, search all folders.

## Steps

### 1 — Read the reference note

Use the `Read and Write Apple Notes: get_note_content` tool to fetch the note by name and folder (if provided).

If the note is not found, ask the user to confirm the exact name and folder.

### 2 — Extract the formatting pattern

Analyze the raw HTML returned and document the following:

**Structure:**
- What tag is the main title? (`<h1>`, `<h2>`, bold `<div>`, etc.)
- What tags are used for section headers? Note if they use `<h2>`, `<h3>`, or bold `<div>`
- Are there subsection levels?

**Lists:**
- What list class is used? (`Apple-dash-list` = dash `–` markers, default `<ul>` = bullet `•`)
- Are lists nested (double `<ul>` inside each other)?
- Do list items have a bold label followed by ` - ` or `:` and plain text?

**Spacing:**
- How are sections separated? (blank `<div><br></div>`, `font-size: 11px` spacers, or both)
- Is there indentation via `\t` tabs in `<div>` items?

**Inline formatting:**
- Are tool/item names in bold followed by ` - ` and description? (Plataformas style)
- Are items plain text? (Reunião style)

### 3 — Summarize the pattern

Before generating content, explicitly state the pattern you identified. Example:

> **Pattern identified:**
> - Main title: `<h1>`
> - Sections: `<h2>` bold
> - "Plataformas" sections: indented `<div>` with **bold name** - plain description
> - "Reunião" sections: nested `Apple-dash-list` with plain text items
> - Spacing: `font-size: 11px` spacers between sections

### 4 — Apply the pattern

Generate the requested content strictly following the identified pattern:

- Mirror the exact same heading hierarchy
- Use the same list type (`Apple-dash-list` vs plain `<ul>`)
- Replicate nesting depth of lists
- Use the same inline bold conventions (bold label + ` - ` or `:`)
- Preserve spacing conventions between sections
- Match the tone and level of detail of the original (descriptive vs concise)

### 5 — Output format

Return the content as formatted text or HTML matching the Apple Notes structure, ready to be pasted or written back via `add_note` or `update_note_content`.

If the user wants to write the content back into Apple Notes, use `update_note_content` or `add_note` accordingly.

## Important Rules

### Timestamp Convention

When adding log entries or progress items with timestamps:
- **Always use Brasília Time (BRT/America/Sao_Paulo timezone)**
- Format: `[DD/MM/YY HH:MM]` (24-hour format)
- Example: `[02/04/26 09:31]` not `[02/04/26 12:31]`
- Convert UTC times: UTC -3 hours = BRT
- This applies to all timestamped entries regardless of context

## Known limitations

- The Apple Notes MCP does not expose: sidebar color bars, dark/light theme, exact font sizes beyond `font-size: 11px` spacers
- The `Apple-dash-list` class signals `–` dash markers — this IS preserved by the MCP
- Tab indentation in `<div>` items IS preserved by the MCP
