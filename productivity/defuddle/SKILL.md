---
name: defuddle
description: Use when extracting clean Markdown from HTML pages with Defuddle CLI.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [note-taking, obsidian, productivity]
    source: obsidianmd/obsidian-skills
    adapted: true
---

# Defuddle

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- Extract clean Markdown from HTML pages with Defuddle CLI

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Extract clean Markdown from a web page with the Defuddle CLI, stripping navigation, advertising, and other page clutter.

## Before running

Confirm the tool is present with `defuddle --help`. If it is missing, say so and offer the install command; never report a successful extraction when the tool is unavailable or returns an error.

## Commands

Markdown output (always pass `--md`):

```bash
defuddle parse <url> --md
```

Write the result to a file:

```bash
defuddle parse <url> --md -o content.md
```

Extract a single metadata property:

```bash
defuddle parse <url> -p title
defuddle parse <url> -p description
defuddle parse <url> -p domain
```

## Output formats

| Flag | Result |
| --- | --- |
| `--md` | Markdown (preferred default) |
| `--json` | JSON containing both HTML and Markdown |
| *(none)* | HTML |
| `-p <name>` | One metadata property |

## Verification

- [ ] `defuddle` is installed and answers `--help`.
- [ ] `--md` was passed for Markdown output.
- [ ] Extraction succeeded before the result was reported.
- [ ] Large pages were written to a file rather than dumped inline.

## Related Skills in This Repo

- [obsidian-bases](../obsidian-bases/SKILL.md) — Use when working with .base files, creating database-like views of notes, or when the user...
- [json-canvas](../json-canvas/SKILL.md) — Use when working with .canvas files, creating visual canvases, mind maps, flowcharts, or w...
- [obsidian-markdown](../obsidian-markdown/SKILL.md) — Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts...
- [obsidian-cli](../obsidian-cli/SKILL.md) — Use when the user asks to interact with their Obsidian vault, manage notes, search vault c...
- [obsidian-vault](../obsidian-vault/SKILL.md) — Use when searching, creating, or managing notes in an Obsidian vault
- [obsidian-note-taking-workflow](../obsidian-note-taking-workflow/SKILL.md) — Use when implementing Obsidian workflows.
- [obsidian](../obsidian/SKILL.md) — Read, search, create, and edit notes in the Obsidian vault.

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills)
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/defuddle/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
