---
name: anysite-market-research
description: Conduct comprehensive market research using Y Combinator data, SEC filings, social media insights, and web scraping via anysite MCP server. Analyze tech markets, research startup ecosystems, study public companies, identify market opportunities, and understand competitive dynamics. Supports startup discovery, industry analysis, public company research, and social sentiment analysis. Use when users need to analyze market opportunities, research industries, evaluate startups, study public companies, or gather market intelligence for strategic planning and investment decisions.
---

# anysite Market Research

Comprehensive market research using Y Combinator, SEC, social media, and web data through anysite MCP. Analyze tech markets, research startups, and study competitive landscapes.

## Overview

- **Research startup ecosystems** via Y Combinator data
- **Analyze public companies** through SEC filings
- **Gather market intelligence** from social platforms
- **Study industry trends** across communities
- **Identify market opportunities** through data analysis

**Coverage**: 70% - Excellent for tech/startup markets; pivoted from local business to tech focus

## Supported Platforms

- ✅ **Y Combinator**: Startup research, batch analysis, founder discovery, funding data
- ✅ **SEC**: Public company filings, financial data, disclosures
- ✅ **Reddit**: Market sentiment, community insights, product discussions
- ✅ **LinkedIn**: Industry trends, company intelligence, professional discussions
- ✅ **Twitter/X**: Market pulse, news, influencer opinions
- ✅ **Web Scraping**: Company websites, industry reports, market data

## v2 MCP Tool Interface

All data fetching uses the universal `execute()` meta-tool. Always call `discover(source, category)` first if you need to verify endpoint names or parameters.

**Core workflow**:
1. `execute(source, category, endpoint, params)` -- fetch data (returns first page + `cache_key`)
2. `get_page(cache_key, offset, limit)` -- paginate through remaining results
3. `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` -- filter/sort/aggregate cached data without new API calls
4. `export_data(cache_key, format)` -- export to CSV, JSON, or JSONL for deliverables

**Error handling**: check response for `llm_hint` field -- it contains actionable guidance when calls fail or return partial data.

## Quick Start

**Step 1: Define Research Scope**

Choose focus:
- Startup ecosystem: `execute("yc", "search", "search", {"query": ...})`
- Public companies: `execute("sec", "search", "search", {"query": ...})`
- Industry sentiment: `execute("reddit", "search", "search", {"query": ...})`, `execute("twitter", "search", "search_users", {"query": ...})`
- Company intelligence: `execute("linkedin", "search", "search_companies", {...})`

**Step 2: Gather Data**

Execute searches:
```
# Startup research
execute("yc", "search", "search", {"query": "fintech", "batch": "W24,S23"})

# Public company research
execute("sec", "search", "search", {"query": "tech company"})

# Market sentiment
execute("reddit", "search", "search", {"query": "fintech trends"})
→ use get_page(cache_key, offset, limit) to collect up to 100 results
```

**Step 3: Analyze Results**

Use `query_cache()` to slice data without re-fetching:
```
# Count startups by category
query_cache(cache_key, aggregate={"field": "category", "function": "count"})

# Filter high-engagement posts
query_cache(cache_key, conditions=[{"field": "score", "operator": ">", "value": 50}], sort_by={"field": "score", "order": "desc"})
```

Extract insights:
- Market size indicators
- Competitive landscape
- Technology trends
- Consumer sentiment
- Funding patterns

**Step 4: Synthesize Findings**

Use `export_data(cache_key, "csv")` or `export_data(cache_key, "json")` to deliver:
- Market opportunity assessment
- Competitive analysis
- Trend identification
- Strategic recommendations

## Common Workflows

### Workflow 1: Startup Ecosystem Analysis

**Scenario**: Analyze fintech startup landscape

**Steps**:

1. **Find Startups**
```
execute("yc", "search", "search", {
  "query": "fintech",
  "batch": "W24,S23,W23,S22"
})
→ use get_page(cache_key, offset, limit) to paginate through all results
```

