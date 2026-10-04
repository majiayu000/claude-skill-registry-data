---
name: ahrefs
description: Complete Ahrefs API integration for SEO analysis. Covers Site Explorer (domains, backlinks, rankings), Keywords Explorer (search volume, difficulty, SERP analysis), Rank Tracker (position monitoring), Site Audit (technical SEO), SERP Overview, Batch Analysis, and Brand Radar. Use for any SEO-related queries including keyword research, backlink analysis, competitor intelligence, technical audits, and rank tracking.
version: 1.2.0
---

# Ahrefs SEO Analysis

Query and analyze SEO data using the Ahrefs API for backlinks, keywords, rankings, and competitive intelligence.

## Prerequisites

### API Access
You need an Ahrefs subscription with API access:
- **Lite**: Basic metrics, limited filtering
- **Standard**: More endpoints, some filtering
- **Advanced**: Advanced filtering, more data
- **Enterprise**: Full API access, advanced filtering, high rate limits

### Setup

1. **Get your API token** from [Ahrefs Account Settings](https://ahrefs.com/api)

2. **Configure in OpenClaw**:
   Add to `~/.openclaw/workspace/.env`:
   ```bash
   AHREFS_API_TOKEN=your_api_token_here
   AHREFS_API_PLAN=enterprise  # Options: lite, standard, advanced, enterprise
   ```

3. **Verify setup**:
   ```bash
   grep AHREFS ~/.openclaw/workspace/.env
   ```

## Plan-Specific Features

### All Plans
- Domain Rating & Ahrefs Rank
- Basic backlinks stats (total counts)
- Organic keywords count
- Organic traffic estimates
- Top pages by traffic

### Standard & Above
- Organic keywords with positions (all positions)
- Keywords in positions 1-3 (via `org_keywords_1_3` metric)
- Referring domains list (basic)

### Advanced & Enterprise
- **Advanced filtering**: Filter keywords by position (1-10 for first page)
- **Geographic filtering**: Filter backlinks by country/TLD (e.g., `.au` domains)
- **Detailed keyword data**: Access to `best_position`, `sum_traffic`, `volume`
- **Detailed backlink data**: Full backlinks list with filtering
- **Higher rate limits**: Fetch larger datasets (5000+ records)

## Core Capabilities

### Site Explorer (Domain Analysis)
Get comprehensive SEO metrics for any domain:
- Domain Rating (DR) & URL Rating (UR)
- Organic traffic estimates
- Referring domains & backlinks
- Organic keywords & rankings
- Top pages by traffic
- Historical data & trends
- **[Advanced/Enterprise]** Filter by country/TLD
- **[Advanced/Enterprise]** Position-based filtering (first page only)

### Keywords Explorer (Keyword Research)
Discover and analyze keywords:
- Search volume (global & country-specific)
- Keyword difficulty (KD) score
- Cost per click (CPC) estimates
- SERP analysis & features
- Related keywords & questions
- Keyword ideas & suggestions
- Parent topic analysis
- Traffic potential estimates

### Rank Tracker (Position Monitoring)
Track keyword rankings over time:
- Position tracking & visibility
- Competitor rankings comparison
- SERP feature tracking
- Historical position data
- Share of voice metrics
- **Note:** Requires pre-configured projects in Ahrefs

### Site Audit (Technical SEO)
Identify technical SEO issues:
- Crawl data & site health scores
- On-page issues by severity
- Internal link analysis
- Page performance metrics
- Mobile usability issues
- **Note:** Requires pre-configured projects in Ahrefs

### SERP Overview (Search Results)
Analyze search engine results:
- Top 100 organic results for any keyword
- SERP features present
- Domain metrics for ranking pages
- Keyword difficulty breakdown
- Click-through rate estimates

### Batch Analysis (Bulk Processing)
Process multiple targets efficiently:
- Analyze up to 100 domains/URLs per request
- Bulk keyword metrics
- Batch backlink data
- Cost-effective for large datasets

### Brand Radar (Brand Monitoring)
Track brand performance:
- Brand mention metrics
- Share of voice
- Competitor brand comparison
- Sentiment analysis preparation

### Competitor Analysis
Compare domains and identify opportunities:
- Side-by-side domain comparison
- Content gap analysis
- Keyword overlaps & differences
- Backlink gap analysis
- Traffic comparison
- **[Advanced/Enterprise]** Filtered comparisons (first page keywords, local backlinks)

## API Structure

Ahrefs API base URL: `https://api.ahrefs.com/v3/site-explorer/`

### Authentication
All requests require the API token in the header:
```
Authorization: Bearer {AHREFS_API_TOKEN}
```

**Important:** Use `AHREFS_API_TOKEN`, NOT `AHREFS_MCP_TOKEN`.

### Required Parameters
All API calls require:
- `date`: Current date in format `YYYY-MM-DD`
- `target`: Domain (e.g., `example.com`)

### Common Endpoints

For detailed endpoint documentation and parameters, see [references/api-endpoints.md](references/api-endpoints.md).

## API Unit Management

### Understanding API Units
- Each API request consumes units from your monthly allowance
- Cost depends on rows returned (minimum 50 units per request)
- Enterprise plans include units; additional units can be purchased
- Track usage at: https://app.ahrefs.com/account/limits-and-usage/web

### Cost Optimization Tips
1. **Limit rows returned**: Use `limit` parameter to reduce cost
2. **Select specific columns**: Use `select` parameter for only needed fields
3. **Batch requests**: Process multiple targets in one call (up to 100)
4. **Cache results**: Store frequently accessed data locally
5. **Use date ranges**: Limit historical data when not needed

### Rate Limits
- **60 requests per minute** (default)
- HTTP 429 returned if limit exceeded
- Implement exponential backoff for retries

## Usage Examples

### Site Explorer - Get Backlinks & Referring Domains
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/backlinks-stats?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

Returns:
```json
{
  "metrics": {
    "live": 4545,
    "all_time": 25318,
    "live_refdomains": 718,
    "all_time_refdomains": 3272
  }
}
```

### Get Organic Keywords & Traffic
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/metrics?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

Returns:
```json
{
  "metrics": {
    "org_keywords": 6925,
    "org_traffic": 38702,
    "org_keywords_1_3": 1560,
    "org_cost": 2372016
  }
}
```

### Get Domain Rating
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/domain-rating?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

Returns:
```json
{
  "domain_rating": {
    "domain_rating": 43.0,
    "ahrefs_rank": 1189155
  }
}
```

### Get Top Pages
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/top-pages?date=$DATE&target=example.com&limit=10&select=url,sum_traffic" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### Keywords Explorer - Keyword Research
```bash
curl -X GET "https://api.ahrefs.com/v3/keywords-explorer/overview?keyword=seo+tools&country=us" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

Returns:
```json
{
  "keyword": "seo tools",
  "volume": 14000,
  "keyword_difficulty": 75,
  "cpc": 25.50,
  "serp_features": ["featured_snippet", "people_also_ask"],
  "traffic_potential": 18500
}
```

### Keywords Explorer - Related Keywords
```bash
curl -X GET "https://api.ahrefs.com/v3/keywords-explorer/related-keywords?keyword=seo+tools&country=us&limit=50" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### SERP Overview - Analyze Search Results
```bash
curl -X GET "https://api.ahrefs.com/v3/serp-overview?keyword=seo+tools&country=us" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

Returns top 100 organic results with domain metrics.

### Rank Tracker - Get Project Rankings
**Note:** Requires pre-configured project in Ahrefs web interface.

```bash
curl -X GET "https://api.ahrefs.com/v3/rank-tracker/project?project_id=12345" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### Site Audit - Get Project Issues
**Note:** Requires pre-configured project in Ahrefs web interface.

```bash
curl -X GET "https://api.ahrefs.com/v3/site-audit/project?project_id=12345" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### Batch Analysis - Multiple Domains
```bash
curl -X POST "https://api.ahrefs.com/v3/site-explorer/batch/metrics" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "targets": ["example.com", "competitor1.com", "competitor2.com"],
    "date": "2026-02-18"
  }'
