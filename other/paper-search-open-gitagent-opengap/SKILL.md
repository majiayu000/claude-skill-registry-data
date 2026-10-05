---
name: paper-search
description: Academic paper search via Google Scholar using Serper API
allowed-tools: paper-search
---

# Paper Search

Search for academic papers and scholarly articles via Google Scholar using the Serper API.

## When to Use

- Finding peer-reviewed research on a topic
- Locating seminal papers and their citation counts
- Searching for systematic reviews and meta-analyses
- Grounding claims in academic literature

## How to Use

1. Formulate an academic-style search query
2. Optionally specify year filters to narrow results by publication date
3. Call `paper_search` with the query
4. Review results for relevance, citation count, and recency

## Result Format

Results are returned in markdown format:

```
**Title of Paper**
Authors: Author A, Author B
Year: 2024 | Citations: 142
Snippet: Brief excerpt from the paper abstract or body...
URL: https://scholar.google.com/...
```

## Constraints

- Results sourced from Google Scholar via Serper API
- Supports year filtering (e.g., papers from 2020-2025)
- Snippet may be from abstract or body text
- Each call counts toward the researcher's 8-call limit per task

## Best Practices

- Use domain-specific terminology for better results
- Include key author names if known
- Filter by year for rapidly evolving topics
- Prefer highly-cited papers for foundational claims
