---
name: gig-proposal-pipeline
description: >
  Finds freelance gigs matching your services, scores them by fit,
  and generates personalized proposals for the best matches.
tags: [inbound, freelance, proposals, pipeline]
---

# Gig Proposal Pipeline

Scans freelance platforms for relevant gigs, scores them by fit and budget, and generates tailored proposals for the top matches.

## Prerequisites

- `agency.config.json` populated (services, ICP, scoring)
- WebSearch available (for platform scanning)
- Browser automation (optional, for auto-submission)

## Capabilities Used

1. `signal-scanner` (gig mode) or `platform-scraper` -- find gigs
2. `lead-scorer` -- score gigs by fit
3. `gig-proposal-writer` -- generate proposals
4. `crm-writer` -- log gigs and proposals

## Phase 0: Intake

Read `agency.config.json`:
- `services[].keywords` -- what to search for
- `scoring` -- how to score matches
- `icp.segments[].markets` -- which markets to target

Platforms to scan (from config or user override):
- Upwork
- Freelancer
- PeoplePerHour
- Guru
- Fiverr

## Phase 1: Scan Platforms

For each platform, search using service keywords:

Search queries generated from `services[].keywords`:
- "shopify store development" on Upwork
- "shopify CRO audit" on Freelancer
- "ecommerce redesign" on PeoplePerHour

Capture for each gig:
- Title, description, budget, platform, URL
- Posted date, client history, skills required

## Phase 2: Score & Filter

Apply `lead-scorer` with gig platform weights:
- Platform base score (Freelancer 45, Upwork 45, etc.)
- Keyword match (primary +10, secondary +5, intent +10)
- Budget tier bonus
- Recency bonus
- Filter out negatives (sellers, spam)

Rank by score. Present top 10-15 matches.

## Phase 3: Generate Proposals

For each HOT gig (score >= threshold), execute `gig-proposal-writer`:
- Analyze the brief
- Match to best case study
- Generate platform-specific proposal
- Include bid amount and timeline

For WARM gigs: generate proposals only if user requests.

## Phase 4: Review & Submit

Present proposals for review:

```
GIG PROPOSALS -- [Date]
---
1. [Platform] - [Title] - Budget: $X - Score: N [HOT]
   Proposal: [preview]
   Bid: $Y / N days
   [Approve] [Edit] [Skip]

2. ...
```

**APPROVAL GATE**: User reviews each proposal before submission.

## Phase 5: Submit or Save

Based on tools:
- **Browser automation**: Navigate to gig page, paste proposal, submit bid
- **Manual**: Save proposals for copy-paste, display submission instructions

Log all proposals to CRM:
- Tab: `crm.tabs.outreach_log`
- Columns: Date, Platform, Gig Title, URL, Bid, Proposal Status, Score

## Example Usage

**Trigger phrases:**
- "Find and propose on Upwork gigs"
- "Scan Freelancer for Shopify projects"
- "Run the gig proposal pipeline"
- "Find freelance leads today"
