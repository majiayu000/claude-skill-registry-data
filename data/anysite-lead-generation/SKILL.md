---
name: anysite-lead-generation
description: Lead generation and prospecting using anysite MCP server for LinkedIn prospect discovery, email finding, company research, and contact enrichment. Extract contacts from websites, find decision-makers at target companies, and build qualified prospect lists for sales, recruiting, and business development. Supports LinkedIn (primary), web scraping for contact extraction, and Instagram business discovery. Research and list-building only - this skill does NOT write to a CRM. For finding leads AND pushing them into a connected CRM use anysite-crm-prospect; for filling gaps in existing CRM records use anysite-crm-enrich. Use when users need to build prospect lists, find decision-makers, extract contact information, or research potential customers outside a CRM context.
---

# anysite Lead Generation

> Query craft for the two big SQL databases now lives in dedicated skills:
> `anysite-company-sourcing` (70M companies) and `anysite-people-sourcing`
> (856M profiles, `search_sql_users`). Prefer them for bulk list building;
> this skill remains the end-to-end research workflow.

Professional lead generation and prospecting using the anysite MCP server. Find prospects on LinkedIn, discover verified emails, extract contacts from websites, and build comprehensive lead lists for sales, recruiting, and business development.

## Overview

The anysite Lead Generation skill helps you:
- **Find qualified prospects** on LinkedIn using advanced search filters
- **Enrich profiles** with work history, education, and skills
- **Discover email addresses** through LinkedIn email finding
- **Extract contact information** from company websites
- **Research companies** to identify target accounts
- **Build prospect lists** formatted for CRM import

This skill provides comprehensive lead generation capabilities with the added benefit of zero configuration and immediate execution through anysite MCP.

## Supported Platforms

- **LinkedIn** (Primary): People search, profile enrichment, email discovery, company research, employee listings
- **Web Scraping**: Contact extraction from websites, sitemap parsing, general web data
- **Instagram**: Business account discovery and profile analysis (supplementary)
- **Y Combinator**: Startup company and founder research (supplementary)

## v2 API Overview

All data fetching uses the universal `execute()` tool with four parameters: `source`, `category`, `endpoint`, `params`. Supporting tools:

- **`execute(source, category, endpoint, params)`** - Fetch data. Returns first page of items + `cache_key`.
- **`get_page(cache_key, offset, limit)`** - Load additional pages from a previous execute() result using the returned `cache_key` and `next_offset`.
- **`query_cache(cache_key, conditions, sort_by, aggregate, group_by)`** - Filter, sort, count, or aggregate already-fetched data without a new API call.
- **`export_data(cache_key, format)`** - Export a full dataset as CSV, JSON, or JSONL. Returns a download URL.
- **`discover(source, category)`** - Inspect available endpoints and their accepted params (use when unsure about params).

### Error Handling

v2 responses may include an `llm_hint` field with human-readable guidance when something goes wrong (e.g., invalid params, rate limits). Always check for `llm_hint` in the response and follow its advice before retrying.

## Quick Start

### Step 1: Identify Your Lead Source

Choose the appropriate data source based on your prospecting goal:

| Goal | v2 Call | Use Case |
|------|---------|----------|
| Find prospects by title/company | `execute("linkedin", "search", "search_users", {...})` | B2B prospecting, targeted outreach |
| Enrich existing leads | `execute("linkedin", "user", "get", {"user": ...})` | Add work history, education, skills |
| Find verified emails | `execute("linkedin", "email", "find", {"user": ...})` | Email outreach campaigns |
| Extract website contacts | `execute("webparser", "parse", "parse", {"url": ...})` | Get emails/phones from contact pages |
| Research target companies | `execute("linkedin", "search", "search_companies", {...})` | Account-based marketing (ABM) |
| Find company employees | `execute("linkedin", "search", "search_users", {...})` + company filter | Multi-threading into accounts |

### Step 2: Execute Data Collection

Use anysite MCP v2 tools directly to gather lead data:

