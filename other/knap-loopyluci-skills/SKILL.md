---
name: knap
description: Use when the user asks to apply a Knap template, turn JSON or CSV data into notes, batch-generate Markdown files, or format Defuddle output into a note.
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

# Knap

> **Adapted for the LoopyLuci Skills collection** from [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- The user asks to apply a Knap template, turn JSON or CSV data into notes, batch-generate Markdown files, or format Defuddle output into a note

## When NOT to Use

- Outside the trigger above; keep the task in the skill that owns it.

## Overview

Render Markdown from templates and structured data with the Knap CLI — variables, filters, and logic, for single renders or batches.

## Before running

Check availability with `knap --help`. If it is missing, explain that Knap needs Node.js 20 or later and offer `npm install -g knap` or `npx knap`. Never report a rendered template when the tool is unavailable or returns an error.

Learn the template language from the CLI's offline reference, then ask for detail on individual items:

```bash
knap help syntax
knap help filters
knap help filter date
knap help tags
knap help tag for
```

## Rendering

Render a template file with JSON variables:

```bash
knap render template.md --data article.json -o note.md
```

Supply template and data inline:

```bash
knap render -t '# {{ title | trim }}' --data-json '{"title":"Hello"}'
```

Override a variable, or pipe JSON in:

```bash
knap render template.md --data article.json --set 'title=Custom title'
cat article.json | knap render template.md --data -
```

Data must be a JSON object; its properties become template variables. `--set` overrides literal top-level keys with strings — use JSON for nested objects, arrays, numbers, and booleans. Choose exactly one template source (file, `-t`, or stdin) and one data source (`--data` or `--data-json`), and never let both read stdin. Without a template file or `-t`, the template comes from stdin. Output goes to stdout by default; `-o` creates parent directories and overwrites the destination only after a successful render. Errors exit `1` with diagnostics on stderr; warnings may accompany successful output.

## Template language

`{{ variable }}` for values, `|` for filters, `{% ... %}` for logic. Example `template.md`:

```knap
---
{{ title | yaml_property:"title" }}
{{ tags | yaml_property:"tags" }}
---
# {{ title | trim }}
{% if author %}
By {{ author }}
{% endif %}

{{ content }}
```

Use `yaml_property` for complete frontmatter properties so values are quoted and indented correctly. The CLI ships standard filters but no Web Clipper browser variables, selectors, prompts, or DOM-dependent HTML filters — pass those through JSON.

Validate a template before rendering it:

```bash
knap validate template.md
```

Validation checks syntax, filter names, and static filter arguments without data or file output. It does not check variable existence, runtime values, or dynamic arguments — render with real data to check runtime behavior.

## Defuddle pipeline

Extract a page as JSON with Markdown content, then render it into a note:

```bash
defuddle parse https://example.com/article --md --json \
  | knap render template.md --data - -o note.md
```

Defuddle's JSON properties (`title`, `content`, and so on) become template variables directly.

## Batch rendering

Create one file per CSV row, JSON array element, or JSON file in a folder:

```bash
knap batch template.md --data articles.csv --output-dir notes \
  --filename '{{ title | safe_name }}.md'
```

Use `--data articles.json` for an array, or `--data ./articles` for a folder of objects. CSV headers become variable names and values stay strings; piped data defaults to JSON, so add `--format csv` for piped CSV. `--dry-run` validates and lists output paths without writing. Existing files require `--overwrite` (including during a dry run), and duplicate output names within a batch are errors even with `--overwrite`. Filename templates must produce a single filename with its extension and no directories; use `safe_name` for data-derived names. Without `--filename`, Knap keeps source JSON basenames or numbers CSV rows and array items `1.md`, `2.md`, and so on.

## Verification

- [ ] `knap` available; template validated.
- [ ] Exactly one template source and one data source; only one reading stdin.
- [ ] Output written with `-o` after a successful render.
- [ ] Batch filenames unique; `--overwrite` used only where intended.

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
- Path: `_sources/obsidianmd_obsidian-skills/plugins/obsidian/skills/knap/SKILL.md`
- License: MIT — Copyright (c) 2026 Steph Ango (@kepano)
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
