---
name: churn-analysis
description: "Analyze customer churn patterns, identify at-risk accounts, create retention playbooks, and build early warning systems"
---

# Churn Analysis

## Overview

Master churn prediction and prevention by analyzing churn patterns, identifying at-risk accounts before they leave, and executing targeted retention strategies. Effective churn analysis turns data into actionable retention playbooks.

## Churn Metrics & Definitions

### 1. Core Churn Metrics

**Churn Rate Calculation**:
```
Monthly Churn Rate = (Customers Lost During Month / Starting Customers) × 100

EXAMPLE:
Starting customers (Jan 1): 200
New customers (Jan): 30
Customers churned (Jan): 5
Ending customers (Jan 31): 225

Monthly Churn Rate = (5 / 200) × 100 = 2.5%

INTERPRETATION:
2.5% monthly churn = 30% annual churn (if consistent)
This is high for SaaS (1-2% monthly is typical)
```

**Related Metrics**:
- **Net Churn**: Revenue churn accounting for expansion revenue
- **Logo Churn**: Number of customers (what we calculated above)
- **Revenue Churn**: Dollar value of lost contracts
- **Cohort Churn**: Churn by customer acquisition cohort (e.g., Q1 2023 cohort)
- **Involuntary Churn**: Payment failures, non-renewal (vs. voluntary cancellation)

### 2. Churn Types

```
VOLUNTARY CHURN (Customer actively leaves):
- Reason: Found better product
- Reason: No longer need capability
- Reason: Switching to competitor
- Reason: Budget cuts
- Typical Rate: 60-70% of total churn
- Intervention: Retention playbook, win-back campaign

INVOLUNTARY CHURN (Payment/technical failure):
- Reason: Payment card declined
- Reason: Non-renewal (contract expired; didn't renew)
- Reason: Delinquent account suspended
- Typical Rate: 30-40% of total churn
- Intervention: Payment processing fix, renewal reminder system

EXPECTED CHURN (Company context):
- Reason: Customer bankruptcy
- Reason: Customer acquires competitor
- Reason: Use case no longer relevant
- Typical Rate: 5-10% of total churn
- Intervention: None; expected; document reason
```

## Churn Analysis Framework

### Step 1: Segment Churn by Dimension

**Analyze Churn by Customer Segment**:

```
CHURN ANALYSIS BY SEGMENT

Segment | Customers | Churned | Churn Rate | Annual Impact
---------|-----------|---------|-----------|---------------
Enterprise | 25 | 1 | 4% | $250K revenue at risk
Mid-Market | 75 | 3 | 4% | $150K revenue at risk
SMB | 200 | 15 | 7.5% | $200K revenue at risk
Startup | 50 | 8 | 16% | $100K revenue at risk
TOTAL | 350 | 27 | 7.7% | $700K revenue at risk

FINDINGS:
- Startup segment is bleeding (16% churn; disproportionate)
- SMB and Enterprise churn rates similar (4-7.5%)
- SMB represents lowest revenue but highest volume
- Startups likely have cash flow issues (expected churn)

ACTIONABLE INSIGHT:
Focus retention efforts on Startup segment (highest churn);
likely to improve with targeted intervention
```

**Analyze Churn by Acquisition Channel**:

```
Channel | Customers | Churned | Churn Rate | Cost Per Acquisition (CPA)
---------|-----------|---------|-----------|---------------------------
Inbound | 120 | 4 | 3.3% | $500
Sales outreach | 90 | 3 | 3.3% | $2,000
Partner | 80 | 6 | 7.5% | $800
Paid advertising | 60 | 14 | 23.3% | $300

FINDINGS:
- Paid advertising channel has HIGHEST churn (23.3%)
- Lowest CPA (paid ads) + highest churn = poor fit
- Inbound and sales outreach much better (3.3% churn)

ACTIONABLE INSIGHT:
Shift budget away from paid ads; they're attracting wrong customers
This is cost problem, not retention problem
```

**Analyze Churn by Acquisition Cohort** (time of signup):

```
Cohort | Customers | Remaining | Months Old | Churn Rate | Retention
--------|-----------|-----------|-----------|-----------|----------
2021 Jan | 40 | 38 | 36 months | 5% | 95%
2022 Jan | 60 | 55 | 24 months | 8% | 92%
2023 Jan | 100 | 85 | 12 months | 15% | 85%
2023 Oct | 80 | 72 | 4 months | 10% | 90%
2024 Jan | 70 | 68 | 1 month | 3% | 97%

FINDINGS:
- Older cohorts have better retention (inverse selection)
- 12-month cohort critical inflection point (big drop 85%)
- Recent cohort retention looks good (2024 Jan)

ACTIONABLE INSIGHT:
Focus on 12-month customer retention (anniversary date)
Build special program around 12-month renewal
Identify what changed in 2023 cohort onboarding process
```

