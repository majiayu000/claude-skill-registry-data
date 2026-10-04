---
name: seo-content
description: >
  Content quality and E-E-A-T analysis with AI citation readiness assessment.
  Enhanced with live Ahrefs (actual keyword rankings, positions) and GSC (search
  query performance) data to validate static E-E-A-T analysis with real user
  behavior. Use when user says "content quality", "E-E-A-T", "content analysis",
  "readability check", "thin content", or "content audit".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
  - ToolSearch
---

# Content Quality & E-E-A-T Analysis

<!-- Updated: 2026-06-10 -->

## E-E-A-T Framework (per Google's Search Quality Rater Guidelines and the "Creating helpful, reliable, people-first content" doc)

Read `seo/references/eeat-framework.md` for full criteria.

> **How Google uses E-E-A-T:** E-E-A-T itself is NOT a direct ranking factor.
> Google's automated systems use a mix of factors to reward content people
> find helpful; quality raters use E-E-A-T to evaluate whether those systems
> are working — rater data is not used directly in ranking.
> Of the E-E-A-T family, **Trust is the most important member** — the other
> three contribute to trust, and content need not demonstrate all of them.

### Experience (first-hand signals)
- Original research, case studies, before/after results
- Personal anecdotes, process documentation
- Unique data, proprietary insights
- Photos/videos from direct experience

### Expertise
- Author credentials, certifications, bio
- Professional background relevant to topic
- Technical depth appropriate for audience
- Accurate, well-sourced claims

### Authoritativeness
- External citations, backlinks from authoritative sources
- Brand mentions, industry recognition
- Published in recognized outlets
- Cited by other experts

### Trustworthiness
- Contact information, physical address
- Privacy policy, terms of service
- Customer testimonials, reviews
- Date stamps, transparent corrections
- Secure site (HTTPS)

## Content Metrics

### Word Count Analysis
Compare against page type minimums:
| Page Type | Minimum |
|-----------|---------|
| Homepage | 500 |
| Service page | 800 |
| Blog post | 1,500 |
| Product page | 300+ (400+ for complex products) |
| Location page | 500-600 |

> **Important:** These are **topical coverage floors**, not targets. Google has confirmed word count is NOT a direct ranking factor. The goal is comprehensive topical coverage — a 500-word page that thoroughly answers the query will outrank a 2,000-word page that doesn't. Use these as guidelines for adequate coverage depth, not rigid requirements.

### Readability
- Flesch Reading Ease: target 60-70 for general audience

> **Note:** Flesch Reading Ease is a useful proxy for content accessibility but is NOT a direct Google ranking factor. John Mueller has confirmed Google does not use basic readability scores for ranking. Yoast deprioritized Flesch scores in v19.3. Use readability analysis as a content quality indicator, not as an SEO metric to optimize directly.
- Grade level: match target audience
- Sentence length: average 15-20 words
- Paragraph length: 2-4 sentences

### Keyword Optimization
- Primary keyword in title, H1, first 100 words
- Natural density (1-3%)
- Semantic variations present
- No keyword stuffing

### Content Structure
- Logical heading hierarchy (H1 → H2 → H3)
- Scannable sections with descriptive headings
- Bullet/numbered lists where appropriate
- Table of contents for long-form content

### Multimedia
- Relevant images with proper alt text
- Videos where appropriate
- Infographics for complex data
- Charts/graphs for statistics

### Internal Linking
- 3-5 relevant internal links per 1000 words
- Descriptive anchor text
- Links to related content
- No orphan pages

### External Linking
- Cite authoritative sources
- Open in new tab for user experience
- Reasonable count (not excessive)

## AI Content Assessment (Sept 2025 QRG addition)

Google's raters now formally assess whether content appears AI-generated.

### Acceptable AI Content
- Demonstrates genuine E-E-A-T
- Provides unique value
- Has human oversight and editing
- Contains original insights

### Low-Quality AI Content Markers
- Generic phrasing, lack of specificity
- No original insight
- Repetitive structure across pages
- No author attribution
- Factual inaccuracies

> **Helpful Content System (March 2024):** The Helpful Content System was merged into Google's core ranking algorithm during the March 2024 core update. It no longer operates as a standalone classifier. Helpfulness signals are now weighted within every core update — the same principles apply (people-first content, demonstrating E-E-A-T, satisfying user intent), but enforcement is continuous rather than through separate HCU updates.

## AI Citation Readiness (GEO signals)

Optimize for AI search engines (ChatGPT, Perplexity, Google AI Overviews):

- Clear, quotable statements with statistics/facts
- Structured data (especially for data points)
- Strong heading hierarchy (H1→H2→H3 flow)
- Answer-first formatting for key questions
- Tables and lists for comparative data
- Clear attribution and source citations

### AI Search Visibility & GEO (2025-2026)

