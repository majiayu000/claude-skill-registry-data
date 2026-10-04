---
name: anysite-competitor-intelligence
description: Competitive intelligence gathering using anysite MCP server across LinkedIn, social media, Y Combinator, and the web. Track competitor activities, analyze hiring patterns, monitor content strategies, benchmark market positioning, research startup competitors, and gather strategic intelligence. Supports LinkedIn (companies, employees, posts), Instagram, Twitter/X, Reddit, YouTube, Y Combinator, and web scraping. Use for tracking a LANDSCAPE of several competitors over time - competitive movements, hiring velocity, content strategies, market positioning across a set of companies. For a deep dossier on one named competitor use anysite-competitor-analyzer; for CRM-tied displacement lists use anysite-crm-competitor-intel.
---

# anysite Competitor Intelligence

Comprehensive competitive intelligence gathering using anysite MCP server. Track competitors across LinkedIn, social media, and the web to understand their strategies, monitor their activities, and identify competitive opportunities.

## Overview

The anysite Competitor Intelligence skill helps you:
- **Track competitor companies** on LinkedIn and Y Combinator
- **Monitor hiring patterns** to identify growth areas and strategic priorities
- **Analyze content strategies** across social platforms
- **Benchmark positioning** and messaging
- **Identify key employees** and leadership changes
- **Track competitive movements** like funding, launches, partnerships

This skill provides 90% coverage of competitive intelligence capabilities with excellent LinkedIn and social media monitoring.

## v2 Tool Interface

All data fetching uses the universal `execute()` meta-tool:

```
execute(source, category, endpoint, params) → returns data + cache_key
```

After fetching, use these for analysis and export:
- `get_page(cache_key, offset, limit)` — paginate through large result sets
- `query_cache(cache_key, conditions, sort_by, aggregate, group_by)` — filter/sort/aggregate cached data without re-fetching
- `export_data(cache_key, format)` — export to CSV, JSON, or JSONL for sharing

Always call `discover(source, category)` first if unsure about endpoint names or params.

**Error handling**: Check response for `llm_hint` field on errors — it provides actionable guidance (e.g., "Likely passed fsd_company URN instead of company: prefix").

## Supported Platforms

- **LinkedIn** (Primary): Company pages, employee search, post monitoring, job listings, growth tracking
- **Y Combinator**: Startup competitor research, funding data, batch analysis
- **Twitter/X**: Social presence monitoring, content strategy, engagement analysis
- **Reddit**: Community sentiment, product discussions, competitor mentions
- **Instagram**: Brand presence, visual content strategy, influencer partnerships
- **YouTube**: Video content, channel growth, community engagement
- **Web Scraping**: Company websites, press releases, blog content
- **SEC**: Public company filings for competitors

## Quick Start

### Step 1: Identify Competitors

Choose your competitor identification method:

| Goal | v2 Call | Output |
|------|---------|--------|
| Find similar companies | `execute("linkedin", "search", "search_companies", {"keywords": "...", "count": 50})` | Company list with metrics |
| Research startup competitors | `execute("yc", "search", "search_companies", {"query": "...", "count": 50})` | YC startups by industry/batch |
| Discover by employee search | `execute("linkedin", "search", "search_users", {...})` → extract companies | Companies from employee profiles |
| Find by keywords/industry | `execute("linkedin", "search", "search_companies", {"keywords": "...", "industry": "...", "count": 50})` | Filtered company list |

### Step 2: Gather Competitive Intelligence

Execute MCP tools to collect competitor data:

**Company Profile Analysis**
```
execute("linkedin", "company", "company", {"company": "competitor-name"})
→ Returns: Description, size, location, website, specialties, URN
```

**Employee Intelligence**
```
execute("linkedin", "search", "search_users", {
  "company_keywords": "Competitor Inc",
  "title": "VP OR Director OR Head",
  "count": 50
})
→ Returns: Key employees, org structure insights
→ Use get_page(cache_key, 10, 50) to load more results
```

