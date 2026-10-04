---
name: lead-qualifier
description: >
  Multi-dimensional lead qualification scoring. Evaluates leads against
  BANT criteria, firmographic fit, behavioral signals, and intent indicators.
  Outputs qualified/disqualified verdict with detailed reasoning.
tags: [sales, qualification, lead-scoring, BANT]
---

# Lead Qualifier

Performs deep, multi-dimensional qualification on a single lead or batch of leads. Goes beyond simple lead scoring by evaluating across BANT (Budget, Authority, Need, Timeline), firmographic fit against ICP, behavioral engagement signals, and intent indicators. Outputs a clear qualified/disqualified verdict with detailed reasoning and recommended next action.

## Prerequisites

- `agency.config.json` populated (ICP, services, pricing context, CRM config)
- Lead data: at minimum, company name and contact name
- WebSearch tool available for enrichment during qualification
- Optional: CRM data for behavioral signal analysis
- Optional: `lead-scorer` capability output as input

## Capabilities Used

1. `company-researcher` -- firmographic data for qualification
2. `person-researcher` -- decision-maker validation
3. `lead-scorer` -- initial lead score as input signal
4. `crm-writer` -- pull engagement history and update qualification status
5. `decision-maker-finder` -- verify authority dimension

## Phase 0: Intake

Read `agency.config.json`:
- `icp.segments[]` -- ideal customer profile criteria
- `services[]` -- what you sell (for need mapping)
- `pricing` -- minimum engagement size, retainer ranges (for budget qualification)
- `crm.tabs` -- locate lead data
- `qualification_rules` -- custom rules if defined in config

Accept parameters:
- `lead` -- (required) lead object or lead name to look up in CRM
- `mode` -- `single` | `batch`. Default: `single`
- `leads` -- (required if mode = `batch`) array of lead objects
- `auto_route` -- boolean, automatically trigger `lead-router` after qualification. Default: `false`
- `depth` -- `quick` | `full`. Default: `full`

Lead object structure:
```json
{
  "contact_name": "Priya Mehta",
  "company_name": "FreshSkin Co",
  "email": "priya@freshskin.co",
  "title": "Founder",
  "source": "inbound_form",
  "notes": "Interested in Shopify store revamp"
}
```

## Phase 1: BANT Assessment

### Budget (Weight: 25%)

Evaluate ability and willingness to pay:

