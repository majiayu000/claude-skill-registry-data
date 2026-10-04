---
name: search-tavily
description: >-
    Owns live-web retrieval through Tavily CLI (`tvly`), search, extract, map, crawl,
    research, on the cheapest verb that answers: relevance resolved server-side, not
    post-filtered locally, and bulk page content routed to disk, never the context window.
    Beats blind single-URL fetching, which ranks and scopes nothing. Any current-web question
    routes here.
---

# [SEARCH_TAVILY]

`tvly` owns live-web retrieval as one intent surface; the cheapest verb that answers wins. An open question is `search` — `--include-answer` returns a synthesized answer with no follow-up call, `--include-raw-content markdown` folds the top results' full content into the same call. Known URLs are `extract`; a site is one `crawl --instructions`, with `map` recon first when URLs must be picked by hand; a cited multi-source report is `research`. Live web routes here over `WebFetch`, which reads one URL blind while `tvly` ranks, scopes, and filters server-side.

Relevance resolves server-side, never a local post-filter: `--include-answer` on `search`, `--query` with `--chunks-per-source` on `extract`, `--instructions` with `--chunks-per-source` on `crawl`. Triage on the score and snippet every `search` result carries and pull full content only for the URLs that earn it — or skip the round-trip with `--include-raw-content` when the whole top set is wanted. Bulk output routes to disk, `-o` for the JSON envelope and `--output-dir` for one markdown file per crawled page, never into the window.

`crawl` starts shallow — `--max-depth 1`, a tight `--limit` — and widens once the site's shape is known; `--instructions` focuses it semantically and collapses a `map`-then-`extract` round-trip into one call, leaving `map` for cheap URL recon alone. `research` is the loose heavy verb, a cited report over 30-120 seconds: take `--output-schema` for a structured result, and never spend it on a fact one `search` settles.

## [01]-[USAGE]

Every command runs as `uvx --from tavily-cli tvly <verb>` under the ambient `TAVILY_API_KEY`; `search` and `extract` also run key-free under a rate cap. `--json` returns the typed envelope, `-o` writes it to a file, and each verb's full flag roster lives behind `--help`; add `--extract-depth advanced` when `extract` or `crawl` hits a JavaScript-rendered page. Reach for the one-call command that fits:

```bash template
uvx --from tavily-cli tvly search "QUERY" --include-answer advanced --max-results 8   # answer inline, no follow-up
uvx --from tavily-cli tvly search "QUERY" --include-raw-content markdown --max-results 8 --json   # fused: ranked hits + full content
uvx --from tavily-cli tvly extract URL_A URL_B --query "QUESTION" --chunks-per-source 3 --format markdown   # known URLs -> content
uvx --from tavily-cli tvly crawl https://example.com --max-depth 1 --limit 20 --instructions "GOAL" --chunks-per-source 3   # site pages -> chunks
uvx --from tavily-cli tvly crawl https://example.com --max-depth 2 --limit 50 --output-dir DIR   # site section -> markdown files
uvx --from tavily-cli tvly research run "QUERY" --citation-format numbered -o report.md   # cited report, blocks 30-120s
```

Take a second call only when one will not do; `--max-results` and `--limit` keep the feed inside `extract`'s 20-URL cap:

```bash template
# few among many — score-gate search hits, then pull only the survivors
uvx --from tavily-cli tvly search "QUERY" --json | jq -r '.results[] | select(.score > 0.5) | .url' | xargs uvx --from tavily-cli tvly extract --query "QUESTION" --chunks-per-source 3
# recon — list a site's URLs to pick from, then extract the chosen ones
uvx --from tavily-cli tvly map https://example.com --instructions "GOAL" --limit 20 --json | jq -r '.results[]'
uvx --from tavily-cli tvly extract PICKED_URL --query "QUESTION" --chunks-per-source 3
# detached research — dispatch now, poll later
uvx --from tavily-cli tvly research run "QUERY" --no-wait
uvx --from tavily-cli tvly research poll REQUEST_ID -o report.md
```