**Example: Find Sales VPs in San Francisco**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "search"
- endpoint: "search_users"
- params: {"title": "VP Sales", "location": "San Francisco Bay Area", "count": 25}
```

**Example: Enrich a LinkedIn Profile**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "user"
- endpoint: "get"
- params: {"user": "linkedin.com/in/johndoe", "with_experience": true, "with_education": true, "with_skills": true}
```

**Example: Find Email Address**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "email"
- endpoint: "find"
- params: {"user": "johndoe"}
```

**Example: Extract Contacts from Website**
```
Tool: mcp__anysite__execute
Parameters:
- source: "webparser"
- category: "parse"
- endpoint: "parse"
- params: {"url": "https://company.com/contact", "extract_contacts": true, "strip_all_tags": true}
```

### Step 3: Process and Analyze Results

After execute() returns data with a `cache_key`, use v2 post-processing:

- **Filter results**: `query_cache(cache_key, conditions=[{"field": "title", "operator": "contains", "value": "VP"}])`
- **Sort results**: `query_cache(cache_key, sort_by=[{"field": "follower_count", "order": "desc"}])`
- **Count results**: `query_cache(cache_key, aggregate=[{"function": "count", "field": "*"}])`
- **Get more pages**: `get_page(cache_key, offset=next_offset, limit=10)`

Also review the returned data for:
- **Profile completeness**: Work history, education, skills presence
- **Contact quality**: Email deliverability, phone format
- **Relevance scoring**: Title match, company fit, location alignment
- **Enrichment opportunities**: Missing data that can be filled

### Step 4: Format Output

Choose your preferred output format:

**Chat Summary (Default)**
- Displays top prospects with key details
- Includes actionable next steps
- Shows data quality metrics

**CSV Export (via v2 export_data)**
```
Tool: mcp__anysite__export_data
Parameters:
- cache_key: <cache_key from execute>
- format: "csv"
```
Returns a download URL. Ready for CRM import (Salesforce, HubSpot, etc.)

**JSON Export (via v2 export_data)**
```
Tool: mcp__anysite__export_data
Parameters:
- cache_key: <cache_key from execute>
- format: "json"
```
Returns a download URL. Structured data for custom integration.

## Common Workflows

### Workflow 1: LinkedIn B2B Prospecting

**Scenario**: Find 50 qualified prospects at SaaS companies in specific roles

**Steps**:

1. **Search for prospects**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "search"
- endpoint: "search_users"
- params: {"keywords": "SaaS software cloud", "title": "Head of Marketing, VP Marketing, CMO", "location": "United States", "company_keywords": "software", "count": 50}
```

2. **Enrich top prospects** (for first 10-20 results)
```
For each prospect from step 1:
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "user"
- endpoint: "get"
- params: {"user": "<prospect_username>", "with_experience": true, "with_education": true}
```

3. **Find email addresses**
```
For each qualified prospect:
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "email"
- endpoint: "find"
- params: {"user": "<prospect_username>"}
```

4. **Export to CRM**
```
Tool: mcp__anysite__export_data
Parameters:
- cache_key: <cache_key from search>
- format: "csv"
```
Import the CSV to your CRM system and set up outreach sequences.

**Expected Output**:
- 50 prospects with LinkedIn profiles
- 10-20 enriched profiles with complete work history
- 5-15 verified email addresses
- CSV file ready for CRM import

### Workflow 2: Account-Based Marketing (ABM)

**Scenario**: Find decision-makers at specific target companies

**Steps**:

1. **Research target companies**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "search"
- endpoint: "search_companies"
- params: {"keywords": "<your ICP description>", "industry": "<target industry>", "employee_count": ["51-200", "201-500"], "location": "<target location>", "count": 20}
```

2. **Get company details**
```
For each target company:
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "company"
- endpoint: "get"
- params: {"company": "<company_identifier or URL>"}
```

3. **Find employees at target companies**
```
For each target company:
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "search"
- endpoint: "search_users"
- params: {"company_keywords": "<Company Name>", "title": "VP, Director, Head of, Chief", "count": 10}
```

4. **Enrich decision-makers**
```
For each decision-maker:
Tool: mcp__anysite__execute
  source: "linkedin", category: "user", endpoint: "get", params: {"user": "<username>"}
Tool: mcp__anysite__execute
  source: "linkedin", category: "email", endpoint: "find", params: {"user": "<username>"}
