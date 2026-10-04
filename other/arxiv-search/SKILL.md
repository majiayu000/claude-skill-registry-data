---
name: arxiv-search
description: Search arXiv for papers by topic, author, or ID. Use when finding research, surveying recent publications, or looking up a specific paper.
user-invocable: true
argument-hint: <search query or arXiv ID, e.g. "transformer attention" or "2301.07041">
metadata:
  version: "1.0.0"
---

# arXiv Paper Search

Search the arXiv API for academic papers. No authentication required.

## When to Use

- User wants to find papers on a topic
- User asks about recent research in a field
- User provides an arXiv ID and wants details
- User wants to compare papers or find related work

## API Details

- **Base URL:** `https://export.arxiv.org/api/query`
- **Auth:** None required
- **Rate limit:** 1 request per 3 seconds (be polite)
- **Response format:** Atom XML

## How to Search

### By topic/keywords

```bash
curl -sL "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=10&sortBy=submittedDate&sortOrder=descending"
```

Replace spaces in QUERY with `+`. For multi-word phrases, use `%22phrase%22` for exact match.

### By specific field

- `ti:` — title
- `au:` — author
- `abs:` — abstract
- `cat:` — category (e.g. `cs.AI`, `cs.CL`, `stat.ML`)
- `all:` — all fields

Combine with `AND`, `OR`, `ANDNOT`:

```bash
# Papers about transformers in NLP
curl -sL "https://export.arxiv.org/api/query?search_query=ti:transformer+AND+cat:cs.CL&max_results=10&sortBy=submittedDate&sortOrder=descending"

# Papers by a specific author
curl -sL "https://export.arxiv.org/api/query?search_query=au:hinton&max_results=10&sortBy=submittedDate&sortOrder=descending"
```

### By arXiv ID

```bash
curl -sL "https://export.arxiv.org/api/query?id_list=2301.07041"
```

Multiple IDs: `id_list=2301.07041,2305.18290`

### Pagination

Use `start` parameter:

```bash
# Results 11-20
curl -sL "https://export.arxiv.org/api/query?search_query=all:QUERY&start=10&max_results=10&sortBy=submittedDate&sortOrder=descending"
```

## Parsing the Response

The response is Atom XML. Extract these fields from each `<entry>`:

| Field | XML Path | Notes |
|-------|----------|-------|
| Title | `<title>` | May contain line breaks — normalize |
| Authors | `<author><name>` | Multiple entries |
| Abstract | `<summary>` | May contain LaTeX |
| Published | `<published>` | ISO 8601 date |
| Updated | `<updated>` | Latest version date |
| arXiv ID | `<id>` | URL form, extract ID from path |
| PDF link | `<link rel="related" title="pdf">` | Direct PDF URL |
| Categories | `<category term="...">` | Primary + secondary |
| Comment | `<arxiv:comment>` | Page count, conference info |

## Output Format

Present results as a numbered list:

```
1. **Title of Paper** (arXiv:2301.07041)
   Authors: First Author, Second Author, et al.
   Published: 2023-01-17 | Categories: cs.CL, cs.AI
   Abstract: First 2-3 sentences of the abstract...
   PDF: https://arxiv.org/pdf/2301.07041
```

For single paper lookups, show the full abstract.

## Common Categories

| Code | Field |
|------|-------|
| cs.AI | Artificial Intelligence |
| cs.CL | Computation and Language (NLP) |
| cs.CV | Computer Vision |
| cs.LG | Machine Learning |
| cs.SE | Software Engineering |
| cs.CR | Cryptography and Security |
| stat.ML | Machine Learning (Stats) |
| math.OC | Optimization and Control |
| eess.SP | Signal Processing |
| quant-ph | Quantum Physics |

## Tips

- Default to `sortBy=submittedDate&sortOrder=descending` for recent papers
- Use `max_results=10` as default, increase if user wants more
- For broad topics, search by category + keywords to reduce noise
- arXiv IDs after 2007 use the format `YYMM.NNNNN` (e.g. `2301.07041`)
- Older IDs use `subject/YYMMNNN` format (e.g. `hep-th/9901001`)
- The abstract page is at `https://arxiv.org/abs/ID`
- The PDF is at `https://arxiv.org/pdf/ID`

## Reading Full Papers

If the user wants to read a paper's full content, fetch the PDF URL and use the Read tool on it, or use WebFetch on the abstract page for the HTML version.

For the abstract page (lighter weight):
```bash
curl -sL "https://arxiv.org/abs/2301.07041"
```
