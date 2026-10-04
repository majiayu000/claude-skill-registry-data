---
name: pdf-convert
description: '[Document Processing] Use when converting between PDF and Markdown: text PDFs to Markdown (scanned PDFs are reported, not OCR''d), Markdown to styled PDF. --to={markdown|pdf}.'
disable-model-invocation: true
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
## Quick Summary

**Goal:** Convert PDF to Markdown, or Markdown to PDF, through one entry point.

**Workflow:**

1. **Pick a direction** — `--to markdown` (PDF in, Markdown out) or `--to pdf` (Markdown in, PDF out)
2. **Install that direction** — each one has its own `package.json`; install only the one you need
3. **Convert** — run `scripts/convert.cjs --to <direction>` with the direction's own options
4. **Output** — the converter returns JSON with the success status and output path

**Key Rules:**

- `--to` is required. There is no default direction — converting the wrong way silently is worse than an error.
- Every other argument is passed straight to the chosen converter, so each direction keeps its own CLI.
- Dependencies are per direction: `--to markdown` never pulls in the PDF renderer, and vice versa.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# pdf-convert

Convert PDF files to Markdown (with automatic detection of native text vs scanned documents) and
Markdown files to high-quality PDF (with code syntax highlighting and custom CSS).

## Directions

| Flag              | Converts        | Lives in     | Dependencies                             |
| ----------------- | --------------- | ------------ | ---------------------------------------- |
| `--to markdown`   | PDF → Markdown  | `to-markdown/` | `@opendocsg/pdf2md`, `pdfjs-dist`      |
| `--to pdf`        | Markdown → PDF  | `to-pdf/`      | `md-to-pdf`, `gray-matter`             |

## Installation Required

**Each direction installs separately.** Install only the one you need:

```bash
# PDF -> Markdown
cd .claude/skills/pdf-convert/to-markdown
npm install

# Markdown -> PDF
cd .claude/skills/pdf-convert/to-pdf
npm install
```

`ck init` (which runs `install.sh`) handles every skill at once.

**Note:** `--to pdf` may download Chromium (~150MB) on first run unless system Chrome is detected.
OCR for scanned PDFs under `--to markdown` needs extra setup (see OCR Setup below).

## Quick Start

```bash
# PDF -> Markdown (auto-detects native text vs scanned)
node .claude/skills/pdf-convert/scripts/convert.cjs --to markdown --input ./document.pdf

# PDF -> Markdown with an explicit output path and forced native mode
node .claude/skills/pdf-convert/scripts/convert.cjs --to markdown -i ./doc.pdf -o ./out.md --mode native

# Markdown -> PDF
node .claude/skills/pdf-convert/scripts/convert.cjs --to pdf --input ./README.md

# Markdown -> PDF with custom CSS
node .claude/skills/pdf-convert/scripts/convert.cjs --to pdf -i ./doc.md --css ./my-style.css
```

`--to=markdown` and `--to markdown` are equivalent. A missing or unknown `--to` prints the valid
directions and exits 1.

## CLI Options

### Dispatcher

| Option   | Description                                    | Default    |
| -------- | ---------------------------------------------- | ---------- |
| `--to`   | Conversion direction: `markdown` or `pdf`      | (required) |

### `--to markdown` (PDF → Markdown)

| Option     | Short | Description                              | Default      |
| ---------- | ----- | ---------------------------------------- | ------------ |
| `--input`  | `-i`  | Input PDF file path                      | (required)   |
| `--output` | `-o`  | Output markdown file path                | `{input}.md` |
| `--mode`   | `-m`  | Conversion mode: `auto`, `native`, `ocr` | `auto`       |
| `--help`   | `-h`  | Show help message                        |              |

### `--to pdf` (Markdown → PDF)

| Option           | Short | Description                 | Default       |
| ---------------- | ----- | --------------------------- | ------------- |
| `--input`        | `-i`  | Input markdown file path    | (required)    |
| `--output`       | `-o`  | Output PDF file path        | `{input}.pdf` |
| `--css`          | `-c`  | Custom CSS file path        | built-in      |
| `--no-highlight` |       | Disable syntax highlighting | false         |
| `--help`         | `-h`  | Show help message           |               |

Run `scripts/convert.cjs --to <direction> --help` to see a direction's full help.

## Features

**PDF → Markdown**

- **Auto-Detection:** determines whether the PDF has native text or needs OCR
- **Native PDFs:** fast extraction via `@opendocsg/pdf2md`
- **Tables:** basic table structure preservation
- **No System Dependencies:** pure JavaScript

**Markdown → PDF**

- **Syntax Highlighting:** code blocks rendered with highlight.js
- **Custom CSS:** override the default stylesheet with your own
- **System Chrome:** uses installed Chrome/Chromium when available
- **Frontmatter Support:** YAML frontmatter supplies the title and metadata

Both directions work on Windows, macOS and Linux.

## Conversion Modes (`--to markdown`)

### Auto (default)

Checks whether the first page has extractable text. Uses native extraction if it does, otherwise
reports that the document appears to be scanned.

### Native

Fast direct text extraction. Best for PDFs with selectable text.

### OCR (scanned PDFs) — coming soon

Not yet implemented; the skill tells you when a PDF appears to be scanned.

## Default Styling (`--to pdf`)

- Serif body font (Georgia), monospace code font (Consolas/Monaco)
- 2cm page margins
- Code block background highlighting
- Table borders with alternating row colors

Override any of it with `--css`.

## Output

Both directions return JSON on success:

```json
{
    "success": true,
    "input": "/path/to/input.pdf",
    "output": "/path/to/output.md",
    "stats": {
        "pages": 5,
        "mode": "native"
    }
}
```

`--to pdf` returns `pages` instead of `stats`. On failure both return
`{ "success": false, "error": "..." }` and exit 1.

## Limitations

- Complex multi-column layouts may not preserve structure
- Scanned PDF OCR accuracy depends on image quality
- Mathematical formulas may not convert perfectly
- First-run OCR downloads language data (~15MB)
- Large documents converted to PDF may need more memory — consider splitting the input

## OCR Setup (optional)

For scanned PDF support, add these to the `to-markdown` direction:

```bash
cd .claude/skills/pdf-convert/to-markdown
npm install tesseract.js pdfjs-dist canvas
```

**Note:** the `canvas` package may require build tools on some systems.

## Troubleshooting

**Chrome not found (`--to pdf`):** the converter downloads Chromium automatically. Set
`PUPPETEER_SKIP_DOWNLOAD=1` to prevent that.

**Missing dependencies:** the error output carries a `hint` with the exact `cd … && npm install`
command for the direction you invoked.

**Font issues:** embed fonts via CSS `@font-face` with base64-encoded fonts for consistent rendering.

## Tests

```bash
cd .claude/skills/pdf-convert && node tests/dispatcher.test.cjs   # routing and --to validation
cd .claude/skills/pdf-convert/to-markdown && node tests/run-tests.cjs
cd .claude/skills/pdf-convert/to-pdf && node tests/run-tests.cjs
```

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Convert PDF to Markdown, or Markdown to PDF, through one entry point — `scripts/convert.cjs --to {markdown|pdf}`.

**IMPORTANT MUST ATTENTION** `--to` is required — never guess the direction for the user
**IMPORTANT MUST ATTENTION** each direction installs its own dependencies; the error `hint` names the exact directory
**IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting
**IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
**IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.