```

5. **Filter and analyze with query_cache**
```
Tool: mcp__anysite__query_cache
Parameters:
- cache_key: <cache_key from employee search>
- conditions: [{"field": "title", "operator": "contains", "value": "VP"}]
- sort_by: [{"field": "name", "order": "asc"}]
```

6. **Create ABM campaign**
- Group prospects by company
- Identify multi-threading opportunities
- Build company-specific messaging

**Expected Output**:
- 20 target companies with full profiles
- 50-100 decision-makers across all companies
- 20-40 verified email addresses
- Account map showing org structure

### Workflow 3: Website Contact Extraction

**Scenario**: Extract contact information from a list of company websites

**Steps**:

1. **Get company websites**
```
From LinkedIn company search or existing list
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "company"
- endpoint: "get"
- params: {"company": "<company_identifier>"}
Extract: company website URLs
```

2. **Parse contact pages**
```
For each website:
Tool: mcp__anysite__execute
Parameters:
- source: "webparser"
- category: "parse"
- endpoint: "parse"
- params: {"url": "https://company.com/contact", "extract_contacts": true, "strip_all_tags": true}

Alternative pages to try:
- /contact
- /about/contact
- /about/team
- /about
```

3. **Parse team pages** (if available)
```
Tool: mcp__anysite__execute
Parameters:
- source: "webparser"
- category: "parse"
- endpoint: "parse"
- params: {"url": "https://company.com/team", "extract_contacts": true}
```

4. **Get sitemap** (for comprehensive coverage)
```
Tool: mcp__anysite__discover
Parameters:
- source: "webparser"
- category: "parse"
(Use discover to find the sitemap endpoint and its params, then execute accordingly)

Identify pages likely to contain contacts:
- /contact, /team, /about, /leadership
```

5. **Deduplicate and validate**
- Remove duplicate emails
- Validate email formats
- Match emails to LinkedIn profiles if possible

**Expected Output**:
- Contact emails from 60-80% of websites
- Phone numbers where available
- Social media links
- Team member names and titles

### Workflow 4: Recruiter Candidate Sourcing

**Scenario**: Find qualified candidates for open positions

**Steps**:

1. **Define candidate profile**
```
Required skills, titles, experience level, location
```

2. **Search for candidates**
```
Tool: mcp__anysite__execute
Parameters:
- source: "linkedin"
- category: "search"
- endpoint: "search_users"
- params: {"keywords": "Python React AWS", "title": "Software Engineer, Senior Engineer", "location": "Remote", "count": 100}
```

3. **Get more results with pagination**
```
If response includes next_offset:
Tool: mcp__anysite__get_page
Parameters:
- cache_key: <cache_key from search>
- offset: <next_offset>
- limit: 50
```

4. **Enrich candidate profiles**
```
For promising candidates:
Tool: mcp__anysite__execute
  source: "linkedin", category: "user", endpoint: "get", params: {"user": "<username>", "with_experience": true, "with_education": true, "with_skills": true}
```

5. **Find contact information**
```
Tool: mcp__anysite__execute
  source: "linkedin", category: "email", endpoint: "find", params: {"user": "<username>"}
