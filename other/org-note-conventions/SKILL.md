---
name: org-note-conventions
description: Use when creating or editing private or personal Org notes, regardless of directory; not package manuals, project documentation, READMEs, literate configuration, or other separately governed Org files.
---

# Org Note Conventions

Use these conventions when creating or editing an Org note file.

## Scope

- Use for private or personal Org notes, regardless of directory.
- Do not use for package manuals, project documentation, READMEs, literate config files, or other Org files whose format is governed by a separate project convention.

## Structure

- Use `#+title:` for the note title; preserve an existing title rather than adding a duplicate.
- If the file uses a single root note heading (`*`), put its top-level content sections at level two (`**`). Do not add sibling level-one content headings unless the existing file already uses that structure or the user asks for it.
- If the file has no root heading, put top-level content sections at level one (`*`). A `#+title:` keyword does not create a heading parent; do not invent a root or skip to level two merely to apply this convention.
- Preserve existing Org structure: property drawers, IDs, tags, TODO keywords, lists, tables, source/example blocks, citations, links, and local variables.

## Prose

- Keep prose paragraphs unfilled: one physical line per paragraph, except for intentional hard line breaks.
- Do not hard-wrap prose to a fill column. Join only soft wrapping; preserve explicit Org hard breaks (two trailing backslashes) and indentation with structural meaning.
- Preserve structural line breaks in headings, lists, tables, drawers, blocks, and other non-prose Org elements.

## Updating Existing Notes

Follow the file's established structure unless the user asks to normalize it. If the existing structure conflicts with these conventions, make the smallest change that satisfies the user request and state the convention mismatch if it matters.
