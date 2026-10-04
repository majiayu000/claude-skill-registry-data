---
name: mkt-seo-audit
version: 1.0.0
description: Audit a page or site across keywords, on-page, content gaps, and technical health, then return a prioritized impact/effort action list.
author: matrixx0070
tags: [marketing, seo, audit, content, technical, on-page]
capabilities: []
---

## When to use

Use this when you need to know why a page or site underperforms in search and what to fix first, covering the four layers that move rankings: keywords, on-page, content, and technical.

**Not for:** writing the optimized content itself (use mkt-draft-content), paid search/SEM, or claims that require live crawl or analytics data you do not have — mark those as unverifiable.

## Method

1. Set scope and intent. Confirm the URL(s), audience, and primary search intent (informational, commercial, navigational, transactional). Decision point: if intent is unknown, infer from the content and state it.
2. Keywords. Identify the primary keyword, secondary and long-tail variants, and intent match. Flag cannibalization or missing target terms.
3. On-page. Check title tag, meta description, H1 and heading hierarchy, keyword placement, internal links, image alt text, URL structure, and readability.
4. Content gaps. Compare coverage against ranking pages; find missing subtopics, thin sections, outdated facts, and schema/FAQ opportunities.
5. Technical. Review indexability (robots, canonical, sitemap), speed signals, mobile-friendliness, structured data, and broken links — at the level the available data allows. Decision point: mark what needs a live crawl to confirm.
6. Prioritize. Score each finding by impact and effort, then order the fixes with quick wins flagged.

## Example

Page targets "expense management software" but the H1 says "Welcome." On-page: no keyword in title, meta description missing, one H2. Content gap: ranking rivals all cover "integrations" and "pricing" — this page covers neither. Fix order: (1) rewrite title + H1 with keyword (high impact, low effort), (2) add meta description, (3) add integrations + pricing sections. Technical: canonical looks correct but needs a live crawl to confirm indexing.

## Pitfalls

- Chasing technical minutiae while the page targets the wrong keyword or intent.
- Recommending fixes without impact/effort scoring, so everything looks equally urgent.
- Asserting technical findings (index status, speed) that actually require a live crawl — label them.
- Optimizing for a keyword whose intent does not match the page's purpose.

## Output format

```
Scope + target keyword + search intent: <...>

Findings by layer:
- Keywords: <short list>
- On-page: <short list>
- Content gaps: <short list>
- Technical: <short list>

Issue table:
| Area | Issue | Impact (H/M/L) | Effort (H/M/L) | Fix |

Prioritized action plan: <top items first, quick wins flagged>
Unverifiable without live crawl / analytics: <...>
```

## Reference

### Audit workflow (run in this order)
1. Crawl the site (Screaming Frog / Sitebulb) for status codes, titles, canonicals, redirects.
2. Pull Google Search Console: top queries, pages, CTR, coverage/indexing errors.
3. Run PageSpeed Insights on the **3 templates** (home, a product/feature page, a blog post) — not all 20 pages; templates repeat.
4. Check `site:domain.com` and branded queries for what's actually indexed.

### P0 catastrophic checks (an audit that skips these can pass a broken site)
- **JS rendering:** compare rendered vs raw HTML (GSC URL Inspection "view crawled page"). SaaS sites on React/Next/Webflow often serve content only after JS — Google may see an empty `<div>`. This invalidates every downstream finding.
- **Accidental noindex / robots block** on production pages.
- **Staging/dev subdomain leak:** `site:staging.` / `site:dev.` — non-prod environments getting indexed (add noindex + auth).

### Core Web Vitals thresholds (good)
LCP < 2.5s · INP < 200ms · CLS < 0.1 · TTFB < 0.8s. Report each as good / needs-improvement / poor per template.

### On-page patterns
- Title: `Primary Keyword | Benefit — Brand` (≤ ~60 chars). Meta description ≤ ~155 chars with the keyword + a CTA.
- One H1 per page, keyword-bearing. **Anti-pattern:** generic H1s like "Welcome" or "Simple plans for everyone" that carry no query.
- Add OpenGraph + Twitter card tags (CTR in social/SERP snippets).
- SaaS-specific: build comparison / "vs" / alternatives pages — highest commercial-intent pipeline lever.

### Prioritization quadrant
Score each fix Impact (H/M/L) × Effort (H/M/L):
- High-impact / low-effort → **do now** (quick wins).
- High-impact / high-effort → **plan** (e.g. rendering fixes, content builds).
- Low-impact → backlog. **Backlinks** are the longest-lead-time lever — start early even though results lag.