```

6. **Filter candidates with query_cache**
```
Tool: mcp__anysite__query_cache
Parameters:
- cache_key: <cache_key from search>
- conditions: [{"field": "location", "operator": "contains", "value": "Remote"}]
- sort_by: [{"field": "follower_count", "order": "desc"}]
```

7. **Build candidate pipeline**
- Score candidates on skills match
- Prioritize by years of experience
- Create outreach sequence

**Expected Output**:
- 100 potential candidates
- 30-50 fully enriched profiles
- 20-30 email addresses
- Scored and prioritized candidate list

## MCP Tools Reference

### Primary Tools

#### LinkedIn People Search
**v2 Call**: `execute("linkedin", "search", "search_users", {...})`

Search for LinkedIn users by various criteria.

**Parameters** (passed in `params`):
- `keywords` (optional): General keywords for search
- `title` (optional): Job title keywords (e.g., "VP Sales", "Software Engineer")
- `company_keywords` (optional): Company name keywords
- `location` (optional): Location (city, state, country)
- `school_keywords` (optional): School/university keywords
- `first_name` (optional): First name
- `last_name` (optional): Last name
- `count` (default: 10): Number of results to return

**Returns**: List of user profiles with name, title, location, profile URL, and URN. Includes `cache_key` for pagination and filtering.

**Use Cases**:
- Find prospects by title and location
- Discover employees at target companies
- Search for alumni from specific schools
- Build prospect lists for outreach

**Pagination**: If `next_offset` is returned, call `get_page(cache_key, next_offset, limit)` for more results.

#### LinkedIn Profile Details
**v2 Call**: `execute("linkedin", "user", "get", {"user": ...})`

Get comprehensive profile information for a LinkedIn user.

**Parameters** (passed in `params`):
- `user` (required): LinkedIn username or full profile URL
- `with_education` (default: true): Include education history
- `with_experience` (default: true): Include work experience
- `with_skills` (default: true): Include skills

**Returns**: Complete profile with work history, education, skills, certifications, and more

**Use Cases**:
- Enrich prospect data before outreach
- Qualify leads based on work history
- Research candidate backgrounds
- Understand prospect's career path

#### Email Finding
**v2 Call**: `execute("linkedin", "email", "find", {"user": ...})`

Search for email addresses associated with LinkedIn profiles.

**Parameters** (passed in `params`):
- `user` (required): LinkedIn username or profile URL

**Returns**: Email addresses associated with the LinkedIn profile

**Use Cases**:
- Find verified emails for prospects
- Enrich contact databases
- Build email outreach lists

#### Company Search
**v2 Call**: `execute("linkedin", "search", "search_companies", {...})`

Search for LinkedIn companies by various criteria.

**Parameters** (passed in `params`):
- `keywords` (optional): Company name or description keywords
- `location` (optional): Company location
- `industry` (optional): Industry type
- `employee_count` (optional): Array of employee count ranges (e.g., ["51-200", "201-500"])
- `count` (required): Number of results to return

**Returns**: List of companies with name, industry, size, location, and URN. Includes `cache_key`.

**Use Cases**:
- Identify target accounts for ABM
- Research competitors
- Build company prospect lists
- Market segmentation analysis

#### Company Details
**v2 Call**: `execute("linkedin", "company", "get", {"company": ...})`

Get detailed information about a LinkedIn company.

**Parameters** (passed in `params`):
- `company` (required): Company identifier or LinkedIn URL

**Returns**: Company profile with description, industry, size, specialties, website

**Use Cases**:
- Research target accounts
- Understand company positioning
- Extract company websites for further research
- Qualify accounts before prospecting

#### Company Employee Stats
**v2 Call**: `discover("linkedin", "company")` to find the employee stats endpoint, then `execute(...)` with the discovered endpoint and params.

Get employee statistics and insights for a company.

**Use Cases**:
- Track hiring velocity (company growth)
- Identify growing departments
- Assess company size and scale
- Competitive intelligence on hiring

### Supporting Tools

#### Web Contact Extraction
**v2 Call**: `execute("webparser", "parse", "parse", {"url": ...})`

Extract content and contact information from web pages.

**Parameters** (passed in `params`):
- `url` (required): Webpage URL
- `extract_contacts` (default: false): Extract emails, phones, social links
- `strip_all_tags` (default: true): Remove HTML tags
- `only_main_content` (default: true): Extract only main content area

**Returns**: Page content, contacts (emails, phones), links

**Use Cases**:
- Extract contacts from company websites
- Get email addresses from contact pages
- Find phone numbers and addresses
- Discover team member information

#### Sitemap Parsing
**v2 Call**: `discover("webparser", "parse")` to find the sitemap endpoint, then `execute(...)` with discovered endpoint and params.

Retrieve sitemap URLs from a website.

**Use Cases**:
- Find all pages on a website
- Identify contact/team pages
- Comprehensive website crawling
- Discover hidden landing pages

#### LinkedIn User Posts
**v2 Call**: `execute("linkedin", "post", "get_user_posts", {"user": ...})`

Get recent posts from a LinkedIn user for engagement research.

**Use Cases**:
- Research prospect interests and activity
- Identify conversation starters
- Analyze thought leadership topics

#### LinkedIn Post Search
**v2 Call**: `execute("linkedin", "post", "search_posts", {...})`

Search LinkedIn posts by keywords.

**Use Cases**:
- Find prospects discussing relevant topics
- Monitor industry conversations
- Identify engaged professionals

#### LinkedIn Job Search
**v2 Call**: `execute("linkedin", "job_search", "search_jobs", {...})`

Search LinkedIn job postings.

**Use Cases**:
- Identify companies that are hiring (growth signals)
- Find companies investing in specific roles
- Research market demand

#### Google LinkedIn Search
**v2 Call**: `execute("linkedin", "google", "search", {"query": ...})`

Search Google for LinkedIn profiles.

**Use Cases**:
- Find profiles that LinkedIn search misses
- Search by specific phrases
- Discover profiles with particular keywords

## Output Formats

### Chat Summary (Default)

The skill will provide:
- **Prospect count**: Total leads found
- **Key insights**: Notable patterns or high-value prospects
- **Quality metrics**: Percentage with emails, complete profiles, etc.
- **Top prospects**: 5-10 best matches with details
- **Next steps**: Recommended actions

Example:
```
Found 47 qualified prospects matching your criteria:

