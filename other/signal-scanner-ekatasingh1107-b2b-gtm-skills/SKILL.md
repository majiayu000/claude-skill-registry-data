---
name: signal-scanner
description: Search the web for companies showing buying signals matching the agency ICP. Enforces 75/25 geo split and 20 gig + 5 company daily targets.
tags: [signals, prospecting, web-search, lead-generation]
---

# Signal Scanner

Searches multiple platforms for companies and individuals showing real-time buying signals that match the agency's ICP. Uses WebSearch to find leads across Reddit, Twitter/X, LinkedIn, job boards, funding news, Shopify Community, HackerNews, and gig platforms.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and `scoring` sections
- WebSearch tool available
- Optional: `crm-writer` skill for dedup against existing CRM leads

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[].keywords` -- all service keyword arrays
   - `icp.segments[]` -- each segment's markets, industries, titles, description
   - `icp.primary_keywords`, `icp.secondary_keywords`, `icp.intent_keywords`
   - `icp.negative_keywords` -- to filter out self-promoters
   - `scoring.platform_weights` -- to know which platforms to search
   - `scoring.hiring_signals` -- phrases that indicate active buying

   **CRITICAL**: All search queries MUST be derived from `agency.config.json` keywords. When Plasho's positioning changes week-to-week, queries change automatically. NEVER hardcode search queries.

3. Accept optional parameters:
   - `platforms` -- list of platforms to search (default: all from platform_weights)
   - `max_results` -- max leads to return (default: 25)
   - `time_window` -- how far back to search (default: "past week")
   - `focus_segment` -- specific ICP segment to target (default: all)
   - `daily_targets` -- read from `agency.config.json outreach.daily_targets` (default: 20 gig + 5 company = 25 total)
   - `geo_split` -- read from `agency.config.json outreach.geo_split` (default: 75% international, 25% India)

## Phase 1: Query Generation

Build search queries by combining service keywords with intent signals and platform-specific syntax.

### Lead Type Targeting

Queries are split into two categories:

**GIG LEAD QUERIES (target: 20 leads)**
Platforms: Freelancer, Upwork, PeoplePerHour, Guru, Fiverr
Must show clear buying signal and budget.

**COMPANY LEAD QUERIES (target: 5 leads)**
Platforms: LinkedIn, Reddit, Twitter/X, Funding News, Product Hunt, Shopify Community, Instagram Brands, Google Maps, Shopify Store Discovery
Must show very strong signal + ICP fit.

### Geo Split Enforcement

75% of queries target international markets (US, UK, AU, EU):
- Add geo modifiers: "United States", "UK", "Australia", "Europe"
- Filter by .com, .co.uk, .com.au domains where applicable

25% of queries target India:
- Add geo modifiers: "India", "Mumbai", "Delhi", "Bangalore"
- Include Indian platforms and directories

### Query templates per platform:

**Reddit:**
- `site:reddit.com "{service_keyword}" "{intent_keyword}" after:{date}`
- Subreddits to target: r/shopify, r/ecommerce, r/smallbusiness, r/startups, r/Entrepreneur, r/DTC
- Example: `site:reddit.com "shopify developer" "need help" after:2024-01-01`

**Twitter/X:**
- `site:twitter.com OR site:x.com "{service_keyword}" "{intent_keyword}"`
- Example: `site:x.com "looking for shopify expert" "hire"`

**LinkedIn:**
- `site:linkedin.com/posts "{service_keyword}" "{intent_keyword}"`
- `site:linkedin.com/jobs "{service_keyword}"`
- Example: `site:linkedin.com/posts "shopify developer" "hiring"`

**Job Boards:**
- `site:indeed.com OR site:glassdoor.com "{service_keyword}" "{market}"`
- `site:angel.co OR site:wellfound.com "{service_keyword}"`

**Funding News:**
- `"{industry} startup" "raises" OR "funding" OR "seed round" OR "series A" {time_window}`
- Filter to companies in ICP industries

**Shopify Community:**
- `site:community.shopify.com "{intent_keyword}" "{service_keyword}"`

**HackerNews:**
- `site:news.ycombinator.com "{service_keyword}" "{intent_keyword}"`

**Gig Platforms (Freelancer, Upwork, PeoplePerHour, Guru, Fiverr):**
- `site:freelancer.com/projects "{service_keyword}"`
- `site:peopleperhour.com "{service_keyword}"`

**Upwork:**
- `site:upwork.com/jobs "{service_keyword}"`
- Example: `site:upwork.com/jobs "shopify developer"`

**Twitter/X (Brand Discovery):**
- `site:twitter.com OR site:x.com "{d2c_keyword}" "shopify" OR "ecommerce" OR "d2c"`
- Also: `site:x.com "{industry}" "just launched" OR "coming soon" OR "new store"`
- Focus on brand accounts, not agencies

**Instagram Brands:**
- `site:instagram.com "{d2c_keyword}" "shop" OR "store" OR "link in bio"`
- Target hashtags: #shopifystore, #d2cbrand, #ecommerce, #shopifyseller
- Extract: profile name, handle, website link from bio

**Product Hunt:**
- `site:producthunt.com "{d2c_keyword}" OR "ecommerce" OR "shopify"`
- Focus on recently launched D2C products

**Google Maps / Business Directories:**
- `site:google.com/maps "{industry}" "{market}"` + justdial.com (India), yelp.com (US/UK)
- Extract: business name, phone, website

**Shopify Store Discovery:**
- `site:myshopify.com "{industry_keyword}"` + `site:builtwith.com "shopify" "{industry}"`
- Look for stores with basic themes (Dawn, Debut) indicating redesign need

### Query generation rules:

- Generate queries to hit daily targets: 20 gig leads + 5 company leads.
- Prioritize platforms with higher `platform_weights` scores.
- Include market/country filters for geo-targeted segments.
- Allocate queries based on daily targets. Gig platforms need more queries (20 leads vs 5).
- Enforce geo split: 75% of queries must target US/UK/AU/EU markets, 25% India.

## Phase 2: Search Execution

Execute searches using WebSearch with rate limiting:

- **Max 3 concurrent searches** at any time.
- **2-second pause between batches** of 3.
- Process results as they return; do not wait for all to complete.

For each search result, extract:
- `url` -- the source URL
- `title` -- page title or post title
- `snippet` -- the text excerpt from the search result
- `platform` -- which platform (inferred from URL domain)
- `posted_date` -- if visible in the search result

## Phase 3: Signal Validation

For each raw result, validate it is a genuine buying signal:

1. **Negative keyword filter**: Check title + snippet against `icp.negative_keywords`. Discard if any match (these are self-promoters, not buyers).

2. **Relevance check**: The result must contain at least one `primary_keyword` OR one `secondary_keyword` AND at least one `intent_keyword`. If it has only keywords but no intent, mark as LOW confidence.

3. **Recency check**: Prefer results from the last 7 days. Flag anything older than 30 days as STALE.

4. **Duplicate check**: Compare URLs against previously returned results in this session. Skip exact URL duplicates. Also skip if the same company/person appears from a different URL (same underlying signal).

5. **Lead type classification**: Classify each result as either "gig" or "company" based on the source platform. Gig platforms (Freelancer, Upwork, PPH, Guru, Fiverr) = gig lead. Everything else = company lead.

6. **Geo classification**: Determine the lead's geography. Classify as "international" (US/UK/AU/EU) or "india" based on content, URL, currency, or explicit location mentions.

## Phase 4: Entity Extraction

For each validated signal, extract structured data:

```json
{
  "company": "Company name (if identifiable)",
  "website": "Company website (if findable from context)",
  "person": "Name of the person posting/mentioned",
  "title": "Their job title (if available)",
  "url": "Source URL where signal was found",
  "platform": "Reddit | Twitter | LinkedIn | Freelancer | Upwork | etc.",
  "signal_type": "hiring | funding | job_posting | community_question | gig_request | tech_migration | product_launch | brand_discovery | store_discovery",
  "urgency": "HIGH | MEDIUM | LOW",
  "reason": "1-line summary of why this is a signal",
  "country": "Country (if determinable)",
  "posted_date": "ISO date or relative",
  "raw_snippet": "The relevant text excerpt",
  "confidence": "HIGH | MEDIUM | LOW",
  "lead_type": "gig | company",
  "geo_bucket": "international | india",
  "contact_surfaces": {
    "has_email": true,
    "has_linkedin": false,
    "has_instagram": false,
    "has_phone": false,
    "has_website": true,
    "channel_count": 2,
    "discovery_notes": "Email from gig platform. Website from company field."
  }
}
```

### Contact surface defaults by platform:

| Platform | email | linkedin | instagram | phone | website |
|----------|-------|----------|-----------|-------|---------|
| Freelancer/Upwork/PPH/Guru/Fiverr | YES | NO | NO | NO | MAYBE |
| LinkedIn Posts/Jobs | MAYBE | YES | MAYBE | MAYBE | MAYBE/YES |
| Reddit | NO | MAYBE | MAYBE | NO | MAYBE |
| Twitter/X | NO | MAYBE | MAYBE | NO | MAYBE |
| Instagram Brands | NO | MAYBE | YES | NO | YES |
| Shopify Community | NO | MAYBE | MAYBE | NO | YES |
| Funding News | MAYBE | YES | MAYBE | MAYBE | YES |
| Product Hunt | MAYBE | YES | MAYBE | NO | YES |
| Google Maps | MAYBE | NO | MAYBE | YES | YES |
| Shopify Store Discovery | NO | MAYBE | MAYBE | NO | YES |

Use these defaults when extracting contact surfaces. Override with actual data when found in the signal content. `channel_count` = number of YES/MAYBE channels confirmed as available.

### Urgency rules:
- **HIGH**: Explicit hiring/buying language + budget mentioned + recent (< 48h)
- **MEDIUM**: Intent keywords present + relevant service match + recent (< 7 days)
- **LOW**: Relevant topic but weak intent signal or older than 7 days

## Phase 5: Dedup Against CRM

If `crm-writer` skill is available and CRM is configured:

1. Read existing leads from the relevant CRM tab (e.g., "Hawk Leads", "Researched Leads").
2. Compare by: company name (fuzzy), URL (exact), person name + company combo.
3. Mark duplicates as `"is_duplicate": true` but still include them in output with a note.

## Phase 6: Review

Present the results to the user, separated by lead type:

```
Found {N} signals across {M} platforms:

