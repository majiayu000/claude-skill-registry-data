---
name: to-md
description: "Use when the user needs to convert files (PDF, DOCX, PPTX, XLSX, HTML, images, audio, ZIP) to structured Markdown via MarkItDown. Suitable for text extraction, RAG ingestion, or format normalization. NOT for document editing — use docx or pptx skills instead."
---

# To Markdown

This skill defines the unified policy for converting files to structured Markdown without summarizing or altering the original content. Prefer Microsoft's **MarkItDown** Python package when a Python interpreter is available.

## Skill routing

| Task | Use this skill | NOT |
|------|----------------|-----|
| Single-file text extraction | **to-md** | docx, pptx, workspace-indexer |
| Workspace batch conversion + index.md | **workspace-indexer** | to-md directly |
| DOCX tracked-changes review | **docx** (pandoc) | to-md |
| DOCX/PPTX creation or editing | **docx** / **pptx** | to-md |

## Supported formats

- **Documents**: PDF (.pdf), Word (.docx), PowerPoint (.pptx), Excel (.xlsx)
- **Data & Web**: HTML, CSV, JSON, XML
- **Media**: Images (EXIF metadata and OCR), Audio (speech transcription)
- **Archives**: ZIP files

## Dependency check

Run these checks **in order**. Do not start a long package-install loop before confirming an interpreter exists.

### 1. Locate a Python interpreter

```bash
command -v python3 || command -v python
```

PowerShell: `Get-Command python3, python -ErrorAction SilentlyContinue`

If neither exists, go to **step 4** (system extractors) or install a Python runtime with the environment’s package manager (`apt`, `brew`, etc.) **only when that is clearly allowed and quick**. Prefer `python3` once available.

### 2. Confirm MarkItDown (or install it)

Use the interpreter and matching pip module — do not assume bare `pip`/`pip3` are on `PATH`:

```bash
PY="$(command -v python3 || command -v python)"
"$PY" -c "import markitdown" 2>/dev/null || "$PY" -m pip install "markitdown[all]"
```

PowerShell:

```powershell
$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py) { throw "No Python interpreter on PATH" }
& $py.Source -c "import markitdown" 2>$null
if ($LASTEXITCODE -ne 0) { & $py.Source -m pip install "markitdown[all]" }
```

If pip install fails (no network, managed environment, missing pip), go to **step 4**. Do not invent file contents.

### 3. Convert with MarkItDown

When import succeeds, use the MarkItDown CLI or Python API for all supported formats. See [references/conversion_guide.md](references/conversion_guide.md).

### 4. Fallback when MarkItDown cannot run

If there is no usable Python/MarkItDown path, extract text with **already-installed** system CLIs only — do not invent bytes, and do not spend the session installing large OCR/Python stacks unless the user explicitly needs MarkItDown features:

| Format | Prefer (if present) |
|--------|---------------------|
| PDF (text layer) | `pdftotext` |
| Images / scanned PDF | `tesseract` |
| HTML | read the file directly or a simple HTML-to-text filter already on the system |
| DOCX/PPTX/XLSX | report that MarkItDown is required, or follow the specialized **docx** / **pptx** skill when applicable |

After extraction, write Markdown that preserves the extracted text; do not summarize or hallucinate missing content.

## Conversion workflow

Prefer MarkItDown when step 2 succeeds. Otherwise use step 4 and state which extractor produced the text.

## Core execution principles

1. **Prefer MarkItDown** for file-to-Markdown when Python is available. Do not parse Office/PDF binaries with ad-hoc Python libraries (PyMuPDF, python-docx, python-pptx, openpyxl) or legacy Pandoc for plain reading unless a specialized skill requires it (e.g. DOCX tracked changes in **docx**).
2. **Preserve original text**: Do not hallucinate, summarize, or alter extracted text. Rely strictly on parser/OCR output.
3. **Structure & readability**: Prefer MarkItDown’s structure (headings, tables, lists) when available; fallback output may be flatter plain text wrapped as Markdown.
4. **Fail fast on environment gaps**: Missing `python`/`pip` is not a signal to retry the same install recipe. Preflight, then fallback or install the interpreter once.
