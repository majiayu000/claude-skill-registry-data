---
name: pypdf
description: Manipulate PDF documents programmatically. Merge, split, rotate, and
  watermark PDFs. Extract text and metadata. Handle form filling and encryption/decryption.
version: 1.0.0
category: data
type: skill
capabilities:
- pdf_merging
- pdf_splitting
- page_rotation
- watermarking
- text_extraction
- metadata_handling
- form_filling
- encryption_decryption
tools:
- python
- pypdf
- reportlab
tags:
- pdf
- document-manipulation
- merge
- split
- watermark
- encryption
- office-automation
platforms:
- windows
- macos
- linux
related_skills:
- python-docx
requires: []
scripts_exempt: true
---

# Pypdf

## Overview

PyPDF is a pure-Python library for working with PDF files. This skill covers comprehensive patterns for PDF manipulation including:

- **PDF merging** - Combine multiple PDFs into one document
- **PDF splitting** - Extract specific pages or split into multiple files
- **Page rotation** - Rotate pages by 90, 180, or 270 degrees
- **Watermarking** - Add text or image watermarks to pages
- **Text extraction** - Extract text content from PDF pages
- **Metadata handling** - Read and modify PDF metadata
- **Form filling** - Fill PDF form fields programmatically
- **Encryption/Decryption** - Secure PDFs with passwords

## When to Use This Skill

### USE when:

- Merging multiple PDF files into a single document
- Splitting large PDFs into smaller files
- Extracting specific pages from PDFs
- Adding watermarks or stamps to documents
- Extracting text content for analysis
- Reading or modifying PDF metadata
- Filling PDF forms programmatically
- Encrypting or decrypting PDF files
- Adding page numbers or headers/footers
- Rotating or reordering pages
- Automating PDF workflows in pipelines
### DON'T USE when:

- Creating PDFs from scratch (use reportlab or weasyprint)
- Need advanced text layout control (use reportlab)
- Converting other formats to PDF (use dedicated converters)
- Need OCR for scanned documents (use pytesseract + pdf2image)
- Working with complex form creation (use reportlab)
- Need to edit existing text content (limited support)

## Prerequisites

### Installation

```bash
# Basic installation
pip install pypdf

# Using uv (recommended)
uv pip install pypdf

# With crypto support for encryption
pip install pypdf[crypto]


*See sub-skills for full details.*
### Verify Installation

```python
from pypdf import PdfReader, PdfWriter, PdfMerger
from pypdf.errors import PdfReadError

print("pypdf installed successfully!")
print(f"Version: {pypdf.__version__}")
```

## Version History

### 1.0.0 (2026-01-17)

- Initial skill creation
- Core capabilities documentation
- 6 complete code examples
- Batch processing patterns
- Encryption and form handling

## Resources

- **Official Documentation**: https://pypdf.readthedocs.io/
- **GitHub Repository**: https://github.com/py-pdf/pypdf
- **PyPI Package**: https://pypi.org/project/pypdf/
- **Migration from PyPDF2**: https://pypdf.readthedocs.io/en/latest/migration.html

## Related Skills

- **reportlab** - PDF creation from scratch
- **python-docx** - Word document handling
- **pillow** - Image processing for PDF images
- **pdf2image** - Convert PDF pages to images

---

*This skill provides comprehensive patterns for PDF manipulation refined from production document processing systems.*

## Sub-Skills

- [1. PDF Merging](1-pdf-merging/SKILL.md)
- [2. PDF Splitting](2-pdf-splitting/SKILL.md)
- [3. Page Rotation and Transformation](3-page-rotation-and-transformation/SKILL.md)
- [4. Watermarking and Stamping](4-watermarking-and-stamping/SKILL.md)
- [5. Text Extraction and Metadata](5-text-extraction-and-metadata/SKILL.md)
- [6. Encryption and Form Filling](6-encryption-and-form-filling/SKILL.md)
- [Batch PDF Processing Pipeline](batch-pdf-processing-pipeline/SKILL.md)
- [1. Memory Management (+2)](1-memory-management/SKILL.md)
- [Common Issues](common-issues/SKILL.md)
