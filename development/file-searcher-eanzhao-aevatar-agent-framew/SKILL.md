---
name: file-searcher
description: Grep the workspace for a pattern using file_search.
allowed-tools:
  - file_search
---

## When to use
- User asks "where is X used/defined" or "find occurrences of pattern".

## Procedure
1) Translate the question into a concise regex pattern.
2) Call `file_search`:
   - `pattern`: the regex
   - optional `extensions`: narrow to `.cs,.md,.proto` etc
3) Return results as a short list: file + line + snippet.
4) If truncated, narrow the search (extensions / more specific pattern) and repeat.


