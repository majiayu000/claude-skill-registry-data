---
name: file-search
description: Search files under a directory with ripgrep and get structured results.
permissions:
  fs-read: ["~/**"]
  commands: ["rg", "jq"]
commands:
  - id: search
    run: ./scripts/search.sh {{query}} {{dir}}
    description: Find matches for a query under a directory (default cwd)
    output: json
---
# file-search

Search a directory for text using ripgrep.

- `search` takes a query and an optional directory (defaults to the app data dir).
- Results render as a table bound to "$.search".