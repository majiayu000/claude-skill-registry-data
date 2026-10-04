---
name: icp-builder
description: Define and refine ICP segments with persona cards and validation
tags: [icp, strategy, segmentation, personas]
---

# ICP Builder

Guides the user through defining, refining, and validating Ideal Customer Profile segments. Produces persona cards for each segment and generates ICP config entries compatible with `agency.config.json`. The output feeds into `signal-scanner` for targeted lead generation and `message-generator` for segment-specific messaging.

## Prerequisites

- `agency.config.json` in the project root
- User input on existing clients and pipeline data
- Optional: CRM data for pipeline validation (Phase 6)

## Phase 0: Read Existing Config

1. Read `agency.config.json` from the project root.
2. Extract `icp.segments[]` if they exist -- these are the current segments.
3. Extract `services[].name` and `services[].keywords` to understand what the agency offers.
4. Extract `outreach.tone` for voice alignment context.
5. Note any existing `icp.primary_keywords`, `icp.secondary_keywords`, `icp.intent_keywords`.
6. If segments already exist, present them to the user:
   ```
   CURRENT ICP SEGMENTS:
   1. [segment_name] -- [markets], [company_size], [industries]
   2. ...

   Refining existing segments or building from scratch?
   ```

## Phase 1: Client Analysis

Ask the user for their top 5 best clients (or as many as they have). For each client, gather:

```
CLIENT: [Name]
Industry: [their industry]
Deal Size: [monthly retainer or project value]
How They Found Us: [referral, inbound, outbound, platform, event]
Decision Maker Title: [who signed the deal]
Company Size: [employees, revenue range if known]
Why They Bought: [the specific pain that made them choose us]
How Long to Close: [days/weeks from first contact to signed deal]
Retention: [still active? how long?]
Satisfaction: [high/medium/low -- would they refer?]
```

If the user has fewer than 3 clients, supplement with:
- "Describe 2-3 companies that would be your DREAM clients"
- "What industry/size companies reach out to you most?"

Store all responses as structured data for pattern extraction.

## Phase 2: Pattern Extraction

Analyze across all client data to find common traits:

**Industry patterns:**
- Which industries appear more than once?
- Are there adjacent industries that share characteristics?

**Company size patterns:**
- What's the employee range of best clients?
- Revenue range correlation with deal size?

**Decision maker patterns:**
- What titles are most common? (Founder, CEO, Head of Marketing, Ecommerce Manager)
- Seniority level (C-suite, VP, Director, Manager, Individual contributor)

**Acquisition channel patterns:**
- Where do the best clients come from?
- Which channel produces the fastest close?
- Which channel produces the highest deal value?

**Pain point patterns:**
- What problems are repeated across clients?
- Which agency service solves the most common pain?

**Buying trigger patterns:**
- What event made them buy NOW vs later?
- Seasonal patterns?
- Growth stage correlation?

Present findings:
```
PATTERN ANALYSIS
---
Strongest industry signal: [industry] (appeared in X/Y clients)
Typical company size: [range]
Primary decision maker: [title] at [seniority]
Best acquisition channel: [channel] (fastest close: [days])
Top 3 pain points:
1. [pain] -- present in X/Y clients
2. [pain] -- present in X/Y clients
3. [pain] -- present in X/Y clients
Most common buying trigger: [trigger]
```

## Phase 3: Build Persona Cards

For each distinct segment identified, create a persona card:

```
PERSONA: [Descriptive Name]
---
Title: [2-3 typical titles, comma-separated]
Company: [size range] employees, [industry/industries], [stage: early, growth, mature]
Revenue: [range if known]
Geography: [markets]

Pain Points:
1. [specific, actionable pain]
2. [specific, actionable pain]
3. [specific, actionable pain]
4. [specific, actionable pain -- if applicable]
5. [specific, actionable pain -- if applicable]

Buying Triggers:
- [what makes them buy NOW, not next quarter]
- [event or situation that creates urgency]
- [competitive pressure or market shift]

Top Objections:
1. [most common reason they say no or stall]
2. [second most common]
3. [third most common]

Channels:
- Primary: [where they spend professional time]
- Secondary: [backup channel]
- Content: [what content they consume]

Decision Process:
- Type: [solo decision / small committee / formal procurement]
- Timeline: [typical days from first contact to close]
- Influencers: [who else is involved]
- Budget approval: [who signs off]

Budget Range: [typical deal size, monthly or project]

Messaging Angle:
- Lead with: [the value prop that resonates most]
- Avoid: [what turns them off]
- Proof needed: [case study type, metrics they care about]
```

