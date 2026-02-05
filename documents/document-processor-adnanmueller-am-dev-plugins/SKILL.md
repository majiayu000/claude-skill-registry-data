---
name: document-processor
description: |
  Extract and process content from PDFs and DOCX files. Handles large files, OCR for scanned documents, page splitting, and markdown conversion. Use when: (1) Processing PDF references in notes, (2) Extracting text from large documents for analysis, (3) Converting DOCX to markdown, (4) Handling scanned/image PDFs with OCR, (5) Integrating with Obsidian or note-taking workflows, (6) Splitting large documents into manageable chunks.

  Invoke with: /process-document, /extract-pdf, /extract-docx, or say "use document-processor skill to..."
---

# Document Processor

Extract content from PDFs and DOCX files for analysis, summarization, and note integration.

## Design Philosophy

### The Large File Problem

Claude can read PDFs directly, but large files (>5MB) often fail or timeout. This skill provides extraction scripts that handle files of any size by processing page-by-page and optionally splitting output into chunks.

### Extract First, Summarize Second

The Python scripts focus on extraction quality, not summarization. They produce clean text output that Claude can then analyze, summarize, or integrate into notes. This separation means extraction is deterministic and repeatable.

### Progressive Enhancement

The tools work with minimal dependencies (pure Python) but support enhanced extraction when additional tools are installed:
- **Base**: `pypdf` + `python-docx` (always works)
- **Better PDF**: `pdftotext` via poppler (better text extraction)
- **OCR**: `tesseract` + `pytesseract` (scanned documents)

### Format Preservation

DOCX conversion to markdown preserves document structure: headings become `#`, bold becomes `**`, tables become markdown tables. This makes extracted content immediately useful in markdown-based note systems.

---

## Anti-Patterns: What to Avoid

### The Direct Read Timeout
**Symptom:** Trying to read a 50MB PDF directly with Claude's Read tool.
**Problem:** Large files timeout or consume excessive context.
**Solution:** Use `extract_pdf.py` to process the file, then read the extracted text.

### The OCR Assumption
**Symptom:** Running OCR on every PDF.
**Problem:** OCR is slow and OCR dependencies are heavy.
**Solution:** Only use `--ocr` flag when standard extraction returns minimal text.

### The Full Document Dump
**Symptom:** Extracting 500 pages and asking Claude to summarize all of it.
**Problem:** Context overflow, poor summaries.
**Solution:** Use `--split 50` to process in chunks, summarize each chunk, then synthesize.

### The Missing Dependency Loop
**Symptom:** User tries to use OCR but hasn't installed tesseract.
**Problem:** Confusing errors, wasted time.
**Solution:** Scripts detect missing dependencies and provide clear install instructions.

---

## Quick Start

### Check File Size First

Before processing, check file size to choose the right strategy:

```bash
ls -lh document.pdf
```

| Size | Strategy |
|------|----------|
| < 5MB | Try Claude's Read tool first |
| 5-20MB | Use extraction scripts |
| > 20MB | Use extraction scripts with `--split` |

### Basic Extraction

```bash
# PDF extraction
python scripts/extract_pdf.py --file document.pdf

# DOCX to markdown
python scripts/extract_docx.py --file document.docx --markdown
```

---

## PDF Processing Workflow

### Step 1: Assess the PDF

```bash
# Check file size and type
ls -lh document.pdf

# Quick metadata check
python scripts/extract_pdf.py --file document.pdf --metadata-only
```

### Step 2: Extract Content

**For text-based PDFs:**
```bash
python scripts/extract_pdf.py --file document.pdf
```

**For scanned/image PDFs:**
```bash
# First, try normal extraction
python scripts/extract_pdf.py --file document.pdf

# If little text extracted, use OCR
python scripts/extract_pdf.py --file document.pdf --ocr
```

### Step 3: Handle Large Documents

For documents > 50 pages, split into chunks:

```bash
# Split into 50-page chunks
python scripts/extract_pdf.py --file large.pdf --split 50
```

### Step 4: Extract Specific Pages

```bash
# Single page
python scripts/extract_pdf.py --file document.pdf --page 5

# Page range
python scripts/extract_pdf.py --file document.pdf --pages 1-10

# Specific pages
python scripts/extract_pdf.py --file document.pdf --pages 1,5,10,15
```

---

## DOCX Processing Workflow

### Step 1: Basic Extraction

```bash
# Plain text
python scripts/extract_docx.py --file document.docx

# As markdown (preserves structure)
python scripts/extract_docx.py --file document.docx --markdown
```

