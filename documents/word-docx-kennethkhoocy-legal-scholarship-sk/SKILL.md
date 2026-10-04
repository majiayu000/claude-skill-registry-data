---
name: word-docx
description: >-
  Unified skill for Microsoft Word .docx workflows: extracting comments or tracked changes,
  summarizing reviewer feedback, generating response-to-comments documents, building Word
  memos or reports, applying tracked edits, auditing OOXML internals, validating and repairing
  documents, accepting revisions, adding or resolving comments, converting legacy .doc files,
  unpacking or repacking .docx files, simplifying redline markup, rendering .docx to images,
  and building Word documents with tables of contents, multi-column layouts, or page-numbered
  headers and footers. Use whenever a task involves reading, reviewing, building, editing, or
  analyzing .docx files. Prefer this skill over ad-hoc python-docx or docx2python usage. Route
  PDFs, spreadsheets, presentations, Google Docs, and LaTeX-to-Word conversion pipelines to
  their dedicated skills.
---

# word-docx

Unified CLI for Microsoft Word `.docx` review and generation workflows.
Converts `.docx` content into structured JSON/Markdown before any LLM
reasoning, and builds new `.docx` files from structured specs.

## Core Principle

Never modify source `.docx` files in place. Never ask the LLM to parse
raw `.docx` XML directly. The pipeline always works in two steps:

1. **Extract** structured data (JSON/Markdown) from the `.docx`
2. **Reason** over the structured data, then **build** a new `.docx` if needed

## CLI Entry Point

All commands run through a single entry point:

```bash
python scripts/word_docx.py <command> [options]
```

The scripts directory is at `~/.claude/skills/word-docx/scripts/`.

## Command Routing

| User intent | Command | Primary library |
|-------------|---------|-----------------|
| Read comments / reviewer feedback | `extract-comments` | docx2python |
| Read tracked changes / redlines | `extract-revisions` | docx-revisions, OOXML fallback |
| Read ordinary text and tables | `extract-text` | python-docx |
| Full inspection (all of the above) | `inspect` | all |
| Build a new Word document | `build` | python-docx or docxtpl |
| Render to PDF | `render-pdf` | LibreOffice |
| Apply edits (auto-detect mode) | `apply-edits` | lxml + zipfile (OOXML) |
| Apply tracked edits (force) | `apply-tracked-edits` | lxml + zipfile (OOXML) |
| Apply silent edits (force) | `apply-non-tracked-edits` | lxml + zipfile (OOXML) |

## Backend Matrix

| Command | Backend | Notes |
|---------|---------|-------|
| `inspect`, `extract-comments`, `extract-revisions`, `extract-text` | Python (word-docx) | docx2python / docx-revisions / python-docx |
| `apply-edits`, `apply-tracked-edits`, `apply-non-tracked-edits` | Python (word-docx) | lxml + zipfile |
| `render-pdf`, `audit-ooxml` | Python (word-docx) | LibreOffice / lxml |
| `build` | Python or Node | auto-routes via spec markers — see Build Reference |
| `add-comment` | Hybrid | unpack → Python edit → comment.py → pack |
| `validate`, `accept-changes`, `convert-doc`, `unpack`, `pack`, `simplify-redlines`, `docx-to-images` | Python (anthropic) | subprocess to anthropic-agent-skills plugin |

## Library Roles

Each library has a specific role. Do not substitute one for another:

- **docx2python**: extraction of comments, headers, footers, text,
  footnotes, endnotes, properties, images
- **docx-revisions**: reading tracked changes (insertions, deletions,
  replacements) with author/date metadata; optional fallback for
  writing tracked replacements
- **lxml + zipfile (apply_edits)**: writing paragraph-scoped tracked
  changes (replace, insert, delete) with author/date metadata via
  direct OOXML manipulation
- **python-docx**: ordinary DOCX construction, paragraph/table reading,
  style manipulation
- **docxtpl**: rendering Word templates from structured data (Jinja2
  syntax inside Word)
- **lxml + zipfile**: raw OOXML audit and diagnostics

## Commands

### inspect

Full extraction and audit in one pass.

```bash
python scripts/word_docx.py inspect INPUT.docx --out OUTDIR
```

Produces:
- `manifest.json` — file list, timestamps, diagnostics
- `diagnostics.json` — OOXML audit results and warnings
- `comments.json` / `comments.md` — reviewer comments
- `revisions.json` / `revisions.md` — tracked changes
- `document.md` / `paragraphs.json` — body text

### extract-comments

```bash
python scripts/word_docx.py extract-comments INPUT.docx --out OUTDIR
```