### Step 2: Identify Churn Reasons

**Build Exit Interview Template**:

```
CUSTOMER EXIT INTERVIEW - [Customer Name]

Thank you for using [Product]. We're sorry to see you go. Your feedback
will help us improve. Would you answer a few quick questions?

1. What is the primary reason you're canceling?
   [ ] Found better product
   [ ] Price too high
   [ ] Wasn't meeting our needs
   [ ] Budget constraints
   [ ] Using competitor instead (who? _________)
   [ ] Company restructuring
   [ ] No longer need this capability
   [ ] Poor customer support
   [ ] Technical issues / performance
   [ ] Other: _____________________________

2. On a scale of 1-10, how likely would you recommend [Product]?
   (This is your NPS question)

3. What features would have made us stay?
   _________________________________________________

4. What could we have done differently?
   _________________________________________________

5. May we follow up in 90 days to check if you're interested again?
   [ ] Yes [ ] No

6. Contact info if interested in future win-back: _____________
```

**Analysis of Exit Interview Data**:

```
CHURN REASONS - LAST 6 MONTHS (27 customers lost)

Reason | Count | % | Action
--------|-------|----|---------
Better competitor found | 8 | 30% | Product roadmap gap analysis
Price too high | 6 | 22% | Pricing tier redesign needed
Not meeting needs | 5 | 18% | Onboarding/discovery process issue
Budget cuts | 4 | 15% | Expected churn; downsizing
Poor support | 2 | 7% | CS training needed; SLA tightening
Technical issues | 2 | 7% | Product stability issues

INSIGHTS:
- Competitor churn (30%): Losing to specific product?
- Price churn (22%): Opportunity for mid-tier pricing?
- Feature gap (18%): Feature adoption low during onboarding?
- Budget cuts (15%): Can't fix; expected
- Support/Technical (14%): Operational issues; low hanging fruit

TOP 3 OPPORTUNITIES:
1. Analyze competitor product features; roadmap gaps
2. Introduce mid-tier pricing ($X-$Y/month)
3. Improve onboarding to accelerate feature adoption
```

### Step 3: Build At-Risk Account Model

**Early Warning Signals**:

```
CHURN RISK INDICATORS

Indicator | Weight | Red Flag Threshold | Action
-----------|--------|-------------------|-------
Health score | 25% | <50 (from current 80) | Weekly check-in
Feature adoption | 20% | <50% features used | Training program
Support tickets | 20% | 5+ in last 30 days | Issue resolution
Usage decline | 15% | Down 30% MoM | Root cause call
NPS/Satisfaction | 15% | <0 (vs. 50 average) | Executive outreach
Contract renewal | 5% | <90 days until expiry | Renewal proposal
```

**At-Risk Account Scoring Model**:

```
ACCOUNT RISK SCORE (0-100; higher = more at risk)

Account | Health | Adoption | Tickets | Usage | NPS | Renewal Days | Risk Score | Status
---------|--------|----------|---------|-------|-----|--------------|-----------|--------
Acme Corp | 65 | 45% | 8 | Down 25% | -5 | 120 days | 72 | RED
Beta Inc | 80 | 60% | 2 | Up 10% | 45 | 200 days | 35 | GREEN
Gamma Ltd | 55 | 30% | 12 | Down 40% | -20 | 60 days | 88 | RED
Delta Co | 75 | 75% | 1 | Up 5% | 60 | 300 days | 25 | GREEN
Epsilon | 40 | 20% | 15 | Down 50% | -30 | 15 days | 95 | RED

RISK CATEGORIES:
RED (>70): Immediate intervention required; weekly check-ins
YELLOW (40-70): Monitor closely; monthly check-ins; build plan
GREEN (<40): Healthy; standard quarterly reviews

AT-RISK ACCOUNTS REQUIRING IMMEDIATE ACTION: 3 (Acme, Gamma, Epsilon)
```

## Retention Playbooks

### Playbook 1: Feature Gap Churn

**Trigger**: Customer states "found better product" or "feature X not available"

