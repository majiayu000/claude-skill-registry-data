---
name: evo-citation-verifier
description: Queries external academic APIs (CrossRef, Semantic Scholar, DBLP, doi.org) to verify whether a citation exists. Implements robust HTTP sessions with retry logic, exponential backoff, and rate limiting.
---

# evo-citation-verifier

Verifies citations against academic APIs.

## Key Functions

- `get_robust_session()` - Create requests session with retry/backoff
- `verify_doi_exists(doi, session)` - Check if DOI resolves via CrossRef
- `query_crossref(title, session)` - Search CrossRef by title
- `query_semantic_scholar(title, session)` - Search Semantic Scholar
- `query_dblp(title, session)` - Search DBLP
- `verify_citation(citation, session)` - Full verification pipeline for one citation
- `rate_limited_query(session, url, params, headers, delay)` - Rate-limited GET

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-citation-verifier/scripts')
from utils import get_robust_session, verify_citation, verify_doi_exists

session = get_robust_session()
result = verify_citation({'title': 'Some Paper', 'doi': '10.1234/fake'}, session)
print(result['doi_exists'])  # False for fake DOIs
```
