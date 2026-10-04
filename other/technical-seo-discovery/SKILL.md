---
name: technical-seo-discovery
description: Diagnose, implement, and verify technical SEO and public-content discovery for web products, including crawlability, indexability, redirects, canonicals, metadata, structured data, sitemaps, rendering, internal links, quality thresholds, and search-console evidence.
---

# Technical SEO Discovery

Make valuable public pages discoverable without generating index bloat, duplicate routes, or thin programmatic content.

## Workflow

1. Inventory public page types, canonical hosts, authentication boundaries, rendering modes, and content quality signals.
2. Trace one URL through DNS, redirects, status, response headers, HTML robots, canonical, rendered content, internal links, and sitemap membership.
3. Separate crawl, index, canonicalization, rendering, quality, and ranking problems. Do not treat sitemap submission as indexing proof.
4. Define an indexability policy per page type. Private, empty, duplicate, filtered, and low-quality pages should not enter discovery surfaces.
5. Make public pages return stable `200` responses with server-rendered primary content, self-canonicals, useful titles and descriptions, and no accidental `noindex` header.
6. Build sitemap indexes or bounded sitemaps from canonical, indexable records only. Use stable URLs and meaningful modification timestamps.
7. Add internal links from crawlable hubs. Keep redirect chains to one hop and use one canonical host consistently.
8. Add structured data only when the visible page supports it. Never fabricate ratings, jobs, organizations, or profile claims.
9. Verify with raw headers, rendered HTML, robots and sitemap fetches, schema validation, and search-console inspection. Record recrawl latency as an external dependency.

## Programmatic SEO Rules

- Publish pages because they answer a distinct query, not because a database row exists.
- Do not index expired jobs, empty profiles, private posts, search results, or unlimited filter combinations.
- Paginated or faceted directories need bounded crawl paths and canonical policy.
- A large sitemap with zero indexed pages is a quality or technical signal to investigate, not a reason to create more URLs.
- Rankings require content usefulness, links, reputation, and time after technical eligibility is fixed.

## Delivery Contract

Provide or implement:

1. **URL inventory** - page types, canonical policy, and indexability rules.
2. **Diagnosis** - status, redirects, headers, robots, rendering, links, and sitemap evidence.
3. **Fixes** - routing, metadata, structured data, sitemaps, and quality gates.
4. **Verification** - commands or inspected responses for representative URLs.
5. **Monitoring** - coverage, crawl errors, indexed quality pages, impressions, and regressions.
6. **Expectations** - what is technically fixed versus what still depends on recrawl and ranking signals.

## Reference

Read [references/indexing-checklist.md](references/indexing-checklist.md) for a release or search-console incident.
