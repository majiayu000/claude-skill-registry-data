---
name: mineru-file-processing
description: Extract text, tables, formulas, or structure and run OCR on PDFs, images, and Office documents when the task needs document parsing.
---

# MinerU File Processing

## Overview

Use local reading when it provides the needed content. When external parsing is appropriate and authorized, choose MinerU lightweight for small files or precise for larger, OCR, batch, or structured extraction. Check permission at the external-transfer boundary for confidential or nonpublic material, and resolve any unapproved cost; reuse that decision throughout the same parsing job. Having a token alone does not authorize an upload.

Deliver the requested extracted content or answer. Keep parsing diagnostics and editorial boundaries in native comments when useful; if the output format has no comments, put them in the conversation rather than the extracted text. Preserve source content without adding compliance statements or routine warnings.

## Supported Files

- PDF
- Images: `png`, `jpg`, `jpeg`, `jp2`, `webp`, `gif`, `bmp`
- Word: `doc`, `docx`
- PowerPoint: `ppt`, `pptx`
- Excel: `xls`, `xlsx`
- HTML is supported by the precise API with `model_version: "MinerU-HTML"`

Lightweight is suitable for a single small file when local reading is insufficient. The documented lightweight formats include PDF, images, `docx`, `pptx`, and `xlsx`; URL mode may also accept `doc` and `ppt`. If the service rejects the format or limits, switch to an available precise route within the same authorized scope; ask only if that changes cost or data-transfer authorization.

## Routing Rules

| Situation | Default action |
|---|---|
| Small supported file, ≤10MB and ≤20 pages | Read locally first; use lightweight if external parsing is needed and authorized |
| Image the current model can read | Read it directly |
| Batch, larger files, OCR, high accuracy, or structured exports | Use an available precise route within approved scope |
| User specifies a parsing service or method | Use that method when supported; resolve a concrete blocker if unavailable |
| Unsupported file or no usable source | Try a supported local conversion or ask for the missing source |

Small file means a single file within the lightweight API limits: ≤10MB and ≤20 pages. The precise API supports files up to 200MB, 200 pages, and batches up to 200 files.

## API Choice

### ⚡ Agent Lightweight Parse API

Use for small single files in normal agent workflows.

- Token: not required
- Limits: ≤10MB, ≤20 pages, single file only
- No `Authorization` header
- Output: Markdown CDN link
- Endpoints:
  - URL input: `https://mineru.net/api/v1/agent/parse/url`
  - File input: `https://mineru.net/api/v1/agent/parse/file`
- Flow: submit task, then poll result

### 🎯 Precise Parse API

Use when accuracy, OCR, tables, formulas, layout, structured output, batch work, or larger files matter.

- Token: required
- Header: `Authorization: Bearer $MINERU_API_TOKEN`
- Single-file endpoint: `https://mineru.net/api/v4/extract/task`
- Batch URL endpoint: `https://mineru.net/api/v4/file-urls/batch`
- Limits: ≤200MB, ≤200 pages, batch ≤200 files
- Default model: use `vlm` unless a reason exists to use `pipeline` or `MinerU-HTML`
- Default exports: Markdown and JSON
- Optional `extra_formats`: `docx`, `html`, `latex`

## Token Configuration

Do not hardcode the token in skill files, prompts, source code, or logs.

Generate the token in MinerU's API management page, then expose it as an environment variable:

```bash
export MINERU_API_TOKEN="your-token-here"
```

For persistent shell config, prefer fish universal variable because the user uses fish:

```fish
set -Ux MINERU_API_TOKEN "your-token-here"
```

A plain `export MINERU_API_TOKEN=...` is session-only unless placed in shell startup files.

For agent launches that do not inherit the interactive shell environment, use the local config file:

```bash
# file: ~/.config/mineru/env
MINERU_API_TOKEN=your-token-here
```

Before calling the precise API from shell commands, load it without printing the secret:

```bash
set -a
source ~/.config/mineru/env
set +a
```

For a project, prefer `.env` or the project secret manager:

```env
MINERU_API_TOKEN=your-token-here
```

## Precise API Request Defaults

For PDF, Office, Excel, and images:

```json
{
  "url": "https://example.com/file.pdf",
  "model_version": "vlm",
  "is_ocr": false,
  "enable_formula": true,
  "enable_table": true,
  "language": "ch"
}
```

Use `is_ocr: true` for scans, screenshots, image-only PDFs, or when text extraction is poor.

Use `extra_formats` only when the user needs those files:

```json
{
  "extra_formats": ["docx", "html", "latex"]
}
```

For HTML input:

```json
{
  "url": "https://example.com/page.html",
  "model_version": "MinerU-HTML"
}
```

## cURL Example

```bash
curl --location --request POST 'https://mineru.net/api/v4/extract/task' \
  --header "Authorization: Bearer $MINERU_API_TOKEN" \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "url": "https://cdn-mineru.openxlab.org.cn/demo/example.pdf",
    "model_version": "vlm",
    "enable_formula": true,
    "enable_table": true,
    "language": "ch"
  }'
```

## Missing decisions

Ask only for the missing permission, cost approval, credential setup, or usable source that blocks the selected route. Do not request credentials in chat. Once a route is approved, polling, parsing its result, and passing normalized records to subsequent local steps need no repeated approval.

## Common Mistakes

- Do not use the token-based precise API for a small single file unless precision or structured output matters.
- Apply external-transfer authorization to either API; file size does not determine confidentiality.
- Do not send images to MinerU when the active model can directly read images and the user only needs visual understanding.
- Do not hardcode or print `MINERU_API_TOKEN`.
- Do not claim parsing succeeded until the async task result has been polled and the output link or parsed content exists.
