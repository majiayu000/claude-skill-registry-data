---
name: seo-technical
description: >
  Technical SEO audit across 8 categories: crawlability, indexability, security,
  URL structure, mobile, Core Web Vitals, structured data, and JavaScript
  rendering. Enhanced with live GSC (indexing status, crawl data) and Ahrefs
  (backlink profile) data when MCPs are available. Use when user says "technical
  SEO", "crawl issues", "robots.txt", "Core Web Vitals", "site speed", or
  "security headers".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Technical SEO Audit

## Categories

### 1. Crawlability
- robots.txt: exists, valid, not blocking important resources
- XML sitemap: exists, referenced in robots.txt, valid format
- Noindex tags: intentional vs accidental
- Crawl depth: important pages within 3 clicks of homepage
- JavaScript rendering: check if critical content requires JS execution
- Crawl budget: for large sites (>10k pages), efficiency matters

#### AI Crawler Management

As of 2025-2026, AI companies actively crawl the web to train models and power AI search. Managing these crawlers via robots.txt is a critical technical SEO consideration.

**Known AI crawlers:**

| Crawler | Company | robots.txt token | Purpose |
|---------|---------|-----------------|---------|
| GPTBot | OpenAI | `GPTBot` | Model training |
| ChatGPT-User | OpenAI | `ChatGPT-User` | Real-time browsing |
| ClaudeBot | Anthropic | `ClaudeBot` | Model training |
| PerplexityBot | Perplexity | `PerplexityBot` | Search index + training |
| Bytespider | ByteDance | `Bytespider` | Model training |
| Google-Extended | Google | `Google-Extended` | Gemini training (NOT search) |
| CCBot | Common Crawl | `CCBot` | Open dataset |

**Key distinctions:**
- Blocking `Google-Extended` prevents Gemini training use but does NOT affect Google Search indexing or AI Overviews (those use `Googlebot`)
- Blocking `GPTBot` prevents OpenAI training but does NOT prevent ChatGPT from citing your content via browsing (`ChatGPT-User`)
- ~3-5% of websites now use AI-specific robots.txt rules

**Example — selective AI crawler blocking:**
```
# Allow search indexing, block AI training crawlers
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

# Allow all other crawlers (including Googlebot for search)
User-agent: *
Allow: /
```

**Recommendation:** Consider your AI visibility strategy before blocking. Being cited by AI systems drives brand awareness and referral traffic. Cross-reference the `seo-geo` skill for full AI visibility optimization.

### 2. Indexability
- Canonical tags: self-referencing, no conflicts with noindex
- Duplicate content: near-duplicates, parameter URLs, www vs non-www
- Thin content: pages below minimum word counts per type
- Pagination: rel=next/prev or load-more pattern
- Hreflang: correct for multi-language/multi-region sites
- Index bloat: unnecessary pages consuming crawl budget

### 3. Security
- HTTPS: enforced, valid SSL certificate, no mixed content
- Security headers:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Frame-Options
  - X-Content-Type-Options
  - Referrer-Policy
- HSTS preload: check preload list inclusion for high-security sites

### 4. URL Structure
- Clean URLs: descriptive, hyphenated, no query parameters for content
- Hierarchy: logical folder structure reflecting site architecture
- Redirects: no chains (max 1 hop), 301 for permanent moves
- URL length: flag >100 characters
- Trailing slashes: consistent usage

### 5. Mobile Optimization
- Responsive design: viewport meta tag, responsive CSS
- Touch targets: minimum 48x48px with 8px spacing
- Font size: minimum 16px base
- No horizontal scroll
- Mobile-first indexing: Google indexes mobile version. **Mobile-first indexing is 100% complete as of July 5, 2024.** Google now crawls and indexes ALL websites exclusively with the mobile Googlebot user-agent.

### 6. Core Web Vitals
- **LCP** (Largest Contentful Paint): target <2.5s
- **INP** (Interaction to Next Paint): target <200ms
  - INP replaced FID on March 12, 2024. FID was fully removed from all Chrome tools (CrUX API, PageSpeed Insights, Lighthouse) on September 9, 2024. Do NOT reference FID anywhere.
- **CLS** (Cumulative Layout Shift): target <0.1
- Evaluation uses 75th percentile of real user data
- Use PageSpeed Insights API or CrUX data if MCP available

### 7. Structured Data
- Detection: JSON-LD (preferred), Microdata, RDFa
- Validation against Google's supported types
- See seo-schema skill for full analysis

### 8. JavaScript Rendering
- Check if content visible in initial HTML vs requires JS
- Identify client-side rendered (CSR) vs server-side rendered (SSR)
- Flag SPA frameworks (React, Vue, Angular) that may cause indexing issues
- Verify dynamic rendering setup if applicable

#### JavaScript SEO — Canonical & Indexing Guidance (December 2025)