Uses docx2python. Cross-checks against raw OOXML comment count.
Stable IDs: C001, C002, ...

### extract-revisions

```bash
python scripts/word_docx.py extract-revisions INPUT.docx --out OUTDIR
```

Tries docx-revisions first, falls back to raw OOXML scanning.
Stable IDs: R001, R002, ...

### extract-text

```bash
python scripts/word_docx.py extract-text INPUT.docx --out OUTDIR
```

Paragraphs and tables via python-docx. Outputs Markdown and JSON.

### build

```bash
python scripts/word_docx.py build --spec SPEC.json --out OUTPUT.docx
python scripts/word_docx.py build --spec SPEC.json --out OUTPUT.docx --template TEMPLATE.docx
```

Build spec JSON shape:
```json
{
  "title": "Document Title",
  "subtitle": "Optional subtitle",
  "sections": [
    {"heading": "Section heading", "paragraphs": ["Para 1 with a citation.[^1]"]}
  ],
  "items": [
    {
      "comment_id": "C001",
      "comment": "Reviewer comment",
      "response": "Response text",
      "revision_made": "Revision description"
    }
  ],
  "footnotes": {"1": "See Smith (2020) at 15."}
}
```

Footnotes use `[^N]` markers in paragraph text. The `footnotes` dict
maps each N to the footnote content. The build command creates proper
OOXML footnotes (`word/footnotes.xml` + `w:footnoteReference` elements)
via post-processing.

### audit-ooxml

```bash
python scripts/word_docx.py audit-ooxml INPUT.docx --out OUTDIR
```

Fast structural lint over the raw OOXML: counts paragraphs, tables,
tracked-change elements, comments, footnotes, endnotes. Writes
`diagnostics.json` to `--out`. Use `validate` instead for schema-grade
checks with auto-repair.

### render-pdf

```bash
python scripts/word_docx.py render-pdf INPUT.docx --out OUTPUT.pdf
```

Requires LibreOffice. Reports a clear error if unavailable.

### apply-tracked-edits

```bash
python scripts/word_docx.py apply-tracked-edits INPUT.docx --edits EDITS.json --out OUTPUT.docx
```

Applies tracked edits via direct OOXML manipulation (lxml + zipfile),
producing `w:ins` and `w:del` elements that appear as tracked changes
when the output is opened in Microsoft Word.

Supported operations:
- **replace**: Wraps `old_text` in `w:del` and inserts `new_text` in
  `w:ins` at the matched location. Handles text that spans multiple
  runs within a paragraph.
- **insert**: Appends `new_text` as a tracked insertion (`w:ins`) at
  the end of the target paragraph.
- **delete**: Wraps `old_text` in `w:del` as a tracked deletion in the
  target paragraph.

All operations are scoped to the paragraph specified by
`paragraph_index` (zero-based index into the document's `w:p`
elements). Each tracked change carries `w:author` and `w:date`
attributes; if `date` is omitted from the edit spec, the current UTC
timestamp is used.

Diagnostic behaviour:
- Warns and skips when `paragraph_index` is out of range.
- Warns and skips when `old_text` is not found in the target paragraph
  (for replace and delete).
- Reports applied/skipped counts.

### apply-edits (auto-detect)

```bash
python scripts/word_docx.py apply-edits INPUT.docx --edits EDITS.json --out OUTPUT.docx
```

Auto-detects whether the input document contains existing tracked changes
(w:ins/w:del elements). If tracked changes are present, applies edits as
tracked changes (same as `apply-tracked-edits`). Otherwise, applies edits
silently (same as `apply-non-tracked-edits`). This is the recommended
default command for applying edits.

### apply-non-tracked-edits

```bash
python scripts/word_docx.py apply-non-tracked-edits INPUT.docx --edits EDITS.json --out OUTPUT.docx
```

Same operations as `apply-tracked-edits` (replace, insert, delete) but
without tracked-change markup. The output reads as if the text was
always written that way. Uses the same JSON format; `author` and `date`
fields are accepted for compatibility but have no effect on output.

### Edits spec & matching semantics (all apply-* commands)

Verified against `apply_edits.py` internals (2026-07-08); these are the
gotchas that cause silent misfires:

- **EDITS.json is a top-level ARRAY** of operation objects, not an
  object wrapping them:
  ```json
  [
    {"operation": "replace", "paragraph_index": 12,
     "old_text": "and—subject to exceptions—is",
     "new_text": "and (subject to exceptions) is"}
  ]
  ```
  Wrapping in `{"edits": [...]}` fails with
  `EditOperation() argument after ** must be a mapping, not str`.
