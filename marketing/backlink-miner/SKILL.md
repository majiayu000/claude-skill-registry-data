---
name: backlink-miner
description: Find broken links, competitor backlinks, and link building outreach targets
tags: [seo, backlinks, link-building, outreach, broken-links]
---

# Backlink Miner

Discovers link building opportunities by finding broken links on relevant sites, analyzing competitor backlink profiles via search operators, and identifying guest post and editorial link targets. Scores each opportunity by estimated domain authority and topical relevance. Outputs a prioritized backlink targets list ready for outreach.

## Prerequisites

- WebSearch tool available for search operator queries and SERP analysis
- Browser automation tool available for page crawling and link checking
- Target domain or competitor domain(s) to analyze
- Optional: `agency.config.json` for industry context and service keywords

## Phase 0: Read Config

1. Read `agency.config.json` from the project root (if available).
2. Extract `services[].keywords` to understand topical relevance for link targets.
3. Extract `icp.segments[].industries` to identify relevant verticals for outreach.
4. Check `tools.websearch` and `tools.browser` availability.
5. Accept parameters:
   - `target_domain` -- (required) the domain you want to build links to
   - `competitor_domains` -- (optional) array of competitor domains to mine backlinks from
   - `niche_keywords` -- (optional) array of industry/niche keywords for finding relevant sites
   - `mode` -- `broken-links` | `competitor-backlinks` | `guest-posts` | `all`. Default: `all`
   - `depth` -- `quick` (top 20 targets) | `standard` (50 targets) | `deep` (100+ targets). Default: `standard`

## Phase 1: Broken Link Discovery

### Find Resource Pages with Broken Links
- WebSearch: `"{{niche_keyword}}" inurl:resources` -- find resource pages in the niche
- WebSearch: `"{{niche_keyword}}" inurl:links` -- find link roundup pages
- WebSearch: `"{{niche_keyword}}" "useful links" OR "helpful resources" OR "recommended sites"`
- WebSearch: `"{{niche_keyword}}" intitle:resources intitle:links`

### Identify Dead Links on Resource Pages
For each discovered resource page:
- Visit the page via browser automation
- Extract all outbound links
- Check each link for HTTP status (404, 410, 500, timeout)
- Record: page URL, anchor text of dead link, original destination, page topic

### Match Dead Links to Your Content
For each broken link found:
- Analyze the anchor text and surrounding context
- Determine if the target domain has (or could create) equivalent content
- Score the replacement opportunity:
  - Exact match: target already has a page that fits perfectly
  - Near match: target has related content that could work with minor edits
  - Content gap: target would need to create new content, but the topic is relevant

### Compile Broken Link Targets
For each opportunity:
- Resource page URL and contact information (email, contact form)
- Broken link anchor text and original URL
- Suggested replacement URL from target domain
- Page authority estimate (based on domain and page metrics)

## Phase 2: Competitor Backlink Mining

### Discover Competitor Backlinks via Search Operators
For each competitor domain:
- WebSearch: `"{{competitor_domain}}" -site:{{competitor_domain}}` -- find pages linking to competitor
- WebSearch: `link:{{competitor_domain}}` -- direct backlink search
- WebSearch: `"{{competitor_domain}}" intext:"{{competitor_domain}}"` -- find text mentions with links
- WebSearch: `"{{competitor_brand}}" -site:{{competitor_domain}}` -- brand mentions that may include links

### Categorize Backlink Sources
Classify each discovered backlink source:
- **Editorial**: mentioned in articles, blog posts, news stories
- **Directory**: listed in business directories, industry listings
- **Guest Post**: competitor authored content on another site
- **Forum/Community**: mentioned in forums, Q&A sites, Reddit, Quora
- **Social**: social media profiles and posts
- **Review Site**: listed on review platforms (G2, Capterra, Clutch)
- **Roundup**: included in "best of" or "top X" list articles
- **Sponsorship**: sponsor mentions, event listings

### Identify Replicable Backlinks
For each competitor backlink:
- Can the target domain get listed on the same site? (directories, roundups)
- Can the target domain pitch a similar guest post?
- Can the target domain offer a better resource for the same editorial context?
- Is the linking site accepting contributions or listings?
- Flag easy wins: open directories, "submit your site" pages, active guest post programs

## Phase 3: Guest Post and Editorial Opportunities

### Find Guest Post Targets
- WebSearch: `"{{niche_keyword}}" "write for us"` -- explicit guest post invitations
- WebSearch: `"{{niche_keyword}}" "guest post" OR "guest article" OR "contribute"`
- WebSearch: `"{{niche_keyword}}" "become a contributor" OR "submit an article"`
- WebSearch: `"{{niche_keyword}}" inurl:write-for-us OR inurl:guest-post OR inurl:contribute`
- WebSearch: `"{{niche_keyword}}" "accepting guest posts" OR "guest authors"`

### Evaluate Guest Post Sites
For each potential guest post target:
- Visit the site, assess content quality and relevance
- Check publishing frequency (active sites > dormant ones)
- Look for guest post guidelines and editorial standards
- Check if they allow dofollow links in author bio or content
- Estimate domain authority via search signals

