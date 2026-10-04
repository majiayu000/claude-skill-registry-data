---
name: signal-to-lead
description: >
  Full pipeline from signal detection to scored lead in CRM. Chains
  signal-scanner, lead-scorer, and crm-writer into one flow.
tags: [lead-generation, pipeline, composite]
---

# Signal to Lead

Detects buying signals across the web and converts them into scored, deduplicated leads in your CRM. This is the primary lead generation composite.

## Prerequisites

- `agency.config.json` populated (ICP, services, scoring, CRM)
- WebSearch tool available

## Capabilities Used

1. `signal-scanner` -- search for buying signals
2. `lead-scorer` -- score and classify leads
3. `crm-writer` -- write to CRM

## Phase 0: Intake

Read `agency.config.json` and determine:
- Which ICP segments to scan (default: all)
- Which markets (from segment config)
- Daily target: how many new leads to find (default: 20 companies)

Optional user overrides:
- "Focus on [segment name] today"
- "Only scan [platform]"
- "Find leads in [market]"

## Phase 1: Signal Detection

Execute `signal-scanner` with agency config:

For each ICP segment, generate search queries from `services[].keywords` + `icp.segments[].markets`:

Example queries for a Shopify agency targeting India D2C:
- "looking for shopify developer India"
- "need shopify agency d2c brand"
- "shopify store redesign help"
- "hiring shopify expert ecommerce"

Search platforms:
1. **Reddit** -- r/shopify, r/ecommerce, r/smallbusiness, r/Entrepreneur, r/DTC
2. **Twitter/X** -- keyword searches for service + intent keywords
3. **LinkedIn** -- job postings, posts mentioning services
4. **Job boards** -- Indeed, Wellfound for relevant hiring signals
5. **Funding news** -- Crunchbase, TechCrunch for recently funded companies
6. **Freelance platforms** -- Upwork, Freelancer for active gigs (if platform-scraper available)
7. **Community forums** -- Shopify Community, HackerNews, IndieHackers

Run max 3 searches concurrently. Pause 2 seconds between batches to avoid rate limits.

For each signal found, capture:
```json
{
  "company": "company name if visible",
  "website": "their website if mentioned",
  "person": "who posted/is hiring",
  "url": "link to the signal source",
  "platform": "where found",
  "signal_type": "funding|hiring|community_post|gig_listing|social_post|news",
  "signal_date": "when the signal appeared",
  "description": "what they're looking for",
  "budget": "if mentioned",
  "market": "country/region",
  "contact": "contact info if available",
  "contact_surfaces": {
    "has_email": false,
    "has_linkedin": true,
    "has_instagram": false,
    "has_phone": false,
    "has_website": true,
    "channel_count": 2,
    "discovery_notes": "LinkedIn from post URL. Website from company profile."
  }
}
```

## Phase 2: Score & Classify

For each signal, execute `lead-scorer`:

1. Apply platform base score from `scoring.platform_weights`
2. Check keyword matches against `icp.primary_keywords`, `icp.secondary_keywords`, `icp.intent_keywords`
3. Filter out matches against `icp.negative_keywords` (score = 0)
4. Apply hiring signal bonus (+20 if detected)
5. Apply budget tier bonus from `scoring.budget_tiers`
6. Apply recency bonus from `scoring.recency_bonuses`
7. Apply market boost from `scoring.market_boosts`
8. Apply contact surface bonus from `scoring.contact_surface_bonus` (channels_3_plus: +15, channels_2: +5)

Classify:
- HOT: score >= `scoring.thresholds.hot` (default 60)
- WARM: score >= `scoring.thresholds.warm` (default 35)
- COOL: score < warm threshold

## Phase 3: Deduplicate

Before writing to CRM:
1. Read existing leads from CRM pipeline tab
2. Match by URL (exact) or company name + website (fuzzy)
3. Remove duplicates
4. Count: N new leads after dedup

## Phase 4: Review

Present results:
```
SIGNAL SCAN RESULTS
---
Total signals found: N
After dedup: M new leads
Breakdown: X HOT, Y WARM, Z COOL

TOP HOT LEADS:
1. [Company] -- [Signal] -- Score: [N] -- Channels: EMAIL, LINKEDIN, WEBSITE (3) -- [URL]
2. ...
3. ...

WARM LEADS: [count]
COOL LEADS (not written to CRM): [count]
```

Only HOT and WARM leads are written to CRM. COOL leads are logged but not actioned.

## Phase 5: Write to CRM

Execute `crm-writer` to append HOT and WARM leads:

Tab: `crm.tabs.pipeline` (or `crm.tabs.hawk_leads` for platform-scraped leads)

Columns:
- Date, Company, Platform, URL, Budget, Description, Urgency, Score, Market, Contact, Status, Signal_Type, Signal_Date, Contact_Surfaces, Channel_Count

Set initial status: "NEW"

## Phase 6: Summary

```
DAILY SIGNAL-TO-LEAD SUMMARY
---
Platforms scanned: [list]
Total signals: N
New leads added to CRM: M (X HOT, Y WARM)
Duplicates filtered: D
Next step: Run /lead-enrichment-pipeline to research and enrich these leads
```

## Example Usage

**Trigger phrases:**
- "Find new leads today"
- "Run the signal scanner"
- "Scan for buying signals"
- "Find Shopify leads on Reddit"
- "Run signal-to-lead for India D2C segment"

**Daily automation:**
Run at 9 AM as part of `/morning-pipeline`
