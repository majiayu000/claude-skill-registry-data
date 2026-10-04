---
name: evo-document-text-extraction
description: Extracts text from PDF, DOCX, and PPTX files using PyPDF2, pdfplumber, pdftotext CLI, and stdlib zipfile+XML fallbacks.
---
# evo-document-text-extraction

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-document-text-extraction/scripts')
from utils import extract_text, extract_text_pdf, extract_text_docx, extract_text_pptx

text = extract_text('/path/to/file.pdf')  # auto-detects format
```

## Key Functions
- `extract_text(filepath, max_pages=3)` - unified interface, auto-detects by extension
- `extract_text_pdf(filepath, max_pages=3)` - PDF with fallback chain: PyPDF2 -> pdftotext -> pdfplumber
- `extract_text_docx(filepath)` - DOCX via zipfile+XML stdlib
- `extract_text_pptx(filepath)` - PPTX via zipfile+XML stdlib
- `extract_text_pdftotext_cli(filepath, max_pages=3)` - pdftotext CLI wrapper
