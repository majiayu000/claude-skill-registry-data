---
name: docx-convert
version: 2.0.0
description: '[Document Processing] Use when converting between Word DOCX and Markdown (GFM, math rendering). --to={markdown|docx}.'
disable-model-invocation: true
---

## Quick Summary

**Goal:** Convert Word DOCX to Markdown, or Markdown to Word DOCX, through one entry point.

**Workflow:**

1. **Pick a direction** — `--to markdown` (DOCX in, Markdown out) or `--to docx` (Markdown in, DOCX out)
2. **Install that direction** — each one has its own `package.json`; install only the one you need
3. **Convert** — run `scripts/convert.cjs --to <direction>` with the direction's own options
4. **Output** — the converter returns JSON with the success status and output path

**Key Rules:**

- `--to` is required. There is no default direction — converting the wrong way silently is worse than an error.
- Every other argument is passed straight to the chosen converter, so each direction keeps its own CLI.
- Dependencies are per direction: `--to markdown` never pulls in the DOCX writer, and vice versa.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# docx-convert

Convert Microsoft Word (.docx) files to GitHub-Flavored Markdown, and Markdown files to editable
Word documents with tables, code blocks, images and LaTeX math.

## Directions

| Flag            | Converts        | Lives in       | Dependencies                             |
| --------------- | --------------- | -------------- | ---------------------------------------- |
| `--to markdown` | DOCX → Markdown | `to-markdown/` | `mammoth`, `turndown`, `turndown-plugin-gfm` |
| `--to docx`     | Markdown → DOCX | `to-docx/`     | `markdown-docx`, `gray-matter`           |

## Installation Required

**Each direction installs separately.** Install only the one you need:

```bash
# DOCX -> Markdown
cd .claude/skills/docx-convert/to-markdown
npm install

# Markdown -> DOCX
cd .claude/skills/docx-convert/to-docx
npm install
```

`ck init` (which runs `install.sh`) handles every skill at once.

## Quick Start

```bash
# DOCX -> Markdown
node .claude/skills/docx-convert/scripts/convert.cjs --to markdown --input ./document.docx

# DOCX -> Markdown, extracting images to a folder instead of inlining base64
node .claude/skills/docx-convert/scripts/convert.cjs --to markdown -i ./doc.docx --images ./images/

# Markdown -> DOCX
node .claude/skills/docx-convert/scripts/convert.cjs --to docx --input ./README.md

# Markdown -> DOCX with a custom theme
node .claude/skills/docx-convert/scripts/convert.cjs --to docx -i ./doc.md --theme ./theme.json
```

`--to=markdown` and `--to markdown` are equivalent. A missing or unknown `--to` prints the valid
directions and exits 1.

## CLI Options

### Dispatcher

| Option   | Description                                 | Default    |
| -------- | ------------------------------------------- | ---------- |
| `--to`   | Conversion direction: `markdown` or `docx`  | (required) |

### `--to markdown` (DOCX → Markdown)

| Option     | Short | Description                    | Default       |
| ---------- | ----- | ------------------------------ | ------------- |
| `--input`  | `-i`  | Input DOCX file path           | (required)    |
| `--output` | `-o`  | Output markdown file path      | `{input}.md`  |
| `--images` |       | Directory for extracted images | inline base64 |
| `--help`   | `-h`  | Show help message              |               |

### `--to docx` (Markdown → DOCX)

| Option     | Short | Description         | Default        |
| ---------- | ----- | ------------------- | -------------- |
| `--input`  | `-i`  | Input markdown file | (required)     |
| `--output` | `-o`  | Output DOCX path    | `{input}.docx` |
| `--theme`  | `-t`  | Custom theme JSON   | built-in       |
| `--title`  |       | Document title      | filename       |
| `--help`   | `-h`  | Show help           |                |

Run `scripts/convert.cjs --to <direction> --help` to see a direction's full help.

## Features

**DOCX → Markdown**

- **GFM Tables:** Word tables become markdown tables
- **Images:** embedded images extracted (base64 inline, or written to a folder)
- **Lists:** ordered and unordered lists preserved
- **Code Blocks:** monospace text converted to code blocks
- **Links and Headings:** hyperlinks and heading levels maintained

**Markdown → DOCX**

- **GFM Support:** tables, strikethrough, task lists
- **Code Blocks:** syntax preserved with a monospace font
- **Images:** local and URL images embedded
- **Math:** LaTeX equations rendered by default (`$...$`, `$$...$$`)
- **Frontmatter:** YAML metadata supplies the title
- **No System Dependencies:** pure JavaScript, no Chrome needed

Both directions work on Windows, macOS and Linux.

## Conversion Pipeline (`--to markdown`)

```
DOCX → mammoth → HTML → turndown → Markdown
```

The two-stage conversion follows mammoth's official recommendation for best results.

## Output

Both directions return JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.docx",
    "output": "/path/to/output.md",
    "stats": {
        "images": 3,
        "tables": 2,
        "headings": 5
    }
}
```

`--to docx` omits `stats`. On failure both return `{ "success": false, "error": "..." }` and exit 1.

## Compatibility (`--to docx`)

Generated DOCX files open in Microsoft Word (2007+), Google Docs, LibreOffice Writer and Apple Pages.

## Limitations

- Complex layouts (columns, text boxes) may not preserve structure
- Merged table cells produce basic markdown tables
- Comments and track changes are stripped
- Some formatting (fonts, colors) is lost in conversion

## Troubleshooting

**Missing dependencies:** the error output carries a `hint` with the exact `cd … && npm install`
command for the direction you invoked.

## Tests

```bash
cd .claude/skills/docx-convert && node tests/dispatcher.test.cjs   # routing and --to validation
cd .claude/skills/docx-convert/to-markdown && node tests/run-tests.cjs
cd .claude/skills/docx-convert/to-docx && node tests/run-tests.cjs
```

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Convert Word DOCX to Markdown, or Markdown to Word DOCX, through one entry point — `scripts/convert.cjs --to {markdown|docx}`.

**IMPORTANT MUST ATTENTION** `--to` is required — never guess the direction for the user
**IMPORTANT MUST ATTENTION** each direction installs its own dependencies; the error `hint` names the exact directory
**IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
**IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
