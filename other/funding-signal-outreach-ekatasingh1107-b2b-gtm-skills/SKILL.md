---
name: funding-signal-outreach
description: Outreach triggered by funding events with post-funding needs analysis and personalized drafts
tags: [funding, signals, outreach, prospecting, trigger-based]
---

# Funding Signal Outreach

Monitors and acts on funding announcements from companies matching ICP. For each funded company, researches what they will likely need post-funding, matches needs to agency services, scores timing urgency, and drafts personalized outreach referencing their round. Outputs qualified leads with funding context and ready-to-send messages.

## Prerequisites

- `agency.config.json` in the project root
- WebSearch tool for finding funding announcements
- Optional: `company-researcher` for deep company analysis
- Optional: `cold-email-drafter` for polished email generation
- Optional: `person-researcher` for finding the right contact

## Capabilities Used

1. `company-researcher` -- for deep-dive on funded companies
2. `person-researcher` -- for identifying decision-makers at funded companies
3. `cold-email-drafter` -- for generating polished outreach emails
4. `lead-scorer` -- for scoring the funded company against ICP
5. `crm-writer` -- for logging qualified leads to CRM

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract ICP definition:
   - `icp.segments[]` -- target segments with industry, size, geography
   - `icp.geography` -- target geographies
   - `icp.company_size` -- revenue or employee range
3. Extract `services[]` -- services to match against post-funding needs.
4. Extract `outreach.tone` and `outreach.banned_phrases` for email drafting.
5. Extract `case_studies[]` for proof points relevant to funded companies.
6. Check `tools.research` for data source preferences.

## Phase 1: Search for Funding Announcements

Search for recent funding events matching ICP:

**Search queries (via WebSearch):**
```
- "[industry] funding announcement [current_month] [current_year]"
- "[industry] Series A OR Series B OR seed round [geography]"
- "D2C brand funding [geography] [current_year]"
- "e-commerce startup funding round [current_month]"
- site:techcrunch.com "[industry] funding [current_year]"
- site:crunchbase.com "[industry] funding rounds"
- "[geography] startup funding news this week"
```

**Additional sources to check:**
- Crunchbase recent rounds (via WebSearch: `site:crunchbase.com/funding_round`)
- TechCrunch funding coverage
- Inc42 (for India), TechInAsia (for Asia)
- Press releases on PR Newswire / BusinessWire
- LinkedIn funding announcements

For each result, extract:
```
Company: [name]
Round: [Seed / Series A / Series B / etc.]
Amount: $[X]M
Date: [announcement date]
Investors: [lead investor(s)]
Industry: [sector]
Geography: [HQ location]
Website: [URL]
Source: [where we found this]
```

## Phase 2: Filter and Match to ICP

Score each funded company against ICP:

```
ICP MATCH SCORING
===
Company          | Industry Match | Geo Match | Size Match | ICP Score | Status
-----------------|---------------|-----------|------------|-----------|--------
FreshD2C         | D2C (exact)   | India     | Series A   | 95/100    | STRONG
GlowSkin         | Skincare D2C  | US        | Seed       | 80/100    | GOOD
TechWidget       | SaaS (miss)   | India     | Series B   | 30/100    | SKIP
SportyBrand      | Sports D2C    | UK        | Series A   | 85/100    | GOOD
```

Discard companies with ICP score below 50. Proceed with matches.

## Phase 3: Post-Funding Needs Analysis

For each qualified company, predict what they need post-funding:

**Post-funding need patterns by round:**

| Round | Typical Needs | Timing Urgency |
|-------|--------------|----------------|
| Seed | Brand identity, initial store build, MVP website | HIGH -- building from scratch |
| Series A | Scale operations, revamp website, CRO optimization, marketing | HIGH -- pressure to grow fast |
| Series B | Performance marketing at scale, international expansion, advanced CRO | MEDIUM -- already have some team |
| Series C+ | Enterprise features, custom development, data infrastructure | LOW -- likely have in-house team |