**Hiring Velocity Analysis**
```
execute("linkedin", "company", "company_employee_stats", {
  "urn": {"type": "company", "value": "<company_id>"}
})
→ Returns: Growth metrics, department distribution
→ Use query_cache(cache_key, sort_by=[{"field": "count", "order": "desc"}]) to rank departments
```

**Content Strategy**
```
execute("linkedin", "company", "company_posts", {
  "urn": {"type": "company", "value": "<company_id>"},
  "count": 20
})
→ Returns: Recent posts, engagement, messaging themes
→ Use query_cache(cache_key, aggregate=[{"field": "reactions", "function": "avg"}]) for engagement stats
```

### Step 3: Process and Analyze

Analyze gathered data for:
- **Growth signals**: Hiring velocity, funding, expansion
- **Strategic priorities**: Department hiring, job postings, content themes
- **Market positioning**: Messaging, target audience, value props
- **Competitive threats**: New products, partnerships, key hires

Use `query_cache()` to filter and aggregate without re-fetching:
```
query_cache(cache_key, conditions=[{"field": "department", "operator": "contains", "value": "Engineering"}])
```

### Step 4: Format Output

**Chat Summary**: Competitive insights with key findings
**CSV Export**: `export_data(cache_key, "csv")` → Competitor comparison matrix
**JSON Export**: `export_data(cache_key, "json")` → Complete data for tracking over time

## Common Workflows

### Workflow 1: Comprehensive Competitor Profile

**Scenario**: Deep dive on a specific competitor

**Steps**:

1. **Company Overview**
```
execute("linkedin", "company", "company", {"company": "competitor"})
→ Size, industry, description, website, founding year
→ Save the URN (convert fsd_company to company: prefix for sub-endpoints)
```

2. **Leadership Team**
```
execute("linkedin", "search", "search_users", {
  "company_keywords": "Competitor Inc",
  "title": "C-level OR VP OR SVP OR President",
  "count": 50
})
→ C-suite and VP-level executives
→ Use get_page(cache_key, 10, 50) for more results
```

3. **Organizational Structure**
```
execute("linkedin", "company", "company_employee_stats", {
  "urn": {"type": "company", "value": "<company_id>"}
})
→ Total employees, growth rate, department breakdown

For each department:
  execute("linkedin", "search", "search_users", {
    "company_keywords": "Competitor Inc",
    "title": "<department_title>",
    "count": 50
  })
→ Team sizes, key roles
```

4. **Hiring Intelligence**
```
execute("linkedin", "search", "search_jobs", {"keywords": "Competitor Inc", "count": 50})
→ Open positions, hiring priorities, expansion areas
→ Use query_cache(cache_key, group_by="location") to see geographic expansion
```

5. **Content Strategy**
```
execute("linkedin", "company", "company_posts", {
  "urn": {"type": "company", "value": "<company_id>"},
  "count": 50
})
→ Posting frequency, themes, engagement levels

execute("twitter", "user", "user", {"user": "competitor"})
execute("twitter", "user", "user_posts", {"user": "competitor", "count": 50})
→ Social media presence and strategy
```

6. **Product/Market Intelligence**
```
execute("webparser", "parse", "parse", {"url": "https://competitor.com"})
→ Positioning, messaging, product offerings

execute("webparser", "parse", "parse", {"url": "https://competitor.com/blog"})
→ Content topics, thought leadership

execute("reddit", "search", "search_posts", {"query": "Competitor Inc", "count": 20})
→ Customer sentiment, product feedback
```

**Expected Output**:
- Complete company profile
- Leadership team roster (10-20 executives)
- Hiring velocity and priorities
- Content strategy analysis
- Product positioning insights
- Customer sentiment summary
- Use `export_data(cache_key, "csv")` to create downloadable competitor report

### Workflow 2: Competitive Landscape Mapping

**Scenario**: Map all competitors in your space

**Steps**:

