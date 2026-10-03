---
name: mistral-pdf-to-markdown
description: Convert PDFs to Markdown with Mistral OCR and extracted images. Use for scanned PDFs or complex layouts where structured text or images matter.
user-invocable: true
---

# Mistral PDF to Markdown Converter

Convert PDF documents to Markdown via Mistral's OCR API, preserving headers and structure and extracting embedded images. OCR makes it work on scanned, image-based PDFs.

## Quick Start

`<skill-dir>` in the commands below is the directory containing this `SKILL.md` — substitute the real path.

```bash
# Convert entire PDF
uv run --script <skill-dir>/scripts/convert_pdf_to_markdown.py input.pdf output.md

# Convert specific pages
uv run --script <skill-dir>/scripts/convert_pdf_to_markdown.py input.pdf output.md --pages "1-5"
uv run --script <skill-dir>/scripts/convert_pdf_to_markdown.py input.pdf output.md --pages "1,3,5"
```

## Output Structure

Each conversion is a self-contained folder. Passing `Output/PDFConversions/paper_alpha.md` creates `Output/PDFConversions/paper_alpha/paper_alpha.md`, with extracted images beside it under `images/` as JPEGs, referenced relatively:

```
Output/PDFConversions/
├── paper_alpha/
│   ├── paper_alpha.md   # references images/img-N.jpeg
│   └── images/
│       ├── img-0.jpeg
│       └── img-1.jpeg
└── paper_beta/
    ├── paper_beta.md
    └── images/
        ├── img-0.jpeg
        └── ...
```

An existing foldered markdown path such as `Output/PDFConversions/paper_alpha/paper_alpha.md` is kept as given. A directory creates `<directory>/<input-pdf-stem>.md`.

## Usage in Code

```python
from pathlib import Path
import subprocess

# Run conversion script
result = subprocess.run([
    "uv", "run", "--script",
    "<skill-dir>/scripts/convert_pdf_to_markdown.py",
    "input.pdf",
    "Output/PDFConversions/output.md",
    "--pages", "1-10"
], capture_output=True, text=True)

print(result.stdout)
```

## Requirements

A Mistral API key (below), plus `mistralai`, `python-dotenv`, `pypdf`, and `pyyaml` — declared inline in the script's PEP 723 header.

## API Key Setup

The script checks these locations in order (first match wins):

1. **Environment variable** `MISTRAL_API_KEY` — recommended for personal use (e.g. `export MISTRAL_API_KEY=your-key` in `secrets.sh`)
2. **Shared config** — `.claude/agent-contract.yaml` or `~/.config/agent-contract/config.yaml` under `paper-reader.mistral_api_key`
3. **`Notes/.env`** — add `MISTRAL_API_KEY=your-key`; gitignored but Dropbox-synced, so it travels with a shared project folder

> **Never commit API keys to git.** Use environment variables or Dropbox-synced `Notes/.env` instead.

## Error Handling

**API Key Not Found:**
```
Error: Mistral API key not found
```
→ Configure it per **API Key Setup** above

**Page Out of Range:**
```
Warning: Page 100 out of range, skipping
```
→ Check the PDF page count and adjust the page selection

**API Rate Limit:**
→ Retry after a moment, or reduce the page count per request

## Notes

- Large PDFs take longer — API limits apply. Narrow with `--pages`.
- Use the `pdf` skill instead for local manipulation and plain text extraction with no OCR or API calls.
- Load [`references/reference.md`](references/reference.md) for the OCR API surface, programmatic and batch usage, cost, and troubleshooting.
