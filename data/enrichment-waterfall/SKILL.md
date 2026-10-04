---
name: enrichment-waterfall
description: Build multi-vendor data enrichment waterfalls in n8n — cascading API calls across SerpAPI, Hunter.io, Apollo, Clearbit, LLM extractors, and scrapers with cost-aware fallbacks. Use this skill whenever the user wants to enrich leads, contacts, companies, or any entity with external data in n8n — phrases like "lead enrichment", "email finder", "data waterfall", "Clay alternative", "find LinkedIn profile", "get company info", "enrich this list of leads". Also use when designing any flow where multiple vendors are tried in sequence until one succeeds. Use this skill before designing such workflows because naive sequential API calls produce $10/lead costs — the waterfall pattern drops that to $0.10 by ordering vendors correctly.
---

# Enrichment Waterfall for n8n

A **waterfall** = try cheapest/fastest vendor first, fall through to more expensive/accurate vendors only when the previous fails. This is how Clay, Clearbit, and every production enrichment pipeline actually works.

## The core pattern

```
Input (name, email, or domain)
  ↓
Vendor 1 (cheap, fast, ~60% hit rate) — e.g., Hunter.io
  ↓ IF no match
Vendor 2 (medium cost, ~80% cumulative) — e.g., Apollo
  ↓ IF no match
Vendor 3 (expensive / LLM extract, ~95% cumulative) — e.g., SerpAPI + LLM
  ↓ IF no match
Dead letter: log as "unenrichable"
```

At each step, a hit short-circuits the rest. You pay only for what the cheap vendors miss.

## Ordering: cost × accuracy × rate limit

Order vendors by **expected cost per successful enrichment**, not sticker price. Calculate:

```
effective_cost = price_per_call / hit_rate
```

Example for email-from-name+company:

| Vendor | Price/call | Hit rate | Effective cost |
|---|---|---|---|
| Hunter.io | $0.004 | 55% | $0.007 |
| Apollo bulk | $0.01 | 75% | $0.013 |
| SerpAPI + LLM extract | $0.02 | 90% | $0.022 |
| Manual LinkedIn scrape | $0.05 | 60% | $0.083 |

Order: Hunter → Apollo → SerpAPI+LLM → dead letter. Effective cost per enriched lead ≈ $0.012 vs $0.083 if you'd started with the scraper.

## n8n implementation

### Structure

```
1. Trigger (Webhook / Schedule / Manual)
2. Set — normalize input (lowercase email, strip whitespace, extract domain)
3. MySQL / Google Sheets — check cache (was this already enriched in last 30 days?)
4. IF cache hit → return cached → END
5. HTTP Request: Hunter.io
6. IF match found → Set enriched data → merge back → END
7. HTTP Request: Apollo (on Hunter miss)
8. IF match → merge → END
9. HTTP Request: SerpAPI
10. Information Extractor (LangChain) — extract contact from SERP results
11. IF match → merge → END
12. MySQL insert — dead letter table
```

### Critical configuration

Each HTTP Request node needs:

- `continueOnFail: true` — so one vendor's 500 doesn't kill the pipeline
- `retry.maxTries: 2` with `retry.waitBetweenTries: 3000`
- Timeout: 10s. Waterfalls with 6 vendors at 30s timeouts = 3-minute-per-lead worst case
- Auth via n8n **credentials**, never inline

### The IF check pattern

After each vendor, check BOTH response status AND payload content:

```javascript
// In an IF node expression:
={{ 
  $('Hunter Request').item.json.error 
    ? false 
    : $('Hunter Request').item.json.data?.email != null 
}}
```

Don't just check `.error` — vendors often return 200 with empty results on a miss.

### Cache layer (mandatory)

Enrichment data goes stale in ~30 days but doesn't change daily. Cache aggressively:

```sql
CREATE TABLE enrichment_cache (
  input_key VARCHAR(255) PRIMARY KEY,  -- normalized email/domain
  enriched_data JSON,
  source VARCHAR(50),                   -- which vendor hit
  enriched_at TIMESTAMP,
  INDEX idx_enriched_at (enriched_at)
);
```

Before calling ANY vendor, SELECT on `input_key` WHERE `enriched_at > NOW() - INTERVAL 30 DAY`. Cache hit rate of 40% is normal after a few weeks — that's 40% cost reduction for free.

## LLM extract stage (the Stage 3 secret weapon)

When paid vendors miss, SerpAPI + LLM extract works 80%+ of the time:

1. `HTTP Request` → SerpAPI search: `"{{ $json.first_name }} {{ $json.last_name }}" "{{ $json.company }}" site:linkedin.com`
2. `Information Extractor` with schema:
   ```json
   {
     "linkedin_url": "string",
     "title": "string",
     "location": "string",
     "confidence": "number (0-1)"
   }
   ```
3. IF `confidence < 0.7` → treat as miss

Use Groq `llama-3.3-70b-versatile` for extract — it's fast enough that even at 90% hit rate, per-lead cost stays under 2 cents.

## Rate limits (the silent killer)

Every vendor has limits. Hitting them burns waterfalls silently.

| Vendor | Typical limit | n8n handling |
|---|---|---|
| Hunter.io | 50/min (free tier 25/day) | `Split In Batches` size=1, `Wait` 1200ms between |
| Apollo | 600/min enterprise | Usually fine at batch size 10 |
| SerpAPI | Plan-dependent | Check headers, backoff if `X-RateLimit-Remaining < 5` |

For high-volume pipelines, run the waterfall as a **sub-workflow** called from a `Split In Batches` parent with `batchSize: 10, waitBetweenBatches: 60000`.

## Anti-patterns

- **Parallelizing vendors.** Running all 3 in parallel and picking the best defeats the point — you pay for all 3 on every lead. Waterfall = sequential with early exit.
- **No dead letter.** Unenrichable leads must go somewhere queryable so you can spot-check WHY they're missing. Otherwise vendor regressions go unnoticed.
- **Same timeout across vendors.** Cheap vendors are usually fast (set 5s). Scrapers need 30s. Tune per vendor.
- **No vendor health monitoring.** Add a dashboard query: hit rate per vendor per week. When Hunter's hit rate drops from 55% to 20%, you want to know immediately.

## Output contract

Whatever the source, the waterfall should output a **unified schema** downstream consumers can rely on:

```json
{
  "email": "string",
  "full_name": "string",
  "company": "string",
  "linkedin_url": "string|null",
  "title": "string|null",
  "enrichment_source": "hunter|apollo|serpapi_llm",
  "confidence": "number (0-1)",
  "enriched_at": "ISO timestamp"
}
```

Add a final `Set` node to normalize each vendor's response into this schema before returning.

## Reference

- `references/waterfall-template.json` — importable 18-node starter waterfall
