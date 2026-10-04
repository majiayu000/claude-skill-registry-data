---
name: markdown-writer
description: Applies project documentation standards and markdownlint rules when writing or editing Markdown. Use this skill when creating or editing any Markdown file.
---
# Markdown Writer

## When to Load Standards

Before writing or editing any Markdown file, **eagerly** find and read project-specific sources.
Do not assume generic Markdown rules; project conventions and lint config must drive formatting.

## Find and Read Documentation Standards

Look for and read (in order of priority):

- **Doc-standards directories**: `docs/docs_standards/`, `docs_standards/`, `.cursor/` (rules or docs)
- **Index files**: `docs/docs_standards/README.md`, `docs/README.md` (for links to conventions)
- **Convention docs**: Any file named like `markdown_conventions.md`, `MARKDOWN.md`, or referenced from the index
- **Project meta**: `meta.md`, `ai_files/ai_coding_instructions.md`, `CONTRIBUTING.md` (for doc/lint mentions)

Read the main convention doc(s) so headings, line length, one-sentence-per-line, tables, and heading numbering follow the project.

## Find and Read Markdownlint Config

Look for and read the **first existing** config in the repo root (or current doc tree):

- `.markdownlint.yml` or `.markdownlint.yaml`
- `.markdownlint.json` or `.markdownlint.jsonc`
- `.markdownlint-cli2.jsonc` (may `extend` another file; follow the chain)

Use the config to align with line length (e.g. MD013), list style (e.g. MD004), code block style (e.g. MD046), and any custom rule names (e.g. `no-h1-content`, `one-sentence-per-line`).
If a rule is disabled or configured, respect that in the written output.

## Apply When Writing or Editing

- **Headings**: Match required depth, numbering, uniqueness, and title-case rules from the standards and lint.
- **Structure**: Respect TOC placement (e.g. only under H1, no content between H1 and first H2), no empty headings, no H1 content except TOC where required.
- **Prose**: One sentence per line if enforced; line length within configured limits.
- **Lists/code**: List style (dash vs asterisk), fenced vs indented code blocks, and list/code spacing as specified.
- **Links**: Prefer Markdown links for in-repo paths; follow any anchor or ID patterns from the config (e.g. `allow-custom-anchors`).
- **Traces To sections** (tech specs): "Traces To" subsections MUST be the **last** subsection under their parent Spec Item heading and MUST contain **only** a list of requirement links (no prose).
- **Tables**: Use only if allowed; otherwise use lists or sections per conventions.

## After Editing

- If the project uses a lint command (e.g. `just lint-md`, `npx markdownlint-cli2 --fix`), suggest or run it for the changed file(s) and fix reported issues.

## Quick Checklist

- [ ] Read doc standards from the repo (docs_standards, README, meta, CONTRIBUTING).
- [ ] Read markdownlint config (.markdownlint.yml or equivalent).
- [ ] Apply conventions and config while writing or editing.
- [ ] Run or suggest project lint command and fix any violations.