1. **Identify Competitors**
```
execute("linkedin", "search", "search_companies", {
  "keywords": "<your industry keywords>",
  "industry": "<industry>",
  "employee_count": ["51-200", "201-500", "501-1000"],
  "count": 50
})
```

2. **Filter and Prioritize**
```
For each company:
  execute("linkedin", "company", "company", {"company": "<alias>"})
  → Review description for relevance
  → Check employee count and growth
  → Verify competitive overlap
```

3. **Categorize Competitors**
```
Direct: Same products, same market
Indirect: Similar products, different market
Potential: Adjacent space, could expand
```

4. **Size and Growth Metrics**
```
For each competitor:
  execute("linkedin", "company", "company_employee_stats", {
    "urn": {"type": "company", "value": "<company_id>"}
  })
  → Employee count, growth rate
  → Department distribution
  → Use query_cache() to compare across competitors
```

5. **Positioning Analysis**
```
For each competitor:
  execute("linkedin", "company", "company_posts", {
    "urn": {"type": "company", "value": "<company_id>"},
    "count": 10
  })
  → Key messaging themes

  execute("webparser", "parse", "parse", {"url": "<website>/about"})
  → Value proposition, target market
```

6. **Funding and Traction** (for startups)
```
execute("yc", "search", "search_companies", {"query": "<industry>", "count": 50})
→ YC competitors with funding data
→ Use query_cache(cache_key, sort_by=[{"field": "team_size", "order": "desc"}]) to rank by size

For each YC company:
  execute("yc", "company", "get", {"slug": "<company_slug>"})
  → Batch, team size, description
```

**Expected Output**:
- 20-50 competitors identified
- Categorized by competitive threat level
- Size and growth metrics for each
- Positioning and messaging summaries
- Competitive landscape map
- Use `export_data(cache_key, "csv")` for the full comparison matrix

### Workflow 3: Hiring Velocity Tracking

**Scenario**: Monitor competitor hiring to identify growth areas

**Steps**:

1. **Baseline Employee Count**
```
execute("linkedin", "company", "company_employee_stats", {
  "urn": {"type": "company", "value": "<company_id>"}
})
→ Current total employees
→ Department distribution
```

2. **Track Open Positions**
```
execute("linkedin", "search", "search_jobs", {"keywords": "Competitor Inc", "count": 100})
→ All open positions
→ Use query_cache(cache_key, group_by="location") to group by office

Group by department:
- Engineering roles
- Sales roles
- Marketing roles
- Operations roles
```

3. **Analyze Recent Hires**
```
execute("linkedin", "search", "search_users", {
  "company_keywords": "Competitor Inc",
  "count": 100
})
→ Get all employees
→ Use get_page(cache_key, 10, 100) to paginate through full list

Filter for recent joins:
execute("linkedin", "user", "user_experience", {
  "urn": {"type": "fsd_profile", "value": "<profile_id>"},
  "count": 5
})
→ Start date at current company
→ Identify hires from last 3-6 months
```

4. **Track Key Departures**
```
For former employees:
execute("linkedin", "search", "search_users", {"keywords": "Competitor Inc", "count": 50})
→ Filter profiles showing "Former" or past employment

Identify:
- Leadership departures
- Team exodus (multiple from same department)
- Moves to other competitors
```

5. **Competitive Recruiting Analysis**
```
Identify where competitors hire from:
- For each new hire: get previous companies
- Track talent pipelines
- Identify poaching patterns
→ Use export_data(cache_key, "csv") to build a hiring tracker spreadsheet
```

**Expected Output**:
- Hiring velocity (hires per month/quarter)
- Department growth priorities
- Key hires and their backgrounds
- Leadership changes
- Talent pipeline insights

### Workflow 4: Content Strategy Benchmarking

**Scenario**: Analyze competitor content across platforms

**Steps**:

