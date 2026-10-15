---
name: gomarble-skills-saas-companies
description: "Use for SaaS growth questions: ARR growth, churn risk, CAC payback, cohort performance, expansion revenue, sales funnel conversion, onboarding success, revenue by segment, and a weekly SaaS health report. Needs subscription and CRM data from exports, a warehouse (Snowflake through GoMarble), or a connector added in the GoMarble web app; ad spend comes from GoMarble's ad platform tools."
---

# GoMarble Skills for SaaS Companies

**9 Core Skills + Weekly Health Report** for analyzing and optimizing ARR growth, churn, CAC payback, and customer cohort health.

> **Read-and-recommend only.** These skills never change your accounts. The model reads data and produces recommendations in plain language; you apply them manually.

---

## The 9 Skills

### 1. ARR Growth Tracker
**What it does:** Isolates new ARR vs expansion ARR vs churn. Shows true growth rate vs vanity metrics.

**How it works:**
- Segments revenue by source (new customers, upsells, downgrades, churn)
- Calculates Net Revenue Retention (NRR) — the growth multiplier
- Tracks quarterly growth rate vs goal
- Identifies months where churn spiked (early warning)

**Minimum data needed:** Customer sign-up date, MRR/ARR by customer, monthly changes for last 12 months

---

### 2. Churn Predictor
**What it does:** Flags at-risk customers before they leave. Quantifies churn impact on ARR.

**How it works:**
- Identifies early warning signals (declining usage, no logins for 7+ days, support tickets)
- Correlates with contract length, plan type, and support level
- Calculates revenue at risk from predicted churners
- Recommends retention actions by customer segment

**Minimum data needed:** Customer activity logs, login frequency, support tickets, contract renewal dates

---

### 3. CAC Payback Analyzer
**What it does:** Calculates how many months until acquisition spend pays for itself.

**How it works:**
- Measures CAC per customer (acquisition spend ÷ new customers)
- Calculates payback period (CAC ÷ monthly contribution margin)
- Compares payback by channel (paid, organic, referral, sales)
- Flags long payback periods that indicate inefficient acquisition

**Minimum data needed:** Monthly marketing/sales spend, new customer count, COGS per customer, average MRR per new customer

---

### 4. Cohort Performance Ranker
**What it does:** Shows which acquisition cohorts have the best LTV and lowest churn.

**How it works:**
n- Segments customers by acquisition cohort (month / source / campaign)
- Calculates LTV, churn rate, and expansion rate per cohort
- Identifies cohorts with declining quality (newer cohorts churn more?)
- Recommends which acquisition channels to scale based on LTV

**Minimum data needed:** Acquisition date, customer source, monthly MRR, churn date

---

### 5. Expansion Revenue Spotter
**What it does:** Identifies which upsell opportunities and plans are most profitable.

**How it works:**
- Tracks upgrade rate and average upsell amount per plan
- Identifies which customer cohorts have high expansion rates
- Correlates upsells with usage metrics (seats, API calls, features used)
- Recommends usage-based pricing triggers for upsells

**Minimum data needed:** Plan type, MRR per customer, upgrade history, feature usage

---

### 6. Sales Funnel Auditor
**What it does:** Benchmarks conversion rates at each stage. Finds the biggest leak.

**How it works:**
- Tracks trial-to-paid, paying-to-enterprise, expansion rates
- Compares conversion rates by segment (company size, industry, region)
- Identifies if demo conversion or proposal-to-signed is the bottleneck
- Calculates time-to-contract by stage

**Minimum data needed:** Trial starts, paid conversions, deal stage, contract value, close date

---

### 7. Onboarding Success Mapper
**What it does:** Correlates onboarding quality with churn rate and expansion rate.

**How it works:**
- Measures time-to-first-value (first action, feature adoption, aha moment)
- Tracks onboarding completion rate and training completion
- Correlates with month-3 retention and month-6 retention
- Identifies segments with poor onboarding (churn risk)

**Minimum data needed:** Onboarding start date, first action date, feature adoption timeline, churn date

---

### 8. Segment Revenue Calculator
**What it does:** Breaks revenue by customer segment (company size, industry, use case).

**How it works:**
- Calculates ARR, churn rate, LTV, and CAC by segment
- Identifies high-value vs high-volume segments
- Finds underserved segments with expansion opportunity
- Recommends pricing and positioning changes per segment

**Minimum data needed:** Customer attributes (size, industry, use case), MRR, churn

---

### 9. Weekly SaaS Health Report
**What it does:** ARR, churn, CAC payback, cohort quality, expansion rate. One dashboard, all signals.

**Includes:**
- ARR growth this month vs goal
- Churn rate + customers at risk
- CAC payback by channel
- Best-performing cohort (LTV vs CAC)
- Expansion rate (% expanding customers)
- Onboarding success rate
- Pipeline value + average deal size
- Recommended actions (scale acquisition? improve retention? upsell?)

**Minimum data needed:** Full Stripe/SaaS data export (customers, subscriptions, revenue, usage)

---

## How to Use These Skills

