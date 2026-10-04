---
name: journal
description: Validate and append project journal entries without re-deriving the journal format.
---

# Journal

## Conventions

- Use straight ASCII only. Do not use em dashes, en dashes, or curly quotes.
- Each session entry is one H2 heading: `Project - date: title` (for example
  `## Wholesale - September 18, 2026: preview-data-refresh pilot delivery`).
- Open every entry with a `### Summary` section.
- Do not use emoji, chatbot phrasing, or binary contrasts.
- Language-tag every fenced code block and keep fences balanced.
- Anchor URLs in links. Do not leave bare URLs.
- Do not use double blank lines.
- Run the banned-vocabulary word-boundary scan and require zero hits.

These conventions are mirrored in project memory `mem_1789820913458`.

## Procedure

1. Draft the new entry using the conventions above.
2. Validate the complete new entry, including ASCII, headings, Summary placement, code fences,
   links, blank-line spacing, and the banned-vocabulary word-boundary scan.
3. Peek at the journal tail only as needed to match the existing heading style and
   confirm where the most recent entry ends.
4. Append the new entry at the end of the journal as its own H2. A genuinely new project
   just means a new project name in the heading; never insert under an older entry.
5. Never rewrite or reformat existing entries.

The conventions live here and in project memory. Never re-read the whole journal to re-derive them.
