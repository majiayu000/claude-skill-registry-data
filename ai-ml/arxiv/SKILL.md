---
name: arxiv
description: "Search arXiv papers by keyword, author, category, or ID."
allowed-tools:
  - bash
  - browse_page
enabled: true
related-skills: [academic-paper-review, systematic-literature-review]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# arXiv Research

Search and retrieve academic papers from arXiv via their free REST API. No API
key, no dependencies — just `bash` with `curl`.

## Quick Reference

| Action | Command |
|--------|---------|
| Search papers | `bash("curl -s 'https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5'")` |
| Get specific paper | `bash("curl -s 'https://export.arxiv.org/api/query?id_list=2402.03300'")` |
| Read abstract | `browse_page(url="https://arxiv.org/abs/2402.03300")` |
| Read full paper (PDF) | `browse_page(url="https://arxiv.org/pdf/2402.03300")` |

## Searching Papers

The API returns Atom XML. Parse with `python3` for clean output.

### Basic search

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5"
```

### Clean output (parse XML to readable format)

```bash
curl -s "https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending" | python3 -c "
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.fromstring(sys.stdin.read())
for entry in root.findall('a:entry', ns):
    title = entry.find('a:title', ns).text.strip().replace('\n', ' ')
    published = entry.find('a:published', ns).text[:10]
    summary = entry.find('a:summary', ns).text.strip()[:200]
    link = entry.find('a:id', ns).text
    print(f'{published} | {title}')
    print(f'  {link}')
    print(f'  {summary}...')
    print()
"
```

## Search Query Syntax

| Field | Example |
|-------|---------|
| All fields | `all:transformer` |
| Title | `ti:attention` |
| Author | `au:vaswani` |
| Abstract | `abs:reinforcement` |
| Category | `cat:cs.CL` |
| Combine (AND) | `all:transformer+AND+ti:attention` |
| Combine (OR) | `all:LLM+OR+all:large+language+model` |

## Common Categories

- `cs.CL` — Computation and Language (NLP)
- `cs.CV` — Computer Vision
- `cs.LG` — Machine Learning
- `cs.AI` — Artificial Intelligence
- `stat.ML` — Machine Learning (Stats)
- `physics` — Physics

## Workflow

1. **Search** by keyword/author/category to find relevant papers
2. **Read abstracts** from search results
3. **Fetch full abstract page** with `browse_page` for promising papers
4. **Read PDF** with `browse_page` for full content (if needed)

## Pitfalls

- **Rate limiting**: arXiv API asks for 3-second间隔 between requests. Don't
  hammer it.
- **Query too specific**: `"diffusion models in computer vision for medical
  imaging"` returns 0 results. Use 2-3 core keywords + category filter.
- **sortBy=relevance** is usually better than `submittedDate` for topical
  searches; use `submittedDate` only when user wants chronological order.
- **PDF parsing**: `browse_page` on PDF URLs may return raw text or fail on
  some papers. Prefer abstract pages for reliable content.
