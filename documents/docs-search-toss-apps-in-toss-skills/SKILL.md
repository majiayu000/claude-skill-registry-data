---
name: docs-search
description: Lightweight search utility for Toss / Apps-in-Toss llms-full.txt docs, caching sources and ranking snippets with keyword + similarity (Korean-aware) scoring.
---

# Docs Search

Lightweight search utility and usage guide for the Toss / Apps-in-Toss `llms-full.txt` documents. It retrieves snippets from three sources with simple keyword + similarity scoring.

## Sources

- Apps-in-Toss Developer Center: https://developers-apps-in-toss.toss.im/llms-full.txt
- Toss Mini TDS Mobile: https://tossmini-docs.toss.im/tds-mobile/llms-full.txt
- Toss Mini TDS React Native: https://tossmini-docs.toss.im/tds-react-native/llms-full.txt

## Files

- `requirements.txt`: Python dependency (`requests`).
- `skills/docs-search/core/docs_search.py`: CLI searcher that downloads and caches llms-full.txt files, then ranks paragraphs.
- `skills/docs-search/core/korean_similarity.py`: Korean-aware similarity utilities.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
python -m core.docs_search -q "Unity WebGL optimization" -k 5
```

- `-q / --query`: search query (required)
- `-k / --topk`: number of results to show (default 5)
- `--refresh-cache`: bypass cache and re-download all sources
- Output: `[index] <source URL> - <heading>` / `score: <score>` / `snippet`

## How it works

- Downloads each llms-full.txt and caches under `<temp>/apps-in-toss/skills/.cache/` (cross-platform: `/tmp` on Linux/macOS, `%TEMP%` on Windows).
- Splits by blank lines into paragraphs and attaches the most recent heading (`#`, `##`, etc.) as context.
- Ranks by keyword overlap plus `SequenceMatcher` similarity; returns top results.

## Examples

- Quickly find where an API or guide is described.
- Search optimization/porting/auth/payment references with queries like “Unity WebGL performance”.
- Open the returned source URL in a browser for full context.

## Notes

- Searches only the text contained in llms-full.txt; it does not crawl linked pages.
- Requires network access; deleting the cache triggers re-downloads.

## Core workflow

1. Fetch & cache: download each `llms-full.txt` and store under `<temp>/apps-in-toss/skills/.cache/` (reuse cache when present).
2. Chunk: split by blank lines, tagging each paragraph with the most recent heading.
3. Score: keyword overlap (weight 2) + similarity; Korean text uses `korean_similarity`, otherwise `SequenceMatcher`.
4. Rank & output: sort by score, return top‑k snippets (source URL, heading, score, snippet).

```python
from core.docs_search import search

results = search("Unity WebGL optimization", topk=5, refresh=False)
for item in results:
    print(item["source"], item["heading"], item["score"])
    print(item["snippet"])
```

## Requirements

- Python 3.9+
- `requests>=2.31.0` — HTTP 요청 및 llms-full.txt 다운로드