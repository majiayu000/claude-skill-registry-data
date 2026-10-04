---
name: search-context7
description: >-
    External-package truth: any signature, member, or capability of an imported library
    resolves through Context7 over memory or a guessed git tag. Load before the first lookup.
    Fires on any Context7 mention, doc or API lookup, a new import, "how does <lib> do X",
    and before coding against an uninstalled member. Un-indexed sources belong to search-tavily.
---

# [SEARCH_CONTEXT7]

Two MCP tools and a REST surface: `resolve-library-id` ranks indexed sources, `query-docs` returns cited code per scoped question, REST adds ranked metadata and budgeted pulls.

- Boundary: Context7 owns usage shape, composition, currency, and discovery — never exact signatures.
- Signatures: from source, cheapest first — `.api/<pkg>.md`, then uv-cache/local source, then `uv run --with <pkg>` (C# NuGet, TS node_modules).
- Query: a task sentence naming the exact symbol, one concept per call; a bare keyword or fused query returns shallow noise at more tokens.
- Caps: three calls per MCP tool per question; a known ID (`.api` catalog, memory, earlier turn) skips resolution, freeing budget for `query-docs`.
- Families: `/org/project` repository (production recipes), `/websites/*` doc site (concept prose), `/llmstxt/*` llms.txt bulk.
- Selection: benchmark score rules; snippet count is coverage, never quality; official name punctuation intact (`Next.js`, `Three.js`).
- Versions: a task naming a version takes the roster's `/org/project/version` ID; a version word inside the query does nothing.
- Fallback: "Library not found" means a wrong ID — re-resolve; an un-indexed library or version routes to source via search-tavily, never memory.

## [01]-[SYMBOL_TRUTH]

Any member of an external package about to be written, reviewed, or debugged, cross-library seam names both sides in one query.

Step 1. Resolve the library — skip when the ID is already known; libraryName AND query both required
```text conceptual
mcp__context7__resolve-library-id {"libraryName": "Effect", "query": "retry a failing acquisition with capped exponential backoff and jitter"}
```

Step 2. Query the repo ID; add the doc-site ID in the same block only when the repo answer is thin.
```text conceptual
mcp__context7__query-docs {"libraryId": "/effect-ts/effect", "query": "Effect.retry with a Schedule combining exponential backoff, jitter, and a retry cap"}
mcp__context7__query-docs {"libraryId": "/websites/effect_website", "query": "Effect.retry with a Schedule combining exponential backoff, jitter, and a retry cap"}
```

Step 3. Drill — when a richer owning combinator surfaces, drill the richer symbol the first block surfaced
```text conceptual
mcp__context7__query-docs {"libraryId": "/effect-ts/effect", "query": "Schedule.max combining retry count, elapsed-time budget, and capped backoff into one policy"}
```

## [02]-[CAPABILITY_RESEARCH]

Two passes — discover the package, then map it. Discovery (which package owns the capability): exa `category: "github"` returns best-in-class candidates with the stars, recency, and license the admission gate reads; Context7's index-search token-matches unrelated domains and misses here. Depth (map a chosen package): REST search ranks a named library's indexed sources by the signals the MCP strips (`benchmarkScore`, `trustScore`, `totalTokens`, freshness, `verified`); a token-budgeted topical pull routes bulk to disk per capability axis; the typed variant relevance-gates snippets before window entry; each surfaced symbol drills through `resolve-library-id`/`query-docs`.

```text conceptual
// discovery — best-in-class candidates with admission metadata (stars, recency, license)
mcp__exa__web_search_advanced_exa {"query": "best-in-class Python library for <capability>, compared against <incumbent>", "category": "github", "enableSummary": true, "numResults": 6}
```

```bash copy-safe
# depth 1 — rank a named library's indexed sources, projected compact
xh -j GET https://context7.com/api/v1/search query=='scikit-image restoration' "Authorization: Bearer $CONTEXT7_API_KEY" \
  | jq -r '.results[:8][] | [.id, .benchmarkScore, .trustScore, .totalTokens, .lastUpdateDate[:10]] | @tsv'
# depth 2 — one budgeted pull per capability axis, bulk to disk, never the window
xh GET https://context7.com/api/v1/scikit-image/scikit-image topic=='deconvolution wiener richardson-lucy' tokens==3000 "Authorization: Bearer $CONTEXT7_API_KEY" -o restoration.md
# depth 3 — typed gate: only relevance-cleared snippets enter the window
xh -j GET https://context7.com/api/v1/scikit-image/scikit-image type==json topic=='deconvolution' tokens==2000 "Authorization: Bearer $CONTEXT7_API_KEY" \
  | jq '[.snippets[] | select(.relevance > 0.02) | {title: .codeTitle, code: .codeList[0].code}]'
```
