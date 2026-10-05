---
name: fancy-kanban
description: Generate valid fancy-kanban boards — markdown-embedded kanban boards with typed fields, swimlanes, workflow rules, and card face configuration for Obsidian and compatible tools
---

# Fancy Kanban Board Schema

A self-contained specification for the markdown-based kanban board format. Any app that reads and writes files following this schema will produce compatible boards.

## Overview

Each board lives inside a fenced code block with the identifier `fancy-kanban`. This means:

- A board can be **embedded anywhere in a note**, alongside prose, links, and other content
- A note may contain **zero, one, or multiple** boards
- A file consisting of a single board block is a **standalone board file**
- Without the plugin installed, the block renders as an unstyled code block — the raw text remains fully human-readable

The block contains two sections separated by `---`:

1. A **config section** (YAML-like) defining fields, workflow, and view options
2. A **markdown table** containing the data rows

## Complete Example

````markdown
```fancy-kanban
---
title: My Board
fields:
  - name: title,       type: Text,     label: Title
  - name: status,      type: Select,   options: inbox|doing|done, label: Status, default: inbox
  - name: responsible, type: Text,     label: Responsible
  - name: start_date,  type: Date,     label: Start Date
  - name: notes,       type: Textarea, label: Notes
  - name: effort,      type: Number,   label: Effort
  - name: docs,        type: Link,     label: Docs
  - name: team,        type: Select,   options: frontend|backend, label: Team
card_fields: responsible, effort
lanes: team
workflow: inbox→doing, inbox→done, doing→done, doing→inbox, done→doing, done→inbox
---

| _id    | Title          | Status | Responsible | Start Date | Notes                      | Effort | Docs                  | Team     |
|--------|----------------|--------|-------------|------------|----------------------------|--------|-----------------------|----------|
| x7k2a1 | Fix login bug  | inbox  | Alice       | 2026-01-15 | Needs investigation        | 3      |                       | backend  |
| m3p9b2 | Refactor auth  | doing  | Bob         |            | Multi-line\<br\>content here | 5      | design.md             | backend  |
| q1r4c3 | Setup CI       | done   |             | 2026-01-01 |                            | 1      | setup.md\|guide.md    | frontend |
```
````

## Block Structure

The fenced block contains exactly two sections divided by a `---` line:

```
```fancy-kanban
---
{config}
---

{markdown table}
```
```

Everything before the first `---` is ignored (reserved for future use). Everything between the two `---` lines is the config. Everything after the second `---` is the table.

## Config Section

YAML-like key-value pairs. Parsed line-by-line.

### Keys

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `title` | yes | — | Human-readable board name |
| `fields` | yes | — | List of field definitions (see below) |
| `version` | no | `1` | Format version written by the plugin; boards with a version higher than the current plugin supports open in read-only mode |
| `workflow` | no | all transitions allowed | Comma-separated `from→to` pairs |
| `lanes` | no | none | Field name to use as the swimlane grouping dimension |
| `card_title` | no | auto-detect | Field name to use as the card heading; set to empty string to show no heading |
| `card_fields` | no | none | Ordered comma-separated list of secondary fields to display below the card heading |
| `card_labels` | no | `true` | Set to `false` to hide the label prefix on secondary card fields |
| `card_limit` | no | `0` (no limit) | Maximum number of cards shown per column; cards beyond this count are hidden behind a "Show more" button |

### `card_title`

```yaml
card_title: summary
```

Controls which field is rendered as the card heading:

- **Absent** (default): the first non-`_id`, non-column field is used automatically
- **Set to a field name**: that field's value appears as the heading
- **Set to empty string** (`card_title: `): no heading is shown; the card displays only secondary fields

### `card_fields`

```yaml
card_fields: priority, due, docs
```

An ordered, comma-separated list of **secondary** field names to display below the card heading. These appear as labelled rows beneath the title.

**Default behaviour**: when `card_fields` is absent the card shows only the heading field. Existing boards with no `card_fields` key are unaffected.

**Unknown names**: field names that do not match any defined field are silently ignored at render time. Removing a field from `fields:` automatically hides it from the card face without a parse error.

