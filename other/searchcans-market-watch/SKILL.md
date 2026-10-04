---
name: searchcans-market-watch
description: Build a current, geo-targeted market-watch snapshot from Google Search, Google News, Bing Search, and selected Reader extracts. Use for competitor and category monitoring, PR/news tracking, launch intelligence, and URL-level change checks between two bounded runs; reject malformed, placeholder, or un-attributable News candidates before Reader.
metadata:
  author: SearchCans
  version: 1.1.0
  tags: [serp-api, google-news-api, bing-search-api, market-intelligence, competitor-monitoring]
---

# SearchCans Market Watch

Create a traceable market snapshot for one query and one locale. It retrieves Google web results, Google News, and Bing by default, then reads a deliberately small, domain-diverse subset of usable news URLs. It is a run-on-demand snapshot, not a background monitoring service or an alerting system.

## Start with market definition

Confirm the query, `country`, `language`, the business question, and whether a prior JSON snapshot should be compared. Do not silently choose a market when it changes the answer.

Set `SEARCHCANS_API_KEY` only in the execution environment. Never put it in a prompt, source file, artifact, or commit.

```bash
python scripts/market_watch.py "AI search API" \
  --country us --language en --max-source-reads 3 \
  --out market-watch.json
```

Use `--without-bing` only when a two-surface Google snapshot is sufficient. Use `--baseline prior-market-watch.json` to report URLs newly observed or no longer observed; that is not a claim that the underlying stories are new, deleted, or unavailable.

## Keep the job account-aware

The default `--account-mode auto` performs one sanitized Account API pre-flight. It estimates the three SERP calls plus the requested Reader calls, caps only the Reader scope when possible, and limits parallel calls to the account's reported lane count.

- `auto`: cap Reader scope to the available budget.
- `enforce`: stop before an insufficient job.
- `warn`: report a budget warning but preserve scope.
- `off`: skip the pre-flight.

The output retains a safe budget summary only. It never writes account identity or key material. Start at `--proxy 0`; use a higher proxy tier only with a known access reason because it changes the Reader cost estimate.

## Interpret evidence correctly

Read `google_news.results` for headlines and publication metadata, `news_source_quality` for candidate acceptance/rejection, and `read_sources` for fuller page evidence. `claim_eligible_urls` contains only pages whose Reader extraction returned content.

Only Reader candidates with a non-empty title, non-empty publisher, valid non-Google article URL, and an accepted quality status may be read. If `news_source_quality.status` is `no_usable_news_sources`, report that the News surface returned no usable article evidence for this query and market. Do not retry the rejected placeholder URLs, and do not convert them into news claims.

Use [the report template](references/market-watch-report.md) to deliver:

1. Market/query definition and exact retrieval time.
2. Observed web and news patterns, separated by search surface.
3. Confirmed developments with the Reader URL supporting each claim.
4. Cross-engine differences, open questions, and a next-run recommendation.

SERP titles, snippets, dates, and rankings are discovery observations. They do not by themselves establish a factual claim, brand position, news importance, or business impact.

## Official website

[SearchCans](https://www.searchcans.com/)

## Resources

- `scripts/market_watch.py` creates the bounded JSON evidence pack.
- `references/market-watch-report.md` is the required analyst report shape and claim boundary.