2. **Categorize by Focus**
```
For each startup:
  execute("yc", "company", "get", {"slug": company_slug})

Group by:
- Payments
- Lending
- Investment/Trading
- Banking
- Insurance
- B2B fintech tools

Or use query_cache to group:
  query_cache(cache_key, group_by="category")
```

3. **Analyze Patterns**
```
Identify:
- Hot subcategories (most startups)
- Team size distribution
- Geographic concentration
- Common tech stacks (from job postings)

Use query_cache for aggregation:
  query_cache(cache_key, aggregate={"field": "team_size", "function": "avg"})
```

4. **Research Traction**
```
For promising startups:
  execute("linkedin", "search", "search_companies", {"keywords": startup_name})
  → Check employee growth

  execute("twitter", "search", "search_users", {"query": startup_name})
  → Check social presence and buzz

  execute("webparser", "parse", "parse", {"url": startup_website})
  → Check positioning and features
```

5. **Identify White Spaces**
```
Compare:
- Overcrowded categories
- Underserved segments
- Emerging opportunities
- Geographic gaps
```

**Expected Output**:
- 50-100 startup landscape map
- Category distribution
- Funding trends
- Market gaps identified
- Competitive intensity by segment

Use `export_data(cache_key, "csv")` to deliver the startup list as a spreadsheet.

### Workflow 2: Public Company Competitive Analysis

**Scenario**: Research public competitors in cloud infrastructure

**Steps**:

1. **Find Companies**
```
execute("sec", "search", "search", {
  "query": "cloud"
})
→ use get_page(cache_key, offset, limit) to collect up to 50 results
```

2. **Get Financial Data**
```
For each company:
  execute("sec", "document", "get", {"url": document_url})

Extract:
- Revenue and growth
- Operating margins
- R&D spending
- Geographic breakdown
- Risk factors mentioned
```

3. **Analyze Strategy**
```
From 10-K filings:
- Business model
- Target markets
- Competitive advantages
- Growth initiatives
- Challenges and risks
```

4. **Track Changes**
```
Compare year-over-year:
- Revenue growth trends
- Market focus shifts
- New initiatives
- Risk factor changes
```

5. **Supplement with Social Intel**
```
execute("linkedin", "search", "search_companies", {"keywords": company_name})
→ Employee count, hiring patterns

execute("linkedin", "company", "get", {"company": company_urn})
→ Company details and strategic messaging

execute("reddit", "search", "search", {"query": company_name})
→ Customer sentiment

Use query_cache to filter sentiment:
  query_cache(cache_key, conditions=[{"field": "text", "operator": "contains", "value": "review"}])
```

**Expected Output**:
- Competitive landscape map
- Financial benchmarks
- Strategic positioning
- Growth trajectories
- Market opportunities

Use `export_data(cache_key, "json")` for structured competitive data.

### Workflow 3: Industry Trend Analysis

**Scenario**: Understand AI/ML market evolution

**Steps**:

1. **YC Startup Trends**
```
execute("yc", "search", "search", {
  "query": "AI OR machine learning OR artificial intelligence"
})
→ use get_page(cache_key, offset, limit) to collect up to 200 results

Group by batch to see:
- Trend over time
- Focus area shifts
- Team size changes

query_cache(cache_key, group_by="batch", aggregate={"field": "id", "function": "count"})
```

2. **Public Market Signals**
```
execute("sec", "search", "search", {
  "query": "artificial intelligence"
})
→ use get_page(cache_key, offset, limit) to collect up to 50 results

Check 10-K mentions of:
- "AI" or "machine learning" frequency
- AI-related investments
- AI revenue segments
```

3. **Community Sentiment**
```
execute("reddit", "search", "search", {
  "query": "AI trends 2026"
})
→ use get_page(cache_key, offset, limit) to collect up to 100 results

Analyze for:
- Excitement vs. concern
- Adoption barriers
- Use case validation
- Technology maturity

query_cache(cache_key, sort_by={"field": "score", "order": "desc"})
```