1. **Identify the priority** — Is ARR at risk? Is CAC efficient? Which cohorts to scale?
2. **Gather the data** — Customer cohorts, retention, acquisition spend, usage
3. **Run the relevant skill** — Get diagnosis + financial impact
4. **Take action** — Scale profitable segments, improve retention for at-risk cohorts, optimize acquisition

---

## Data Requirements by Source

| Skill | Stripe API | CSV Export | Analytics | Manual |
|---|---|---|---|---|
| ARR Growth Tracker | ✅ | ✅ | ⚠️ | ✅ |
| Churn Predictor | ✅ | ⚠️ | ✅ | ✅ (activity logs) |
| CAC Payback Analyzer | ⚠️ | ✅ | ✅ | ✅ |
| Cohort Performance Ranker | ✅ | ✅ | ✅ | ✅ |
| Expansion Revenue Spotter | ✅ | ✅ | ✅ | ✅ |
| Sales Funnel Auditor | ⚠️ (CRM needed) | ✅ | ✅ | ✅ (CRM required) |
| Onboarding Success Mapper | ❌ | ⚠️ | ✅ | ✅ (events required) |
| Segment Revenue Calculator | ✅ | ✅ | ✅ | ✅ |
| Weekly SaaS Health Report | ✅ | ✅ | ✅ | ❌ |

✅ = works perfectly | ⚠️ = requires manual input or separate export | ❌ = not possible from this source

---

## Key Metrics Reference

| Metric | Definition | Good Benchmark |
|---|---|---|
| MRR (Monthly Recurring Revenue) | Monthly revenue from active customers | — |
| ARR (Annual Recurring Revenue) | MRR × 12 | — |
| ARR Growth Rate | (New ARR + Expansion − Churn) ÷ Starting ARR | 10%+ monthly is strong |
| Churn Rate | Lost customers ÷ Starting customers | <5% monthly for B2B |
| NRR (Net Revenue Retention) | Ending MRR ÷ Starting MRR | >100% = growing faster than adding customers |
| CAC (Customer Acquisition Cost) | Marketing + Sales spend ÷ New customers | — |
| LTV (Lifetime Value) | Total revenue per customer ÷ 1 − Churn Rate | ≥3x CAC |
| CAC Payback | CAC ÷ Monthly contribution margin | <12 months healthy |
| Expansion Rate | % of customers who expanded in month | ≥20% is strong |
| Time-to-Value | Days from sign-up to first aha moment | <7 days is strong |
| Trial-to-Paid Conversion | Paid ÷ Trial starters | 10–30% typical B2B |

---

## Output Format for Recommendations

```
### [Skill Name]: [Segment/Cohort Name]

Finding:
[1–2 sentences describing the issue or opportunity]

Financial Impact:
| Metric | Current | Benchmark | Gap | Annual Impact |
|--------|---------|-----------|-----|---------------|
| [Metric] | X | Y | $Z | $ABC |

Recommendation:
1. [Specific action with financial and growth rationale]
2. [Specific action with financial and growth rationale]
```

---

## When to Run Each Skill

| Situation | Use Skill | Timeline |
|---|---|------|
| Planning quarterly growth | ARR Growth Tracker | Monthly |
| Customer calls you about leaving | Churn Predictor | Immediately |
| Evaluating acquisition channel | CAC Payback Analyzer | Monthly |
| Deciding which cohort to focus on | Cohort Performance Ranker | Quarterly |
| Finding upsell opportunities | Expansion Revenue Spotter | Monthly |
| Sales pipeline is weak | Sales Funnel Auditor | Weekly |
| New onboarding program launched | Onboarding Success Mapper | After 30 days |
| Pricing strategy review | Segment Revenue Calculator | Quarterly |
| Board meeting prep | Weekly SaaS Health Report | Every Monday |

---

## Common Guardrails

**Before scaling acquisition:**
- ✅ Confirm CAC payback is < 12 months (faster the better)
- ✅ Confirm cohorts are profitable within 3 months
- ✅ Ensure retention is stable (don't scale leaky funnel)

**Before raising pricing:**
- ✅ Confirm NRR is >100% (customers expanding = price increase justified)
- ✅ Segment analysis (different segments may have different price sensitivity)
- ✅ Have churn rate baseline (price changes can trigger churn)

**Before cutting a segment:**
- ✅ Confirm it's truly unprofitable (account for support costs)
- ✅ Ensure it's not strategic (enterprise segment may fund product)

---

## Questions to Ask Yourself

- Is my NRR above 100%? (If not, churn is outpacing growth)
- Which cohort has the best LTV? How do I acquire more customers like them?
- What's my actual CAC payback? Is it faster than my target?
- Where do customers churn? (Month 3? Month 6? Random?)
- Which features drive expansion? Can I trigger upsells based on usage?
- Is my sales funnel leak at qualification, demo, or proposal stage?

---

## Next Steps

1. Pull customer data for last 12 months
2. Run ARR Growth Tracker (baseline health)
3. Audit CAC Payback by channel
4. Analyze Cohort Performance (which to scale?)
5. Run Churn Predictor (who's at risk?)
6. Identify highest-impact fix (retention? acquisition? pricing?)