Top Prospects:
1. Jane Smith - VP Sales at TechCorp (San Francisco)
   - Email: jane.smith@techcorp.com
   - 10 years in SaaS sales leadership
   - Previously at Salesforce, Oracle

2. John Doe - Head of Sales at CloudCo (Remote)
   - Email: Not found (try web scraping)
   - 8 years experience
   - Strong enterprise background

Quality Metrics:
- 32% have verified emails (15/47)
- 91% have complete LinkedIn profiles (43/47)
- 68% in target location (32/47)

Next Steps:
1. Export to CSV for CRM import
2. Set up email outreach sequence
3. Prioritize prospects with emails
4. Research companies for remaining prospects
```

### CSV Export

Use `export_data(cache_key, "csv")` to get a download URL for CRM import and spreadsheet analysis.

**How to Request**:
"Export the results as CSV"

**CSV Structure**:
```csv
Full Name,First Name,Last Name,Title,Company,Location,Email,Phone,LinkedIn URL,Profile URN,Years Experience,Education,Skills,Last Updated
```

**Use Cases**:
- Salesforce/HubSpot import
- Mail merge for outreach
- Spreadsheet analysis and filtering
- Team collaboration via Google Sheets

### JSON Export

Use `export_data(cache_key, "json")` to get a download URL for programmatic access and custom integration.

**How to Request**:
"Export the results as JSON"

**JSON Structure**:
```json
{
  "prospects": [
    {
      "profile": {
        "firstName": "Jane",
        "lastName": "Smith",
        "headline": "VP Sales at TechCorp",
        "location": "San Francisco Bay Area",
        "profileUrl": "https://linkedin.com/in/janesmith",
        "urn": "urn:li:fsd_profile:ABC123"
      },
      "currentPosition": {
        "title": "VP Sales",
        "company": "TechCorp",
        "startDate": "2021-06"
      },
      "contact": {
        "email": "jane.smith@techcorp.com",
        "phone": null
      },
      "experience": [...],
      "education": [...],
      "skills": [...]
    }
  ],
  "metadata": {
    "total": 47,
    "withEmails": 15,
    "timestamp": "2026-01-29T01:00:00Z"
  }
}
```

**Use Cases**:
- Custom CRM integration
- Automated enrichment pipelines
- Data analysis with Python/R
- API integrations with other tools

## Advanced Features

### Multi-Platform Lead Enrichment

Combine LinkedIn data with other platforms for comprehensive lead profiles:

**Pattern**: LinkedIn -> Company Website -> Instagram (for B2C)

1. Find prospect on LinkedIn
2. Get company website from LinkedIn company profile
3. Extract additional contacts from website
4. Check Instagram for business account (B2C companies)
5. Analyze social presence and engagement

**Example**:
```
1. execute("linkedin", "search", "search_users", {"keywords": "Emily Chen", "company_keywords": "FashionBrand"})
2. execute("linkedin", "company", "get", {"company": "FashionBrand"}) -> Get website URL
3. execute("webparser", "parse", "parse", {"url": "<website>/contact", "extract_contacts": true}) -> Get phone, email
4. execute("instagram", "search", "search_users", {"query": "FashionBrand"}) -> Find official account
5. execute("instagram", "user", "user", {"user": "fashionbrand"}) -> Verify business account, get follower count
```

### Boolean Search Patterns

Advanced LinkedIn search using keyword combinations:

**Title Combinations**:
- `"VP Sales" OR "Head of Sales" OR "Director Sales"` - Multiple title variations
- `"Software Engineer" AND "Python"` - Title + required skill
- `"Marketing" NOT "Intern"` - Exclude junior levels

**Company Patterns**:
- `"Google OR Meta OR Amazon"` - Multiple target companies
- `"SaaS" AND "B2B"` - Industry qualifiers
- `"Startup OR Early Stage"` - Company stage targeting

**Location Strategies**:
- `"San Francisco Bay Area"` - Metropolitan areas
- `"United States"` - Country-level
- `"Remote"` - Remote-only positions

### Lead Scoring Framework

Score prospects based on multiple criteria:

**Scoring Dimensions**:
1. **Profile Completeness** (0-20 points)
   - Has email: +10
   - Complete work history: +5
   - Complete education: +3
   - Skills listed: +2

2. **Title Match** (0-30 points)
   - Exact match: +30
   - Similar title: +20
   - Related title: +10
   - Wrong level: +0

3. **Company Fit** (0-25 points)
   - Ideal company size: +25
   - Acceptable size: +15
   - Too small/large: +5

4. **Experience Level** (0-15 points)
   - 5-10 years: +15
   - 3-5 years: +10
   - 10+ years: +10
   - <3 years: +5

5. **Location** (0-10 points)
   - Target location: +10
   - Acceptable location: +5
   - Remote: +8

**Total Score**: 0-100 points
- **90-100**: Hot lead - Contact immediately
- **70-89**: Warm lead - High priority follow-up
- **50-69**: Qualified - Standard outreach
- **<50**: Unqualified - Nurture or discard

Use `query_cache()` to filter by score thresholds:
```
query_cache(cache_key, conditions=[{"field": "score", "operator": ">=", "value": 70}], sort_by=[{"field": "score", "order": "desc"}])
```

### Automated Prospect Enrichment

Systematic enrichment workflow for large lists:

**Process**:
1. **Initial Search**: Get 100-500 prospects from LinkedIn search via execute()
2. **Paginate**: Use get_page() to collect all results beyond the first page
3. **First Filter**: Use query_cache() to remove obviously unqualified (wrong title, location, etc.)
4. **Batch Enrichment**: Enrich top 50 prospects with full profiles via execute()
5. **Email Discovery**: Find emails for top 25 prospects via execute()
6. **Web Research**: Extract company contacts for remaining prospects
7. **Final Scoring**: Apply lead scoring framework
8. **Export**: Use export_data(cache_key, "csv") for top-scored leads

**Efficiency Tips**:
- Start with larger searches (100+) to account for filtering
- Enrich in batches of 10-20 to avoid overwhelming results
- Prioritize email finding for highest-scored prospects first
- Use web scraping as backup when LinkedIn emails unavailable

## Limitations and Alternatives

### Platform Gaps

This skill focuses on B2B lead generation where LinkedIn, web scraping, and professional networks provide the most comprehensive data. For local business discovery and contact extraction, the combination of LinkedIn company search and web scraping provides strong coverage.

**Note on Crunchbase**: Crunchbase tools are disabled in v2. Use LinkedIn company search and Y Combinator data as alternatives for company research and funding information.

### Rate Limits and Timeouts

**Default Timeout**: 300 seconds (5 minutes) per MCP tool call

**Strategies for Large Datasets**:
1. **Batch Processing**: Use `count` parameter to limit results per call
   - Search 25-50 prospects at a time
   - Make multiple calls for larger lists
   - Allow processing time between batches

2. **Pagination**: Use `get_page(cache_key, offset, limit)` to retrieve additional results without re-executing the search.

3. **Parallel Processing**: For independent queries
   - Search multiple locations simultaneously
   - Enrich different prospect segments in parallel
   - Extract contacts from multiple websites at once

**Example**:
```
Instead of:
execute("linkedin", "search", "search_users", {"count": 200}) -> May timeout

