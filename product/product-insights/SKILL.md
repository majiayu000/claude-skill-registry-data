---
name: product-insights
description: >
  Product intelligence for sprint planning, engineering roadmap, and execution priorities.
  Aggregates feature requests, bug reports, and usage patterns from customer calls (Fireflies),
  CRM notes (HubSpot), support interactions, and onboarding friction to produce a prioritized
  backlog and sprint recommendations. Use this skill when the user says "product insights",
  "sprint planning", "what should we build", "roadmap review", "backlog prioritization",
  "product roadmap", "engineering priorities", "what are customers asking for", "product
  sprint", "feature priorities", "bug triage", or any variation of wanting data-driven
  input for product decisions and engineering execution.
---

# Product Insights — Sprint Planning Intelligence

Turn every customer conversation, support interaction, and onboarding session into
structured product input. This skill feeds your engineering team with prioritized,
evidence-backed work items.

## Core Principle

Engineers shouldn't build from gut feel. Every sprint item should trace back to a
real customer moment. This skill extracts, categorizes, and prioritizes product
signals so sprint planning starts with data, not opinions.

## Data Collection (run in parallel)

### Source 1: Feature Requests from Calls (Fireflies)

Pull customer-facing calls:

```
fireflies_get_transcripts: mine=true, fromDate={periodStart}, toDate={periodEnd}, limit=50
```

Get summaries for each:
```
fireflies_get_summary: transcriptId={id}
```

**Search for product-specific signals:**
```
fireflies_search: keyword:"can you" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"wish" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"would be nice" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"doesn't work" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"broken" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"confusing" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"slow" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"error" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"workaround" scope:sentences from:{periodStart} limit:30
fireflies_search: keyword:"manually" scope:sentences from:{periodStart} limit:30
```

**Categorize each signal:**

| Category | Description | Examples |
|----------|-------------|---------|
| **FEATURE_REQUEST** | Explicit ask for new functionality | "Can Annie handle X?", "We need Y" |
| **BUG_REPORT** | Something broken or wrong | "It's showing the wrong payer", "The file didn't upload" |
| **UX_FRICTION** | Confusing, slow, or unintuitive | "I couldn't find where to...", "It took me 10 clicks" |
| **WORKFLOW_GAP** | Missing step in their actual workflow | "After Annie does X, I still have to manually do Y" |
| **INTEGRATION_NEED** | Connection to another system | "We use Z for scheduling, can Annie connect?" |
| **PERFORMANCE** | Speed, reliability, uptime | "It was slow today", "I had to refresh 3 times" |
| **ONBOARDING_FRICTION** | Difficulty getting started | "I'm not sure how to set up...", "My team is confused about..." |

**For each signal, capture:**
- Customer name and company
- Exact quote (verbatim from call)
- Context (what they were trying to do)
- Frequency (first mention or repeat?)
- Impact (blocks their workflow? Annoyance? Workaround exists?)

### Source 2: CRM Notes (HubSpot)

Pull contacts with recent notes:
```
search_crm_objects: objectType="contacts"
  filterGroups: [{ filters: [
    { propertyName: "notes_last_updated", operator: "GTE", value: "{periodStart}" }
  ]}]
  properties: ["firstname", "lastname", "company", "jobtitle",
               "notes_last_updated", "hs_lead_status"]
  limit: 50
```

Pull deals with notes:
```
search_crm_objects: objectType="deals"
  filterGroups: [{ filters: [
    { propertyName: "notes_last_updated", operator: "GTE", value: "{periodStart}" }
  ]}]
  properties: ["dealname", "amount", "dealstage", "notes_last_updated"]
  limit: 30
```

**Extract from deal/contact notes:**
- Feature requests mentioned in sales conversations
- Blockers preventing deal close ("they need X before signing")
- Integration requirements ("they use EHR Y, need compatibility")
- Competitive feature gaps ("competitor Z has this, we don't")

### Source 3: Onboarding Patterns

Search for onboarding calls specifically:
```
fireflies_search: keyword:"onboarding" scope:title from:{periodStart} limit:20
fireflies_search: keyword:"setup" scope:title from:{periodStart} limit:20
fireflies_search: keyword:"training" scope:title from:{periodStart} limit:20
```

**Extract:**
- Where new users get stuck (first 48 hours patterns)
- Questions asked repeatedly (docs/UX gap)
- Time-to-first-value (how long until they see results)
- Setup steps that require manual intervention (automation opportunities)
- Drop-off points (started but never completed a key action)

### Source 4: Competitive Feature Gaps (Web Research)

For key competitors, check recent product updates:
```
WebSearch: "Waystar" product update features {current year}
WebSearch: "CoverMyMeds" new features {current year}
WebSearch: "Availity" product launch {current year}
WebSearch: "CentralReach" product update {current year}
```

Also check G2/Capterra for user complaints about competitors:
```
WebSearch: site:g2.com "prior authorization software" reviews
WebSearch: site:capterra.com "insurance verification" reviews
```

**Extract:**
- Features competitors launched (are we behind?)
- Features users wish competitors had (our opportunity)
- Common complaints (our differentiation)

## Analysis & Prioritization

### RICE Scoring (adapted for early-stage)

Score every product signal using this framework:

