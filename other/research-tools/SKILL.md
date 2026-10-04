---
name: research-tools
description: >-
  Research tools — arXiv paper search, blog/RSS monitoring (blogwatcher), web archive research (Common Crawl/WARC), LLM Wiki knowledge base, and Polymarket prediction market queries. Covers academic, web, and market research.
version: 1.0.0
author: Hermes Agent (curator consolidation)
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: ['research', 'arxiv', 'blogwatcher', 'web-archive', 'llm-wiki', 'polymarket']
lane: worker-flash
reasoning_effort: high
agent: Researcher
routing_hint: |
  **Agent-Scope:** Deep-research, fact-checking, paper-search, knowledge-base. Off-scope: code-building, visual design, writing — return to Yuno.
  
  Routing-Spec: `yuno-team-routing`.
  
---
# Research Tools

Covers: arXiv, blogwatcher, web archives, LLM Wiki, Polymarket.

## arXiv
```bash

set -euo pipefail
# Search papers
arxiv search "transformer architecture" --limit 10
arxiv get 2301.07041
```

## Blogwatcher (RSS/Atom Monitoring)
```bash

set -euo pipefail
blogwatcher add https://example.com/feed.xml
blogwatcher list
blogwatcher check
```

## Web Archive Research
```bash

set -euo pipefail
# Common Crawl CDXJ index
curl "https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=example.com&output=json"
```

## LLM Wiki (Karpathy's Knowledge Base)
```bash

set -euo pipefail
# Build/query interlinked markdown KB
# See references/llm-wiki.md
```

## GreyHack P0/P1-P4 Research Workflow

For GreyHack tool research, keep the priority model explicit:

1. **P0 — build foundation:** fix existing core helpers before adding new tools.
2. **P1-P4 — after P0:** deepen research, tool specs, safety taxonomy, and roadmap.
3. **Mini-spec before code:** create a short implementation spec for each candidate before touching `src/` or `tools/`.
4. **Branch rule:** do not mutate `develop` directly; use a feature branch from `develop`.
5. **Main boundary:** never merge or touch `main` without explicit user approval.

Useful candidate order from the 2026-06-19 GreyHack research pass:

1. `recon-lite` — safe recon/report structure without exploit automation.
2. `mission_report` — standardized mission/writeup documentation.
3. `cli_core` — shared CLI/output helpers.

When implementation starts, `cli_core` is often the safest technical foundation to build first, then implement `recon-lite` and `mission_report` on top of it.

Pitfalls:

- Do not treat P1-P4 as implementation work before P0 is stable.
- Do not overwrite complex legacy tools when a clean new file is safer.
- Do not port real exploit/PoC/credential/network-target content into GreyScript.
- If a subagent/research delegation fails, switch to parent-direct targeted research and document the fallback.

Use this for GitHub Awesome-list / curated-security-list research where the user wants a reusable knowledge base before implementation.

1. **Snapshot first:** clone or otherwise capture the source read-only; record URL, commit, last commit message, and extracted counts.
2. **Extract links into CSV:** parse README tables/lists into `resource, section, url, description` plus GreyHack relevance fields.
3. **Classify before coding:** assign `direct`, `concept`, `learning`, or `low` relevance and `P0/P1/P2/P3` priority.
4. **Top-20 first:** create a prioritized Top-20 recommendation document before touching implementation files.
5. **Knowledge base for the rest:** keep non-top20 resources in a searchable CSV/Markdown knowledge base for later research.
6. **Safety gate:** do not translate real exploit/PoC/credential/network-tool content into game scripts; use only game-safe concepts, dummy data, and methodology.
7. **Validate and prove no script changes:** validate CSV row counts and run `git status --short -- docs src tools` (or equivalent) to confirm implementation files were not changed.

See `references/github-awesome-list-greyhack-research.md` for the concrete GreyHack/Awesome-Hacking workflow and validation pattern.
See `references/greyhack-mini-spec-template.md` for the GreyHack mini-spec shape used after research before implementation.
See `references/greyhack-mini-tools-implementation-2026-06-19.md` for the implemented mini-tool reference, validation command, and parser-safe patterns.

## GreyScript Research-to-Code Guardrails

When Awesome-Hacking research graduates into GreyScript tooling, keep these guardrails active:

1. **P0 first:** stabilize build foundations before P1-P4 research roadmap work.
2. **Branch discipline:** never touch `main` without explicit approval; prefer a feature branch created from `develop` even when `develop` experimentation is allowed.
3. **Parser-safe GreyScript:** avoid one-line `if ... then ... end if` blocks with `return`, assignment, or function calls; convert them to explicit multi-line blocks.
4. **No ternary expressions:** GreyScript/Greybel can reject `a = ("x" if cond else "y")`; rewrite as `if cond ... else ... end if`.
5. **Clean merge debris before debugging:** orphan duplicate blocks and conflict markers (`=======`) can produce misleading parse errors.
6. **CI portability:** build scripts should detect both `greybel-js` and `greybel`, not only `greybel-js`.

See `references/greyhack-build-fixes-2026-06-19.md` for the session-specific P0/P1-P4 notes, parser examples, and validation commands.

## Polymarket
```bash

set -euo pipefail
# Query prediction markets
curl "https://gamma-api.polymarket.com/markets?limit=10"
```

## Liquipedia / MediaWiki API

For esports results, tournament brackets, and standings from Liquipedia (or any MediaWiki wiki), use the MediaWiki API instead of scraping JS-rendered HTML.

```bash

set -euo pipefail
# For rendered HTML (standings, prizepool, participants):
curl -sL --compressed \
  "https://liquipedia.net/counterstrike/api.php?action=parse&page=PAGE_NAME&prop=text&format=json" \
  -H "User-Agent: Mozilla/5.0"

# For raw wikitext (match brackets, structured parsing):
curl -sL --compressed \
  "https://liquipedia.net/counterstrike/api.php?action=parse&page=PAGE_NAME&prop=wikitext&format=json" \
  -H "User-Agent: Mozilla/5.0"
```

Key pitfalls: always use `--compressed` (406 without gzip). Playoffs brackets may NOT appear in the API response (JS-rendered client-side) — use the Prize Pool placement table as a proxy for completed playoff results, or fall back to raw HTML scraping via `curl --compressed` + Python regex. See `references/liquipedia-api-extraction.md` for full parsing guide, Python snippet, raw HTML fallback, and tournament page structure.

## Resilient Multi-Source News Gathering

When building news briefings (esports, tech, cybersecurity), primary sources frequently become unavailable due to Cloudflare, API failures, or search backend issues. Use a fallback chain:

1. **Primary:** `web_search` → `web_extract` on target URLs
2. **Fallback 1:** `curl` directly to target site with HTML stripping (`sed 's/<[^>]*>//g'`)
3. **Fallback 2:** Alternative sources (The Verge, ESPN, Reddit, Archive.org)
4. **Local cache:** Read existing briefing file (`~/Schreibtisch/wichtigsten Nachrichten.md`) for last known state

See `references/hltv-liquipedia-esports-research.md` for the full fallback chain, Cloudflare bypass patterns, source-specific curl recipes, and the quick source reference table.