Do this:
execute("linkedin", "search", "search_users", {"count": 50, "location": "California"})
execute("linkedin", "search", "search_users", {"count": 50, "location": "New York"})
execute("linkedin", "search", "search_users", {"count": 50, "location": "Texas"})
execute("linkedin", "search", "search_users", {"count": 50, "location": "Florida"})
```

### Data Freshness

**LinkedIn Data**: Real-time access through anysite MCP
- Results cached for 7 days via cache_key (use get_page/query_cache without re-fetching)
- Profile updates reflected in new execute() calls
- Company changes visible in real-time

**Recommendation**:
1. Use `execute("linkedin", "email", "find", {"user": ...})` for email discovery
2. Validate emails before sending (use email validation service)
3. Update your CRM when emails bounce

### Privacy and Compliance

**LinkedIn Terms of Service**:
- Respect LinkedIn's usage policies
- Don't automate excessive requests
- Comply with user privacy settings
- Follow GDPR/CCPA requirements

**Email Collection**:
- Only collect publicly available emails
- Provide opt-out mechanisms
- Comply with anti-spam laws (CAN-SPAM, GDPR)
- Maintain suppression lists

**Best Practices**:
- Use data for legitimate business purposes only
- Respect connection request limits
- Don't scrape private profile information
- Maintain data security for collected leads

## Reference Documentation

For advanced techniques and strategies, see:

- **[LINKEDIN_STRATEGIES.md](references/LINKEDIN_STRATEGIES.md)** - Advanced LinkedIn search patterns, Boolean operators, and targeting strategies
- **[WEB_SCRAPING.md](references/WEB_SCRAPING.md)** - Website contact extraction patterns, common page structures, and parsing techniques

## Troubleshooting

### Common Issues

#### 1. No Results from LinkedIn Search

**Symptoms**: Search returns 0 results or very few

**Causes**:
- Overly restrictive search criteria
- Incorrect location format
- Title keywords too specific
- Company name misspelled

**Solutions**:
- Broaden search criteria (remove some filters)
- Try location variations: "San Francisco", "San Francisco Bay Area", "SF"
- Use partial titles: "Sales" instead of "Vice President of Sales"
- Verify company names with `execute("linkedin", "search", "search_companies", {...})` first
- Check `llm_hint` in the response for guidance

**Example Fix**:
```
Too Restrictive:
execute("linkedin", "search", "search_users", {"title": "Vice President of Enterprise Sales", "location": "San Francisco, California", "company_keywords": "Salesforce Inc"})

