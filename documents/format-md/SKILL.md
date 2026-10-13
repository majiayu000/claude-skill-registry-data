---
name: format-md
description: "Format markdown (.md) and MDX (.mdx) files using @takazudo/mdx-formatter. Use when: (1) User wants to format markdown files, (2) User mentions 'format md', 'prettify markdown', or 'fix markdown formatting', (3) Markdown/MDX files need consistent formatting. Features: remark-based AST formatting, MDX (JSX, imports/exports), Japanese text, HTML→md conversion, Docusaurus admonitions, GFM (tables, strikethrough, task lists)."
---

# Format Markdown/MDX Files

Format the specified markdown or MDX file(s) using `@takazudo/mdx-formatter`.

## Usage

The user can specify:

- A specific file path (e.g., `README.md`, `docs/guide.md`)
- Multiple files (e.g., `docs/*.md`)
- If no file is specified, ask the user which file(s) they want to format

## Formatter Details

- **npm package**: `@takazudo/mdx-formatter`
- **Command**: `npx @takazudo/mdx-formatter --write <file-path>`

## Instructions

1. If the user provided a file path or pattern, use it directly
2. If no file was specified, ask the user which file(s) they want to format
3. Run the formatter using the Bash tool:

   ```bash
   npx @takazudo/mdx-formatter --write <file-path>
   ```

4. Report the results to the user

## Examples

```bash
# Format a single file
npx @takazudo/mdx-formatter --write README.md

# Format multiple files with glob pattern
npx @takazudo/mdx-formatter --write "docs/**/*.md"
```

## Features

The formatter provides:

- AST-based formatting with remark
- MDX support (JSX components, imports/exports)
- Japanese text handling
- HTML to markdown conversion
- Docusaurus admonitions preservation
- GFM features (tables, strikethrough, task lists)