1. **LinkedIn Content**
```
execute("linkedin", "company", "company_posts", {
  "urn": {"type": "company", "value": "<company_id>"},
  "count": 50
})
→ Use query_cache(cache_key, aggregate=[{"field": "comment_count", "function": "avg"}]) for engagement stats

Analyze:
- Posting frequency (posts/week)
- Content types (articles, videos, polls)
- Engagement rates (likes, comments, shares)
- Topics and themes
- Employee advocacy (shares/comments from team)
```

2. **Twitter/X Content**
```
execute("twitter", "user", "user", {"user": "competitor"})
execute("twitter", "user", "user_posts", {"user": "competitor", "count": 100})

Analyze:
- Tweet frequency
- Engagement metrics
- Content themes
- Use of threads/media
- Response rates
```

3. **YouTube Content**
```
execute("youtube", "channel", "channel_videos", {"channel": "competitor", "count": 30})

For each video:
  execute("youtube", "video", "video", {"video": "<video_id>"})

Analyze:
- Upload frequency
- View counts
- Engagement (likes, comments)
- Content types (demos, webinars, customer stories)
- Video length and production quality
→ Use query_cache(cache_key, sort_by=[{"field": "view_count", "order": "desc"}]) to find top videos
```

4. **Instagram Content** (if B2C)
```
execute("instagram", "user", "user", {"user": "competitor"})
execute("instagram", "user", "user_posts", {"user": "competitor", "count": 50})

Analyze:
- Post frequency
- Visual style/branding
- Engagement rates
- Use of Reels vs. static posts
- Influencer partnerships
```

5. **Blog/Website Content**
```
execute("webparser", "parse", "parse", {"url": "https://competitor.com/blog"})
execute("webparser", "sitemap", "sitemap", {"url": "https://competitor.com"})
→ Find all blog posts

Analyze:
- Publishing frequency
- Content topics
- SEO keywords
- Thought leadership positioning
```

6. **Community Sentiment**
```
execute("reddit", "search", "search_posts", {"query": "Competitor Inc", "count": 50})
execute("reddit", "search", "search_posts", {"query": "competitor product name", "count": 50})

Analyze:
- Customer feedback
- Common complaints
- Product strengths
- Feature requests
→ Use query_cache(cache_key, sort_by=[{"field": "comment_count", "order": "desc"}]) to find most-discussed threads
```

**Expected Output**:
- Cross-platform content strategy matrix
- Engagement benchmarks
- Content themes and messaging
- Platform prioritization insights
- Community sentiment summary
- Use `export_data(cache_key, "csv")` for cross-platform content comparison

## MCP Tools Reference (v2)

### LinkedIn Company Intelligence

**Company Profile** — `execute("linkedin", "company", "company", {"company": "..."})`
- Get detailed company profile
- Returns: Description, website, size, industry, specialties, URN

**Employee Stats** — `execute("linkedin", "company", "company_employee_stats", {"urn": {"type": "company", "value": "..."}})`
- Get employee statistics and growth
- Returns: Total employees, growth metrics, department distribution
- Note: URN must use `company:` prefix (not `fsd_company`). Convert: `urn:li:fsd_company:1441` → `company:1441`

**Company Posts** — `execute("linkedin", "company", "company_posts", {"urn": {"type": "company", "value": "..."}, "count": N})`
- Get recent company posts
- Returns: Posts with engagement metrics, content, timestamps

### LinkedIn People Intelligence

**Search Users** — `execute("linkedin", "search", "search_users", {"company_keywords": "...", "title": "...", "count": N})`
- Find employees at competitor companies
- Filter by title, department, location
- Returns: Employee profiles with titles and URLs

**User Profile** — `execute("linkedin", "user", "user", {"user": "..."})`
- Get detailed employee profile
- Returns: Work history, education, skills

**User Experience** — `execute("linkedin", "user", "user_experience", {"urn": {"type": "fsd_profile", "value": "..."}, "count": N})`
- Get detailed work history
- Returns: All positions with dates and descriptions

### LinkedIn Jobs

