---
name: site-auditor
description: Technical SEO site audit — meta tags, headings, canonical URLs, robots.txt, sitemap validation, internal links. No API key needed.
metadata: { "nyxclaw": { "emoji": "🔍", "requires": { "bins": ["node"] } } }
---

# Site Auditor

Technical SEO audit for any public website. Fetches pages and analyzes HTML structure.

## Full audit

```bash
node {baseDir}/scripts/audit.mjs "https://example.com" --pages 5
```

Options:

- `--pages <n>`: Number of internal pages to sample (default: 5, max: 20)
- `--timeout <ms>`: Request timeout (default: 10000)

## Output

JSON report with sections:

- **robots**: robots.txt analysis (rules, blocked paths, sitemap references)
- **sitemap**: sitemap.xml validation (URL count, lastmod freshness, errors)
- **pages**: per-page audit (title, description, h1, canonical, og:tags, internal links)
- **summary**: aggregate scores and issues by severity (CRITICAL, WARN, INFO)

## Notes

- Uses `fetch()` — does NOT execute JavaScript. HTTP 403/429 from JS-protected sites (Vercel, Cloudflare) is expected and does NOT mean Googlebot is blocked
- For indexation data, combine with `gsc-analytics` skill
- Always verify claims with `web_search site:domain.com` before reporting zero indexation
