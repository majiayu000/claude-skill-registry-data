---
name: evo-bibtex-parser
description: Parses BibTeX files using bibtexparser 1.4.2 and cleans LaTeX/BibTeX artifacts from fields like title, author, year, DOI, and venue. Produces a normalized list of citation dictionaries ready for verification.
---

# evo-bibtex-parser

Parses BibTeX files and cleans LaTeX artifacts for citation verification.

## Key Functions

- `parse_bibtex_file(file_path)` - Parse a .bib file, returns list of entry dicts
- `clean_bibtex_artifacts(text)` - Remove {}, \commands, LaTeX escapes from strings
- `extract_citation_metadata(entries)` - Extract and clean metadata from parsed entries

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-bibtex-parser/scripts')
from utils import parse_bibtex_file, clean_bibtex_artifacts, extract_citation_metadata

entries = parse_bibtex_file('/root/test.bib')
citations = extract_citation_metadata(entries)
for c in citations:
    print(c['title'], c['doi'])
```

## Notes
- Uses bibtexparser 1.4.2 (NOT v2.x)
- homogenize_fields=True standardizes field names to lowercase
- Handles @article (journal), @inproceedings (booktitle), @book entries
- Cleans curly braces, LaTeX commands, special characters
