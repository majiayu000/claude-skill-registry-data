---
name: seo-audit
description: Audit websites, web apps, and local dev servers for technical SEO, crawlability, indexability, metadata, structured data, sitemap and robots hygiene, content coverage, freshness, and basic performance.
---

# SEO Audit

## Quick Start

Run the deterministic audit first when a site is accessible over HTTP:

```bash
python3 ~/.codex/skills/seo-audit/scripts/seo_audit.py --base-url http://localhost:3000 --sample-limit 80
```

For production:

```bash
python3 ~/.codex/skills/seo-audit/scripts/seo_audit.py --base-url https://www.example.com --sample-limit 120
```

For custom route maps, pass repeated path flags:

```bash
python3 ~/.codex/skills/seo-audit/scripts/seo_audit.py \
  --base-url https://www.example.com \
  --public-path / --public-path /pricing --public-path /blog \
  --private-path /login --private-path /account \
  --sample-prefix /blog/ --sample-prefix /docs/
```

Use the script output as evidence, then apply judgment for business relevance, keyword intent, conversion quality, and content gaps.

## Workflow

1. Confirm the target environment: local preview, staging, or production.
2. Run the audit script and save the JSON or Markdown output if the work needs comparison over time.
3. Check critical public pages manually or with a browser when visual or responsive risk matters.
4. Prioritize fixes in this order: crawl blockers, noindex/canonical mistakes, sitemap gaps, private-page leakage, missing titles/descriptions/H1s, invalid structured data, weak internal linking, stale or inaccurate content, performance regressions.
5. Re-run the audit after changes and report the before/after score, blockers fixed, remaining risks, and deployment-readiness judgment.

## Scoring Standard

Use the score as a quality gate, not as vanity:

- `95-100`: Excellent. Ship if analytics and conversion instrumentation are also intact.
- `90-94`: Strong. Ship, then fix remaining non-blocking issues.
- `80-89`: Good but not finished. Fix high-impact misses before a major launch.
- `70-79`: Risky. Important crawl, metadata, content, or performance gaps remain.
- `<70`: Do not ship as an SEO push unless there is a separate urgent reason.

The bundled script grades:

- Crawlability and indexing, including `robots.txt`, sitemap, status codes, private route leakage, and canonical tags.
- On-page metadata, including title, description, H1, Open Graph, internal links, viewport, and language.
- Structured data validity and rich-result eligibility risks.
- Content coverage, including expected public pages and sitemap-discovered content samples.
- Basic response-time and document-size signals.

## Judgment Rules

- Treat a public SEO URL that redirects to login as a critical failure.
- Treat `robots.txt` blocking a valuable public URL as a critical failure.
- Prefer no structured data over invalid, unsupported, or misleading structured data.
- Do not add ratings, reviews, app availability, prices, or competitor claims unless they are real and current.
- Do not optimize only for crawlers. The page must answer the search intent and make the next user action obvious.
- For programmatic SEO, require crawlable hub pages that link to generated pages. A sitemap alone is not enough.
- For app SEO, verify web-to-app metadata, store links, and pricing copy against current live state.

## Resources

- `scripts/seo_audit.py`: deterministic HTTP/HTML/XML audit with a weighted score and prioritized findings.
- `references/google-search-checklist.md`: compact reference for Google-oriented SEO decisions.

