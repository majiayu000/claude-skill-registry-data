---
name: write-markdown
description: Write and revise Markdown in a clean, consistent style. Draft and edit Markdown documents. Improve formatting for headings, lists, code blocks, tables, or links.
metadata:
    markdownlint: "0.40.0"
    markdownlint-cli2: "0.20.0"
---

# Write Markdown

## Purpose

Write and revise Markdown in a clean, consistent style.

## When to use

Use this skill when the user asks:

- Draft or edit Markdown documents
- Improve formatting for headings, lists, code blocks, tables, or links

## Non-goals

- Do not impose a new house style without user or repository guidance.
- Do not copy bundled assets into a repository as templates.
- Do not run `markdownlint-cli2 --fix` unless the user explicitly asks to run
  `markdownlint-cli2 --fix`.

## Bundled resources

Use bundled resources as read-only references.

- Use `assets/.markdownlint.jsonc` to review available rule names and options.
- Use `assets/markdownlint-config-schema.json` and
  `assets/markdownlint-config-schema-strict.json` to validate configuration
  structure and allowed values.
- Use `scripts/markdownlint-cli2.sh` to run optional verification when
  `markdownlint-cli2` is available.

Do not copy these files into a repository unless the user explicitly requests
it.

## Default writing guidance

Follow repository conventions when they exist. Otherwise, apply these defaults.

### Headings and sections

- Use a single top-level title.
- Do not skip heading levels.
- Surround headings with blank lines.

See `references/headings-and-sections.md`.

### Lists and indentation

- Use a consistent list marker style.
- Keep indentation consistent for nested lists.
- Surround lists with blank lines when mixed with paragraphs.

See `references/lists-and-indentation.md`.

### Code blocks and code spans

- Prefer fenced code blocks.
- Add a language tag when known.
- Surround fenced code blocks with blank lines.
- Keep inline code spans tight.

See `references/code-blocks-and-code-spans.md`.

### Links and images

- Use descriptive link text.
- Avoid empty links.
- Provide alt text for images.
- Keep link style consistent.

See `references/links-and-images.md`.

### Tables

- Keep table column counts consistent.
- Surround tables with blank lines.

See `references/tables.md`.

### Whitespace and newlines

- Avoid trailing spaces and hard tabs.
- Avoid multiple consecutive blank lines.
- End files with a single newline.

See `references/whitespace-and-newlines.md`.

### Other formatting

- Use blockquotes consistently.

  See `references/blockquotes.md`.

- Use emphasis and strong consistently.

  See `references/emphasis-and-strong.md`.

- Use horizontal rules consistently.

  See `references/horizontal-rules.md`.

- Use inline HTML only when necessary.

  See `references/inline-html.md`.

- Keep line length and shell transcripts readable.

  See `references/line-length-and-shell-transcripts.md`.

- Capitalize proper names consistently.

  See `references/proper-names.md`.

## Optional verification

If `markdownlint-cli2` is available, run it after writing or editing.

- Quote glob arguments for cross-platform compatibility.
- Prefer `#` negation patterns for directories such as `node_modules`.

Example command:

```sh
scripts/markdownlint-cli2.sh "**/*.md" "#node_modules"
```

See `references/lint-verification.md`.

## Reporting verification results

When verification runs:

- Summarize which files failed.
- List rule ids that were reported.
- Suggest minimal edits.

If verification cannot run, provide a command the user can run locally.
