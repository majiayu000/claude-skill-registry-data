---
name: evo-pdf-redaction-engine
description: Performs physical redaction of identified content in PDF documents using PyMuPDF's redaction API. Handles exact string redaction, regex-based redaction, hyperlink removal, metadata scrubbing, and secure document saving.
---

# evo-pdf-redaction-engine

Performs physical PDF redaction using PyMuPDF (fitz). Applies redaction annotations, removes hyperlinks, purges metadata, and saves securely with garbage collection.

## Key Functions

- `redact_exact_strings(page, strings)` - Add redaction annotations for exact string matches
- `redact_regex_patterns(page, patterns)` - Add redaction annotations for regex matches
- `redact_page_region(page, rect)` - Redact an entire rectangular region
- `scrub_hyperlinks(page, link_patterns)` - Remove identifying hyperlinks and redact their text
- `scrub_metadata(doc)` - Purge standard and XMP metadata
- `anonymize_pdf(input_path, output_path, exact_strings, regex_patterns, link_patterns)` - Full pipeline
- `save_redacted_document(doc, output_path)` - Save with garbage=4 and deflate=True

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-redaction-engine/scripts')
from redaction import anonymize_pdf

anonymize_pdf(
    input_path='/root/paper1.pdf',
    output_path='/root/redacted/paper1.pdf',
    exact_strings=['Author Name', 'University Name'],
    regex_patterns=[r'arXiv:\d{4}\.\d{4,5}'],
    link_patterns=['arxiv.org', 'github.com']
)
```
