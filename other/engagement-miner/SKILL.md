---
name: engagement-miner
description: Extract warm prospects from competitor and industry post engagers across LinkedIn, Twitter, and blogs
tags: [prospecting, engagement, competitors, warm-leads, social-selling]
---

# Engagement Miner

Finds engaged audiences on competitor posts, industry discussions, and thought-leader content. Extracts commenters and engagers from LinkedIn posts, Twitter threads, and blog comments. These are warm prospects who already care about the topic and are pre-qualified by their own engagement behavior.

## Prerequisites

- `agency.config.json` at repo root with `services`, `icp`, and `scoring` sections
- WebSearch tool available
- Optional: `person-researcher` skill for enriching extracted prospects
- Optional: `crm-writer` skill for logging prospects to CRM

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `services[].keywords` -- topic relevance for filtering
   - `icp.segments[].titles`, `icp.segments[].seniority` -- prospect qualification criteria
   - `icp.segments[].industries` -- industry filters
   - `icp.segments[].company_size` -- company size filters
   - `icp.primary_keywords`, `icp.secondary_keywords` -- topic matching
   - `icp.negative_keywords` -- filter out competitors and service providers
3. Accept parameters:
   - `source_posts` -- list of specific post URLs to mine (default: none, discover automatically)
   - `competitors` -- competitor names/profiles whose posts to mine (default: none, user must supply)
   - `topics` -- topic keywords to find relevant posts (default: use config keywords)
   - `platforms` -- platforms to mine: `linkedin | twitter | blogs` (default: all)
   - `max_prospects` -- max prospects to return (default: 50)
   - `min_engagement` -- minimum engagement threshold for source posts (default: 10 comments)

## Phase 1: Source Post Discovery

If `source_posts` not provided, discover high-engagement posts to mine.

### LinkedIn post discovery:
- `site:linkedin.com/posts "{competitor_name}" "{service_keyword}"`
- `site:linkedin.com/posts "{service_keyword}" "comments" OR "agree" OR "great point"`
- `site:linkedin.com/posts "{icp_industry}" "{intent_keyword}"`
- Prioritize posts with visible comment counts > `min_engagement`.

### Twitter thread discovery:
- `site:twitter.com OR site:x.com "{competitor_name}" "{service_keyword}" "replies"`
- `site:twitter.com OR site:x.com "{service_keyword}" "thread" OR "unpopular opinion" "{icp_industry}"`
- Look for threads with high reply counts.

### Blog comment discovery:
- `"{competitor_name}" blog "{service_keyword}" "comments"`
- `"{industry_keyword}" blog "leave a comment" OR "responses" "{service_keyword}"`
- Target popular industry blogs with active comment sections.

### For each source post, capture:
```json
{
  "post_url": "URL",
  "platform": "LinkedIn | Twitter | Blog",
  "author": "Post author name",
  "author_company": "Author's company if visible",
  "topic": "Main topic of the post",
  "engagement_count": "Number of comments/replies visible",
  "posted_date": "Date if available",
  "relevance": "HIGH | MEDIUM"
}
```

Target 10-20 high-engagement source posts across platforms.

## Phase 2: Engager Extraction

For each source post, extract people who engaged (commented, replied, shared):

### LinkedIn engager extraction:
- Search: `site:linkedin.com "{post_title}" "{commenter_snippet}"` to find comment previews
- Search: `site:linkedin.com/in "{keyword_from_post}" "{icp_title}"` to find people who likely engaged
- Extract from search snippets: commenter names, their titles, companies
- Note: LinkedIn comments are not always fully indexed. Accept partial results.

### Twitter engager extraction:
- Search: `site:twitter.com OR site:x.com "replying to @{author_handle}" "{topic_keyword}"`
- Search for quoted retweets: `site:twitter.com "{post_url_fragment}"`
- Extract: replier handles, names, bios if visible in snippets

### Blog comment extraction:
- Use WebFetch on the blog URL (if available) to read comment sections
- Extract: commenter names, linked websites, comment content
- Commenter websites are valuable for company identification

### For each extracted engager:
```json
{
  "name": "Full name",
  "handle": "Social handle or username",
  "platform": "LinkedIn | Twitter | Blog",
  "title": "Job title if visible",
  "company": "Company name if visible",
  "profile_url": "Profile URL if available",
  "comment_snippet": "What they said (first 200 chars)",
  "source_post_url": "The post they engaged with",
  "source_post_topic": "Topic of the source post"
}
```