### Find Editorial Link Opportunities
- WebSearch: `"{{niche_keyword}}" "expert roundup" OR "expert opinion"` -- roundup participation
- WebSearch: `"{{niche_keyword}}" "interview" OR "Q&A" OR "podcast guest"` -- media appearances
- WebSearch: `"{{niche_keyword}}" "comment" OR "respond" OR "quote"` -- journalist quote opportunities
- WebSearch: `"{{niche_keyword}}" HARO OR "help a reporter"` -- reporter query platforms
- WebSearch: `"{{niche_keyword}}" "link roundup" OR "weekly roundup" OR "monthly roundup"`

## Phase 4: Unlinked Brand Mention Mining

### Find Unlinked Mentions
- WebSearch: `"{{brand_name}}" -site:{{target_domain}} -link:{{target_domain}}` -- mentions without links
- WebSearch: `"{{brand_name}}" -site:{{target_domain}}` -- all external mentions
- For each mention found, visit the page and check if the mention includes a hyperlink
- Record unlinked mentions with page URL, context, and contact information

### Prioritize Mention Conversions
- Higher priority: mentions on high-authority sites, mentions in editorial content
- Medium priority: mentions in forum posts, community discussions
- Lower priority: mentions on low-traffic or low-quality sites

## Phase 5: Scoring and Prioritization

Score each backlink target on a 1-10 scale across:

### Relevance Score
- How topically relevant is the linking site to the target domain?
- Is the content context a natural fit for a link?
- Would a reader on that page find the target domain genuinely useful?

### Authority Score
- WebSearch: `"{{linking_domain}}" "domain authority" OR "DA" OR "domain rating"` -- find reported metrics
- Estimate based on: indexed page count, apparent traffic level, brand recognition
- Sites ranking well for competitive keywords = higher authority signal

### Acquisition Difficulty
- Open submission (directories, guest post programs): Easy
- Outreach required (broken link replacement, mention conversion): Medium
- Relationship-building required (editorial features, partnerships): Hard

### Opportunity Score Calculation
```
Opportunity Score = (Relevance x Authority) / Difficulty
```

Sort all targets by opportunity score descending.

## Phase 6: Output

Return structured JSON:

```json
{
  "target_domain": "example.com",
  "mined_at": "2024-01-15T14:30:00Z",
  "mode": "all",
  "depth": "standard",
  "total_opportunities": 47,
  "broken_link_targets": [
    {
      "resource_page": "https://industry-blog.com/resources",
      "broken_url": "https://defunct-site.com/guide",
      "anchor_text": "Complete guide to X",
      "suggested_replacement": "https://example.com/guides/complete-guide-x",
      "match_quality": "Exact match",
      "authority_score": 7,
      "relevance_score": 9,
      "difficulty": "Medium",
      "opportunity_score": 8.5,
      "contact": "editor@industry-blog.com"
    }
  ],
  "competitor_backlink_targets": [
    {
      "source_url": "https://tech-news.com/best-tools",
      "competitor_linked": "competitor.com",
      "link_type": "Roundup",
      "replicable": true,
      "action": "Pitch inclusion in the same roundup list",
      "authority_score": 8,
      "relevance_score": 8,
      "difficulty": "Medium",
      "opportunity_score": 8.0
    }
  ],
  "guest_post_targets": [
    {
      "site_url": "https://marketing-blog.com",
      "guidelines_url": "https://marketing-blog.com/write-for-us",
      "accepts_dofollow": true,
      "content_quality": "High",
      "publishing_frequency": "2-3 posts/week",
      "authority_score": 7,
      "relevance_score": 8,
      "difficulty": "Easy",
      "opportunity_score": 9.0,
      "suggested_topics": ["Topic 1 relevant to both sites", "Topic 2"]
    }
  ],
  "unlinked_mentions": [
    {
      "page_url": "https://review-site.com/article",
      "mention_context": "...recommended by Example for their...",
      "authority_score": 6,
      "conversion_difficulty": "Easy",
      "contact": "author@review-site.com"
    }
  ],
  "editorial_opportunities": [
    {
      "type": "Expert roundup",
      "url": "https://industry-site.com/expert-roundup",
      "action": "Respond to roundup call with expert quote",
      "authority_score": 8,
      "deadline": "Ongoing"
    }
  ],
  "summary": {
    "broken_link_opportunities": 12,
    "competitor_backlinks_replicable": 18,
    "guest_post_targets": 9,
    "unlinked_mentions": 5,
    "editorial_opportunities": 3,
    "top_3_quick_wins": [
      "Submit to 3 open directories where competitors are listed",
      "Convert 5 unlinked brand mentions via email outreach",
      "Replace 2 broken links on high-DA resource pages"
    ]
  }
}
```

## Example Usage

Trigger phrases:
- "Find backlink opportunities for [domain]"
- "Mine competitor backlinks for [domain] vs [competitor]"
- "Find broken link building opportunities in [niche]"
- "Guest post targets for [industry]"
- "Where can I build links for [domain]?"

```
User: Find backlink opportunities for plasho.com
Assistant: [searches for broken links, competitor backlinks, guest post targets, unlinked mentions, returns scored and prioritized target list]
```

```
User: Mine competitor backlinks: plasho.com vs competitor1.com and competitor2.com
Assistant: [analyzes both competitor backlink profiles, identifies replicable links, returns prioritized outreach list]
```

```
User: Find guest post opportunities for a Shopify agency
Assistant: [searches for write-for-us pages in ecommerce/Shopify/marketing niches, evaluates each site, returns ranked guest post targets with suggested topics]
```
