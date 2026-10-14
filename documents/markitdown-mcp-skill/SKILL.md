---
name: markitdown-mcp-skill
description: "markitdown MCP reference — local docs-to-Markdown (PDF, DOCX, PPTX, XLSX, HTML, EPUB): config, decision tree, fallbacks."
license: Apache-2.0
compatibility: opencode
metadata:
  pattern: mcp-document-reading
category: Configuration
---

## What this skill does

- Documents the `markitdown` MCP server and its single tool `convert_to_markdown`
- Provides `opencode.json` configuration (the `mcp.servers` entry and `permissions` rule)
- Prescribes a decision tree for choosing markitdown vs `image-analyzer-subagent` vs `pdf-specialist-skill` vs `pdftotext` vs built-in `Read`
- Covers usage patterns (large docs, batch conversion, table post-processing)
- Documents privacy guarantees for company-internal document handling
- Provides fallback strategies when the MCP is unavailable

**Reference:** [Upstream microsoft/markitdown](https://github.com/microsoft/markitdown) · [markitdown-mcp on PyPI](https://pypi.org/project/markitdown-mcp/)

## Requirements & Honesty Note

| Requirement                                                          | Status                                                  |
| -------------------------------------------------------------------- | ------------------------------------------------------- |
| `markitdown` MCP server in `opencode.json` `mcp.servers` block        | Required for MCP tool access                            |
| `markitdown-mcp` binary on PATH                                       | Installed via `./deploy/setup.sh` (PyPI, pinned) or baked into Docker |
| `mcp.servers.markitdown.disabled: false` in `opencode.json`          | **Ships `disabled: true`** — user must opt in (#262)     |
| `permissions` rule `{ "action": "markitdown*", "resource": "*", "effect": "allow" }` | **No rule by default** — user must opt in (#262) |

If any requirement is unmet, MCP tool calls return connection errors. Fall back to `pdftotext`, `image-analyzer-subagent`, or built-in `Read` (see **Fallback Strategy** below).

**Privacy note (#487):** markitdown is now the official `markitdown-mcp` from PyPI (stdio, `MARKITDOWN_ENABLE_PLUGINS=false`). Local document conversions (PDF/DOCX/PPTX/XLSX/MSG/...) make zero network calls, and Azure converters never activate. Residual: `markitdown[all]` ships audio/YouTube converters — an **audio file** input uploads to Google Speech and a **YouTube URL** contacts YouTube, so keep those input types away from this tool when zero egress is required. Opt-in (`disabled: true` by default per #262) remains a minimal-footprint choice.

## opencode.json Configuration

The markitdown MCP server ships as opt-in (`disabled: true`) per [#262](https://github.com/darellchua2/civiltekk-opencode-claude-skills/issues/262). To enable:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "markitdown": {
        "type": "local",
        "command": ["markitdown-mcp"],
        "environment": {
          "MARKITDOWN_ENABLE_PLUGINS": "false"
        },
        "disabled": false
      }
    }
  },
  "permissions": [
    { "action": "markitdown*", "resource": "*", "effect": "allow" }
  ]
}
```

**Both flips are required:**
1. `mcp.servers.markitdown.disabled: false` — starts the server process
2. `permissions` rule `{ "action": "markitdown*", "resource": "*", "effect": "allow" }` — grants tool-calling permission. Rules live in the top-level `permissions` array (last matching rule wins); a legacy `permission` map key is ignored by opencode v2.

The sanctioned path does both flips and installs the launcher in one step: `./deploy/setup.sh --enable-pack markitdown` (Linux/macOS) or `.\deploy\setup.ps1 --enable-pack markitdown` (Windows). Manual editing of the deployed config works too. Docker users get the launcher baked in at build time.

Verify: `opencode mcp list` shows `markitdown` as `connected` — after restarting opencode (MCP servers connect at session start; config edits need a restart).

## Available MCP Tools

| Tool                       | Description                                                                          | Use Case                                       |
| -------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------- |
| `convert_to_markdown(uri)` | Convert a document at the given URI to Markdown. Accepts `file:`, `data:`, `http:`, `https:` schemes. | Extract text from binary office docs, fetch remote URLs |

**Tool name is exactly `convert_to_markdown` (snake_case).** The skill name uses kebab-case (`markitdown-mcp-skill`); the MCP tool uses snake_case. Don't confuse them.

### Input schema

```json
{
  "name": "convert_to_markdown",
  "arguments": {
    "uri": "file:///absolute/path/to/document.pdf"
  }
}
```

Returns: `{ "content": [{ "type": "text", "text": "<markdown>" }] }`

## Format Coverage

All converters below are **100% local** (no network calls, verified via `ss -tnp`):

| Format        | Local library                  | Output characteristic                                              |
| ------------- | ------------------------------ | ----------------------------------------------------------------- |
| PDF           | pdfminer.six, pdfplumber       | Page-separated text; tables best-effort                           |
| DOCX          | mammoth, lxml                  | Headings, paragraphs, lists; tables as Markdown tables            |
| PPTX          | python-pptx                    | `<!-- Slide number: N -->` separators per slide                   |
| XLSX / XLS    | openpyxl, pandas, xlrd         | Multi-sheet → `## Sheet N` headers; cells as Markdown tables      |
| Outlook MSG   | olefile, extract-msg           | Headers, body, attachment list                                    |
| HTML          | beautifulsoup4, markdownify    | Cleaned Markdown (scripts/styles stripped)                        |
| CSV / JSON / XML | stdlib / pandas             | Direct conversion to Markdown tables / fenced blocks              |
| EPUB          | zipfile + html parsing         | Chapter-by-chapter                                                |
| IPYNB         | nbformat                       | Code cells as fenced blocks; outputs inline                       |
| ZIP           | zipfile                        | Iterates contents; converts each member                          |
| Images        | local EXIF (exiftool)          | **Metadata only** (camera, GPS, timestamp). No LLM description.   |

**NOT supported (cloud/extra deps deliberately excluded — see Privacy Guarantees):**
- Audio transcription (Google Speech API — excluded)
- YouTube transcripts (YouTube API — excluded)
- Azure Document Intelligence layout analysis (excluded)
- LLM-generated image descriptions (excluded — `llm_client` never passed)

## Decision Tree

Choose the right tool for the job. **Read this before calling `convert_to_markdown`.**

Layout complexity genuinely ambiguous (multi-column? scanned?)? Optionally
consult the `laya_classify` tool (local, offline) with the document
statement — advisory p(yes); escalate to docling when in doubt either way.

```
Need to understand a binary/office document?
│
├─ Is it PLAIN TEXT (.md, .txt, .json, .yaml, source code)?
│  └─ YES → Use built-in Read tool. markitdown adds nothing.
│
├─ Is it a BORN-DIGITAL office doc (.docx, .pptx, .xlsx, .xls, .msg)
│  or born-digital PDF (text-selectable, not scanned)?
│  └─ YES → Use markitdown.convert_to_markdown(uri).
│           Fast (~1s/50 pages), preserves text fidelity, no cloud calls.
│
├─ Did markitdown return EMPTY / GARBAGE / missing tables (complex layout,
│  multi-column, heavy formatting)?
│  └─ YES → Escalate to docling (layout-aware — see AGENTS.md routing rule
│           + docling-mcp-skill). CLI-on-demand: detect → ask consent →
│           pip install docling → docling convert. MCP: --enable-pack docling.
│
├─ Is the PDF SCANNED / image-only (no selectable text)?
│  └─ YES → pdftoppm (bash, if available) → image-analyzer-subagent.
│           markitdown will return empty/garbage for scanned PDFs.
│
├─ Do you need STRUCTURED PDF data (forms, tables as data, fillable fields,
│   OCR-as-purpose, post-edit)?
│  └─ YES → Use pdf-specialist-skill (purpose-built for structured PDF).
│           markitdown gives best-effort text dumps only.
│
├─ Do you need VISUAL UNDERSTANDING (charts, diagrams, screenshots,
│   layout, "what does this look like")?
│  └─ YES → image-analyzer-subagent. markitdown returns text only.
│
├─ Is the document at a REMOTE URL?
│  └─ TWO OPTIONS (equivalent, pick one):
│     • webfetch first → save locally → markitdown.convert_to_markdown(file://)
│     • markitdown.convert_to_markdown(https://...) directly
│       (single requests.get(), no telemetry, equivalent to webfetch)
│
└─ None of the above → Ask the user to clarify format/intent.
```

**PDF routing note:** markitdown and `pdf-specialist-skill` overlap on `.pdf`. Use markitdown for **fast text dumps of born-digital PDFs**. Use `pdf-specialist-skill` for **structured extraction, forms, OCR-as-purpose, or editing**. When unsure, start with markitdown (cheap) and escalate to pdf-specialist-skill if the output is insufficient.

## Usage Patterns

### Large documents (50+ pages)

Pass the URI directly — markitdown handles streaming internally. Don't pre-split. If the result exceeds context, post-process with `head`/`tail`/`grep` via bash, or ask for specific page ranges.

### Table fidelity

XLSX and CSV convert cleanly to Markdown tables. Complex PDF tables (merged cells, nested headers) may need re-alignment — verify before using in critical paths.

### Multi-sheet XLSX

Output uses `## Sheet N` headers (one per sheet). When querying for a specific sheet, grep the output for the sheet name.

### Batch conversion

No batch API. Loop over URIs:
```python
results = [call_tool("convert_to_markdown", {"uri": u}) for u in uris]
```

### Following up with visual analysis

After markitdown conversion, if the document contains charts/diagrams referenced as images, follow up with `image-analyzer-subagent` on those specific elements. markitdown extracts text; it does not interpret visuals.

## Troubleshooting

### MCP not connected / tool returns "server not found"

Three gates, all required:
- `markitdown-mcp` binary on PATH (`--enable-pack markitdown` installs it)
- `mcp.servers.markitdown.disabled: false` in the deployed config
- `permissions` rule `{ "action": "markitdown*", "resource": "*", "effect": "allow" }` (last matching rule wins)

Missing any one leaves the MCP unreachable or its tools denied. Verify with `opencode mcp list` (should show `markitdown` connected) and restart opencode after config edits — there is no hot-reload.

### Tool denied after upgrading from pre-#370 deploys

Earlier releases carried the opt-in denies under a nested `permission.tool` key, which opencode's permission engine never read — so hand-enabled servers worked despite the "deny". Under v2 the denies are `permissions`-array rules and **enforce**. If you enable markitdown/docling/next-devtools by hand, make sure no later deny rule shadows your allow (last matching rule wins) — or re-run `--enable-pack <name>`.

### `markitdown-mcp: command not found`

The server binary isn't on PATH. Fix:
- Linux/macOS: run `./deploy/setup.sh` (installs via `pip install --user` from PyPI); ensure `~/.local/bin` is on PATH
- Windows: run `.\deploy\setup.ps1`; ensure `%APPDATA%\Python\Scripts` is on PATH

### Audio file / YouTube URL conversion silently contacts Google/YouTube

**This is expected, not a bug** — it is the documented residual of running upstream `markitdown[all]` (#487): an audio file input uploads to Google Speech and a YouTube URL contacts YouTube. Keep those input types away from this tool when zero egress is required; born-digital office documents remain fully local.

### Conversion times out for very large file

Split the source:
- PDF: use `pdftk` or `pdfseparate` to split into ranges, convert each
- PPTX: convert slide-by-slide if needed (no native batch)

### `convert_to_markdown` returns empty/garbage for a PDF

The PDF is likely scanned/image-only. Markitdown cannot OCR — switch to `pdftoppm` + `image-analyzer-subagent`.

## Fallback Strategy (No MCP)

When markitdown MCP is disabled, unavailable, or you choose not to enable it:

| Priority | Approach                                                            | When to use                                          |
| -------- | ------------------------------------------------------------------- | ---------------------------------------------------- |
| 1        | bash `pdftotext input.pdf -` (if installed)                          | Born-digital PDFs, fast                             |
| 2        | bash `pdftoppm` → `image-analyzer-subagent`                          | Scanned/image-only PDFs                              |
| 3        | Direct Python libs: `python-docx`, `openpyxl`, `python-pptx`         | If agent has `bash: allow` + Python + the lib         |
| 4        | `image-analyzer-subagent`                                           | Universal fallback (slower, vision-based)            |
| 5        | Tell user: "Please enable markitdown MCP for better results" + setup steps | When conversion quality matters and MCP is missing |

For company-internal docs, option 5 is preferred over option 4 (cheaper, preserves text fidelity, no vision-token cost).

## Privacy Guarantees

This MCP is the official `markitdown-mcp` from PyPI (#487) — stdio-only in our config, plugins off via `MARKITDOWN_ENABLE_PLUGINS=false`. See the upstream repo for the full trust-boundary picture.

| Guarantee                                                | Mechanism                                                              |
| -------------------------------------------------------- | ---------------------------------------------------------------------- |
| Azure converters never register                          | They require constructor kwargs (`docintelligence_endpoint` etc.) — never passed by the MCP server |
| Document conversions are fully local                     | PDF/DOCX/PPTX/XLSX/XLS/MSG/HTML/CSV/EPUB/IPYNB converters make zero network calls |
| Plugins off                                              | `MARKITDOWN_ENABLE_PLUGINS=false` in the server env (also upstream's default) |
| **Residual — audio/YouTube**                             | `markitdown[all]` ships an audio converter (uploads to Google Speech on audio input) and a YouTube converter (contacts YouTube on YouTube URLs) — feed only document formats when zero egress is required |
| No LLM image description (cloud)                         | Launcher never passes `llm_client`; image converter runs EXIF-only      |
| No plugin converters (3rd-party)                         | `enable_plugins=False` hard-coded in constructor (env var belt-and-suspenders) |
| No telemetry / Application Insights                       | Confirmed absent in markitdown source; defense-in-depth via dep exclusion |
| Version drift protection                                 | markitdown pinned `>=0.1.1,<0.2.0` — bumps require explicit audit       |
| Local file conversions                                   | Zero TCP calls (verifiable via `ss -tnp` during conversion)             |
| User-supplied `http:`/`https:` URIs                      | Single `requests.get()` — no Microsoft endpoints, no telemetry headers. Equivalent to built-in `webfetch`. |

**Safe for company-internal documents.** No data leaves the host unless the user explicitly passes an `http:`/`https:` URI (in which case the fetch is identical to what `webfetch` would do).