Better:
execute("linkedin", "search", "search_users", {"title": "VP Sales OR Head of Sales", "location": "San Francisco Bay Area", "company_keywords": "Salesforce"})
```

#### 2. Email Not Found

**Symptoms**: Email find returns no results

**Causes**:
- Email not in database
- User privacy settings
- Email verification required

**Solutions**:
1. Extract email from company website instead
2. Use email pattern guessing (firstname.lastname@company.com)
3. Check for email in LinkedIn profile "Contact Info" section

**Alternative Workflow**:
```
1. execute("linkedin", "user", "get", {"user": "<username>"}) -> Get current company
2. execute("linkedin", "company", "get", {"company": "<company>"}) -> Get company website
3. execute("webparser", "parse", "parse", {"url": "<website>/contact", "extract_contacts": true}) -> Extract company emails
4. Use email pattern: first.last@companydomain.com
```

#### 3. Timeout Errors

**Symptoms**: Request times out after 300 seconds

**Causes**:
- Large result count requested
- Complex search criteria
- Server load issues

**Solutions**:
- Reduce `count` parameter (try 25-50 instead of 100+)
- Break large searches into multiple smaller searches
- Simplify search criteria
- Check `llm_hint` for retry guidance

**Example**:
```
May Timeout:
execute("linkedin", "search", "search_users", {"title": "Software Engineer", "count": 500})