**Research each company (via WebSearch and company-researcher):**
```
POST-FUNDING NEEDS ASSESSMENT: [Company Name]
===
Round: Series A ($5M)
Current website: [URL] -- quality assessment
Current Shopify store: [yes/no, theme quality]
Current team size: [N] (check LinkedIn)
Open positions: [roles being hired -- indicates gaps]
Recent press: [what they say they'll use funds for]

Predicted needs:
1. [Need 1 -- e.g., "Store revamp -- current site is basic Shopify theme"]
2. [Need 2 -- e.g., "CRO -- scaling traffic without optimized conversion"]
3. [Need 3 -- e.g., "Catalog management -- expanding from 50 to 200 SKUs"]

Service match:
- [Your service 1] matches need [1] -- relevance: HIGH
- [Your service 2] matches need [2] -- relevance: HIGH

Timing urgency: HIGH (Series A companies typically spend on growth within 3 months of closing)
```

## Phase 4: Score and Rank Leads

Score each lead on:

```
LEAD SCORING
===
Company     | ICP Fit | Funding Recency | Need Match | Timing | Total Score
------------|---------|-----------------|------------|--------|------------
FreshD2C    | 95      | 5 days ago      | 3 services | HIGH   | 92/100
SportyBrand | 85      | 12 days ago     | 2 services | HIGH   | 85/100
GlowSkin    | 80      | 30 days ago     | 2 services | MEDIUM | 72/100
```

**Scoring weights:**
- ICP fit: 30%
- Funding recency (prefer last 30 days): 25%
- Service need match: 25%
- Timing urgency: 20%

## Phase 5: Draft Personalized Outreach

For each qualified lead, draft outreach using the Signal-Proof-Ask framework:

**Email structure:**
```
Subject: Congrats on the [round] -- [specific observation]

[Reference the funding]: "Saw [Company] just closed [round] -- congrats.
[Most companies at this stage face X]."

[Match to their need]: "With [amount raised], you're likely [scaling/revamping/expanding].
We've helped [similar company] do exactly that."

[Proof point]: "[Case study result -- specific metric]."

[Soft CTA]: "Worth a quick look at how this could work for [Company]?"
```

Generate for each lead:
1. Email draft (using `cold-email-drafter` if available)
2. LinkedIn connection note (under 300 chars)
3. LinkedIn message (if already connected)

**Personalization must include:**
- The specific round and amount
- A specific observation about their current website/store
- A relevant case study matching their industry
- A specific service recommendation based on their needs

## Phase 6: Output

Return structured JSON:

```json
{
  "funding_signal_outreach": {
    "search_date": "2024-03-15",
    "search_criteria": {
      "industries": ["D2C", "e-commerce"],
      "geographies": ["India", "US", "UK"],
      "round_types": ["Seed", "Series A", "Series B"],
      "recency": "last 30 days"
    },
    "funding_events_found": 15,
    "icp_matches": 8,
    "qualified_leads": [
      {
        "company": "FreshD2C",
        "website": "https://freshd2c.com",
        "round": "Series A",
        "amount": "$5M",
        "date": "2024-03-10",
        "investors": ["Sequoia India"],
        "icp_score": 92,
        "predicted_needs": ["store revamp", "CRO", "catalog management"],
        "service_matches": ["Shopify development", "CRO optimization"],
        "timing_urgency": "high",
        "contacts": [
          {
            "name": "Founder Name",
            "title": "CEO",
            "linkedin": "URL",
            "email": "email@freshd2c.com"
          }
        ],
        "outreach": {
          "email_subject": "",
          "email_body": "",
          "linkedin_note": "",
          "linkedin_message": ""
        }
      }
    ],
    "summary": {
      "total_qualified": 5,
      "total_outreach_drafted": 5,
      "top_opportunity": "FreshD2C -- Series A, strong ICP match, 3 service needs"
    }
  }
}
```

Log qualified leads to CRM via `crm-writer` (Researched Leads tab) with source tagged as "funding_signal."

## Example Usage

**Trigger phrases:**
- "Find companies that just raised funding in our ICP"
- "Search for D2C funding announcements this month"
- "Funding signal outreach for this week"
- "Which startups just got funded that we should reach out to?"
- "Find recently funded e-commerce companies in India"

```
User: Find recently funded D2C companies we should reach out to
Assistant: [searches for D2C funding in last 30 days, finds 15 events, filters to 5 ICP matches, researches each company's website and needs, drafts personalized outreach referencing their specific round and current store gaps, logs to CRM]
```

```
User: Any new funding rounds in Indian e-commerce this week?
Assistant: [searches India-focused funding news, finds 3 new rounds, scores against ICP, identifies 2 strong matches, drafts outreach for each with relevant case studies]
```
