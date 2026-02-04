---
name: semantic-search:search
description: Use when searching the codebase with natural language queries like "authentication logic" or "database connection"
---

# Semantic Search

Search the codebase using natural language.

## Action

1. Take the user's query (everything after `/semantic-search:search`)
2. Call `mcp__semantic-search__search_code` with:
   - `query`: the user's search terms
   - `max_results`: 10 (default, adjust if user specifies)
3. Present results clearly showing:
   - File path and line numbers
   - Code snippet
   - Relevance score

## Examples

User: `/semantic-search:search authentication middleware`
→ Search for "authentication middleware"

User: `/semantic-search:search database connection pooling`
→ Search for "database connection pooling"

## Optional Filters

If user specifies filters, pass them:
- `language`: "python", "typescript", etc.
- `file_pattern`: glob pattern like "**/*_test.py"
- `chunk_type`: "function", "class", "method"
