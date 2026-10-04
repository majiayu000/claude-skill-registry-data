---
name: mem
description: Search local memory index (local-first). Use for /mem queries in Telegram.
user-invocable: true
---

# Memory Search (/mem)

## Overview

Run local-first memory search using the cached index.

## Usage

1) Update the index if needed:
```bash
scripts/index-memory.py
```

2) Search the index with the user query:
```bash
scripts/search-memory.py "<query>" --top 5
```

## Output

Return the top hits with their paths and headers. Summarize briefly if needed.