- **`paragraph_index` counts DIRECT children of `w:body` only**
  (`body.findall('w:p')`). Paragraphs inside tables/textboxes are
  excluded, so indices from `python-docx`, docx2python, or an
  `.//w:p` sweep will drift. Derive the index by locating which
  direct-child paragraph contains `old_text`, not by counting from
  another extraction.
- **Replacement flattens formatting to the FIRST matched run's `rPr`.**
  The whole matched span is re-emitted as one run cloned from the first
  affected run. Never let `old_text` span an italicized case name,
  bold phrase, or other formatting change — anchor the span so it
  starts and ends in uniformly formatted text (e.g. for
  `Foss—the rule that`, match `—the rule that …`, leaving the italic
  `Foss` outside the splice).
- **Matches cannot cross group boundaries.** Runs with no `w:t`
  (footnote references, fields) and non-run children (hyperlinks,
  bookmarks, existing `w:ins`/`w:del`) split the paragraph into
  contiguous run groups; `old_text` must sit inside ONE group. An
  `old_text` spanning a footnote marker will report "not found".
- **Pre-validate anchors programmatically** before applying a large
  batch: for each `old_text`, assert (1) it occurs exactly once in the
  whole document, (2) within a single run group, (3) the run containing
  the match start is not italic/styled. This catches every misfire
  before it silently skips.

## Typical LLM Workflow

```
1. inspect marked_up.docx --out ./review
2. LLM reads review/comments.json and review/revisions.json
3. LLM writes response_spec.json
4. build --spec response_spec.json --out response_to_comments.docx
```

## Output Conventions

- All outputs go into an explicit output directory — never alongside
  the source file.
- JSON files use UTF-8 with `ensure_ascii=False`.
- Comment IDs: C001, C002, ... Revision IDs: R001, R002, ...
- Diagnostics record warnings rather than crashing.
- Manifest files track what was produced and any issues.

## Install Prerequisites

word-docx's Python-native commands work standalone. The Anthropic-backed
commands require the document-skills plugin; the JS-routed `build` path
requires Node >= 18 and the `docx` npm package.

    claude plugin marketplace add anthropics/skills
    claude plugin install document-skills@anthropic-agent-skills
    npm install -g docx   # only needed for js-routed builds

If a command needs a backend that is not installed, it raises a clear
error with the exact install command. No silent failures.

## add-comment reference

Three sub-modes, one .docx output per invocation.

### Reply to existing comment

```
python scripts/word_docx.py add-comment INPUT.docx --out OUTPUT.docx \
    --reply-to C001 --text "Your reply." --author "Claude"
```

### Anchor a new comment on a span

```
python scripts/word_docx.py add-comment INPUT.docx --out OUTPUT.docx \
    --anchor-paragraph 3 --anchor-text "the term is 30 days" \
    --text "Should this be 60?" --author "Claude"
```

### Mark a comment as resolved

```
python scripts/word_docx.py add-comment INPUT.docx --out OUTPUT.docx \
    --resolve C001
```

## build spec reference

`build` accepts a JSON spec. Routing is auto by default; set `runtime`
explicitly to override.

### Python-routed example (no js-only features)

```json
{
  "title": "Quarterly Review",
  "page": {"size": "letter", "margins": {"top": 1, "bottom": 1, "left": 1, "right": 1}},
  "sections": [{"heading": "Overview", "paragraphs": ["Revenue grew 15%."]}],
  "footnotes": {"1": "Source: 10-K"}
}
```

### JS-routed example (toc + page numbers + native footnotes)

```json
{
  "title": "Annual Report",
  "toc": {"title": "Contents", "heading_range": "1-3", "hyperlinks": true},
  "columns": 2,
  "page_sections": [{
    "header": [{"type": "text", "value": "Annual Report 2026"}],
    "footer": [{"type": "text", "value": "Page "}, {"type": "page_number"}]
  }],
  "sections": [
    {"heading": "Executive Summary", "paragraphs": ["..."]},
    {"heading": "Results", "paragraphs": ["..."]}
  ],
  "native_footnotes": {"1": "All figures in USD millions."}
}
```

## Failure-mode reference

| Error | Fix |
|-------|-----|
| `AnthropicSkillNotInstalledError` | Run the two `claude plugin` commands above. |
| `BuildSpecRequiresJSError` | Either remove the js-only spec field, or set `"runtime": "auto"` (or omit). |
| `NodeNotInstalledError` | Install Node >= 18 from nodejs.org. |
| `DocxPackageMissingError` | Run `npm install -g docx`. |