**Link fields**: when a `Link` field is included in `card_fields`, its items are rendered as a horizontal list of clickable links on the card face. Vault paths open in a new tab; external URIs open in the browser.

### `card_labels`

```yaml
card_labels: false
```

When set to `false`, the label prefix is omitted from secondary field rows on the card face — only the value is shown. Defaults to `true` (labels visible). The key is only written to the config when its value is `false`.

### `card_limit`

```yaml
card_limit: 5
```

When set to a positive integer, each column shows at most that many cards. Cards beyond the limit are hidden and a **Show more (N)** button appears at the bottom of the column. Clicking it reveals all remaining cards without reloading the board. Setting `card_limit: 0` or omitting the key disables limiting entirely.

This is particularly useful for boards where the **done** column accumulates many completed cards over time — the most recently added cards remain visible at a glance, while older history collapses out of the way.

### `lanes`

When set to a field name (must be a `Select` field), the board renders as a matrix:

- **Columns** — driven by the `status` field's `options` order
- **Swimlane rows** — driven by the `lanes` field's `options` order

Cards with no value for the lanes field appear in an **Unassigned** pseudo-lane at the bottom. Changing `lanes` is a view-config change only — no row data is affected.

## Field Definitions

Each entry in the `fields` list is a comma-separated set of `key: value` pairs on a single line, prefixed with `- `:

```yaml
fields:
  - name: title, type: Text, label: Title
  - name: status, type: Select, options: inbox|doing|done, label: Status, default: inbox
```

**Field ordering convention**: list `title` first, then `status`, then additional fields. The table column order in the data section mirrors the field definition order, and the auto-detected card heading resolves to the first non-`_id`, non-column field — so placing `title` first ensures predictable heading resolution without needing an explicit `card_title` key.

### Field Properties

| Property | Required | Description |
|----------|----------|-------------|
| `name` | yes | Internal identifier. Lowercase, underscores for spaces. |
| `type` | yes | One of: `Text`, `Textarea`, `Date`, `Number`, `Select`, `Link` |
| `label` | yes | Human-readable column header. Must match the markdown table header exactly. |
| `options` | Select only | Pipe-separated (`\|`) list of allowed values |
| `colors` | Select, optional | Pipe-separated `name=hex` pairs assigning a background color to each option (e.g. `High=#e74c3c\|Low=#27ae60`). Options without an entry render as plain text. |
| `default` | no | Default value for new cards |

### Field Types

| Type | Storage Format | Description |
|------|----------------|-------------|
| `Text` | Plain string | Single-line text |
| `Textarea` | String with `<br>` for newlines | Multi-line text |
| `Date` | `YYYY-MM-DD` | Calendar date |
| `Number` | Integer or decimal string | Numeric value |
| `Select` | One of the `options` values | Constrained choice; options may carry hex colors via the `colors` property |
| `Link` | `<br>`-separated list of paths or URIs | Vault-root-relative paths (`notes/doc.pdf`) or external URIs (`https://…`, `ftp://…`, `mailto:…`) |

### Special Field Names

| Name | Role |
|------|------|
| `title` | **Primary display field.** Should be listed first in `fields:`. Used as the auto-detected card heading when `card_title` is not set. |
| `status` | **Required. Kanban column field.** Must be `type: Select`. Cards are grouped into columns by this value. Column order follows `options` order. |

All other fields are secondary — displayed as card metadata when listed in `card_fields`.

## Item Identity

Every card has a **stable hidden ID** stored in a `_id` column in the markdown table. The UI never displays this column.

- Generated on card creation: short random alphanumeric string (e.g. 8 characters: `x7k2a1b3`)
- Preserved through all serialization round-trips
- Survives reordering, drag-and-drop, and field renames
- Used internally for all card operations (move, edit, delete)

Because identity is ID-based and not derived from content, renaming a card's title has no effect on its identity.

## Workflow

Defines which status transitions are allowed in the UI:

```yaml
workflow: inbox→doing, inbox→done, doing→done, doing→inbox, done→doing, done→inbox
```

- Comma-separated list of `from→to` pairs (arrow: `→`, U+2192)
- If `workflow` is omitted, all transitions between status options are permitted
- Used to constrain UI choices (e.g. a "Move to" menu only shows valid targets)
- Hand-edits to the raw table bypass workflow validation by nature of being plain text

