---
name: platform-scraper
description: Scrape gig platforms and communities for leads matching agency services
tags: [scraping, platforms, lead-generation, gigs]
---

# Platform Scraper

Scrapes freelance and community platforms for gig listings and posts matching the agency's services. Covers 17 platforms: Freelancer, PeoplePerHour, Guru, Fiverr, Upwork, Reddit, LinkedIn, Behance, Dribbble, Shopify Community, IndieHackers, Funding News, Twitter/X, Instagram Brands, Product Hunt, Google Maps, and Shopify Store Discovery. Extracted from Hawk's watcher architecture but expressed as Claude-readable instructions, not TypeScript.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and `scoring` sections
- WebSearch tool available
- Optional: `crm-writer` skill for logging results

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[].keywords` -- all service keyword arrays
   - `icp.primary_keywords`, `icp.secondary_keywords`
   - `icp.negative_keywords` -- to filter out self-promoters and irrelevant results
3. Accept parameters:
   - `platforms` -- list of platforms to search, or `"all"` (default: `"all"`)
   - `max_results` -- max leads to return (default: 20)
   - `time_window` -- how far back to search (default: `"past week"`)

4. Available platforms: Freelancer, PeoplePerHour, Guru, Fiverr, Upwork, Reddit, LinkedIn, Behance, Dribbble, Shopify Community, IndieHackers, Funding News, Twitter/X, Instagram Brands, Product Hunt, Google Maps, Shopify Store Discovery.

## Phase 1: Platform-Specific Scraping

For each selected platform, use WebSearch with site-specific queries. Generate 2-3 queries per platform by rotating service keywords. Execute searches with rate limiting: max 3 concurrent, 2-second pause between batches of 3.

### Freelancer.com

- Query: `site:freelancer.com/projects "{keyword}"` for each service keyword
- Extract: project title, description, budget range, skills required, posted date, URL, proposals count
- Note: Freelancer projects always have `/projects/` in the URL path. Filter results missing this pattern.

### PeoplePerHour

- Query: `site:peopleperhour.com "{keyword}" "project"`
- Extract: project title, description, budget, posted date, URL

### Guru

- Query: `site:guru.com/jobs "{keyword}"`
- Extract: title, description, budget, skills, URL

### Fiverr

- Query: `site:fiverr.com/categories "{keyword}"` OR search for buyer request forums
- Note: Fiverr is seller-first. Focus on buyer request threads and "looking for" language, not seller profiles.

### Upwork

- Query: `site:upwork.com/freelance-jobs "{keyword}"`
- Extract: title, description, budget, client history, URL

### Reddit

- Query: `site:reddit.com/r/shopify OR site:reddit.com/r/ecommerce "{keyword}" "{intent_keyword}"`
- Also search: r/smallbusiness, r/Entrepreneur, r/DTC, r/forhire
- Extract: post title, body text, subreddit, author, post date, URL, comment count
- Prioritize posts with question marks and help-seeking language ("need", "looking for", "recommend", "anyone know").

### LinkedIn

- Query: `site:linkedin.com/posts "{keyword}" "{intent_keyword}"`
- Also: `site:linkedin.com/jobs "{keyword}"`
- Extract: post text, author, company, post date, URL
- Note: LinkedIn post URLs are not always indexable. Accept partial results.

### Behance

- Query: `site:behance.net/joblist "{keyword}"`
- Extract: job title, company, description, URL

### Dribbble

- Query: `site:dribbble.com/jobs "{keyword}"`
- Extract: job title, company, description, URL

### Shopify Community

- Query: `site:community.shopify.com "{keyword}" "{intent_keyword}"`
- Extract: thread title, body, author, date, URL
- Focus on threads in "Shopify Design" and "Shopify Apps" categories.

### IndieHackers

- Query: `site:indiehackers.com "{keyword}" "{intent_keyword}"`
- Extract: post title, body, author, date, URL
- Look for founders asking about ecommerce, Shopify, or D2C store builds.

### Funding News

- Query: `"{industry} startup" "raises" OR "funding" OR "seed round" this week`
- Sources to check: TechCrunch, Crunchbase, YourStory (for India)
- Extract: company name, amount raised, round, industry, investors, URL
- Parse headline for company name (usually the first entity before "raises" or "secures").
- Parse for funding amount: look for patterns like `$X million`, `Rs X crore`, etc.

### Twitter/X

- Query: `site:twitter.com OR site:x.com "{keyword}" "shopify" OR "ecommerce" OR "d2c"`
- Also: `site:x.com "{industry}" "just launched" OR "coming soon" OR "new store"`
- Extract: tweet text, handle, bio, website from profile, follower count
- Focus on brand accounts, not agencies or developers

### Instagram Brands

- Query: `site:instagram.com "{keyword}" "shop" OR "store" OR "link in bio"`
- Target hashtags: #shopifystore, #d2cbrand, #ecommerce, #shopifyseller
- Extract: profile name, handle, bio, website link from bio, follower count
- Focus on D2C brands with active storefronts

### Product Hunt

- Query: `site:producthunt.com "{keyword}" OR "ecommerce" OR "shopify"`
- Extract: product name, tagline, maker name, website, launch date, upvotes
- Focus on recently launched D2C products and ecommerce tools

### Google Maps / Business Directories

- Query: `site:google.com/maps "{industry}" "{market}"` + `site:justdial.com "{keyword}"` (India) + `site:yelp.com "{keyword}"` (US/UK)
- Extract: business name, phone number, website, address, rating
- Phone numbers are a key differentiator for multi-channel outreach

### Shopify Store Discovery

- Query: `site:myshopify.com "{industry_keyword}"` + `site:builtwith.com "shopify" "{industry}"`
- Extract: store name, URL, theme (if visible), industry
- Look for stores with basic themes (Dawn, Debut) indicating redesign need
- These are warm leads: they already use Shopify but need upgrades

## Phase 2: Normalize Results

Normalize all results from every platform into a single standard format:

```json
{
  "title": "Project or post title",
  "description": "First 500 chars of description or body text",
  "platform": "Freelancer",
  "url": "https://...",
  "budget": "$500-$1000",
  "posted_date": "2024-01-15",
  "market": "US",
  "contact": "username or name if available",
  "company": "Company name if identifiable from context",
  "skills_required": ["shopify", "liquid", "theme-development"],
  "contact_surfaces": {
    "has_email": false,
    "has_linkedin": false,
    "has_instagram": false,
    "has_phone": false,
    "has_website": true,
    "channel_count": 1,
    "discovery_notes": "Website from store URL."
  },
  "raw_data": {}
}
```

Rules:
- `market` should be inferred from currency symbols, country mentions, or TLD patterns in the content.
- `budget` should be normalized to a consistent format: "$X" or "$X-$Y" or "Rs X" for Indian currency. Set to empty string if not found.
- `contact` should capture the username, author name, or poster identity if visible.
- `skills_required` should be extracted from explicit skill tags or inferred from description keywords.

## Phase 3: Filter

Apply filters in this order:

1. **Negative keyword filter**: Check title + description against `icp.negative_keywords`. Reject any result matching a negative keyword (these are typically self-promoters, spam, or irrelevant categories).

2. **Relevance check**: The result must match at least one `primary_keyword` OR one `secondary_keyword` from the config. Results matching zero keywords are discarded.

3. **Recency filter**: Skip results with a `posted_date` older than the `time_window` parameter. If `posted_date` is empty/unknown, keep the result but mark it with `"date_unknown": true`.

4. **Dedup by URL**: Remove exact URL duplicates. If the same company or person appears from different URLs (same underlying opportunity), keep only the most recent or most detailed one.

## Phase 4: Output

Return an array of normalized leads, sorted by relevance:
1. Primary keyword matches first (stronger signal)
2. Secondary keyword matches second
3. Within each group, sort by recency (newest first)

Present results grouped by platform with counts:

```
Found {N} leads across {M} platforms:

Freelancer ({count}):
1. "Project title" - $budget - URL
2. ...

Reddit ({count}):
1. "Post title" - r/subreddit - URL
2. ...

LinkedIn ({count}):
...

[Other platforms with results]

Total: {N} leads
Filtered out: {X} (negative keywords: {a}, irrelevant: {b}, stale: {c}, duplicates: {d})
```

Trim to `max_results` after sorting. If more results exist, note the overflow count.

## Example Usage

Trigger phrases:
- "Scrape platforms for leads"
- "Find gigs on Freelancer and Upwork"
- "Search all platforms for Shopify projects"
- "Run platform scraper"
- "Find freelance gigs matching our services"

```
User: Scrape Freelancer and Reddit for Shopify leads
Assistant: [reads config, generates site-specific queries for Freelancer and Reddit, executes with rate limiting, normalizes to standard format, filters and deduplicates, presents grouped results]
```

```
User: Run platform scraper on all platforms, last 3 days
Assistant: [same flow across all 12 platforms, time_window set to 3 days]
```