Build 2-4 persona cards. Avoid creating segments that are too narrow (< 100 addressable companies) or too broad (everyone with a website).

## Phase 4: Generate ICP Config

Convert persona cards into `agency.config.json` compatible segments:

```json
{
  "icp": {
    "segments": [
      {
        "name": "[segment_name]",
        "markets": ["IN", "US"],
        "company_size": { "min": 10, "max": 200 },
        "industries": ["industry_1", "industry_2"],
        "titles": ["Founder", "CEO", "Head of Ecommerce"],
        "seniority": ["C-Suite", "VP", "Director"],
        "revenue_range": { "min": "500K", "max": "50M" },
        "stage": ["post-pmf", "growth"],
        "priority": 1
      }
    ],
    "primary_keywords": ["keyword1", "keyword2"],
    "secondary_keywords": ["keyword3", "keyword4"],
    "intent_keywords": ["looking for", "need help with", "hiring"],
    "negative_keywords": ["enterprise", "Fortune 500"]
  }
}
```

Generate one segment entry per persona card. Set priority (1 = highest) based on historical conversion rate and deal value.

## Phase 5: Generate Search Keywords

For each segment, generate keywords for `signal-scanner`:

```
SEGMENT: [name]
---
Platform search queries:
  Reddit: ["need [service] for [industry]", "[pain point] help", "recommend [service type]"]
  LinkedIn: ["hiring [role]", "[industry] [pain point]", "[service] agency"]
  Twitter: ["looking for [service]", "[industry] [challenge]"]
  Job boards: ["[role title]", "[service] specialist"]

Signal keywords (buying intent):
  High intent: ["looking for agency", "need help with", "hiring", "RFP"]
  Medium intent: ["struggling with", "any recommendations", "best tool for"]
  Low intent: ["thinking about", "considering", "next quarter"]

Negative keywords (filter out):
  ["intern", "course", "tutorial", "free", "DIY"]
```

## Phase 6: Pipeline Validation

If CRM data is available, validate segments against real pipeline data:

1. Read existing leads from CRM (pipeline tab).
2. For each lead, classify into the new segments.
3. Calculate per segment:
   - Total leads
   - Conversion rate (leads -> demos -> closed)
   - Average deal value
   - Average time to close
   - Win rate vs loss rate

Present validation:
```
SEGMENT VALIDATION
---
[Segment 1]: [N] leads, [X]% conversion, avg deal [Y], avg close [Z] days
[Segment 2]: [N] leads, [X]% conversion, avg deal [Y], avg close [Z] days

RECOMMENDATION:
- Double down on: [segment with best conversion * deal value]
- Deprioritize: [segment with worst metrics]
- Test more: [segment with insufficient data]
```

If no CRM data, skip validation and note:
```
No pipeline data available for validation. Recommend running for 4-6 weeks, then re-running icp-builder with pipeline data to validate and refine.
```

## Phase 7: Output

Return the complete ICP package:

1. **Persona cards** -- one per segment, in the format from Phase 3
2. **Updated ICP config** -- JSON block ready to merge into `agency.config.json`
3. **Search keywords** -- per segment, ready for `signal-scanner`
4. **Validation summary** -- if pipeline data was available
5. **Recommended next steps**:
   - Run `signal-scanner` with new ICP config
   - Update `message-generator` templates to match persona messaging angles
   - Set calendar reminder to re-validate in 30 days

If the user confirms, write the ICP config directly into `agency.config.json`.

## Example Usage

Trigger phrases:
- "Build my ICP"
- "Define ideal customer profiles"
- "Who should we be targeting?"
- "Refine our ICP segments"
- "Build persona cards for outreach"

```
User: Build my ICP
Assistant: [reads agency.config.json, asks for top 5 clients, extracts patterns, builds persona cards, generates config, validates against pipeline]
```

```
User: We keep closing skincare brands. Should we make that a segment?
Assistant: [analyzes skincare client patterns, builds persona card, generates segment config, compares to existing segments]
```
