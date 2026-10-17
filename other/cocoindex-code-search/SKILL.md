---
name: cocoindex-code-search
metadata:
  mandatory: true
  bypass_allowed: false
  trigger: broad_navigation
description: Require current-root-bound CocoIndex Code retrieval before broad conceptual navigation and confirm hits in live source.
---

# CocoIndex Code search

Before broad or conceptual repository navigation, execute the reviewed
`tools/search_semantic_corpus.py` adapter against a corpus bound to this exact
Git root and current selected source bytes. Read its help and provider/cache
rules. Keep exact filenames, symbols, strings, counts and small known scopes on
direct `rg`. Do not manufacture an irrelevant query to satisfy this requirement.

Retain actual JSON search output. The adapter checks source freshness, the local
CPU model's pinned bytes, returned path scopes and source spans. Installation or
an index marker is not evidence of use. Start with at most five candidates and
confirm relevant hits with exact live source reads. A ranking is not completeness.

Use isolated reviewed provider and cache paths explicitly. Refresh only for a
relevant source change. Never index secrets or unrelated ignored input, upload
private source, overwrite another repository's MCP registration, or interfere
with its daemon/index. If unavailable or stale, diagnose and disclose the exact
failure, then restore the tool before broad navigation. Do not bypass it with
`rg` or another search tool; exact known-scope `rg` remains appropriate. Never
claim an unexecuted search. This is a development tool, not a runtime dependency,
agent efficacy benchmark or delegation permission.
