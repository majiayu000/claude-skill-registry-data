---
name: repo-wiki
description: >
  Repository wiki engine: bi-directional linking, catalog.json, frontmatter injection,
  slug-based link resolution, backlink generation, and structured directory routing
  (core/reference/drafts/archive). Use when organizing docs into a wiki with [[slug]] links,
  generating catalog.json, injecting frontmatter, building backlinks, validating broken links,
  or migrating flat docs into core/reference/drafts/archive. For binary document conversion
  (PDF/DOCX/PPTX/XLSX) or workspace index.md generation, use the workspace-indexer skill instead.
  Triggers: "repo wiki", "catalog.json", "bi-directional links", "backlinks", "docs-tool",
  "문서 위키", "repo-wiki".
---

# Repo Wiki

Wiki engine for repository documentation: metadata, bi-directional links, and catalog management.

> **Not this skill**: Binary → Markdown conversion and `index.md` inventory/keyword maps → use **workspace-indexer**.

## Quick Start

```bash
# Run from the skill's Base Directory
python3 scripts/repo-wiki.py wiki init
python3 scripts/repo-wiki.py wiki add --all
python3 scripts/repo-wiki.py wiki backlinks --build
python3 scripts/repo-wiki.py wiki links --check
```

## Wiki Commands

### `wiki init`

Generate catalog.json, _index.md, and configuration.

```bash
python3 scripts/repo-wiki.py wiki init
```

Creates:
- `_meta/catalog.json` — Full document index with metadata
- `_meta/backlinks/` — Directory for reverse-link data
- `_index.md` — Curated landing page
- `.repo-wikirc` — Configuration file

### `wiki add [--all] [--file PATH]`

Analyze MD file, extract slug, inject frontmatter, update catalog.

```bash
python3 scripts/repo-wiki.py wiki add --file guides/getting-started.md
python3 scripts/repo-wiki.py wiki add --all
```

Adds missing frontmatter fields: `title`, `slug`, `status`, `category`, `tags`, `created`, `updated`.

### `wiki link <from-file> <to-slug> [--section HEADING]`

Convert a relative link to `[[slug]]` or `[[slug#section]]` format.

### `wiki backlinks --build [--file PATH]`

Scan all MD files for `[[slug]]` references. Write `_meta/backlinks/<slug>.json` and append "Referenced by" sections.

### `wiki links --check [--fail-on-broken]`

Validate all `[[slug]]` links against catalog.json. Exit code 1 if broken (CI-friendly).

### `wiki migrate --to structured`

Restructure flat docs into `core/`, `reference/`, `drafts/`, `archive/` based on frontmatter `status`.

### `wiki status`

Print document counts by status and category.

## References

- `references/linking-patterns.md` — `[[slug]]` syntax, cross-file linking, section references
- `references/metadata-schema.md` — frontmatter field definitions and validation rules

## Workflow

1. `wiki init` — Generate catalog.json and _index.md
2. `wiki add --all` — Inject frontmatter into all files
3. `wiki link` — Convert relative links to `[[slug]]` (manual or bulk)
4. `wiki backlinks --build` — Generate reverse references
5. `wiki links --check` — Validate before committing
6. `wiki migrate --to structured` — Reorganize into core/reference/drafts/archive

## Notes

- `.git`, `__pycache__`, `node_modules`, `.github`, `venv` ignored by default
- For binary conversion or workspace `index.md`, switch to **workspace-indexer**