**Search Jobs** — `execute("linkedin", "search", "search_jobs", {"keywords": "...", "count": N})`
- Search job listings by keywords, location, and filters
- Returns: Open positions with company, location, work type

### Y Combinator Intelligence

**Search Companies** — `execute("yc", "search", "search_companies", {"query": "...", "count": N})`
- Search YC companies by industry, batch, filters
- Returns: Company list with batch, team size, status

**Company Details** — `execute("yc", "company", "get", {"slug": "..."})`
- Get detailed YC company profile
- Returns: Description, founders, batch, status, links

**Search Founders** — `execute("yc", "search", "search_founders", {"query": "...", "count": N})`
- Search for founders by criteria
- Returns: Founder profiles with company associations

### Social Media Monitoring

**Twitter/X**:
- `execute("twitter", "search", "search_posts", {"query": "...", "count": N})` — Find competitor mentions
- `execute("twitter", "user", "user", {"user": "..."})` — Get competitor profile
- `execute("twitter", "user", "user_posts", {"user": "...", "count": N})` — Get recent tweets

**Instagram**:
- `execute("instagram", "search", "search_posts", {"query": "...", "count": N})` — Find hashtag/keyword mentions
- `execute("instagram", "user", "user", {"user": "..."})` — Get profile stats
- `execute("instagram", "user", "user_posts", {"user": "...", "count": N})` — Get recent posts

**Reddit**:
- `execute("reddit", "search", "search_posts", {"query": "...", "count": N})` — Find discussions about competitors
- `execute("reddit", "posts", "posts", {"post_url": "..."})` — Get post details and sentiment

**YouTube**:
- `execute("youtube", "search", "search_videos", {"query": "...", "count": N})` — Find competitor videos
- `execute("youtube", "channel", "channel_videos", {"channel": "...", "count": N})` — Get all channel videos
- `execute("youtube", "video", "video", {"video": "..."})` — Get video details and metrics

### Web Intelligence

**Parse Webpage** — `execute("webparser", "parse", "parse", {"url": "..."})`
- Extract content from competitor websites
- Returns: Text content, links, contacts

**Sitemap** — `execute("webparser", "sitemap", "sitemap", {"url": "..."})`
- Get all pages on competitor site
- Returns: URL list for comprehensive analysis

**Web Search** — `execute("duckduckgo", "search", "search", {"query": "..."})`
- Search for competitor mentions across the web
- Returns: Search results with URLs and descriptions

### Data Analysis Tools (use with any cache_key from execute)

**Pagination** — `get_page(cache_key, offset, limit)`
- Load more results beyond first page when `next_offset` is returned

**Filter/Aggregate** — `query_cache(cache_key, conditions, sort_by, aggregate, group_by)`
- Filter, sort, aggregate cached data without new API calls
- Example: `query_cache(cache_key, sort_by=[{"field": "employee_count", "order": "desc"}])`

**Export** — `export_data(cache_key, format)`
- Export to "csv", "json", or "jsonl"
- Returns downloadable URL

## Output Formats

### Chat Summary

Provides competitive intelligence highlights:
- Key findings and insights
- Competitive threats identified
- Growth signals and strategic moves
- Recommended actions
- Top 3-5 competitors to watch

### CSV Export

Use `export_data(cache_key, "csv")` for competitor comparison matrix with:
- Company name, size, location
- Employee count and growth rate
- Posting frequency and engagement
- Key differentiators
- Competitive threat score

### JSON Export

Use `export_data(cache_key, "json")` for complete competitive data for:
- Time-series tracking
- Dashboard visualization
- Automated monitoring
- Integration with BI tools

## Advanced Features

### Competitive Intelligence Dashboard

Track competitors over time by storing data and comparing:

**Monthly Snapshot**:
```json
{
  "date": "2026-01-29",
  "competitors": [
    {
      "name": "Competitor A",
      "employees": 350,
      "monthly_growth": 8,
      "open_positions": 25,
      "linkedin_posts": 12,
      "twitter_followers": 5400,
      "funding_stage": "Series B"
    }
  ]
}
```