**Direct signals** (from form data, emails, conversations):
- Mentioned budget range
- Asked about pricing (positive signal -- they're evaluating)
- Mentioned "cost-effective" or "affordable" (may signal tight budget)
- Mentioned specific investment amount

**Indirect signals** (from research):
- Company revenue/funding (proxy for budget capacity)
- Current spending on similar services (if visible)
- Number of employees (proxy for operational budget)
- Premium vs budget positioning of their brand

**Scoring**:
```
Budget Score:
  5 = Budget confirmed, aligns with services pricing
  4 = Strong budget indicators (funded, premium brand, asked about pricing)
  3 = Moderate indicators (mid-size company, no budget mentioned)
  2 = Weak indicators (small company, mentioned budget constraints)
  1 = Disqualifying (explicitly stated budget far below minimum)
  0 = No data available
```

### Authority (Weight: 25%)

Evaluate decision-making power:

**Title analysis**:
- C-suite (CEO, CMO, CTO): Score 5
- VP/Director level: Score 4
- Head/Manager level: Score 3
- Coordinator/Specialist: Score 2
- Unknown/Intern: Score 1

**Decision-maker validation**:
- Run `decision-maker-finder` if title suggests non-decision-maker
- Check if they mentioned "I need to check with..." (lower authority)
- Check if they said "I'm the one who decides..." (higher authority)
- Company size context: at a 10-person startup, a "Marketing Manager" may be the sole decision-maker

**Scoring**:
```
Authority Score:
  5 = Confirmed decision-maker, signs contracts
  4 = Strong authority (C-suite, founder, sole ecomm person)
  3 = Influencer with access to decision-maker
  2 = Influencer without confirmed path to decision-maker
  1 = No authority, no path identified
  0 = No data available
```

### Need (Weight: 30%)

Evaluate alignment between their problems and your services:

**Explicit need signals**:
- Mentioned specific pain points matching `services[]`
- Requested a specific service by name
- Described a project scope
- Referenced competitors doing something they want

**Implicit need signals**:
- Website quality issues visible on their store
- Outdated design or poor mobile experience
- Low conversion signals (poor product pages, no trust elements)
- Missing features competitors have
- Growing traffic but flat revenue (CRO need)
- New product launches with basic pages (catalog need)

**Service mapping**:
For each detected need, map to a specific service from `services[]`:
```
Detected need -> Service match -> Fit strength
"Store looks outdated" -> Shopify Store Development -> STRONG
"Want more traffic" -> Performance Marketing -> STRONG
"Conversion is low" -> CRO -> STRONG
"Need better photos" -> Catalog Management -> MODERATE
```

**Scoring**:
```
Need Score:
  5 = Explicit, urgent need perfectly matching core services
  4 = Clear need matching services, moderate urgency
  3 = Need exists but vague, or matches secondary services
  2 = Peripheral need, weak match to services
  1 = No apparent need for offered services
  0 = No data available
```

### Timeline (Weight: 20%)

Evaluate urgency and readiness to start:

**Urgency indicators**:
- Mentioned specific deadline ("need this before Diwali sale")
- Mentioned event-driven timeline ("launching new line in Q2")
- Mentioned competitive pressure ("competitor just relaunched")
- Mentioned internal pressure ("board wants ecomm growth this quarter")

**Readiness indicators**:
- Already evaluated other agencies (deep in buying process)
- Has a brief or scope document ready
- Mentioned budget is approved
- Asked about start dates and timelines

**Anti-urgency indicators**:
- "Just exploring for now"
- "Maybe next quarter"
- "No rush"
- "We're in early stages of thinking about this"

**Scoring**:
```
Timeline Score:
  5 = Immediate need, ready to start within 2 weeks
  4 = Near-term, wants to start within 1-2 months
  3 = Medium-term, planning for next quarter
  2 = Long-term, 6+ months out
  1 = No timeline, "just exploring"
  0 = No data available
```

## Phase 2: Firmographic Qualification

Compare the lead's company against ICP segments:

### Segment Match
For each `icp.segments[]` entry, evaluate:
- Industry match: Does their vertical match?
- Company size match: Within the segment's range?
- Geography match: Correct market?
- Revenue/stage match: Post-PMF? Mid-market? Early-stage?
- Platform match: On Shopify or moving to Shopify?

### Firmographic Score
```
Firmographic Score:
  5 = Perfect ICP match (right industry, size, geo, stage, platform)
  4 = Strong match (3-4 criteria match)
  3 = Partial match (2-3 criteria match)
  2 = Weak match (1-2 criteria match)
  1 = No match but adjacent (could become ICP with growth)
  0 = Anti-ICP (wrong industry, too small/large, wrong platform)
```

### Deal Breakers
Check for automatic disqualifiers:
- Company in a prohibited industry
- Company too small (below minimum engagement size)
- Company on a platform you don't serve with no migration interest
- Geographic restrictions (if applicable)
- Direct competitor of an existing client (conflict of interest)

## Phase 3: Behavioral Qualification

Pull engagement data from CRM (if available):

### Engagement Signals
- Email opens and clicks (frequency, recency)
- Website visits (pages viewed, time on site)
- Content downloads (guides, templates)
- Webinar attendance
- Social media engagement (liked, commented, shared)
- Form submissions (which forms, how detailed)
- Meeting requests or demo bookings

### Engagement Score
```
Engagement Score:
  5 = High engagement (multiple touchpoints, recent, deep)
  4 = Good engagement (responded to outreach, visited key pages)
  3 = Moderate engagement (opened emails, some website visits)
  2 = Low engagement (minimal interaction)
  1 = No engagement (cold lead, no response to outreach)
  0 = No data available
```

## Phase 4: Intent Signal Analysis

Look for buying intent signals:

### High-Intent Signals (score 3 each)
- Searched for "[your service] agency" or similar
- Visited pricing page
- Requested a proposal or audit
- Asked about contracts or terms
- Compared you to competitors by name
- Mentioned urgency or deadline

### Medium-Intent Signals (score 2 each)
- Downloaded a case study
- Attended a webinar
- Engaged with multiple content pieces
- Followed on LinkedIn
- Visited portfolio/case study page

### Low-Intent Signals (score 1 each)
- Subscribed to newsletter
- Single blog post visit
- Social media follow only
- Opened a cold email but no reply

### Intent Score
```
Intent Score: sum(signals) normalized to 1-5 scale
  5 = Strong buying intent (4+ high-intent signals)
  4 = Good intent (2-3 high-intent signals)
  3 = Moderate intent (medium signals present)
  2 = Weak intent (low signals only)
  1 = No intent signals detected
```

## Phase 5: Composite Qualification

Calculate the composite qualification score:

```
composite_score = (
  budget_score * 0.25 +
  authority_score * 0.25 +
  need_score * 0.30 +
  timeline_score * 0.20
)

firmographic_modifier:
  5 = +0.5
  4 = +0.25
  3 = 0
  2 = -0.25
  1 = -0.5
  0 = DISQUALIFY (automatic)

behavioral_modifier:
  5 = +0.3
  4 = +0.15
  3 = 0
  2 = -0.1
  1 = -0.2

intent_modifier:
  5 = +0.3
  4 = +0.15
  3 = 0
  2 = -0.1
  1 = -0.2

final_score = composite_score + firmographic_modifier + behavioral_modifier + intent_modifier
```

### Qualification Verdict

```
QUALIFIED (score >= 3.5):
  - MQL (Marketing Qualified Lead): score 3.5-4.0
  - SQL (Sales Qualified Lead): score 4.0-4.5
  - HOT (Ready to close): score 4.5+

DISQUALIFIED (score < 3.5 or deal breaker triggered):
  - NURTURE: score 2.5-3.49 (not ready, but could be)
  - UNQUALIFIED: score < 2.5 (poor fit)
  - DEAL_BREAKER: automatic disqualifier triggered
```

## Phase 6: Output

Return structured JSON:

```json
{
  "lead": {
    "contact_name": "Priya Mehta",
    "company_name": "FreshSkin Co",
    "title": "Founder",
    "source": "inbound_form"
  },
  "qualification": {
    "verdict": "SQL",
    "final_score": 4.2,
    "confidence": "HIGH",
    "reasoning": "Strong ICP fit (D2C skincare, post-PMF), founder-level authority, explicit need for store revamp, Q2 timeline mentioned. Budget unconfirmed but funding round suggests capacity."
  },
  "bant": {
    "budget": {"score": 3, "notes": "No explicit budget mentioned. Series A funded, premium pricing suggests healthy margins."},
    "authority": {"score": 5, "notes": "Founder and sole decision-maker."},
    "need": {"score": 5, "notes": "Explicitly requested Shopify store revamp. Current store has poor mobile experience and outdated design."},
    "timeline": {"score": 4, "notes": "Mentioned wanting to launch before Q2 seasonal push."}
  },
  "firmographic": {
    "score": 4,
    "icp_segment": "Post-PMF D2C India",
    "match_details": {"industry": true, "size": true, "geo": true, "stage": true, "platform": true}
  },
  "behavioral": {
    "score": 4,
    "signals": ["Opened 3/3 emails", "Visited case study page twice", "Downloaded CRO guide"]
  },
  "intent": {
    "score": 4,
    "signals": ["Requested audit", "Visited pricing page", "Asked about timelines"]
  },
  "deal_breakers": [],
  "recommended_action": {
    "next_step": "Schedule discovery call with founder",
    "assigned_to": "founder_direct",
    "urgency": "This week",
    "talking_points": ["Reference their mobile experience issues", "Share skincare D2C case study if available"]
  },
  "generated_at": "2026-03-07T10:00:00Z"
}
```

## Phase 7: Review and Routing

Present qualification results.

If `auto_route` = true, trigger `lead-router` with the qualification output.

**APPROVAL GATE**: "Lead qualified as [verdict]. Route to [assignment]?"

Update CRM via `crm-writer`:
- Set qualification status
- Set lead score
- Add qualification notes
- Set next action and assigned owner

## Example Usage

Trigger phrases:
- "Qualify this lead: [name] at [company]"
- "Is [prospect] a good fit for us?"
- "Run BANT qualification on the new inbound leads"
- "Score and qualify [lead]"
- "Should we pursue [company]? Qualify them."
- "Batch qualify this week's inbound leads"
