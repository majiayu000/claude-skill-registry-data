---
name: obsidian-markdown
description: Create and edit Obsidian-specific Markdown syntax, including wikilinks, embeds, block references, callouts, properties, tags, and comments. Use for Obsidian notes when these extensions matter; ordinary Markdown is assumed knowledge.
license: MIT
metadata:
  copilot-enabled-agents: opencode, claude, codex
  copilot-builtin-version: "1"
  copilot-upstream-revision: "a1dc48e68138490d522c04cbf5822214c6eb1202"
---

# Obsidian Markdown

Use Obsidian-specific syntax accurately. Do not spend tokens explaining ordinary
CommonMark or GFM unless the user asks.

## Workflow

1. Preserve existing frontmatter keys and formatting when editing a note.
2. Use wikilinks for vault notes and Markdown links for external URLs.
3. Use embeds, callouts, properties, tags, comments, and block references only
   when they improve the requested note.
4. Check link targets, YAML validity, and block IDs after editing.
5. Read the focused reference file when the task needs more syntax detail.

## Wikilinks and block references

~~~markdown
[[Note Name]]
[[Note Name|Display Text]]
[[Note Name#Heading]]
[[Note Name#^block-id]]
[[#Heading in this note]]

This paragraph is addressable. ^block-id
~~~

Put a block ID on its own line after a list or quote block.

## Embeds

Prefix a wikilink with <code>!</code>:

~~~markdown
![[Note Name]]
![[Note Name#Heading]]
![[image.png|300]]
![[document.pdf#page=3]]
~~~

See [Embeds](references/EMBEDS.md) for media, PDF, and query forms.

## Callouts

~~~markdown
> [!warning] Custom title
> Important content.

> [!faq]- Collapsed by default
> Foldable content.
~~~

See [Callouts](references/CALLOUTS.md) for types, aliases, folding, and nesting.

## Properties, tags, and comments

~~~yaml
---
title: My Note
date: 2026-07-21
tags:
  - project
aliases:
  - Alternate Name
related: "[[Other Note]]"
---
~~~

Quote wikilinks used as YAML values. See
[Properties](references/PROPERTIES.md) for supported property types and tag rules.

Use <code>#nested/tag</code> for inline tags. Hide content from reading view with
<code>%%inline comments%%</code> or a matching pair of <code>%%</code> markers on
separate lines.

## Attribution

Adapted from <code>kepano/obsidian-skills</code> at revision
<code>a1dc48e68138490d522c04cbf5822214c6eb1202</code>. See <code>LICENSE</code>.