Better:
execute("linkedin", "search", "search_users", {"title": "Software Engineer", "count": 50})
# Then use get_page(cache_key, next_offset, 50) for additional results
```

#### 4. Incomplete Profile Data

**Symptoms**: Profile missing work history, education, or skills

**Causes**:
- User profile not complete on LinkedIn
- Privacy settings limit data access
- Profile hasn't been updated

**Solutions**:
- Set `with_experience`, `with_education`, `with_skills` to true in params
- Accept incomplete data and supplement with web research
- Focus on prospects with complete profiles

#### 5. Invalid User URN

**Symptoms**: Error when using URN in follow-up calls

**Causes**:
- Incorrect URN format
- URN from different data source
- Stale URN reference

**Solutions**:
- Use LinkedIn username instead of URN when possible
- Verify URN format: `urn:li:fsd_profile:XXXXXXXXX`
- Get fresh URN from recent search
- Use profile URL as alternative identifier

### Getting Help

**anysite MCP Server Issues**:
- Verify MCP server is running and configured
- Check MCP server logs for errors
- Ensure authentication is set up correctly
- Check `llm_hint` field in error responses for actionable guidance

**Skill-Specific Questions**:
- Review reference documentation in `references/` folder
- Check examples in this SKILL.md file
- Review common workflows section

**Data Quality Issues**:
- Validate search criteria before large batches
- Test with small `count` values first
- Review data quality in chat summary before export
- Use `query_cache()` to filter low-quality results

**Integration Problems**:
- Verify CSV format matches your CRM requirements
- Test JSON structure before building integrations
- Check timezone and date formats in exports

## Example Use Cases

### Use Case 1: Enterprise SaaS Sales

**Goal**: Find 100 qualified enterprise sales prospects

**Process**:
1. Define ICP: VP/Director level, Enterprise Software, 500-5000 employees
2. Search LinkedIn: `execute("linkedin", "search", "search_users", {"title": "VP Sales", "company_keywords": "Enterprise Software", "count": 100})`
3. Filter by company size using `execute("linkedin", "search", "search_companies", {...})`
4. Enrich top 30 prospects with full profiles
5. Find emails for top 20 prospects
6. Export CSV via `export_data(cache_key, "csv")` for Salesforce import

**Success Metrics**:
- 100 prospects found and qualified
- 30 enriched with full work history
- 15-20 verified emails obtained
- 2-3 hours total time investment

### Use Case 2: Tech Recruiter Sourcing

**Goal**: Source 50 Python engineers for startup

**Process**:
1. Search: `execute("linkedin", "search", "search_users", {"keywords": "Python Django AWS", "title": "Software Engineer", "location": "Remote", "count": 100})`
2. Filter: Use `query_cache()` to remove <2 years experience
3. Enrich: Get skills and education for top 50
4. Score: Rank by skills match and experience level
5. Contact: Find emails for top 25
6. Outreach: Personalized emails referencing their skills/projects

**Success Metrics**:
- 50 qualified candidates sourced
- 25 emails obtained
- 5-10 candidates engaged
- Time to first response: <24 hours

### Use Case 3: Partnership Outreach

**Goal**: Find potential integration partners in marketing tech

**Process**:
1. Search companies: `execute("linkedin", "search", "search_companies", {"keywords": "marketing automation", "employee_count": ["51-200"]})`
2. Identify decision-makers: `execute("linkedin", "search", "search_users", {"title": "VP Product OR Head of Partnerships", "company_keywords": "<company>"})`
3. Research: Get company details and recent LinkedIn posts via `execute("linkedin", "post", "get_user_posts", {"user": ...})`
4. Enrich: Full profiles for all decision-makers
5. Personalize: Reference their product and use cases
6. Multi-channel: LinkedIn + email outreach

**Success Metrics**:
- 30 potential partners identified
- 40 decision-makers found
- 25 emails + LinkedIn connection requests sent
- 10-15 responses received

---

**Ready to start generating leads?** Ask Claude to help you find prospects, enrich profiles, or build comprehensive lead lists using this skill!
