---
name: writing-style
description: >-
  Generates a WRITING.md file with YAML tokens for prose consistency — voice,
  tense, forbidden words, citation format, equation format, locked spellings —
  paired with usage rationale. Use when establishing prose standards, updating
  style rules, or when user says "WRITING.md", "style guide", "prose standards",
  "writing tokens", "voice", "style system", or "writing rules". Does NOT write
  content — generates the style reference only.
model: sonnet
effort: medium
---

# Writing Style — WRITING.md Generation

Generates a `WRITING.md` file that gives Claude Code a persistent,
structured understanding of your universe's prose standards.

## The Format

1. **YAML front matter** — Machine-readable style tokens
2. **Markdown body** — Usage rationale by document type

Read `references/writing-md-template.md` for the full template.

## The Style Questionnaire

1. **Document types** — What types of files does this project produce?
2. **Voice per type** — Academic third-person? Engaged analytical? Close-third?
3. **Tense rules** — Present for laws? Past for history?
4. **Forbidden words** — Generic filler to avoid
5. **Citation format** — Inline parenthetical? Footnote?
6. **Locked spellings** — Proper nouns with specific forms

Write to project root as `WRITING.md`.

## Out of Scope

Does NOT write content. Does NOT audit prose (use /auditing-canon).
