---
name: personalization-enricher
description: >
  Builds a hyperpersonalization packet for each lead by chaining company-researcher,
  cro-auditor, and person-researcher. The packet feeds into message-generator
  for Tier 3 personalized outreach.
tags: [personalization, research, enrichment]
---

# Personalization Enricher

Chains three research skills to build a "personalization packet" for each lead. This packet contains everything needed for Tier 3 hyperpersonalized outreach: company pain points, CRO findings, personal interests, and the original trigger signal.

## Prerequisites

- `agency.config.json` populated
- Lead data: company name, website, contact name, linkedin URL
- Signal data: what triggered this lead (from signal-scanner or manual)

## Capabilities Used

1. `company-researcher` -- business overview, tech stack, social presence, pain points
2. `cro-auditor` -- specific website issues with outreach hooks
3. `person-researcher` -- contact's recent activity, posts, interests

## Phase 0: Intake

Gather for each lead:
1. Company name + website URL
2. Contact name + LinkedIn URL
3. Contact title + company size (for role-appropriate messaging)
4. Signal/trigger that initiated this lead

Batch mode: accept a list of leads (from CRM query) to process sequentially.

## Phase 1: Company Research

Execute `company-researcher` for each lead:
- Visit their website via WebSearch
- Research their business, tech stack, social presence
- Identify pain points and growth signals
- Output: `company_research` JSON

## Phase 2: CRO Audit

Execute `cro-auditor` for each lead:
- Audit homepage, product page, collection page
- Find 3 specific, actionable issues
- Each issue includes an `outreach_hook` for natural email reference
- Output: `cro_audit` JSON

## Phase 3: Person Research

Execute `person-researcher` for each lead:
- Search for their recent LinkedIn posts, talks, articles
- Identify topics they care about
- Find personalization hooks (shared interests, recent achievements)
- Output: `person_research` JSON

## Phase 4: Assemble Packet

Combine all three research outputs + the original signal into one personalization packet:

```json
{
  "lead_id": "...",
  "company": {
    "name": "Brand X",
    "website": "brandx.com",
    "summary": "D2C skincare brand, 2 years old, growing fast on Instagram",
    "tech_stack": { "platform": "Shopify", "theme": "Dawn 2.0" },
    "pain_points": ["No customer reviews visible", "Slow mobile load time"],
    "social": { "instagram": "@brandx", "followers": "15K" }
  },
  "cro_findings": [
    {
      "issue": "No customer reviews on product pages",
      "impact": "Reviews increase conversion by 15-25%",
      "outreach_hook": "Noticed your product pages don't show customer reviews -- this alone could be leaving 15-25% of conversions on the table."
    },
    {
      "issue": "4-step checkout process",
      "impact": "Each step adds 10-15% abandonment",
      "outreach_hook": "Your checkout has 4 steps -- simplifying to 1-step could recover a significant chunk of abandoned carts."
    }
  ],
  "person": {
    "name": "Sarah Chen",
    "title": "Head of Ecommerce",
    "recent_posts": [
      { "topic": "D2C unit economics challenges", "date": "2 days ago", "hook": "Loved your take on D2C unit economics" }
    ],
    "career_notes": "Joined 6 months ago from Glossier",
    "personalization_hooks": ["Reference her post about unit economics", "Her Glossier background means she values CRO"]
  },
  "signal": {
    "type": "linkedin_post",
    "description": "Posted asking for Shopify CRO recommendations",
    "date": "3 days ago",
    "url": "https://linkedin.com/posts/..."
  },
  "recommended_approach": {
    "framework": "PAS",
    "primary_hook": "Their LinkedIn post about CRO + missing reviews on their site",
    "case_study_to_use": "Kibi Sports -- CRO audit, similar situation",
    "opening_line": "Sarah, your post about D2C unit economics resonated -- took a quick look at Brand X and found a few things that might be costing you conversions."
  }
}
```

## Phase 5: Review

Present the packet for each lead:
- Company summary (1 line)
- Top CRO finding with outreach hook
- Person's key interest/post
- Recommended approach + opening line

User can approve, modify, or skip each lead.

## Phase 6: Store

Save packets to CRM via `crm-writer`:
- Update lead stage from NEW to RESEARCHED
- Write personalization data to notes/description columns
- Or export as JSON for `message-generator` consumption

## Batch Processing

For multiple leads:
1. Process company research for all leads first (most WebSearch-heavy)
2. Then CRO audits (visit each site)
3. Then person research
4. Assemble packets
5. Present batch summary

Expected throughput: 5-10 leads per session (limited by WebSearch rate)

## Example Usage

**Trigger phrases:**
- "Research and personalize these leads"
- "Build personalization packets for today's HOT leads"
- "Enrich [company name] for outreach"
- "Deep research [contact name] at [company]"
