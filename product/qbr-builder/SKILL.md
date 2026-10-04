---
name: qbr-builder
description: >
  Builds Quarterly Business Review decks for active clients. Pulls metrics,
  generates structured QBR with wins, challenges, roadmap, and recommendations.
  Uses crm-writer to read client data.
tags: [account-management, qbr, client-success, reporting]
---

# QBR Builder

Generates a complete Quarterly Business Review for an active client account. Pulls performance metrics, organizes wins and challenges, builds a forward-looking roadmap, and produces actionable recommendations tied to agency services.

## Prerequisites

- `agency.config.json` populated (services, case studies, CRM config)
- Active client data in CRM (engagement history, deliverables, metrics)
- Client name and review period specified
- Optional: access to Shopify Admin API for store metrics

## Capabilities Used

1. `crm-writer` -- read client history from CRM tabs
2. `company-researcher` -- refresh company intel for context
3. `message-generator` -- generate executive summary narrative

## Phase 0: Intake

Read `agency.config.json`:
- `services[]` -- available agency services for recommendation mapping
- `case_studies[]` -- reference for benchmarking results
- `crm.tabs` -- locate client data

Accept parameters:
- `client_name` -- (required) the client account name
- `quarter` -- (required) e.g. "Q1 2026" or "Jan-Mar 2026"
- `metrics_source` -- `crm` | `shopify_api` | `manual`. Default: `crm`
- `include_financials` -- boolean, whether to include revenue/billing data. Default: `false`
- `format` -- `full_deck` | `executive_summary` | `one_pager`. Default: `full_deck`

## Phase 1: Data Collection

### Client Profile
Query CRM for the client record:
- Account name, primary contact, contract start date
- Service package (which `services[]` are active)
- Monthly retainer value (if `include_financials` = true)
- Account health score (if tracked)

### Engagement History
Pull records for the review quarter:
- Deliverables completed (tasks, projects, launches)
- Meetings held (count, attendance, topics)
- Communication log (emails, Slack messages, calls)
- Support tickets or requests raised

### Performance Metrics
Based on `metrics_source`:

**CRM path**: Read metrics columns from client tab
**Shopify API path**: Pull store analytics for the quarter
**Manual path**: Prompt user to input key metrics

Target metrics:
- Store traffic (sessions, unique visitors)
- Conversion rate (overall + by device)
- Average order value (AOV)
- Revenue (total, month-over-month)
- Top-performing products
- Cart abandonment rate
- Page load speed
- Bounce rate by page type

## Phase 2: Analysis

### Win Identification
Scan collected data for positive outcomes:
- Metrics that improved quarter-over-quarter
- Deliverables that exceeded expectations
- Problems solved or fires put out
- New features or pages launched
- Speed or performance improvements

Rank wins by impact (revenue impact > conversion impact > operational impact).

### Challenge Identification
Scan for areas of concern:
- Metrics that declined or stagnated
- Deliverables that were delayed or descoped
- Recurring issues or support tickets
- External factors (market shifts, platform changes, seasonality)

For each challenge, note:
- Root cause (if known)
- Impact on business
- Current status (resolved, in-progress, unaddressed)

### Benchmark Comparison
Compare client metrics against:
- Their own previous quarter
- Industry benchmarks for their vertical
- Agency benchmarks from `case_studies[]` where applicable

## Phase 3: Roadmap Construction

Build a forward-looking plan for the next quarter:

### Continuing Initiatives
- Ongoing projects with status and next milestones
- Recurring services (monthly CRO reviews, catalog updates, ad management)

### New Recommendations
Cross-reference challenges and metrics gaps against `services[]`:
- If conversion is low: recommend CRO audit or product page optimization
- If traffic is flat: recommend performance marketing or SEO
- If catalog is outdated: recommend catalog management refresh
- If store is slow: recommend theme optimization or migration

Each recommendation includes:
- What: specific action
- Why: tied to a metric or challenge
- Expected impact: quantified where possible
- Timeline: estimated weeks/months
- Investment: if `include_financials` = true

### Priority Matrix
Rank recommendations:
- P0: Critical, do this quarter
- P1: Important, start planning
- P2: Nice to have, backlog

## Phase 4: Deck Assembly

Build the QBR structure:

