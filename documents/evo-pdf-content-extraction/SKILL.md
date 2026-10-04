---
name: evo-pdf-content-extraction
description: Extracts and analyzes text content from PDF pages to identify author-revealing information including names, affiliations, emails, arXiv IDs, venue/conference mentions, and other identity-leaking content.
---

# evo-pdf-content-extraction

Extracts text from academic PDFs and identifies all content that could reveal authorship for anonymization purposes.

## Key Functions

- `extract_page_text(page)` - Get plain text from a page
- `extract_words_with_positions(page)` - Get words with bounding box coordinates
- `identify_author_block_region(page)` - Find the author block area on first page
- `detect_arxiv_identifiers(text)` - Find arXiv IDs in text
- `detect_email_addresses(text)` - Find email addresses
- `detect_affiliations(text)` - Find institutional affiliations
- `detect_venue_statements(text)` - Find venue/conference acceptance statements
- `get_all_redaction_targets(pdf_path)` - Main function: analyze a PDF and return all strings to redact

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-pdf-content-extraction/scripts')
from extraction import get_all_redaction_targets

targets = get_all_redaction_targets('/root/paper1.pdf')
print(targets['exact_strings'])  # List of exact strings to redact
print(targets['regex_patterns'])  # List of regex patterns to apply
print(targets['link_patterns'])   # URL patterns to scrub
```
