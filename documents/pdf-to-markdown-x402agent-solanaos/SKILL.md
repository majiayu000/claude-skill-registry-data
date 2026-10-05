---
name: pdf-to-markdown
description: "Convert PDF documents to clean structured Markdown for LLM context. Supports two modes: fast (PyMuPDF) and accurate (IBM Docling TableFormer AI). Features aggressive persistent caching, image extraction with metadata, table detection, and batch processing. Use when asked to convert PDFs, extract PDF content, parse documents, or prepare PDF data for AI/LLM consumption."
version: 1.0.0
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["python3","uv"]},"os":["darwin","linux","windows"]}}
---

# PDF to Markdown Converter

Extract entire PDF content as clean, structured Markdown optimized for LLM context windows.

## Quick Start

```bash
# Install dependencies (fast mode)
uv pip install pymupdf pymupdf4llm

# Convert a PDF
python pdf_to_md.py document.pdf

# Accurate tables (IBM Docling AI)
uv pip install docling docling-core
python pdf_to_md.py document.pdf --docling
```

## Two Extraction Modes

### Fast Mode (default)

Uses PyMuPDF with text-based table detection. Good for most documents.

```bash
python pdf_to_md.py report.pdf
# Output: report.md (with images/ directory if PDF has images)
```

- Speed: ~0.05 sec/page
- Tables: text-strategy detection (handles borderless tables)
- Images: extracted at source resolution
- Best for: simple layouts, text-heavy docs, quick processing

### Accurate Mode (Docling)

Uses IBM's TableFormer AI model for ~93.6% table extraction accuracy.

```bash
python pdf_to_md.py report.pdf --docling
# First run downloads AI models (~2-3 min one-time setup)
```

- Speed: ~1 sec/page
- Tables: AI-powered structure detection (complex/borderless)
- Images: configurable resolution (default 4x)
- Best for: financial reports, scientific papers, complex layouts

## Persistent Caching

Extractions are cached in `~/.cache/pdf-to-markdown/`. Cache is keyed by file content hash + extraction mode — the same PDF extracts once and reuses forever.

```bash
# View cache stats
python pdf_to_md.py --cache-stats

# Clear cache for one PDF
python pdf_to_md.py document.pdf --clear-cache

# Clear entire cache
python pdf_to_md.py --clear-all-cache
```

Cache invalidates automatically when:
- Source PDF content changes (hash-based detection)
- Extractor version bumps (logic improvements)
- You explicitly clear it

## Output Format

```markdown
---
source: document.pdf
total_pages: 42
extracted_at: 2026-03-23T22:00:00
images_dir: images
---

# Document Title

Content here...

| Column A | Column B |
|----------|----------|
| data     | data     |

![Figure](images/figure_0001.png)

**[Image: figure_0001.png (1920x1080, 245.3KB)]**

---

## Extracted Images

| # | File | Dimensions | Size |
|---|------|------------|------|
| 1 | figure_0001.png | 1920x1080 | 245.3KB |
```

## Usage Patterns

### Basic Conversion

```bash
python pdf_to_md.py input.pdf                    # → input.md
python pdf_to_md.py input.pdf output.md          # custom output path
python pdf_to_md.py input.pdf --docling           # accurate tables
python pdf_to_md.py input.pdf --no-progress       # suppress progress
```

### Programmatic Usage

```python
from extractor import extract_pdf_fast, extract_pdf_docling, get_page_count

# Fast extraction
pages = get_page_count("report.pdf")
markdown = extract_pdf_fast("report.pdf", image_dir="./images")

# Accurate extraction with images
markdown, image_paths = extract_pdf_docling(
    "report.pdf",
    output_dir="./images",
    images_scale=4.0,
    show_progress=True,
)
```

### With Caching (recommended)

```python
from pdf_to_md import CacheManager, ExtractionConfig, ImageManager

cache = CacheManager()
config = ExtractionConfig(pdf_path="report.pdf", docling=False)

valid, cache_key = cache.is_valid(config)
if valid:
    result = cache.load(cache_key)
    markdown = result.markdown
else:
    # Extract and cache
    markdown = extract_pdf_fast("report.pdf")
    cache.save(cache_key, ExtractionResult(
        markdown=markdown, image_dir=None, total_pages=pages
    ), config)
```

### Batch Processing

```bash
# Convert all PDFs in a directory
for f in *.pdf; do python pdf_to_md.py "$f"; done

# Parallel with xargs
ls *.pdf | xargs -P4 -I{} python pdf_to_md.py {}
```

## Architecture

```
pdf_to_md.py          — CLI entry point, cache orchestration, output formatting
extractor.py          — Extraction backends (fast + docling)
~/.cache/pdf-to-markdown/
  └── {hash16}/
      ├── metadata.json    — source info, mtime, version
      ├── full_output.md   — cached markdown
      └── images/          — cached extracted images
```

### Key Classes

| Class | Purpose |
|-------|---------|
| `ExtractionConfig` | PDF path, mode (fast/docling), image scale |
| `ExtractionResult` | Markdown output, image dir, page count, cache flag |
| `CacheManager` | Content-hash keying, atomic writes, validation |
| `ImageManager` | Temp dir tracking, image metadata, path rewriting |

### Cache Key Generation

```
SHA256(file_size | SHA256(first_64KB + last_64KB) | mode)[:16]
```

This means:
- Same PDF content → same cache key (regardless of filename)
- Different extraction modes → different cache entries
- File renames don't invalidate cache
- Content changes always invalidate

## Dependencies

| Package | Mode | Purpose |
|---------|------|---------|
| `pymupdf` | Both | PDF parsing, image extraction |
| `pymupdf4llm` | Fast | Markdown conversion with table detection |
| `docling` | Accurate | IBM document AI pipeline |
| `docling-core` | Accurate | Document model and export |

### Install

```bash
# Fast mode only
uv pip install pymupdf pymupdf4llm

# Both modes
uv pip install pymupdf pymupdf4llm docling docling-core
```

## Image Handling

Images are extracted to an `images/` directory next to the output markdown file. References use relative paths for portability.

- Fast mode: extracts all embedded images via xref deduplication
- Docling mode: extracts figures at configurable resolution (default 4x)
- Cache preserves images and copies them to output location on cache hit
- CMYK images auto-convert to RGB

## Tips

- Use `--docling` for financial reports, academic papers, or any document with complex table layouts
- Cache stats help monitor disk usage: `--cache-stats`
- For LLM context windows, the metadata header provides page count and source info
- Page breaks use `<!-- PAGE_BREAK -->` sentinels (not `-----`) to avoid false splits
- Extractor version (`3.3.0`) is tracked in cache to auto-invalidate on upgrades