| Factor | Question | Scale |
|--------|----------|-------|
| **Reach** | How many customers mentioned this? | 1-5 (1=one customer, 5=majority) |
| **Impact** | How much does this affect their workflow? | 1-5 (1=minor annoyance, 5=blocks core workflow) |
| **Confidence** | How clear is the requirement? | 1-5 (1=vague wish, 5=specific with clear spec) |
| **Effort** | Engineering effort estimate | 1-5 (1=XL/quarter, 5=S/day) |

**RICE Score = (Reach x Impact x Confidence) / Effort**

### Revenue Impact Multiplier

Boost priority for signals tied to revenue:
- **Deal blocker**: Item blocking a deal worth $X → 2x multiplier
- **Churn risk**: Item causing a paying customer to consider leaving → 1.5x multiplier
- **Expansion blocker**: Item preventing upsell/cross-sell → 1.3x multiplier

### Category Buckets

Group scored items into sprint-planning buckets:

| Bucket | Criteria | Sprint Allocation |
|--------|----------|------------------|
| **Must Fix** | Bugs + RICE > 40 | 30% of sprint |
| **Must Build** | Features + RICE > 30 + revenue impact | 40% of sprint |
| **Should Improve** | UX/Performance + RICE > 20 | 20% of sprint |
| **Nice to Have** | Everything else | 10% or backlog |

## Report Structure

```
# Product Insights Report
## Period: {startDate} — {endDate}
## Sprint: [current/next sprint identifier]

---

## SPRINT RECOMMENDATIONS (top 10, ranked by RICE)

| # | Item | Category | RICE | Customers | Revenue Impact | Effort |
|---|------|----------|------|-----------|---------------|--------|
| 1 | ... | BUG | XX | [names] | $X deal blocked | S |
| 2 | ... | FEATURE | XX | [names] | Churn risk at [company] | M |
| ... |

---

## MUST FIX (Bugs & Breaks)

### Bug 1: [title]
- **Reported by**: [customer, date, call link]
- **Quote**: "[exact words]"
- **Impact**: [what it breaks in their workflow]
- **Frequency**: [one-off or recurring]
- **Suggested fix**: [technical direction if obvious]

### Bug 2: ...

---

## MUST BUILD (Feature Requests)

### Feature 1: [title]
- **Requested by**: [customer list with dates]
- **Customer quotes**: "[verbatim from calls]"
- **Use case**: [what they're trying to accomplish]
- **Current workaround**: [what they do today without it]
- **Revenue impact**: [deals blocked, churn risk, expansion]
- **Competitive context**: [do competitors have this?]
- **Suggested scope**: [MVP definition — what's the smallest useful version]

### Feature 2: ...

---

## SHOULD IMPROVE (UX & Performance)

### Improvement 1: [title]
- **Signal**: [what customers said/did]
- **Current experience**: [what happens today]
- **Ideal experience**: [what should happen]
- **Impact**: [time saved, confusion eliminated, drop-off reduced]

---

## ONBOARDING GAPS

| Step | Friction Point | Frequency | Fix Type |
|------|---------------|-----------|----------|
| ... | ... | X customers | Docs / UX / Automation |

### Time to First Value: [current avg] → Target: [goal]

---

## COMPETITIVE FEATURE MAP

| Feature | Us | Waystar | CoverMyMeds | CentralReach | Customer Demand |
|---------|-----|---------|-------------|-------------|----------------|
| ... | Y/N/Partial | ... | ... | ... | X asks |

---

## WORKFLOW GAPS (manual steps customers still do)

| After Annie Does... | Customer Still Has To... | Automation Opportunity | Effort |
|---------------------|------------------------|----------------------|--------|

---

## INTEGRATION REQUESTS

| System | Customers Asking | Use Case | Effort |
|--------|-----------------|----------|--------|
| ... | [names] | [what they need] | S/M/L |

---

## BACKLOG (lower priority, track for later)

| Item | Category | RICE | Notes |
|------|----------|------|-------|
| ... | ... | XX | [why it's deferred] |

---

## ENGINEERING HEALTH SIGNALS

- Repeat bug rate: [are we re-introducing fixed bugs?]
- Feature request backlog growth: [growing or shrinking vs. last period]
- Onboarding friction trend: [improving or getting worse]
- Customer-reported vs. internally-found bugs ratio: [should trend toward internal]
```

## Delivery

1. Save report to `~/Documents/Claude/SALES/Product_Insights_{YYYY-MM-DD}.md`
2. Display in terminal: Top 3 sprint items with RICE scores, biggest bug, biggest feature gap
3. Ask: "Want me to create Jira/Linear tickets from these, drill into a specific customer's requests, or scope any feature?"

## Important Rules

- **Every item traces to a customer.** No "we should probably build X." Only "Customer Y said Z on [date]."
- **Quote verbatim.** Engineers need to hear the customer's actual words, not paraphrased requirements.
- **RICE everything.** No prioritization by gut. Score it, rank it, defend it with data.
- **Scope to MVP.** For every feature request, define the smallest useful version.
- **Separate bugs from features.** Bugs get fixed. Features get scoped. Don't mix them.
- **Track workarounds.** A customer's workaround tells you exactly what the MVP needs to do.
- **Competitive context matters.** If a competitor has it and customers mention it, priority goes up.
- **Default period**: Last 14 days (sprint-aligned). User can specify any range.