## Board Templates

When creating a new board, a set of predefined templates provides common `status` option sets. Templates only pre-fill the `status` field options and `workflow` — all other fields are added by the user.

| Template | Status options | Default workflow |
|----------|---------------|------------------|
| **Basic** | `inbox \| doing \| done` | All transitions |
| **Software** | `backlog \| todo \| in-progress \| review \| done` | Forward + one step back |
| **Content** | `idea \| draft \| review \| published` | Forward only |
| **Project** | `planning \| active \| blocked \| complete` | All except → planning |
| **Custom** | User-defined | User-defined |

Selecting **Custom** opens a free-form editor for `status` options and workflow transitions.

## Markdown Table

The table appears immediately after the closing `---` of the config section.

### Structure

```
| _id    | Header1 | Header2 |
|--------|---------|---------|
| abc123 | value   | value   |
```

1. **Header row** — first column is always `_id`; remaining columns are field labels in schema definition order
2. **Separator row** — standard markdown table separator
3. **Data rows** — one row per card; `_id` cell contains the card's stable ID

### Rules

- Column order in the table must match field definition order (after `_id`)
- Empty cells are valid (field value = empty string)
- Row order within a status group is the display order
- An empty table (header + separator, no data rows) is valid
- The `_id` column is always first and is never shown in the rendered board

### Escaping

| Character in value | Escaped as |
|-------------------|------------|
| `\|` (pipe) | `\|` (backslash-pipe) |
| Newline | `<br>` |
| Carriage return | `<br>` |

When reading: `\|` → `|`, `<br>` → newline.
When writing: `|` → `\|`, any newline → `<br>`.

## Parsing Algorithm

1. Extract the raw string between the opening and closing fences of the `fancy-kanban` block
2. Split on the first `---` line to locate the config section start
3. Split on the second `---` line to separate config from table
4. Parse config line-by-line: extract `title`, `version`, `fields`, `workflow`, `lanes`, `card_title`, `card_fields`, `card_labels`, `card_limit`
5. For `fields`, collect lines starting with `- ` and parse each as comma-separated `key: value` pairs; `colors` is decoded as pipe-separated `name=hex` tokens
6. Find table lines in the body (lines starting with `|`)
7. First table line is the header row — extract column labels; `_id` is always first
8. Map remaining header labels to field names via case-insensitive label lookup
9. Parse each data row: split on unescaped `|`, trim cells, unescape `\|` and `<br>`
10. First cell of each data row is the card's `_id`
11. Group cards by `status` field value, seeding groups in `options` order

**Schema reconciliation (applied after parsing):**
- Fields present in schema but missing from a card's data: backfill with the field's `default` (or empty string)
- Fields present in card data but removed from the schema: preserve as orphaned hidden data (not deleted)

## Writing Algorithm

1. Reconstruct the config section from the current schema (preserve original formatting where possible)
2. Generate header row: `_id` first, then field labels in schema definition order
3. Generate separator row
4. Generate one data row per card: `_id` first, then field values in schema order, with pipes and newlines escaped
5. Generate a new card `_id` using a random alphanumeric string if the card has no existing ID
6. Reconstruct the full block: opening fence, config, `---`, blank line, table, closing fence

**Write-back principle:** only the text range of the affected block is patched in the source file — surrounding content is never rewritten.

## Minimum Viable Board

```
```fancy-kanban
---
title: My Board
fields:
  - name: title, type: Text, label: Title
  - name: status, type: Select, options: inbox|doing|done, label: Status, default: inbox
workflow: inbox→doing, inbox→done, doing→done, doing→inbox, done→doing, done→inbox
---

| _id | Title | Status |
|-----|-------|--------|
```
```

## Compatibility Notes

- Without the plugin, the block renders as a plain code block — all data is still visible as plain text
- The markdown table inside the block is valid markdown and readable in any text editor
- The config section follows YAML conventions familiar to static site generators and note-taking apps
- Removing the plugin leaves all data intact and recoverable

## Deprecated Features

See [docs/deprecations.md](deprecations.md) for the full list of deprecated field types and config keys, their replacements, and planned removal versions.