Google updated its JavaScript SEO documentation in December 2025 with critical clarifications:

1. **Canonical conflicts:** If a canonical tag in raw HTML differs from one injected by JavaScript, Google may use EITHER one. Ensure canonical tags are identical between server-rendered HTML and JS-rendered output.
2. **noindex with JavaScript:** If raw HTML contains `<meta name="robots" content="noindex">` but JavaScript removes it, Google MAY still honor the noindex from raw HTML. Serve correct robots directives in the initial HTML response.
3. **Non-200 status codes:** Google does NOT render JavaScript on pages returning non-200 HTTP status codes. Any content or meta tags injected via JS on error pages will be invisible to Googlebot.
4. **Structured data in JavaScript:** Product, Article, and other structured data injected via JS may face delayed processing. For time-sensitive structured data (especially e-commerce Product markup), include it in the initial server-rendered HTML.

**Best practice:** Serve critical SEO elements (canonical, meta robots, structured data, title, meta description) in the initial server-rendered HTML rather than relying on JavaScript injection.

### 9. IndexNow Protocol
- Check if site supports IndexNow for Bing, Yandex, Naver
- Supported by search engines other than Google
- Recommend implementation for faster indexing on non-Google engines

## Output

### Technical Score: XX/100

### Category Breakdown
| Category | Status | Score |
|----------|--------|-------|
| Crawlability | ✅/⚠️/❌ | XX/100 |
| Indexability | ✅/⚠️/❌ | XX/100 |
| Security | ✅/⚠️/❌ | XX/100 |
| URL Structure | ✅/⚠️/❌ | XX/100 |
| Mobile | ✅/⚠️/❌ | XX/100 |
| Core Web Vitals | ✅/⚠️/❌ | XX/100 |
| Structured Data | ✅/⚠️/❌ | XX/100 |
| JS Rendering | ✅/⚠️/❌ | XX/100 |

### Critical Issues (fix immediately)
### High Priority (fix within 1 week)
### Medium Priority (fix within 1 month)
### Low Priority (backlog)

---

## Live Data Insights (MCP Overlay)

> This section appears only when MCP data sources are available. The static analysis above is complete and unchanged regardless of MCP availability.

### MCP Availability Check

Follow the self-contained check pattern from `seo/references/mcp-degradation.md`:
1. Use ToolSearch with query "+google-search-console" — if tools returned, GSC is available
2. Use ToolSearch with query "+ahrefs" — if tools returned, Ahrefs is available
3. Proceed with whichever MCPs are available; skip sections for unavailable MCPs

See `seo/references/gsc-api-reference.md` for GSC tool call details and property format.

### Live Indexing Status (GSC)

If GSC available: fetch `inspect_url` for the target URL to get live indexing data. Add a `### Live Indexing Status (GSC)` section:

```
### Live Indexing Status (Google Search Console)

| Field | Value |
|-------|-------|
| Indexing Status | Indexed / Not Indexed |
| Last Crawled | YYYY-MM-DD |
| Crawled As | Desktop / Mobile |
| Canonical (Google-selected) | https://example.com/page |
| Canonical (User-declared) | https://example.com/page |
| Mobile Usability | Usable / Issues found |
| Verdict | PASS / FAIL |
```

If the URL is not indexed, show the specific reason returned by GSC (e.g., "Page with redirect", "Excluded by 'noindex' tag", "Crawled - currently not indexed", etc.).

If GSC is unavailable, note: *"GSC data unavailable — live indexing status requires Google Search Console MCP."*

### Backlink Profile Summary (Ahrefs)

If Ahrefs available: fetch `site-explorer-backlinks-stats` (or `site-explorer-metrics`) for the domain. Add a `### Backlink Profile Summary` section — useful for technical context (e.g., a new site with few referring domains may explain slow Googlebot crawl frequency):

```
### Backlink Profile Summary (Ahrefs)

| Metric | Value |
|--------|-------|
| Domain Rating (DR) | XX/100 |
| Total Backlinks | XX,XXX |
| Referring Domains | X,XXX |
| Dofollow Referring Domains | X,XXX |
| Dofollow Ratio | XX% |

> Context: Sites with low DR (<20) and few referring domains often experience slower Googlebot crawl rates and may see delays in indexing new content.
```

**Note:** All monetary values from Ahrefs are in cents — divide by 100 before displaying as USD.

---

## Data Sources

Always append this footer to the technical audit output:

| Source | Status | Data Provided |
|--------|--------|---------------|
| Static Analysis | Always available | robots.txt, sitemap, canonicals, security headers, mobile, CWV signals, JS rendering |
| GSC MCP | Available / Not connected | Live indexing status, crawl date, canonical selection, mobile usability |
| Ahrefs MCP | Available / Not connected | Total backlinks, referring domains, dofollow ratio, DR for crawl context |