```
QUARTERLY BUSINESS REVIEW
[Client Name] -- [Quarter]
Prepared by: [agency.name] ([agency.domain])

1. EXECUTIVE SUMMARY
   - Quarter at a glance (3-4 sentences)
   - Key metric: [headline number]
   - Overall account health: [GREEN/YELLOW/RED]

2. WINS
   - Win 1: [title] -- [metric impact]
   - Win 2: [title] -- [metric impact]
   - Win 3: [title] -- [metric impact]

3. KEY METRICS
   - Traffic: [value] ([+/-]% vs last quarter)
   - Conversion Rate: [value] ([+/-]% vs last quarter)
   - AOV: [value] ([+/-]% vs last quarter)
   - Revenue: [value] ([+/-]% vs last quarter)
   - [Additional metrics as relevant]

4. DELIVERABLES COMPLETED
   - [List of completed work with dates]

5. CHALLENGES & LEARNINGS
   - Challenge 1: [description] -- [status] -- [learning]
   - Challenge 2: [description] -- [status] -- [learning]

6. NEXT QUARTER ROADMAP
   - P0: [critical items]
   - P1: [important items]
   - P2: [backlog items]

7. RECOMMENDATIONS
   - Recommendation 1: [what + why + expected impact]
   - Recommendation 2: [what + why + expected impact]

8. DISCUSSION TOPICS
   - [Open questions for the client]
```

**APPROVAL GATE**: "Here's the QBR structure. Review and adjust before I finalize?"

## Phase 5: Output

Return structured JSON:

```json
{
  "client_name": "Kibi Sports",
  "quarter": "Q1 2026",
  "prepared_by": "Plasho",
  "account_health": "GREEN",
  "executive_summary": "Strong quarter with 18% conversion rate improvement after product page redesign. Traffic grew 12% from organic. Two major deliverables completed on time.",
  "wins": [
    {
      "title": "Product Page Redesign",
      "metric_impact": "+18% conversion rate on redesigned pages",
      "category": "CRO"
    },
    {
      "title": "Site Speed Optimization",
      "metric_impact": "Load time reduced from 4.2s to 2.1s",
      "category": "Performance"
    }
  ],
  "metrics": {
    "traffic": {"value": "45,200 sessions", "change": "+12%", "trend": "up"},
    "conversion_rate": {"value": "2.8%", "change": "+18%", "trend": "up"},
    "aov": {"value": "INR 2,450", "change": "+5%", "trend": "up"},
    "revenue": {"value": "INR 31,00,000", "change": "+22%", "trend": "up"},
    "bounce_rate": {"value": "42%", "change": "-8%", "trend": "improved"},
    "page_speed": {"value": "2.1s", "change": "-50%", "trend": "improved"}
  },
  "deliverables_completed": [
    {"item": "Product page redesign (12 SKUs)", "date": "2026-01-20"},
    {"item": "Navigation restructure", "date": "2026-02-10"},
    {"item": "Mobile checkout optimization", "date": "2026-03-01"}
  ],
  "challenges": [
    {
      "description": "Cart abandonment rate increased to 72%",
      "root_cause": "New payment gateway integration caused friction",
      "status": "resolved",
      "learning": "Test payment flows in staging before production rollout"
    }
  ],
  "roadmap": {
    "p0": ["Launch loyalty program integration", "Holiday season prep"],
    "p1": ["Catalog photography refresh for new SKUs"],
    "p2": ["Blog content strategy", "Email automation setup"]
  },
  "recommendations": [
    {
      "what": "Implement Klaviyo email automation",
      "why": "No post-purchase or abandoned cart email flows currently active",
      "expected_impact": "10-15% revenue recovery from abandoned carts",
      "timeline": "4 weeks",
      "service": "Performance Marketing",
      "priority": "P0"
    }
  ],
  "discussion_topics": [
    "Q2 budget allocation for performance marketing",
    "New product line launch timeline and catalog needs"
  ],
  "format": "full_deck",
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Example Usage

**Trigger phrases:**
- "Build a QBR for Kibi Sports"
- "Generate Q1 review deck for [client]"
- "Prepare quarterly business review for [client]"
- "QBR time for [client], pull the data"
- "Create an executive summary for [client]'s quarter"
