---
name: ghc-search
description: >-
  Find a public announcement, current fact or original X/Twitter posts through ghc-proxy web and
  social search. When you don't have a URL, choose the web or X engine, filter by domain, handle or
  date as supported, and return an answer with deduplicated source URLs. Not for
  official-document-verification.
metadata:
  revision: "7"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "web and X/Twitter search via a local ghc-proxy Responses API; answer plus deduped sources"
  summary_zh: "经本机 `ghc-proxy` Responses API 做 web 与 X/Twitter 搜索；返回答案加去重来源"
  kind: "entry"
---

# ghc-search

Web and X search through a local `ghc-proxy` Responses API. The script owns request
building, parsing, inline-citation stripping, and URL dedup — you get an answer plus a
clean source list.

## Use it

The engine is a required first argument: `gpt` searches the web, `x` searches
X/Twitter. They hit different corpora, so there is no default.

The script is `scripts/ghc_search.py` relative to this skill's directory.
Only if a script command fails (for example `uv` is not found), read [references/troubleshooting.md](references/troubleshooting.md).

```bash
S="<skill-dir>/scripts/ghc_search.py"

uv run "$S" gpt "what is the current stable .NET SDK version"
uv run "$S" x --handle SpaceXAI "newest post"
uv run "$S" gpt --domain dotnet.microsoft.com --json "latest .NET SDK version"
uv run "$S" x --handle dotnet --from-date 2026-08-01 "what shipped this month"
```

| Flag | Engine | |
|---|---|---|
| `--model` | both | defaults below (env-overridable) |
| `--effort low\|medium\|high` | both | defaults `high` (gpt), `medium` (x) |
| `--handle NAME` | x | restrict to a handle; repeatable |
| `--exclude-handle NAME` | x | repeatable |
| `--from-date` / `--to-date` | x | `YYYY-MM-DD` |
| `--domain HOST` / `--block-domain HOST` | gpt | repeatable |
| `--context-size low\|medium\|high` | gpt | how much page text the tool pulls back |
| `--country CC` | gpt | two-letter code, for geo-sensitive results |
| `--limit N` | both | sources listed, default 10 |
| `--json`, `--max-tokens`, `--timeout`, `--endpoint` | both | |

A flag from the wrong engine is rejected before any network call.

## Configuration

Defaults assume a local `ghc-proxy` on `127.0.0.1:4141`. Set your proxy
endpoint and per-engine model IDs via environment variables (or pass
`--endpoint` / `--model`):

| Env var | Overrides | Default |
|---|---|---|
| `GHC_SEARCH_ENDPOINT` | proxy endpoint | `http://127.0.0.1:4141/v1/responses` |
| `GHC_SEARCH_MODEL_GPT` | gpt-engine model | required unless `--model` is passed |
| `GHC_SEARCH_MODEL_X` | x-engine model | required unless `--model` is passed |

`--model` and `--endpoint` flags win over env vars.

## What you need to know

- **Latency ~3-20s** measured; date-filtered X searches are the slow end.
- If a model returns HTTP 400 on `/v1/responses`, read [model/endpoint compatibility](references/models/responses-api-compatibility.md).
- **`--handle` restricts results but does not steer the model**, so the script appends
  the handles to the prompt for you. That is why a terse `x --handle X "newest post"`
  works; without the appending it draws a clarifying question instead of a search.
- **An empty source list is possible** — the model sometimes answers from its own
  knowledge without searching. No sources means no citation; judge the answer
  accordingly, and add `--domain` or ask it to cite if you need provenance.
- A response cut off by `--max-tokens` keeps its answer, flagged `[truncated]`, rather
  than being discarded. Raise `--max-tokens` and re-run if the tail matters.
- Exit code is non-zero with a one-line stderr message on any failure; a partial parse is
  never printed as success.

## Prerequisite

A running `ghc-proxy` is required; the script reports the endpoint it could not reach.

## When this is not the right tool

Without a reachable ghc-proxy this skill cannot run; fall back to whatever browser
automation your runtime offers (e.g. drive **Bing** with `&setlang=en`; Google may
serve a block page).

Reach for something else when you already have what you need: fetch the page
directly when you have the URL, and prefer a documentation source (`context7`
MCP) over general search when looking up a named library or API.

## Check

```bash
uv run "$(dirname "$S")/test_ghc_search.py"   # offline, no network required
```