**Trend Analysis**:
- Employee growth over 6 months
- Content output changes
- Positioning shifts
- Leadership changes

### SWOT Analysis Framework

**Strengths** (from LinkedIn, website, reviews):
- Team expertise (LinkedIn profiles)
- Product features (website, Reddit feedback)
- Market position (company size, growth)
- Brand recognition (social followers, engagement)

**Weaknesses** (from reviews, job postings, employee turnover):
- Customer complaints (Reddit, review sites)
- Hiring challenges (multiple re-postings)
- Employee turnover (LinkedIn departures)
- Product gaps (feature requests in forums)

**Opportunities** (from market analysis):
- Underserved segments (job posting patterns)
- Geographic expansion (new office locations)
- Product expansion (new roles, content themes)

**Threats** (from competitive monitoring):
- New entrants (YC batch analysis)
- Competitive hiring (talent poaching)
- Product launches (company posts, blogs)
- Pricing changes (website updates)

### Win/Loss Analysis

Track deals against specific competitors:

**Data Points to Collect**:
- Competitor encountered (company name)
- Deal stage (lost/won)
- Key differentiators discussed
- Pricing comparison
- Feature comparison
- Decision factors

**Intelligence Gathering**:
```
For each competitor in win/loss:
1. execute("linkedin", "company", "company", {"company": "..."}) → Current positioning
2. execute("webparser", "parse", "parse", {"url": "<website>/pricing"}) → Pricing strategy
3. execute("webparser", "parse", "parse", {"url": "<website>/features"}) → Feature set
4. execute("reddit", "search", "search_posts", {"query": "competitor", "count": 20}) → Customer feedback
5. execute("linkedin", "company", "company_posts", {"urn": {"type": "company", "value": "..."}, "count": 10}) → Recent messaging
```

**Analysis**:
- Win rate by competitor
- Common objections
- Competitive advantages/disadvantages
- Pricing positioning
- Feature gaps

## Recommendations

**For Local/Retail Competitors**:
Focus on:
- LinkedIn company presence
- Instagram brand content
- Website location pages
- Reddit community discussions

**For Tech/SaaS Competitors**:
Excellent coverage through:
- LinkedIn (primary intelligence)
- Y Combinator (for startups)
- Twitter (tech community presence)
- Product Hunt mentions

**For Enterprise Competitors**:
- LinkedIn extremely comprehensive
- SEC filings for public companies
- Professional social presence
- Limited need for consumer platforms

## Reference Documentation

- **[ANALYSIS_PATTERNS.md](references/ANALYSIS_PATTERNS.md)** - Competitive analysis frameworks, SWOT templates, and intelligence gathering patterns

## Troubleshooting

### Issue: Competitor Not Found on LinkedIn

**Solution**:
- Try company name variations
- Search for employees and extract company
- Check if using DBA vs. legal name
- Try website domain search
- Error `412` means not found — check the `llm_hint` in the response for guidance

### Issue: Limited Employee Data

**Solution**:
- Employees may have privacy settings
- Try searching by title without company filter
- Focus on public leadership team
- Use website team pages as alternative

### Issue: No Recent Company Posts

**Solution**:
- Company may not be active on LinkedIn
- Check Twitter/Instagram instead
- Use website blog for content analysis
- Focus on employee posts mentioning company

### Issue: URN Format Errors (422)

**Solution**:
- Company sub-endpoints require `company:` prefix, NOT `fsd_company`
- Convert: `urn:li:fsd_company:1441` → use `{"type": "company", "value": "1441"}`
- User sub-endpoints require `fsd_profile` URN from `/linkedin/user` response
- Always get URNs from the parent endpoint response first

---

**Ready to analyze competitors?** Ask Claude to help you research competitors, track hiring patterns, or benchmark competitive positioning using this skill!
