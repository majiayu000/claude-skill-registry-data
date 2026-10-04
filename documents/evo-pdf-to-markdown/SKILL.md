---
name: evo-pdf-to-markdown
description: Converts academic PDF to Markdown using marker-pdf v1.3.3, preserving LaTeX math delimiters in $$ format.
---

# evo-pdf-to-markdown

Converts PDF files to Markdown text using the marker-pdf library (v1.3.3),
preserving LaTeX formulas in $$ delimiters.

## Key Functions

- `setup_marker_models()` - Initialize marker-pdf deep learning models
- `convert_pdf_to_markdown(pdf_path, force_ocr=False)` - Convert PDF to Markdown

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-to-markdown/scripts')
from utils import convert_pdf_to_markdown

markdown_text = convert_pdf_to_markdown('/path/to/paper.pdf')
```

## Notes

- marker-pdf outputs display math as `$$ ... $$` and inline math as `$ ... $`
- Multi-line equations may be split into multiple $$ blocks
- Equation numbers may be included inside the $$ delimiters (needs post-processing)
- force_ocr=True forces visual math recognition instead of relying on PDF text streams
- The converter uses surya-ocr suite and texify model for math OCR
