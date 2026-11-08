---
name: obsidian-markdown
description: 'Applies Obsidian Flavored Markdown (wikilinks, embeds, callouts, frontmatter properties). Use when the user wants to write or edit vault notes ("add a callout", "use a wikilink", "OFM syntax"). Not for .base database views (use obsidian-bases).'
argument-hint: '[optional: specific OFM feature or note to work on]'
allowed-tools: Read
---

## Overview

This skill provides authoritative Obsidian Flavored Markdown (OFM) syntax knowledge. It covers wikilinks, embeds, callouts, frontmatter properties, tags, math, Mermaid, and footnotes. Treat the rules below as the OFM reference — they are not suggestions, they are the syntax contract.

## When to Use

Writing or editing Obsidian Flavored Markdown (wikilinks, embeds, callouts, tags, frontmatter properties, math, Mermaid) inside an Obsidian vault or for content destined for one.

### When NOT to use

- `.base` files, Bases views or filter formulas — use `obsidian-bases`.
- Shell commands against a running vault — use `obsidian-cli`.
- Standard markdown outside an Obsidian context — plain CommonMark/GFM applies, not OFM.
- Dataview queries or DataviewJS — that is a separate plugin with its own query language.
- Templater/Meta Bind DSLs — not part of OFM core.

## Core Process

1. Read the vault's `CLAUDE.md` (or equivalent vault-level guidance) if present to learn project-specific conventions — folder layout, tag taxonomy, note naming, template usage.
1. Apply the syntax rules in Techniques below. For specific lookups (full callout aliases, every property type, every embed variant), grep the matching `references/<file>.md` instead of loading the whole file.
1. Use wikilinks `[[Note]]` for internal vault notes. Use standard Markdown links `[text](url)` only for external URLs.
1. Before writing any wikilink, validate that it resolves to a real note in the vault. Unresolved wikilinks create orphan stubs and silently degrade graph quality.

## Techniques

### Wikilinks

- `[[Note]]` — link to a note by name (uses Obsidian's wikilink resolution).
- `[[Note|Display text]]` — link with custom display text.
- `[[Note#Heading]]` — link to a specific heading within a note.
- `[[Note#^block-id]]` — link to a specific block.
- `[[#Same-note heading]]` — link to a heading within the current note.
- Block IDs: place `^block-id` at the END of the paragraph being identified. For lists and blockquotes, place the `^block-id` on a separate line immediately after the item.

### Embeds (full list in `${CLAUDE_SKILL_DIR}/references/embeds.md`)

- `![[Note]]` — embed a note.
- `![[image.png]]` — embed an image.
- `![[file.pdf#page=3]]` — embed a specific PDF page.
- `![[Note#^block-id]]` — embed a specific block.

### Tags

- Inline: `#tag` — letters, numbers (not as first character), underscores, hyphens, and forward slashes are allowed.
- Frontmatter: `tags: [tag1, tag2]` — list format. Singular `tag:` is deprecated since Obsidian 1.9.
- Nested: `#parent/child` — creates a tag hierarchy.

### Frontmatter (full property types in `${CLAUDE_SKILL_DIR}/references/properties.md`)

- Default built-in properties (plural since 1.9): `tags`, `aliases`, `cssclasses`.
- Property types: Text, Number, Checkbox, Date, Date & Time, List, Links.
- Date format: `YYYY-MM-DD`. Date & Time format: `YYYY-MM-DDTHH:mm`.

### Callouts (full type list with aliases in `${CLAUDE_SKILL_DIR}/references/callouts.md`)

- Syntax:
  ```
  > [!type] Title
  > content
  ```
- Foldable: `> [!type]- Title` (collapsed by default) or `> [!type]+ Title` (expanded by default).
- Nestable: indent with an extra `>` for each level of nesting.

### Obsidian-specific syntax

- Highlight: `==highlighted text==`.
- Hidden comment: `%%hidden%%` — never renders.
- LaTeX inline: `$equation$`. LaTeX block:
  ```
  $$
  equation
  $$
  ```
- Mermaid: use a standard ```` ```mermaid ```` code fence. To link graph nodes to vault notes, add `class NodeName internal-link;` — Obsidian then resolves the node label as a wikilink.

## Red Flags

- Using Markdown links `[text](path)` for internal vault notes — use `[[wikilinks]]` instead so Obsidian's graph and backlinks work.
- Using singular `tag:` or `alias:` in frontmatter — deprecated since Obsidian 1.9; use the plural `tags:` and `aliases:` list forms.
- Placing a `^block-id` before the content it identifies — block IDs attach to the paragraph/line immediately preceding them.
- Confusing `[[Note#Heading]]` with `[[Note#^block-id]]` — `#` prefixes a heading, `^` prefixes a block ID. They are not interchangeable.

## Verification

To confirm: can you write a note that includes (a) a wikilink to another note, (b) a callout with a title, and (c) frontmatter with `tags` and `aliases`? Check that tags use YAML list syntax (`tags: [a, b]` or multi-line `- tag`) and every internal link uses `[[]]`, not `[]()`.

## References

- `${CLAUDE_SKILL_DIR}/references/callouts.md`: callout syntax, every callout type and its aliases. Grep it for the type or alias you need.
- `${CLAUDE_SKILL_DIR}/references/embeds.md`: embed variants for notes, images, audio, video, PDFs, blocks and search queries. Grep it for the variant you need.
- `${CLAUDE_SKILL_DIR}/references/properties.md`: default properties, property types, tag rules and multi-line list syntax. Grep it for the property type you need.