## Phase 3: Prospect Qualification

Filter and score extracted engagers against ICP:

### Title matching:
- Compare `title` against `icp.segments[].titles` and `icp.segments[].seniority`.
- Exact title match: +30 points
- Seniority level match: +20 points
- No title available: +5 points (benefit of the doubt)

### Company relevance:
- If `company` matches ICP industries: +20 points
- If company size is estimable and within ICP range: +10 points
- If company is a known competitor (from `competitors` param): -100 points (disqualify)

### Engagement quality:
- Comment shows pain point or need: +25 points
- Comment asks a question: +20 points
- Comment shares experience: +15 points
- Generic agreement ("Great post!"): +5 points
- Self-promotional comment: -50 points (disqualify)

### Negative keyword filter:
- Check name, title, company, and comment against `icp.negative_keywords`.
- Disqualify any match.

### Scoring thresholds:
- **HOT PROSPECT** (60+): Strong title match + relevant engagement
- **WARM PROSPECT** (35-59): Partial match, worth researching
- **COOL** (<35): Weak match, skip unless volume is low

## Phase 4: Deduplication

1. Deduplicate by name + company combination (same person across multiple posts).
2. For duplicates, keep the entry with the richest data (most fields populated).
3. Merge comment snippets from multiple engagements into a single prospect record.
4. Deduplicate by profile URL if available (exact match).

## Phase 5: Output

Return structured prospect list:

```json
{
  "mining_summary": {
    "source_posts_analyzed": 15,
    "total_engagers_extracted": 120,
    "after_qualification": 50,
    "after_dedup": 42,
    "breakdown": {
      "hot": 8,
      "warm": 22,
      "cool": 12
    }
  },
  "prospects": [
    {
      "name": "Jane Doe",
      "title": "Head of Ecommerce",
      "company": "BrandCo",
      "platform": "LinkedIn",
      "profile_url": "https://linkedin.com/in/janedoe",
      "score": 75,
      "tier": "HOT",
      "engagement_context": "Commented on CRO post asking about checkout optimization",
      "comment_snippets": ["We've been struggling with cart abandonment..."],
      "source_posts": ["https://linkedin.com/posts/..."],
      "recommended_approach": "Reference their checkout concern, offer CRO audit insight",
      "next_step": "RESEARCH | CONNECT | EMAIL"
    }
  ]
}
```

Present formatted summary:

```
ENGAGEMENT MINING REPORT
Source posts analyzed: {N} across {platforms}
Total engagers found: {N}
Qualified prospects: {N} ({hot} HOT, {warm} WARM)

HOT PROSPECTS ({count}):
1. {name} -- {title} at {company} -- Score: {N}
   Context: "{comment_snippet}"
   Approach: {recommended_approach}
   Next: {next_step}

WARM PROSPECTS ({count}):
1. {name} -- {title} at {company} -- Score: {N}
   Context: "{comment_snippet}"
   Next: {next_step}

DISQUALIFIED: {count} (competitors: {a}, self-promoters: {b}, irrelevant: {c})

TOP ENGAGEMENT TOPICS:
1. {topic} -- {count} qualified engagers found
```

## Phase 6: CRM Logging

If `crm-writer` is available and user approves:
- Log HOT and WARM prospects to CRM pipeline tab
- Columns: Date, Name, Title, Company, Platform, Source Post, Score, Tier, Context, Status
- Set initial status: "MINED"

## Example Usage

Trigger phrases:
- "Mine engagement on competitor posts"
- "Find prospects from LinkedIn comments"
- "Extract engagers from this post: [URL]"
- "Who's engaging with Shopify CRO content on LinkedIn?"
- "Mine warm leads from competitor content"
- "Find people commenting on ecommerce topics"

```
User: Mine engagement from WebSavvy and Starter Labs LinkedIn posts about Shopify
Assistant: [reads config, discovers high-engagement posts by those competitors, extracts commenters, qualifies against ICP, scores and deduplicates, presents ranked prospect list with approach recommendations]
```

```
User: Extract prospects from these 3 LinkedIn posts: [URL1, URL2, URL3]
Assistant: [same flow but uses provided URLs directly as source posts, skips discovery phase]
```
