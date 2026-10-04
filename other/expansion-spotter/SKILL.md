---
name: expansion-spotter
description: >
  Finds upsell and cross-sell opportunities in existing client accounts.
  Detects new product launches, traffic growth, hiring signals, funding events,
  and underutilized services. Maps opportunities to agency service offerings.
tags: [account-management, upsell, cross-sell, expansion, revenue]
---

# Expansion Spotter

Analyzes existing client accounts for upsell and cross-sell opportunities. Combines CRM data, live company research, and service utilization analysis to identify where clients need more help, then maps those needs to specific agency services from `agency.config.json`.

## Prerequisites

- `agency.config.json` populated (services, case studies, CRM config)
- Active client accounts in CRM with current service packages
- WebSearch tool available for company research
- Optional: Shopify Admin API for store performance data

## Capabilities Used

1. `crm-writer` -- read client data and service history
2. `company-researcher` -- detect growth signals and changes
3. `message-generator` -- draft expansion pitch messages

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- full service catalog with names and keywords
- `case_studies[]` -- proof points for upsell conversations
- `crm.tabs` -- locate client data
- `icp.segments[]` -- understand client segments for relevant offers

Accept parameters:
- `scan_scope` -- `all_active` | `specific_client`. Default: `all_active`
- `client_name` -- (required if scope = `specific_client`)
- `min_opportunity_value` -- minimum estimated value to flag. Default: `0` (flag all)
- `include_pitch` -- boolean, generate pitch messaging. Default: `true`

## Phase 1: Service Utilization Audit

For each active client, map their current service engagement:

```
Client: [Name]
Active Services: [list from CRM]
Available Services (not using): [diff against services[]]
Contract Value: [monthly retainer]
Client Since: [start date]
Last Expansion: [date of last upsell, if any]
```

Flag accounts where:
- Client uses < 50% of available services
- No expansion in 6+ months
- Contract value below segment average

## Phase 2: Growth Signal Detection

Run `company-researcher` (quick depth) for each client to detect:

### 2a: Product and Catalog Signals
- New product lines launched or announced
- New SKU categories added to the store
- Seasonal collection launches approaching
- Product photography looking outdated vs new launches

**Opportunity mapping**: New products = catalog management, product page design, collection pages

### 2b: Traffic and Performance Signals
- Traffic growth (store getting more visitors than current setup can convert)
- Conversion rate plateau (traffic up, revenue flat)
- Mobile traffic surge (may need mobile optimization)
- International traffic growth (may need multi-currency, translation)

**Opportunity mapping**: Traffic growth = CRO, performance marketing scale-up

### 2c: Hiring and Team Signals
- Hiring for marketing roles (may need agency support during transition)
- Hiring for ecommerce roles (may be bringing in-house, or scaling team)
- New CMO or Head of Ecommerce (relationship risk, but also expansion opportunity)
- Team expansion in general (company growing, budgets growing)

**Opportunity mapping**: New marketing hire = partner with them on performance marketing

### 2d: Funding and Financial Signals
- New funding round announced
- Revenue milestones mentioned in press
- Expansion to new markets or geographies
- New retail or wholesale channels

**Opportunity mapping**: Funding = budget for store upgrade, performance marketing, CRO

### 2e: Competitive and Market Signals
- Competitors upgrading their stores
- Industry trend shifts requiring store updates
- Platform changes (Shopify updates, new features to leverage)
- Market events (festivals, sale seasons) approaching

**Opportunity mapping**: Competitor upgrades = urgency for client to match or exceed

## Phase 3: Opportunity Scoring

For each detected opportunity, score across three dimensions:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| Revenue potential | 40% | Estimated additional monthly value |
| Client readiness | 35% | Budget signals, growth trajectory, relationship health |
| Fit with services | 25% | How well the opportunity maps to agency capabilities |

```
opportunity_score = (revenue_potential * 0.4) + (client_readiness * 0.35) + (service_fit * 0.25)
```

Score on 1-10 scale:
- **8-10**: HOT -- pursue this quarter
- **5-7**: WARM -- plant the seed, revisit next quarter
- **1-4**: COOL -- note for future reference

## Phase 4: Pitch Construction

For HOT and WARM opportunities (if `include_pitch` = true):

Build a pitch for each opportunity:
- **Hook**: Reference the specific signal detected (e.g., "Saw you launched the new winter collection")
- **Bridge**: Connect the signal to a specific need
- **Offer**: Map to an agency service with specifics
- **Proof**: Reference a `case_studies[]` entry that demonstrates results
- **Ask**: Specific next step (meeting, mini-audit, proposal)

Draft using `message-generator` with context:
- Tone: consultative, not salesy (this is an existing client)
- Length: 3-5 sentences
- Channel: email or meeting agenda item

## Phase 5: Expansion Report

```
EXPANSION OPPORTUNITIES -- [Date]
Scanned: N active accounts
---
HOT OPPORTUNITIES (pursue now):
1. [Client] -- [Opportunity] -- Score: 9/10
   Signal: [what triggered it]
   Service: [which service to pitch]
   Est. Value: [monthly amount]
   Pitch: [2-line summary]

2. [Client] -- [Opportunity] -- Score: 8/10
   ...

WARM OPPORTUNITIES (plant seeds):
1. [Client] -- [Opportunity] -- Score: 6/10
   ...

UNDERUTILIZED SERVICES:
- [Client]: Not using [Service A], [Service B]
- [Client]: Not using [Service C]

---
Total expansion potential: INR [amount]/month
HOT opportunities: N
WARM opportunities: N
```

## Phase 6: Output

Return structured JSON:

```json
{
  "report_date": "2026-03-07",
  "accounts_scanned": 8,
  "opportunities": [
    {
      "client_name": "Kibi Sports",
      "opportunity_type": "upsell",
      "signal_category": "product_launch",
      "signal_detail": "Launched 3 new badminton racket SKUs with basic product pages",
      "recommended_service": "Catalog Management",
      "service_specifics": "Professional product photography + optimized product pages for new SKUs",
      "opportunity_score": 9.2,
      "score_tier": "HOT",
      "estimated_monthly_value": 25000,
      "case_study_reference": "Kibi Sports CRO -- product page redesign drove +18% conversion",
      "pitch_message": "The new racket line looks great. The product pages are basic though, and based on what we saw with the last CRO round, optimized pages could drive significantly more conversions. Want to scope a quick catalog sprint for the new SKUs?",
      "recommended_channel": "email",
      "recommended_timing": "This week"
    }
  ],
  "underutilized_services": [
    {
      "client_name": "BrandY",
      "current_services": ["Shopify Store Development"],
      "unused_services": ["Conversion Rate Optimization", "Performance Marketing", "Catalog Management"],
      "top_recommendation": "Conversion Rate Optimization"
    }
  ],
  "summary": {
    "hot_opportunities": 3,
    "warm_opportunities": 5,
    "cool_opportunities": 2,
    "total_expansion_potential_monthly": 150000
  },
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Example Usage

**Trigger phrases:**
- "Find upsell opportunities across clients"
- "Which clients could use more services?"
- "Expansion scan for [client]"
- "Where can we grow revenue with existing accounts?"
- "Cross-sell opportunities this quarter"
- "Run the expansion spotter"
