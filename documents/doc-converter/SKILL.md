---
name: doc-converter
description: "Convert documents between PDF, DOCX and Markdown (PDF to Markdown, DOCX to Markdown, Markdown to PDF, Markdown to DOCX), preserving structure, tables and code. Use to turn a PDF or Word file into clean markdown, or markdown notes into a downloadable PDF or Word document."
---

# Document Format Converter

Convert documents between PDF, DOCX, and Markdown formats while preserving structure, tables, code blocks, and formatting.

## Workflow Decision Tree

### Input → Markdown
| Source | Method |
|--------|--------|
| PDF (text-based) | `pdfplumber` for text extraction, manual markdown formatting |
| PDF (scanned/image) | `pytesseract` OCR → markdown formatting |
| DOCX | `pandoc` conversion with post-processing |

### Markdown → Output
| Target | Method |
|--------|--------|
| PDF | `pandoc` with PDF engine or Python `reportlab` |
| DOCX | `pandoc` direct conversion |
## Conversion recipes

Read the recipe for the conversion at hand before starting. Each holds the code, options and pitfalls.

- **PDF to Markdown** (text-based `pdfplumber`, scanned OCR): `references/pdf-to-markdown.md`
- **DOCX to Markdown** (`pandoc`, tracked changes): `references/docx-to-markdown.md`
- **Markdown to PDF** (`pandoc`/LaTeX, styling, TOC, `reportlab`): `references/markdown-to-pdf.md`
- **Markdown to DOCX** (`pandoc`, reference doc, `python-docx`): `references/markdown-to-docx.md`

## Complete Conversion Workflow

For complex documents, follow this workflow:

1. **Analyze source document**: Identify structure (headings, tables, code, images)
2. **Choose conversion method**: Select based on source format and quality
3. **Extract content**: Use appropriate tool for source format
4. **Clean and format**: Apply post-processing to fix artifacts
5. **Validate output**: Verify structure, tables, and formatting preserved
6. **Save to outputs**: Place final file in `/mnt/user-data/outputs/`

## Dependencies

```bash
# PDF processing
pip install pdfplumber pypdf reportlab --break-system-packages

# OCR for scanned PDFs
pip install pytesseract pdf2image --break-system-packages
sudo apt-get install -y tesseract-ocr poppler-utils

# DOCX processing
pip install python-docx --break-system-packages

# Pandoc (for all conversions)
sudo apt-get install -y pandoc

# LaTeX for PDF generation via pandoc
sudo apt-get install -y texlive-xetex texlive-fonts-recommended
```

## Quality Checklist

Before delivering converted document:

- [ ] Headings properly formatted with correct hierarchy
- [ ] Tables converted with proper alignment
- [ ] Code blocks preserved with syntax indication
- [ ] Lists (bulleted/numbered) properly formatted
- [ ] Bold/italic/code formatting preserved
- [ ] Page breaks handled appropriately
- [ ] Images extracted/referenced (if applicable)
- [ ] No conversion artifacts or garbage characters