4. **Professional Discussion**
```
execute("linkedin", "post", "search_posts", {
  "keywords": "artificial intelligence"
})

Check:
- Industry adoption
- Job market signals
- Skill requirements
- Thought leader opinions
```

5. **Web Intelligence**
```
For key AI companies:
  execute("webparser", "parse", "parse", {"url": website + "/blog"})
  → Technology updates, product launches
```

**Expected Output**:
- Market evolution timeline
- Technology adoption curves
- Sentiment analysis
- Opportunity identification
- Risk assessment

Use `export_data(cache_key, "csv")` for trend data tables.

## MCP Tools Reference (v2)

### Data Fetching
- `execute(source, category, endpoint, params)` -- Universal data fetcher; always returns `cache_key`

### Pagination
- `get_page(cache_key, offset, limit)` -- Load additional pages from a previous execute()

### Analysis
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` -- Filter, sort, and aggregate cached data

### Export
- `export_data(cache_key, format)` -- Export to CSV, JSON, or JSONL; returns download URL

### Y Combinator Research
- `execute("yc", "search", "search", {"query": ...})` -- Find startups by industry, batch, filters
- `execute("yc", "company", "get", {"slug": ...})` -- Get detailed company profile

### SEC Research
- `execute("sec", "search", "search", {"query": ...})` -- Find public companies and filings
- `execute("sec", "document", "get", {"url": ...})` -- Get full document content

### Social Intelligence
- `execute("reddit", "search", "search", {"query": ...})` -- Community insights and sentiment
- `execute("twitter", "search", "search_users", {"query": ...})` -- Real-time market pulse
- `execute("linkedin", "post", "search_posts", {"keywords": ...})` -- Professional trends

### Company Intelligence
- `execute("linkedin", "search", "search_companies", {"keywords": ...})` -- Find companies
- `execute("linkedin", "company", "get", {"company": ...})` -- Company details
- `execute("webparser", "parse", "parse", {"url": ...})` -- Extract website data

### Market Discovery
- Use `discover(source, category)` to explore available endpoints for any source
- `execute("webparser", "parse", "parse", {"url": ...})` -- Scrape any URL for market data

**Note**: Crunchbase endpoints are disabled in v2. Use LinkedIn company search and Y Combinator data as alternatives for company research.

## Market Analysis Frameworks

**TAM/SAM/SOM Analysis**:
```
Total Addressable Market (TAM):
- Count YC companies in category x avg market size
- SEC filing market size mentions
- Industry reports via execute("webparser", "parse", "parse", {"url": report_url})

Serviceable Addressable Market (SAM):
- Filter by geography, segment using query_cache()
- LinkedIn company search by ICP
- YC companies by batch/stage

Serviceable Obtainable Market (SOM):
- Realistic capture based on competition
- Competitive analysis via LinkedIn/social
- Market share indicators
```

**Porter's Five Forces**:
```
Using anysite v2 data:

1. Competitive Rivalry:
   - YC startups in space
   - LinkedIn company counts
   - Social mention volume

2. Threat of New Entrants:
   - Recent YC batches
   - Funding announcements
   - Talent movement (LinkedIn)

3. Supplier Power:
   - Technology dependencies
   - Integration partners

4. Buyer Power:
   - Customer reviews (Reddit)
   - Pricing transparency
   - Switching costs mentioned

5. Threat of Substitutes:
   - Alternative solutions
   - Adjacent markets
```

## Output Formats

**Chat Summary**:
- Key market insights
- Competitive landscape summary
- Opportunity identification
- Strategic recommendations

**CSV Export** (via `export_data(cache_key, "csv")`):
- Company list with metrics
- Market segmentation data
- Trend indicators

**JSON Export** (via `export_data(cache_key, "json")`):
- Complete research data
- Time-series analysis
- Cross-platform correlations

## Reference Documentation

- **[RESEARCH_METHODS.md](references/RESEARCH_METHODS.md)** - Market research methodologies, analysis frameworks, and data synthesis techniques

---

**Ready for market research?** Ask Claude to help you analyze markets, research startups, or study competitive landscapes using this skill!
