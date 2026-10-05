---
name: pdf
description: "Comprehensive PDF manipulation toolkit. For batch/bulk extraction (1K+\
  \ PDFs), use pdftotext (poppler) via subprocess \u2014 fastest and most reliable\
  \ at scale. For single-document understanding, OpenAI Codex PDF-to-Markdown gives\
  \ best results. Also supports text/table extraction, PDF creation, merging/splitting,\
  \ and forms."
type: reference
version: 1.2.2
last_updated: 2026-01-04
category: data
related_skills:
- pdf-text-extractor
- document-rag-pipeline
- knowledge-base-builder
capabilities: []
requires: []
see_also:
- pdf-pdftotext-poppler
tags: []
freedom: medium
---

# Pdf

## Overview

This skill enables comprehensive PDF operations through Python libraries and command-line tools. Use it for reading, creating, modifying, and analyzing PDF documents.

## Quick Start

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
for page in reader.pages:
    text = page.extract_text()
    print(text)
```

## Tool Selection (WRK-1277 + WRK-1302 + WRK-1303 Learnings)

### Scenario → Tool Mapping

| Scenario | Tool | Why |
|----------|------|-----|
| Batch extraction (1K+ PDFs) | **pdftotext (poppler)** via subprocess | Proven at 297K scale; reliable timeout via SIGTERM; subprocess isolation |
| Single-doc understanding | **OpenAI Codex** PDF→Markdown | Best quality; too expensive for bulk |
| Single-doc text extraction | **PyMuPDF (fitz)** | Fast, good API, in-process |
| Readability classification | **pypdfium2** | Replaces pdfplumber for page sampling; no D-state hangs; Apache-2.0 license |
| Table extraction | **pdfplumber** (single doc only) | Best table detection; DO NOT use in multiprocessing pools |
| Structured markdown (tables+equations) | **Docling** (targeted use only) | MIT license; 1731 table rows from 6 docs; ~310s/doc on CPU |
| LLM/RAG markdown | **pymupdf4llm** (monitor only) | 0.12s/doc, good markdown; **AGPL license blocks adoption** |

### Quality & Completeness Index (measured on dev-primary)

Scores: text completeness (% of content captured vs best-in-class), structure
preservation, and batch viability. Based on WRK-1302 (243 PDFs) and WRK-1303 (6 PDFs).

| Tool | Text Completeness | Structure | Tables | Equations | Speed | Batch Safe | License |
|------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **pdftotext** (baseline) | 100% | none | none | unicode only | 0.02s | yes | GPL-2 |
| **pypdfium2** | 86% | none | none | unicode only | 0.02s | no (thread-unsafe) | Apache-2.0 |
| **pdfplumber** | ~95% | partial | good (69-93%) | none | 0.10s | no (D-state) | MIT |
| **Docling** | 117% | full (md) | good (md rows) | unicode+context | 310s | no (CPU bound) | MIT |
| **PyMuPDF (fitz)** | ~98% | partial | basic | unicode only | 0.01s | yes | AGPL |
| **pymupdf4llm** | ~100% | full (md) | good (md) | unicode+context | 0.12s | untested | AGPL |
| **Codex API** | ~100% | full (md) | excellent | LaTeX | ~2s | no (API cost) | proprietary |

**Column definitions:**
- **Text Completeness**: chars extracted vs pdftotext baseline (WRK-1302: 243 PDFs, WRK-1303: 6 PDFs)
- **Structure**: none = raw text | partial = some layout | full = headings, lists, sections
- **Tables**: none | basic = cell text only | good = rows+cols preserved | excellent = multi-span
- **Equations**: unicode only = captures symbols | unicode+context = in structured output | LaTeX = formula markup
- **Batch Safe**: can run in ProcessPoolExecutor on NFS/NTFS without hangs or crashes

> **WARNING**: pdfplumber hangs in kernel D-state (disk sleep) on NTFS and NFS mounts.
> SIGALRM cannot interrupt kernel I/O. Use pdftotext via `subprocess.run(timeout=N)` for
> any batch/parallel work — the subprocess can be killed reliably on timeout.

> **Benchmarks**: `scripts/data/doc_intelligence/benchmark_pdf_tools.py` (WRK-1302),
> `scripts/data/doc_intelligence/benchmark_docling.py` (WRK-1303)

## When to Use

- **Batch PDF processing** - Use pdftotext (poppler) via subprocess for bulk extraction
- **Converting PDFs to Markdown** - Use OpenAI Codex for intelligent conversion (single docs)
- Extracting text and metadata from PDF files
- Merging multiple PDFs into a single document
- Splitting large PDFs into individual pages
- Adding watermarks or annotations to PDFs
- Password-protecting or decrypting PDFs
- Extracting images from PDF documents
- OCR processing for scanned documents
- Creating new PDFs with reportlab
- Extracting tables from structured PDFs

## Showing PDF Evidence to the User

When a user asks to "open" or "show" a PDF, prefer direct display, but verify rendering:

1. Try opening the PDF in the browser/viewer using its absolute `file://` path.
2. If the browser PDF viewer renders blank or cannot show the page, convert the relevant page(s) to images with Poppler and return `MEDIA:` links:

```bash
mkdir -p /tmp/pdf-pages
pdftoppm -f 1 -l 1 -png -singlefile "$PDF" /tmp/pdf-pages/document_page_01
pdftoppm -f "$PAGE" -l "$PAGE" -png -singlefile "$PDF" /tmp/pdf-pages/document_page_${PAGE}
file /tmp/pdf-pages/document_page_01.png /tmp/pdf-pages/document_page_${PAGE}.png
```

3. For evidence questions, render both the cover/first page and the controlling clause page so the user can visually verify document identity and operative text.
4. If visual inspection is needed, run image analysis on the rendered page and confirm the visible section/page before reporting.


## Version History

- **1.2.2** (2026-01-04): Fixed P2 issue - added `parents=True` to all `mkdir()` calls to handle nested output paths; prevents FileNotFoundError when creating directories with non-existent parent paths
- **1.2.1** (2026-01-04): Fixed CLI tool missing imports - added complete standalone script with all required imports (openai, pypdf, logging) and function definitions; resolved P1 issue from Codex review
- **1.2.0** (2026-01-04): **MAJOR UPDATE** - Added OpenAI Codex integration for PDF-to-Markdown conversion as recommended first step for all PDF processing; includes batch conversion, chunking for large files, cost-effective options, and complete CLI tool
- **1.1.0** (2026-01-02): Added Quick Start, When to Use, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.0.0** (2024-10-15): Initial release with pypdf, pdfplumber, reportlab, CLI tools

## Sub-Skills

- [Why Convert to Markdown First?](why-convert-to-markdown-first/SKILL.md)
- [OpenAI Codex Conversion](openai-codex-conversion/SKILL.md)
- [pypdf - Core PDF Operations (+2)](pypdf-core-pdf-operations/SKILL.md)
- [pdftotext (Poppler) (+2)](pdftotext-poppler/SKILL.md)
- [Why Use PDF-Large-Reader? (+8)](why-use-pdf-large-reader/SKILL.md)
- [OCR for Scanned Documents (+3)](ocr-for-scanned-documents/SKILL.md)
- [Execution Checklist](execution-checklist/SKILL.md)
- [Common Errors](common-errors/SKILL.md)
- [Metrics](metrics/SKILL.md)
- [Quick Reference](quick-reference/SKILL.md)
- [Dependencies](dependencies/SKILL.md)
