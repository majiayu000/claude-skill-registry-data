---
name: seo-news-discover
description: Use when auditing or planning publisher visibility for Google News, Discover, news search, or comparable freshness-sensitive surfaces across editorial policy, article pages, dates/bylines, corrections, large images, NewsArticle markup, news sitemaps, feeds, paywalls, and first-party reports; require current policy evidence and never promise inclusion, Top stories, Discover traffic, subscriptions, or revenue.
---

# News and Discover SEO

Audit the publisher system behind freshness-sensitive discovery: editorial transparency, article pages, dates and corrections, media, structured data, sitemaps/feeds, access state, and reporting.

Read [news-discover-protocol.md](references/news-discover-protocol.md) before a formal audit.

## Procedure

1. Define publications, editions/locales, article types, paywall/access model, newsroom owners, publishing cadence, and target surfaces.
2. Capture representative article/listing pages, raw/rendered metadata, bylines, dates, corrections, publisher/contact/about evidence, images, structured data, sitemap/feed rows, canonicals, and access directives.
3. Reconcile visible headline, author, publication/modification dates, section, image, publisher, paywall state, and NewsArticle/Article data. Preserve correction history rather than silently rewriting time-sensitive facts.
4. Inspect news sitemap membership and freshness, article retirement/update rules, crawl/index state, large-image delivery, responsive page experience, internal discovery, and feed parity.
5. Apply current platform content and spam policies to sensational, misleading, scraped, scaled, synthetic, or thin publication patterns. AI-assisted content still requires accuracy, quality, relevance, and accountable editorial review.
6. Use first-party News/Discover/Search performance exports when supplied. Discover is not a stable keyword-ranking surface; keep its reporting separate from query-based search and AI visibility.
7. Route schema to `seo-schema`, images to `seo-images`, content to `seo-content`, technical access to `seo-technical`, video to `seo-video`, and measurement to `seo-performance`.
8. Package formal findings as SEO Findings `1.1.0` with `news_property`, `web_page`, `sitemap`, or `media_set` targets and `news-discover`, `policy`, `freshness`, `content`, `media`, or `technical` categories.

## Guardrails

Never fabricate authorship, publication dates, updates, corrections, sources, images, reports, or policy eligibility. Do not refresh dates without substantive updates or promise inclusion and traffic.

## Formal evidence handoff

Package only supported observations as SEO Findings `1.1.0`. Let `<suite-root>` mean `${CLAUDE_PLUGIN_ROOT}` in Claude Code. In Codex, read `.seo-suite-runtime.json` beside this `SKILL.md` when present and use its `suite_root` value; otherwise use the absolute repository checkout, then run `python "<suite-root>/scripts/validate_seo_findings.py" validate-findings <bundle>/seo-findings.json --bundle <bundle>`. Keep the handoff provisional until this command passes.

## Output

Return the publisher/article scope, transparency and policy evidence, article metadata parity, sitemap/feed freshness, media/access findings, reporting limits, owners, verification, and rollback.