**Google AI Mode** launched publicly in May 2025 as a separate tab in Google Search, available in 180+ countries. Unlike AI Overviews (which appear above organic results), AI Mode provides a fully conversational search experience with **zero organic blue links** — making AI citation the only visibility mechanism.

**Key optimization strategies for AI citation:**
- **Structured answers:** Clear question-answer formats, definition patterns, and step-by-step instructions that AI systems can extract and cite
- **First-party data:** Original research, statistics, case studies, and unique datasets are highly cited by AI systems
- **Schema markup:** Article, FAQ (for non-Google AI platforms), and structured content schemas help AI systems parse and attribute content
- **Topical authority:** AI systems preferentially cite sources that demonstrate deep expertise — build content clusters, not isolated pages
- **Entity clarity:** Ensure brand, authors, and key concepts are clearly defined with structured data (Organization, Person schema)
- **Multi-platform tracking:** Monitor visibility across Google AI Overviews, AI Mode, ChatGPT, Perplexity, and Bing Copilot — not just traditional rankings. Treat AI citation as a standalone KPI alongside organic rankings and traffic.

**Generative Engine Optimization (GEO):**
GEO is the emerging discipline of optimizing content specifically for AI-generated answers. Key GEO signals include: quotability (clear, concise extractable facts), attribution (source citations within your content), structure (well-organized heading hierarchy), and freshness (regularly updated data). Cross-reference the `seo-geo` skill for detailed GEO workflows.

## Content Freshness

- Publication date visible
- Last updated date if content has been revised
- Flag content older than 12 months without update for fast-changing topics

## Output

### Content Quality Score: XX/100

### E-E-A-T Breakdown
| Factor | Score | Key Signals |
|--------|-------|-------------|
| Experience | XX/25 | ... |
| Expertise | XX/25 | ... |
| Authoritativeness | XX/25 | ... |
| Trustworthiness | XX/25 | ... |

### AI Citation Readiness: XX/100

### Issues Found
### Recommendations

---

## Live Data Insights (MCP Overlay)

> This section appears only when MCP data sources are available. The static analysis above is complete and unchanged regardless of MCP availability.

### MCP Availability Check

Follow the self-contained check pattern from `seo/references/mcp-degradation.md`:
1. Use ToolSearch with query "+ahrefs" — if tools returned, Ahrefs is available
2. Use ToolSearch with query "+google-search-console" — if tools returned, GSC is available
3. Proceed with whichever MCPs are available; skip sections for unavailable MCPs

### Actual Keyword Rankings (Ahrefs)

If Ahrefs available: fetch `site-explorer-organic-keywords` filtered to the specific URL being analyzed (full URL with https://). Show what Google actually associates with this content — this complements the static keyword analysis by replacing estimation with real ranking data. Add a `### Actual Keyword Rankings (Ahrefs)` section:

```
### Actual Keyword Rankings (Ahrefs)

Top 10 keywords this page actually ranks for:

| Keyword | Position | Monthly Volume | Est. Traffic | Traffic % |
|---------|----------|----------------|--------------|-----------|
| keyword 1 | #X | X,XXX | XXX | X.X% |
| keyword 2 | #XX | X,XXX | XXX | X.X% |
| ... | ... | ... | ... | ... |

> Position data reflects current Google rankings. Compare with static keyword analysis above to identify gaps between targeted vs. actual ranking keywords.
```

**Note:** `cpc` values from Ahrefs are in cents — divide by 100 before displaying as USD.

### Search Query Performance (GSC)

If GSC available: fetch `get_search_analytics` filtered to this specific URL for the last 28 days. Add a `### Search Query Performance (GSC)` section to validate E-E-A-T signals with real user behavior data:

```
### Search Query Performance (Google Search Console — Last 28 Days)

| Metric | Value |
|--------|-------|
| Total Impressions | XX,XXX |
| Total Clicks | X,XXX |
| Overall CTR | X.X% |
| Average Position | X.X |

**Top Queries Triggering This Page:**

| Query | Impressions | Clicks | CTR | Avg Position |
|-------|-------------|--------|-----|--------------|
| query 1 | X,XXX | XXX | X.X% | X.X |
| ... | ... | ... | ... | ... |

> High impressions with low CTR on relevant queries suggests title/meta description optimization is needed.
> CTR displayed as percentage (API returns decimal — multiply by 100 for display).
```

---

## Data Sources

Always append this footer to the content analysis output:

| Source | Status | Data Provided |
|--------|--------|---------------|
| Static Analysis | Always available | E-E-A-T scoring, readability, keyword density, structure, AI citation readiness |
| Ahrefs MCP | Available / Not connected | Actual ranking keywords, positions, search volumes, traffic estimates |
| GSC MCP | Available / Not connected | Impressions, clicks, CTR, avg position, top queries for this page |
