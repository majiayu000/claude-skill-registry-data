---
name: seo
description: SEO analysis and optimization skill. Analyze search performance, optimize content, track rankings, and improve organic traffic using Search Console, Ahrefs, SE Ranking, and Google Analytics data.
allowed-tools: Read, Write, Bash, WebSearch
---

# SEO Specialist Skill

Analyze and optimize your website's search performance using Search Console, Ahrefs, SE Ranking, and Google Analytics data.

## When to Use

- User asks about SEO performance
- User wants to analyze search rankings
- User needs content optimization recommendations
- User asks "how's our SEO?" or "check search performance"
- Creating or updating content for better search visibility

## Data Sources

### Search Console MCP
Use the Search Console MCP tools for organic search data:
- `mcp__search-console__get_performance_summary` - Overall traffic metrics
- `mcp__search-console__get_top_queries` - What people search for
- `mcp__search-console__get_top_pages` - Best performing pages
- `mcp__search-console__query_search_analytics` - Detailed analytics with filters

### Ahrefs MCP
Use for backlinks, domain authority, organic keywords, and competitor analysis:
- `mcp__ahrefs__doc` - Always call first to get input schema for other tools
- `mcp__ahrefs__site-explorer-domain-rating` - Domain authority score
- `mcp__ahrefs__site-explorer-metrics` - SEO performance overview
- `mcp__ahrefs__site-explorer-organic-keywords` - Keywords ranking for
- `mcp__ahrefs__site-explorer-top-pages` - Best pages by traffic
- `mcp__ahrefs__site-explorer-referring-domains` - Backlink sources
- `mcp__ahrefs__site-explorer-organic-competitors` - Competitor domains
- `mcp__ahrefs__serp-overview` - SERP analysis for a keyword
- `mcp__ahrefs__keywords-explorer-overview` - Keyword metrics (volume, difficulty)

### SE Ranking MCP
Use for keyword research, domain analysis, backlinks, SERP analysis, website audits, and AI search visibility:
- **Keyword Research**: `DATA_getSimilarKeywords`, `DATA_getRelatedKeywords`, `DATA_getLongTailKeywords`, `DATA_getKeywordQuestions`, `DATA_exportKeywords`
- **Domain Analysis**: `DATA_getDomainKeywords`, `DATA_getDomainCompetitors`, `DATA_getDomainOverviewHistory`
- **Backlinks**: `DATA_getAllBacklinks`, `DATA_getBacklinksMetrics`, `DATA_getBacklinksSummary`, `DATA_getBacklinksRefDomains`, `DATA_getDomainAuthority`
- **SERP**: `DATA_getSerpResults` - Full SERP analysis with organic, ads, featured snippets, AI Overview
- **Website Audit**: `DATA_createStandardAudit`, `DATA_getAuditReport`, `DATA_getCrawledPages`, `DATA_getIssuesByUrl`
- **AI Search Visibility**: `DATA_getAiOverview`, `DATA_getAiPromptsByBrand` - Track visibility in ChatGPT, Perplexity etc.

**Note**: SE Ranking tools are prefixed with `DATA_` (Data API) or `PROJECT_` (Project API). Call tools via the `mcp__se-ranking__*` namespace.

### Google Analytics
Use for engagement and behavior data:
```bash
bun .claude/skills/google-analytics/scripts/ga-report.ts pages
bun .claude/skills/google-analytics/scripts/ga-report.ts sources
```

## Workflow

### 1. Performance Check
```bash
mcp__search-console__get_performance_summary(days=28)
mcp__search-console__get_top_queries(days=28, limit=25)
mcp__search-console__get_top_pages(days=28, limit=25)
```

### 2. Identify Opportunities

**High impressions, low clicks (CTR < 2%):**
Pages ranking but not getting clicks. Opportunities:
- Improve title tags
- Write better meta descriptions
- Add structured data

**Position 5-20:**
On page 1-2 but not top positions. Opportunities:
- Content expansion
- Internal linking
- Backlink building

**High CTR, low impressions:**
Compelling content but not ranking well. Opportunities:
- Keyword optimization
- Content depth
- Technical SEO

### 3. Content Recommendations

For each underperforming page, provide:
1. Current metrics (impressions, clicks, CTR, position)
2. Target keywords (from query data)
3. Specific recommendations:
   - Title tag optimization
   - H1/H2 structure
   - Content gaps to fill
   - Internal linking opportunities

### 4. Track Progress

Document recommendations in: `docs/seo/YYYY-MM-DD-seo-review.md`

## Example Output

```markdown
# SEO Review - [Month Year]

## Performance Summary (Last 28 Days)
- Total Clicks: 1,234 (+12% vs previous)
- Impressions: 45,678
- Average CTR: 2.7%
- Average Position: 18.3

## Top Opportunities

### 1. "target keyword" - Position 8.2
**Page:** /blog/your-article
**Impressions:** 890 | Clicks: 34 | CTR: 3.8%

**Recommendations:**
- Add video tutorial (increases dwell time)
- Update for latest information
- Add structured data (HowTo schema)

## Action Items
1. [ ] Update top article with fresh content
2. [ ] Add structured data to top 5 how-to articles
3. [ ] Build internal links to underperforming pages
```

## Technical SEO Checks

When doing a full audit:
- Check robots.txt
- Verify sitemap generation
- Check canonical URLs
- Review Core Web Vitals via Google Analytics
- Review structured data implementation

## Related Skills Reference

These skill guides are available in `related-skills/` for deeper dives:

| Skill | File | Use When |
|-------|------|----------|
| **Schema Markup** | `schema-markup.md` | Adding structured data (FAQ, Article, HowTo) |
| **Copywriting** | `copywriting.md` | Optimizing titles, metas, headlines for CTR |
| **Page CRO** | `page-cro.md` | Improving page conversion rates |
| **Programmatic SEO** | `programmatic-seo.md` | Building pages at scale (glossary, comparisons) |
| **Competitor Pages** | `competitor-alternatives.md` | Creating "vs" and "alternative" pages |
| **Analytics Tracking** | `analytics-tracking.md` | Setting up GA4, measuring SEO impact |