```
RETENTION PLAYBOOK - FEATURE GAP

IMMEDIATE ACTIONS (Day 1):
1. CSM calls customer within 24 hours
2. Acknowledge gap; don't defend product
3. Understand priority: "How critical is feature X to your use case?"
4. If not critical: Explore alternative workflow
5. If critical: Escalate to Product Manager

PRODUCT ENGAGEMENT (Days 2-5):
1. Product Manager calls customer; discuss vision
2. Share product roadmap; if feature in plans: timeline
3. If not in plans: Explain why; discuss alternatives
4. Offer: Beta testing, custom integration, or workaround

VALUE REINFORCEMENT (Days 5-15):
1. Showcase usage data: "You're getting $X value from Y features"
2. Reference case studies of similar companies
3. Offer expansion: "While we build feature X, try Y (expansion)"
4. Provide success stories: "Customer Z was in similar situation"

DECISION POINT (Day 20):
1. If customer willing to wait: Set feature release date; quarterly check-ins
2. If customer leaving: Attempt win-back discount (if approved)
3. If leaving: Ensure good experience; offer 90-day trial if returning

SUCCESS CRITERIA:
- Customer delays cancellation pending feature release
- Customer adopts alternative workflow; stays
- Customer expands while waiting for feature
- Customer leaves but remains warm for future win-back
```

### Playbook 2: Price Sensitivity Churn

**Trigger**: Customer states "price too high" or "budget cuts"

```
RETENTION PLAYBOOK - PRICE SENSITIVITY

UNDERSTAND CONTEXT (Day 1):
1. CSM calls; understand budget situation
2. Is this company-wide budget cuts? Or product-specific?
3. Can they afford lower tier? Or need discount?
4. When do they expect budget recovery?
5. What would make them stay? (price, features, support)

PRICING OPTIONS (Days 2-5):
Option A: Lower Tier
- Current: $10K/month (full features)
- Propose: $5K/month (limited features; most used)
- Trade-off: Lose some features; keep core
- Customer impact: 50% cost reduction

Option B: Annual Discount
- Current: $10K/month = $120K/year
- Propose: $100K/year (17% discount for annual commit)
- Benefit to us: Annual commitment; cash flow
- Customer benefit: Savings + budget certainty

Option C: Usage-Based Pricing
- Current: Flat $10K/month
- Propose: Pay per transaction ($X per transaction)
- If light user: Save money immediately
- If heavy user: May cost more (transparency good)

Option D: Expansion to Justify Price
- Current: Finance dept only ($10K/month)
- Propose: Expand to Ops dept (add $5K/month)
- Net: Still only $15K (not $20K for separate license)
- Value: Better analytics across organization

DECISION POINT (Day 10):
1. If customer accepts lower tier: Implement immediately; monitor usage
2. If customer accepts discount: Document business justification
3. If customer still leaving: Offer 90-day free trial of lower tier (win-back)
4. If leaving: Ensure smooth transition; seasonal re-engagement campaign

SUCCESS CRITERIA:
- Customer downgrades instead of churning (revenue retention)
- Customer commits to annual term (cash flow benefit)
- Customer expansion possible (upsell path)
- Customer willing to upgrade if budget recovers
```

### Playbook 3: Lack of Adoption Churn

**Trigger**: Low feature usage (<30% features), declining logins, support frustration

```
RETENTION PLAYBOOK - LOW ADOPTION

ROOT CAUSE DIAGNOSIS (Days 1-5):
Call questions:
1. "How's the product working for your team?"
2. "What's your biggest frustration?"
3. "Are you using it daily, weekly, or less?"
4. "Did training help? What was missing?"
5. "What would make this easier?"

Likely findings:
- Onboarding insufficient (didn't understand core features)
- Change management poor (team resisting new tool)
- Integration gaps (doesn't work with existing workflow)
- User training needed (power users unavailable to train)

INTERVENTION PLAN (Days 5-15):
1. Detailed 1:1 training (CSM with each user; 30-45 min each)
2. Custom workflow mapping (document current process + new process)
3. Integration setup (if needed; technical team involved)
4. Recurring cadence (weekly 30-min check-in for 4 weeks)
5. Win over power users (they influence adoption)

ENGAGEMENT METRICS (Weeks 2-8):
Track during intervention:
- Login frequency (target: daily)
- Features used (target: 80%+ of core features)
- Support ticket trend (target: down 50%)
- User satisfaction (target: NPS 50+)

ESCALATION IF NOT IMPROVING (Week 8):
1. Executive sponsor call: Why is this important?
2. Renewed commitment: "We're investing in your success"
3. Continued training and support
4. If no improvement: Acknowledge fit issue; graceful exit

SUCCESS CRITERIA:
- 80% of users active (daily or weekly)
- 80% of features being used
- Support tickets down (issues resolved, not escalating)
- Customer indicates satisfaction improvement
- Renewed contract confidence
```