### Step 2: Extract with Images

```bash
# Extract text and save images
python scripts/extract_docx.py --file document.docx --markdown --extract-images --output-dir ./images/
```

### Step 3: Metadata Only

```bash
python scripts/extract_docx.py --file document.docx --metadata-only
```

---

## Obsidian Integration

### Processing PDF References in Notes

When a note contains PDF references like `[[document.pdf]]` or `[Report](attachments/report.pdf)`:

1. Identify the PDF path
2. Check file size
3. Extract content using appropriate strategy
4. Insert summary below the reference

**Output format:**

```markdown
> **PDF Summary: [Document Title]**
> **Pages:** [count] | **Type:** [article/manual/report]
>
> **Overview:** [2-3 sentence summary]
>
> **Key Sections:**
> - [Section 1]: [brief description]
> - [Section 2]: [brief description]
>
> <details>
> <summary>Extracted Content</summary>
>
> [Page-by-page text content]
>
> </details>
```

### Processing DOCX References

For `[[document.docx]]` or `[Document](path/to/file.docx)`:

1. Extract as markdown
2. Optionally extract images to attachments folder
3. Insert content or summary

---

## Script Reference

### extract_pdf.py

| Flag | Description |
|------|-------------|
| `--file`, `-f` | PDF file to extract (required) |
| `--ocr` | Use OCR for scanned documents |
| `--use-pdftotext` | Use pdftotext instead of pypdf |
| `--split N`, `-s N` | Split into chunks of N pages |
| `--page N`, `-p N` | Extract only page N |
| `--pages RANGE` | Extract page range (e.g., 1-10 or 1,3,5) |
| `--metadata-only`, `-m` | Extract only metadata |
| `--json`, `-j` | Output as JSON |

### extract_docx.py

| Flag | Description |
|------|-------------|
| `--file`, `-f` | DOCX file to extract (required) |
| `--markdown`, `-md` | Convert to markdown format |
| `--extract-images`, `-i` | Extract embedded images |
| `--output-dir`, `-o` | Directory for extracted images |
| `--metadata-only`, `-m` | Extract only metadata |
| `--json`, `-j` | Output as JSON |

---

## Dependency Installation

### Core Dependencies (Required)

```bash
pip install pypdf python-docx
```

Or using the requirements file:

```bash
pip install -r scripts/requirements.txt
```

### Enhanced PDF Extraction (Optional)

```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt install poppler-utils
```

### OCR Support (Optional)

```bash
# macOS
brew install tesseract poppler

# Python packages
pip install pytesseract pdf2image Pillow
```

---

## JSON Output Mode

For programmatic use, both scripts support JSON output:

```bash
# PDF
python scripts/extract_pdf.py --file document.pdf --json > output.json

# DOCX
python scripts/extract_docx.py --file document.docx --json > output.json
```

JSON schema includes:
- `success`: boolean
- `file_path`: string
- `metadata`: object with document properties
- `pages` or `content`: extracted text
- `error`: string (if failed)

---

## Troubleshooting

### "pypdf not installed"
```bash
pip install pypdf
```

### "python-docx not installed"
```bash
pip install python-docx
```

### "tesseract not installed" (for OCR)
```bash
brew install tesseract  # macOS
sudo apt install tesseract-ocr  # Ubuntu
```

### "Very little text extracted"
The PDF may be scanned/image-based. Try:
```bash
python scripts/extract_pdf.py --file document.pdf --ocr
```

### "File too large for Claude to read"
Use extraction scripts instead of Read tool:
```bash
python scripts/extract_pdf.py --file large.pdf --split 50
```

---

## Examples

### Example 1: Process Research Paper

```bash
# Extract with page numbers
python scripts/extract_pdf.py --file research-paper.pdf

# Get just abstract and intro (pages 1-3)
python scripts/extract_pdf.py --file research-paper.pdf --pages 1-3
```

### Example 2: Convert Contract to Markdown

```bash
# Full conversion with structure preserved
python scripts/extract_docx.py --file contract.docx --markdown > contract.md
```

### Example 3: Process Scanned Receipt

```bash
# OCR extraction
python scripts/extract_pdf.py --file receipt.pdf --ocr --json
```

### Example 4: Batch Process Directory

```bash
# Process all PDFs in a directory
for f in *.pdf; do
  python scripts/extract_pdf.py --file "$f" --json > "${f%.pdf}.json"
done
```
