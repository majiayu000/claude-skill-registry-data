---
name: evo-pdf-context-extractor
description: Extracts text from PDF files using pypdf 5.x. Use when you need to read PDF documents to understand background context, column definitions, and scoring rules for data analysis tasks.
---

# PDF Context Extractor

Extracts text content from PDF files using pypdf 5.x (PdfReader API).

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-context-extractor/scripts')
from utils import extract_pdf_text, get_all_pages_text

# Get all text from a PDF
text = extract_pdf_text('/path/to/file.pdf')

# Get text as list of pages
pages = get_all_pages_text('/path/to/file.pdf')
```

## Key Functions

- `extract_pdf_text(filepath)` - Returns all text from PDF as single string
- `get_all_pages_text(filepath)` - Returns list of strings, one per page

## Technical Notes

- Uses `from pypdf import PdfReader` (NOT PyPDF2)
- Uses `page.extract_text()` method
- Handles malformed PDFs gracefully