## Win-Back Campaigns

**30-60 Days Post-Churn**:

```
WIN-BACK EMAIL SEQUENCE (Cancelled 45 days ago)

EMAIL 1 (Day 45 - Post Cancellation Check-in):
Subject: We miss you - How can we help?

Hi [Customer],

We noticed you cancelled [Product] 45 days ago. We wanted to check in
and see how you're doing with [Competitor/Alternative].

We've made some updates you might find interesting:
- Feature X (you wanted this)
- Performance improvements (50% faster)
- New integration with [Your System]

If you're open to it, we'd love to show you what's new.
No pressure - just wanted to reach out.

[Button: Schedule 15-min call]

---

EMAIL 2 (Day 60 - Case Study Approach):
Subject: [Industry Peer] found 40% efficiency gain

Hi [Customer],

One of your peers in [Industry] recently shared their success story
using [Product]. They're now [Key Benefit].

Here's their story: [Link to case study]

Curious if this resonates with you?

[Button: Read case study]

---

EMAIL 3 (Day 75 - Special Offer):
Subject: We want you back - Special returning customer offer

Hi [Customer],

We'd love to welcome you back. For 30 days, returning customers
get 50% off your previous plan.

This offer is valid through [Date] only.

[Button: Reactivate account]

---

EMAIL 4 (Day 90 - Farewell):
Subject: You're always welcome back

Hi [Customer],

We're closing out your cancellation file. If you ever want to
revisit [Product], you know where to find us.

Best of luck with your project!

[Button: Contact us anytime]
```

**Win-Back Success Metrics**:
- Email open rate: 30-40%
- Click-through rate: 10-15%
- Reactivation rate: 5-10% (goal)

## Churn Prevention System

**Automated At-Risk Alert System**:

```
SYSTEM: Send weekly report to CS leadership

WEEKLY CHURN ALERT REPORT

AT-RISK ACCOUNTS (Risk score >70):

1. Acme Corp [ENTERPRISE] - Risk: 72
   - Health score down from 80 to 65 (alert: -15 points)
   - Support tickets spiked: 8 last month (vs. 1 avg)
   - Feature adoption: 45% (down from 65%)
   - Renewal in: 120 days
   - CSM Action: Escalate to executive sponsor
   - Recommendation: Conduct executive business review

2. Gamma Ltd [MID-MARKET] - Risk: 88
   - Health score: 55 (critical)
   - Usage down 40% (potential abandonment)
   - Support tickets: 12 (unresolved issues)
   - Renewal in: 60 days (urgent)
   - CSM Action: Emergency intervention call
   - Recommendation: Offer free consulting/implementation support

3. Epsilon [SMB] - Risk: 95 (HIGHEST)
   - Health score: 40 (lowest threshold)
   - Usage down 50%
   - Support tickets: 15 (escalating)
   - Renewal in: 15 days (CRITICAL)
   - CSM Action: Daily check-in until resolved
   - Recommendation: Offer refund if leaving; understand why

WEEKLY ACTIONS REQUIRED:
- Executive sponsor call with Acme (by Wednesday)
- Emergency resolution call with Gamma (by Tuesday)
- Daily touching base with Epsilon (immediate)

SYSTEM ALERTS WHEN:
- Health score declines 15+ points in 7 days
- Support ticket spike (>5x normal)
- Usage decline >30% in a week
- Renewal date <60 days + risk signals
```

## Best Practices

1. **Measure Accurately**: Understand your churn definition; apply consistently
2. **Segment Analysis**: Churn varies by customer type; address root causes
3. **Early Detection**: Automated alerts + proactive CSM check-ins
4. **Playbook Execution**: Train CS team on retention playbooks
5. **Document Everything**: Exit interviews; lessons learned
6. **Share Learnings**: Product/Marketing/Sales need churn intelligence
7. **Win-Back Program**: 30-50% of cancelled customers can be re-activated
8. **Renewal Focus**: Plan renewal outreach 120 days before expiry
9. **Expansion Prevention**: Expanding customers churn less
10. **Culture Shift**: "Churn is everyone's problem" not just CS

---

**Use this skill to**: Predict and prevent customer churn, identify at-risk accounts early, and execute targeted retention strategies to improve customer lifetime value.
