---
name: obsidian-bases
description: 'Builds and edits Obsidian Bases (.base files) with filters, formulas and views. Use when the user wants a database view of vault notes (".base file", "Bases view", "filter formula", "vault database"). Not for note syntax (use obsidian-markdown).'
argument-hint: '[optional: base file name or query to build]'
allowed-tools: Read
---

# Obsidian Bases

## Overview

Obsidian Bases is a native database/spreadsheet feature introduced in Obsidian 1.x. A `.base` file is a YAML document that defines filtered, formula-enriched, grouped views over vault notes. This skill provides authoritative Bases syntax — filters, formulas, property namespaces, view types, and summaries — so edits to `.base` files produce valid, working queries.

## When to Use

Writing, editing or debugging `.base` files: filters, formulas, views and summaries that list, group or summarize notes across the vault.

### When NOT to use

- Dataview queries (DQL, `TABLE`, `LIST`, `WHERE` syntax, or JavaScript views) — different query language, not Bases, and out of scope for `obsidian-markdown` too.
- Wikilinks, callouts or frontmatter edits on a single note — no Bases file involved; use `obsidian-markdown`.
- Obsidian plugin development or community plugin config — Bases is a core feature, not a plugin.

## Core Process

1. **Read vault CLAUDE.md** (if present) for custom property naming conventions before writing any formula. Property names in formulas must match the vault's frontmatter keys exactly.
1. **Determine filter criteria** — which notes the view should include. Translate the user's intent into `file.hasTag`, `file.inFolder`, frontmatter property comparisons, or compound `and`/`or`/`not` blocks.
1. **Define properties, formulas, and view type** — pick `table`, `cards`, `list`, or `map`; list the columns/fields; add formulas for any computed values.
1. **Watch for Duration pitfalls** — subtracting two dates returns a `Duration`, not a `Number`. Always chain `.days` / `.hours` / `.minutes` before feeding into numeric functions or display.

## Techniques

**File structure.** A `.base` file is valid YAML with these optional top-level keys: `filters`, `formulas`, `properties`, `summaries`, `views`.

**Filters.**

```yaml
filters: "file.hasTag('project')"

filters:
  and:
    - "file.hasTag('project')"
    - "file.inFolder('02 - Areas')"

filters:
  not: "file.hasTag('archived')"
```

Filter functions: `file.hasTag(tag)`, `file.hasLink(note)`, `file.inFolder(path)`, `.matches(regex)`. Logical operators inside strings: `&&`, `||`, `!`.

**Property namespaces.**

- Note frontmatter: `propertyName` (direct, unqualified).
- File metadata: `file.name`, `file.basename`, `file.path`, `file.folder`, `file.ext`, `file.size`, `file.ctime`, `file.mtime`, `file.tags`, `file.links`, `file.backlinks`, `file.embeds`, `file.properties`.
- Computed: `formula.formulaName`.
- `this` resolves to the current note in main content, the embed host inside an embed, and the sidebar target when viewed in the sidebar.

**Formulas.**

```yaml
formulas:
  age: "date.now() - file.ctime"
  daysSinceModified: "(date.now() - file.mtime).days"
```

Duration pitfall: `date.now() - file.mtime` returns a `Duration`. Access `.days`, `.hours`, `.minutes`, etc., before passing to numeric functions, rounding, or comparisons against numbers.

**Views.**

```yaml
views:
  - type: table
    name: "All Notes"
    properties: [file.name, status, file.mtime]
    sort: [{property: file.mtime, direction: desc}]
    groupBy: status
```

View types: `table`, `cards`, `list`, `map`.

**Summaries.**

```yaml
summaries:
  status:
    formula: count
```

Built-in summary formulas: `Average`, `Min`, `Max`, `Sum`, `Range`, `Median`, `Stddev`, `Earliest`, `Latest`, `Checked`, `Unchecked`, `Empty`, `Filled`, `Unique`, `Count`.

**Embedding.**

- `![[MyBase.base]]` embeds the full base.
- `![[MyBase.base#View Name]]` embeds a specific named view.

**YAML quoting.** When a formula string contains double quotes, wrap the string in single quotes:

```yaml
formulas:
  label: 'if(status == "done", "done", "open")'
```

## Red Flags

- Using `(date.now() - file.mtime)` directly as a number — must access `.days` / `.hours` / etc. Duration is not a Number.
- Using DQL keywords (`TABLE`, `FROM`, `WHERE`, `SORT`) — that is Dataview, not Bases. Bases uses YAML with filter functions.
- Wrapping a formula string in double quotes when the formula itself contains double quotes — YAML parse error. Use single quotes around the outer string.
- Using `tag:` (singular frontmatter-style) inside a filter expression instead of `file.hasTag()` — filter context needs the function call form.
- Referencing a frontmatter property with the `file.` prefix (e.g., `file.status`) — frontmatter properties are unqualified. `file.` is reserved for file metadata.

## Verification

To confirm the skill was applied correctly, output a sample `.base` snippet that lists all notes with tag `project`, sorted by `file.mtime` descending, showing name and status columns. The snippet should parse as valid YAML and use only the namespaces and functions documented above.

## References

- `${CLAUDE_SKILL_DIR}/references/functions-reference.md`: formula function signatures by return type (Date, Duration, String, Number, Boolean, List, File). Grep it for the function name or category you need while writing a formula.
