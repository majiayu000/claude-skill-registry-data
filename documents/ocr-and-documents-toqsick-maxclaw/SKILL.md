---
name: ocr-and-documents
description: Extract text from PDFs/scans (pymupdf, marker-pdf).
version: 2.3.0
author: Hermes Agent
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: ['PDF', 'Documents', 'Research', 'Arxiv', 'Text-Extraction', 'OCR']
    related_skills: ['powerpoint']
lane: worker-flash
reasoning_effort: high
agent: Researcher
routing_hint: |
  **Agent-Scope:** Deep-research, fact-checking, paper-search, knowledge-base. Off-scope: code-building, visual design, writing — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# PDF & Document Extraction

For DOCX: use `python-docx` (parses actual document structure, far better than OCR).
For PPTX: see the `powerpoint` skill (uses `python-pptx` with full slide/notes support).
This skill covers **PDFs and scanned documents**.

## Step 1: Remote URL Available?

If the document has a URL, **always try `web_extract` first**:

```

set -euo pipefail
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

This handles PDF-to-markdown conversion via Firecrawl with no local dependencies.

Only use local extraction when: the file is local, web_extract fails, or you need batch processing.

## Step 2: Choose Local Extractor

| Feature | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **Text-based PDF** | ✅ | ✅ |
| **Scanned PDF (OCR)** | ❌ | ✅ (90+ languages) |
| **Tables** | ✅ (basic) | ✅ (high accuracy) |
| **Equations / LaTeX** | ❌ | ✅ |
| **Code blocks** | ❌ | ✅ |
| **Forms** | ❌ | ✅ |
| **Headers/footers removal** | ❌ | ✅ |
| **Reading order detection** | ❌ | ✅ |
| **Images extraction** | ✅ (embedded) | ✅ (with context) |
| **Images → text (OCR)** | ❌ | ✅ |
| **Markdown output** | ✅ (via pymupdf4llm) | ✅ (native, higher quality) |
| **EPUB** | ✅ (via pymupdf4llm→pandoc) | ✅ (via marker→pandoc) |
| **Install size** | ~25MB | ~3-5GB (PyTorch + models) |
| **Speed** | Instant | ~1-14s/page (CPU), ~0.2s/page (GPU) |

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis.

If the user needs marker capabilities but the system lacks ~5GB free disk:
> "This document needs OCR/advanced extraction (marker-pdf), which requires ~5GB for PyTorch and models. Your system has [X]GB free. Options: free up space, provide a URL so I can use web_extract, or I can try pymupdf which works for text-based PDFs but not scanned documents or equations."

---

## pymupdf (lightweight)

```bash

set -euo pipefail
pip install pymupdf pymupdf4llm
```

**Via helper script**:
```bash

set -euo pipefail
python scripts/extract_pymupdf.py document.pdf              # Plain text
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # Tables
python scripts/extract_pymupdf.py document.pdf --images out/ # Extract images
python scripts/extract_pymupdf.py document.pdf --metadata    # Title, author, pages
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # Specific pages
```

**Inline**:
```bash

set -euo pipefail
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf (high-quality OCR)

```bash

set -euo pipefail
# Check disk space first
python scripts/extract_marker.py --check

pip install marker-pdf
```

**Via helper script**:
```bash

set -euo pipefail
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # JSON with metadata
python scripts/extract_marker.py document.pdf --output_dir out/  # Save images
python scripts/extract_marker.py scanned.pdf                 # Scanned PDF (OCR)
python scripts/extract_marker.py document.pdf --use_llm      # LLM-boosted accuracy
```

**CLI** (installed with marker-pdf):
```bash

set -euo pipefail
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # Batch
```

---

## PDF → ePub Production Pipeline

For a **production-quality EPUB** (cover, TOC, e-reader CSS, MTP deployment), use the dedicated skill:

```bash

set -euo pipefail
# Load the epub-export skill and follow its workflow:
# 1. Extract to Markdown (see pymupdf section above)
# 2. Clean the Markdown (remove PDF artifacts)
# 3. pandoc with CSS + cover + TOC
# 4. Deploy via GVFS/MTP
skill_view(name='epub-export')
```

The `epub-export` skill handles: cover SVG generation, e-reader-optimized CSS (Tolino, Kobo, PocketBook), metadata (identifier, publisher, rights, description), `--split-level` strategy, MTP deployment via `gio copy`, and all the pandoc flags that differ between versions.

### Quick Start (no optimization needed)

```bash

set -euo pipefail
uv run python3 -c "
import pymupdf4llm
md = pymupdf4llm.to_markdown('input.pdf')
with open('/tmp/input.md', 'w') as f: f.write(md)
" && pandoc /tmp/input.md -o output.epub
```

### Markdown Cleaning (remove PDF layout artifacts)

PDF-generated markdown often has page numbers, footer text, and markup from bold headings:

```python
import re
def clean_pdf_md(md):
    lines = md.split("\n")
    cleaned = []
    for line in lines:
        s = line.strip()
        if re.match(r'^Seite \d+$', s): continue           # page numbers
        if re.match(r'^\*\*KAPITEL', s): continue           # chapter markers
        if 'E-Book-freundliche Ausgabe' in s: continue       # PDF ad footers
        # Clean bold-from-asterisks in headings
        h = re.match(r'^(#{1,6})\s+\*\*(.+?)\*\*\s*$', line)
        if h: cleaned.append(f"{h.group(1)} {h.group(2).strip()}"); continue
        cleaned.append(line)
    return re.sub(r'\n{4,}', '\n\n\n', "\n".join(cleaned))
```

set -euo pipefail
See `epub-export` skill for the full cleaning function including Lesefunktion headers, book-title footers, and extraction typo fixes.

---

## Arxiv Papers

```
# Abstract only (fast)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# Search
web_search(query="arxiv GRPO reinforcement learning 2026")
```

set -euo pipefail
## Split, Merge & Search

pymupdf handles these natively — use `execute_code` or inline Python:

```python
# Split: extract pages 1-5 to a new PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

set -euo pipefail
```python
# Merge multiple PDFs
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

set -euo pipefail
```python
# Search for text across all pages
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

No extra dependencies needed — pymupdf covers split, merge, search, and text extraction in one package.

---

## Notes

- `web_extract` is always first choice for URLs
- pymupdf is the safe default — instant, no models, works everywhere
- marker-pdf is for OCR, scanned docs, equations, complex layouts — install only when needed
- Both helper scripts accept `--help` for full usage
- marker-pdf downloads ~2.5GB of models to `~/.cache/huggingface/` on first use
- For Word docs: `pip install python-docx` (better than OCR — parses actual structure)
- For PowerPoint: see the `powerpoint` skill (uses python-pptx)
