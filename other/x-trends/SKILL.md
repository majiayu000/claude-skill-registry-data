---
name: x-trends
description: Use for generic X public-data research, trend discovery, recent-post checks, and social attention signals. Provides app-only bearer auth, endpoint patterns, field selection, error handling, and compact JSON evidence guidance.
---

# X Trends

Use X as an attention and recency signal. This skill explains how to query public X endpoints and return compact evidence. The caller owns interpretation.

## Auth

Use app-only bearer auth for public reads:

```bash
TOKEN="${X_BEARER_TOKEN:-$TWITTER_BEARER_TOKEN}"
```

Never print token values.

## Trend Lookup

Use WOEID trend lookup first when a suitable WOEID is known:

```bash
curl -fsS "https://api.x.com/2/trends/by/woeid/1?max_trends=20&trend.fields=trend_name,tweet_count" \
  -H "Authorization: Bearer $TOKEN"
```

Useful WOEIDs:

| Place | WOEID |
| --- | ---: |
| Worldwide | `1` |
| India | `23424848` |
| Mumbai | `2295411` |
| Delhi | `20070458` |
| Bengaluru | `2295420` |
| United States | `23424977` |
| New York | `2459115` |
| London | `44418` |

For an unknown city/country, use worldwide plus the closest known country/city and note uncertainty.

## Recent Search Fallback

If WOEID trends are unavailable, too broad, or opaque, use recent search for caller-supplied terms. Always request explicit fields because defaults are minimal.

```bash
curl -fsS "https://api.x.com/2/tweets/search/recent?max_results=25&query=<url-encoded-query>&tweet.fields=created_at,public_metrics,lang" \
  -H "Authorization: Bearer $TOKEN"
```

Useful fields:

- `tweet.fields=created_at,public_metrics,lang`
- `expansions=author_id` when author context matters
- `user.fields=verified,public_metrics` when author context is requested

## Parallel Calls

When the caller supplies multiple markets, WOEIDs, topics, or query angles, run independent API calls in parallel when practical. Keep the merged return compact.

Parallelism is API-level. Do not spawn additional Codex subagents from this skill.

## Merge Rules

- Deduplicate by normalized trend name, query, and obvious aliases.
- Keep market count, WOEIDs checked, max tweet count, and public metric summaries when available.
- Preserve uncertainty for opaque trend names or hashtags.
- Mark API errors, missing auth, unavailable WOEIDs, and rate limits clearly.
- Do not decide final cultural meaning or product relevance. The caller owns interpretation.

## Return Shape

Return compact JSON-like evidence:

```json
{
  "source": "x",
  "markets": ["worldwide", "india", "mumbai"],
  "trendSignals": [
    {
      "name": "trend name",
      "markets": ["india", "mumbai"],
      "tweetCountMax": 12345,
      "recentSearchQuery": null,
      "notes": "short factual signal summary"
    }
  ],
  "errors": []
}
```