```

Returns metrics for all domains in one request.

## Common Workflows

### Keyword Research Workflow
1. Get keyword overview (volume, difficulty, CPC)
2. Fetch related keywords and questions
3. Analyze SERP for top-ranking content
4. Identify keyword difficulty and traffic potential
5. Export prioritized keyword list

### Competitive Analysis Workflow
1. Compare domain metrics (DR, traffic, keywords)
2. Analyze competitor backlink profiles
3. Identify content gaps
4. Find keywords competitors rank for but you don't
5. Discover backlink opportunities

### Technical SEO Audit Workflow
**Requires Site Audit project**
1. Fetch site health overview
2. Identify critical issues by severity
3. Analyze internal linking structure
4. Review page performance metrics
5. Generate prioritized fix list

### Content Strategy Workflow
1. Research target keywords (Keywords Explorer)
2. Analyze top-ranking content (SERP Overview)
3. Identify content gaps vs competitors
4. Plan content based on traffic potential
5. Track rankings over time (Rank Tracker)

### Batch Domain Analysis Workflow
1. Compile list of target domains
2. Make batch API request (up to 100 domains)
3. Compare metrics across all domains
4. Identify patterns and opportunities
5. Export comparative analysis

## Best Practices

1. **Rate Limits**: Respect API rate limits (60 req/min default)
2. **API Units**: Monitor usage and optimize queries (limit rows, select columns)
3. **Caching**: Cache responses for frequently accessed data
4. **Pagination**: Use `limit` and `offset` parameters for large datasets
5. **Batch Requests**: Use batch endpoints when analyzing multiple targets
6. **Error Handling**: Check for 401 (auth), 429 (rate limit), 404 (not found)
7. **Project Requirements**: Rank Tracker and Site Audit require pre-configured projects

## Environment Variables

Load the token from the workspace `.env` file:
```powershell
# PowerShell
$env:AHREFS_API_TOKEN = (Get-Content ~/.openclaw/workspace/.env -Raw | Select-String "AHREFS_API_TOKEN=([^\r\n]+)" | ForEach-Object { $_.Matches.Groups[1].Value })
```

```bash
# Bash
export AHREFS_API_TOKEN=$(grep AHREFS_API_TOKEN ~/.openclaw/workspace/.env | cut -d'=' -f2)
```

## Response Format

API responses vary by endpoint but typically return JSON:

**Stats endpoints** (backlinks-stats, metrics, domain-rating):
```json
{
  "metrics": { /* metric fields */ },
  "domain_rating": { /* rating fields */ }
}
```

**List endpoints** (top-pages, backlinks, etc.):
```json
{
  "pages": [ /* array of results */ ],
  "backlinks": [ /* array of results */ ]
}
```

## Troubleshooting

### Authentication Errors
- Verify token is correctly set in `.env`
- Check token hasn't expired
- Ensure Bearer token format in header

### Rate Limiting
- Implement exponential backoff
- Cache responses where appropriate
- Use batch endpoints when available

### Data Not Found
- Verify domain/URL format
- Check if domain exists in Ahrefs index
- Try alternative target formats (with/without www)
