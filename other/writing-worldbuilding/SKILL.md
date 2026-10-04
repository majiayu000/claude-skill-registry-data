---
name: writing-worldbuilding
description: >-
  Writes new worldbuilding content: civilizations, characters, locations, factions,
  events, languages, or narrative elements. Use when creating new entries, expanding
  existing ones, or when user says "create", "write", "add", "flesh out", "build",
  or "expand" for any non-science content. Does NOT write science files — use
  /writing-science for that.
model: sonnet
effort: high
---

# Writing Worldbuilding

Write new non-science worldbuilding content following repo conventions.

## Prerequisites

1. Read CLAUDE.md for conventions and locked spellings
2. Read `references/writing-standards.md` for prose anti-patterns
3. If the project has a foundations audit toolkit, read it when writing
   civilizations, conflicts, or recovery arcs
4. Search existing files for related content (grep key terms)
5. Check science directories for universal rules the content must obey

## Process

1. Add YAML frontmatter: title, tags, status: draft
2. One entity per file — no mega-documents
3. kebab-case filenames
4. Cross-link to related files with relative markdown links
5. Flag potential contradictions: `<!-- REVIEW: potential conflict with [file] -->`

## Derivation-First Builds

For civilizations being built from scratch — especially in novel environments
or with non-human species — use `/civilization-build` instead of the scaffold
below. The scaffold's categories (governance, economy) are useful shorthand
for human civilizations in familiar contexts, but they can import assumptions
when applied to novel situations. The `/civilization-build` command ensures
every social structure is derived from biology and environment first.

The scaffold below remains useful for quick expansions of existing civilizations
or for human civilizations in Earth-like contexts where the derivation has
already been done (implicitly, by history).

## Civilization Scaffold

When creating a civilization, address: governance, cultural identity,
economy, technology, internal tensions, external relations, and how
they interpret the universe's fundamental forces.

## After Writing

- Update the relevant _index.md
- Add new terms to GLOSSARY.md
- Add dated events to MASTER-TIMELINE.md
- Present for author review — do NOT commit

## Out of Scope

Does NOT write science files (use /writing-science).
Does NOT audit content (use /auditing-canon).
Does NOT design physical world foundations (use /designing-worlds).
