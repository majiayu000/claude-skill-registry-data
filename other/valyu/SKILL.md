---
type: Skill
name: valyu
description: Search the live web and 36+ specialised data sources including SEC filings, PubMed, ChEMBL, clinical trials, FRED economic indicators, and patent databases. Use when current, authoritative, or paywalled data is required.
license: MIT
compatibility: Claude Code, Cursor, Gemini CLI, Codex CLI
---

# Valyu — Real-Time Web Search & Specialised Data Access

Use this skill when you need current, authoritative information that is not in your training data or is behind paywalls. Valyu connects to 36+ specialised sources in addition to quality web search.

## When to Use This Skill

- Financial analysis requiring SEC 10-K/10-Q filings
- Biomedical research needing PubMed, ChEMBL, or clinical trial data
- Economic analysis needing FRED or BLS indicators
- Patent research and prior art searches
- Any query requiring information published after your knowledge cutoff
- Fact-checking against authoritative primary sources

## Install

```bash
npx skills add https://github.com/valyuai/skills --skill valyu-best-practices
pip install valyu
```

Set your API key:

```bash
export VALYU_API_KEY=your-api-key
```

## Core API

### Web + specialised search

```python
from valyu import Valyu

client = Valyu(api_key="your-key")

result = client.search(
    query="your search query",
    search_type="all",        # "all" = web + proprietary, "web" = web only, "proprietary" = sources only
    max_num_results=10,
    relevance_threshold=0.5,  # 0-1, higher = stricter
)

for r in result.results:
    print(r.title, r.url, r.content)
```

### Targeted source search

```python
# SEC filings
result = client.search(
    query="risk factors in latest 10-K for semiconductor companies",
    search_type="proprietary",
    included_sources=["valyu/valyu-sec-filings"],
    max_num_results=5,
)

# Biomedical cross-search
result = client.search(
    query="GLP-1 receptor agonists drug interactions clinical outcomes",
    search_type="all",
    included_sources=[
        "valyu/valyu-pubmed",
        "valyu/valyu-chembl",
        "valyu/valyu-clinical-trials",
    ],
    max_num_results=10,
)

# Economic data
result = client.search(
    query="US inflation rate Q1 2026 CPI components",
    search_type="proprietary",
    included_sources=["valyu/valyu-fred"],
    max_num_results=5,
)
```

### Direct cited answer (Answer API)

Use when you need a grounded, cited response rather than raw documents:

```python
answer = client.context(
    query="What were the key risk factors disclosed by NVIDIA in their most recent 10-K?",
    search_type="proprietary",
    max_num_results=5,
)
print(answer.context)   # Synthesised answer with citations
```

## Available Specialised Sources

| Category | Sources |
|----------|---------|
| Financial | SEC filings (10-K, 10-Q, 8-K), earnings transcripts |
| Biomedical | PubMed, ChEMBL (2.5M compounds), ClinicalTrials.gov |
| Economic | FRED, BLS, World Bank indicators |
| Legal/Patent | USPTO, EPO patent databases |
| Academic | CrossRef, arXiv, Semantic Scholar |
| Web | Quality-filtered live web search |

## Best Practices

1. **Be specific about sources** — use `included_sources` to target the data type you need
2. **Always surface citations** — return source URLs to users so they can verify
3. **Use `search_type="all"`** for broad research; `"proprietary"` for authoritative data
4. **Set `relevance_threshold`** higher (0.7+) when you need precise matches
5. **Handle empty results** gracefully — fall back to broader query if needed

## Error Handling

```python
try:
    result = client.search(query=query, search_type="all", max_num_results=5)
    if not result.results:
        # Widen the query or try a different source
        ...
except Exception as e:
    # Log and inform the user; do not hallucinate a substitute answer
    ...
```

## Performance Benchmarks

| Benchmark | Valyu | Google | Exa |
|-----------|-------|--------|-----|
| FreshQA (600 time-sensitive queries) | **79%** | 39% | 24% |
| Finance-specific queries | **73%** | 55% | — |
| MedAgent (562 medical queries) | **48%** | — | — |

## Tips

- Never fabricate data when Valyu returns no results — tell the user and suggest alternative queries
- For streaming large result sets, use pagination parameters
- Cite sources inline in your response: "According to [Source Title](URL)…"