COMPANY LEADS ({count}/5 target):
1. [Platform] Company - "reason" (urgency: HIGH, confidence: HIGH, geo: US)
2. ...

GIG LEADS ({count}/20 target):
1. [Platform] "gig title" - "reason" (urgency: HIGH, budget: $X, geo: UK)
2. ...

GEO SPLIT: {X}% international, {Y}% India (target: 75/25)
Duplicates skipped: {count}
Rejected (self-promoters): {count}
```

Write directly to CRM (no approval gate).

## Phase 7: Log to CRM

Use `crm-writer` to append new signals to the configured CRM tab. Write one row per signal with columns: Date, Platform, Company, Person, URL, Signal Type, Urgency, Reason, Country, Lead Type, Geo Bucket, Score.

## Example Usage

Trigger phrases:
- "Scan for signals"
- "Find buying signals"
- "Run a signal scan"
- "Search for leads showing intent"
- "Find companies looking for Shopify help"

```
User: Scan for buying signals this week
Assistant: [reads config, generates queries across Reddit/LinkedIn/Freelancer/Upwork/etc., executes with rate limiting, validates and structures results, presents sorted by lead type with geo split]
```

```
User: Find signals on Reddit and Shopify Community only
Assistant: [same flow but limited to those 2 platforms]
```
