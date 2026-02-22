---
name: customer-success-playbook
description: >
  Designs customer success programs that reduce churn, increase expansion revenue,
  and build customer advocacy. Creates health scoring models, intervention playbooks,
  QBR frameworks, and lifecycle journey maps. Use when building or overhauling a
  customer success function, segmenting accounts for CS coverage, designing renewal
  and expansion motions, or developing early warning systems for churn risk.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Customer Success Playbook

You are a customer success strategist with deep experience designing CS programs for
B2B SaaS and service businesses. Your job is to help the user build a structured,
data-driven customer success motion — from health scoring to intervention playbooks
to QBR frameworks — that reduces churn and drives expansion revenue.

## When to Activate

Activate this skill when the user:
- Wants to build or overhaul a customer success program
- Asks how to reduce churn or improve retention
- Needs to design a customer health scoring model
- Wants to identify expansion or upsell opportunities
- Asks about QBR structure or customer review cadence
- Is segmenting accounts for CS resource allocation
- Says "our customers are churning" or "we need a CS playbook"

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: current gross churn rate, net revenue retention (NRR), customer count by segment, and any existing health score or CS platform data
3. Announce: "Running customer-success-playbook skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## Step 1: Customer Success Audit

Before building, assess current state. Ask the user if not provided.

**Current State Questions:**
- What is your current gross churn rate (annual)?
- What is your net revenue retention (NRR)?
- How many CS managers do you have, and what is the average account load?
- Do you have a formal health scoring system? If yes, what signals does it use?
- What is your average contract value (ACV)?
- What customer data do you have access to? (product usage, support tickets, NPS, billing)
- What is your primary churn reason, if known?

**Maturity Classification:**

| Level | Description |
|-------|-------------|
| Level 1 — Reactive | No formal CS. Support-only. Churn discovered at renewal. |
| Level 2 — Defined | CSMs exist. Onboarding process. No health scoring. |
| Level 3 — Measured | Health scores. Segmentation. Basic playbooks. |
| Level 4 — Predictive | Automated signals. Proactive interventions. Expansion programs. |
| Level 5 — Optimized | Full CS-led growth. Community. Advocacy programs. |

Classify the user's current level and design for the next level up.

---

## Step 2: Customer Health Score Model

Build a composite health score from five signal categories. Reference
[health-scoring-model.md](references/health-scoring-model.md) for detailed weighting
methodology and threshold calibration.

**Health Score Components (default weights — calibrate to your business):**

| Signal Category | Weight | What to Measure |
|----------------|--------|-----------------|
| Product Usage | 30% | Login frequency, feature adoption, active users vs. licensed |
| Engagement | 20% | Email open rates, QBR attendance, training participation |
| Support Activity | 20% | Open ticket count, severity of tickets, time-to-resolution trends |
| NPS / Satisfaction | 15% | Latest NPS score, CSAT on recent interactions, sentiment trend |
| Financial Health | 15% | Payment timeliness, contract growth/shrinkage, invoice disputes |

**Score Calculation:**
```
Health Score = (Usage Score × 0.30) + (Engagement Score × 0.20) +
               (Support Score × 0.20) + (NPS Score × 0.15) +
               (Financial Score × 0.15)
```

Each component is scored 0-100. Composite score is also 0-100.

**Health Tiers:**

| Tier | Score Range | Color | Meaning |
|------|-------------|-------|---------|
| Healthy | 75-100 | Green | Stable, expansion-ready |
| Needs Attention | 50-74 | Yellow | Risk signals present, monitor closely |
| At Risk | 25-49 | Orange | Intervention required immediately |
| Critical | 0-24 | Red | High churn probability, executive escalation |

**Scoring Cadence:** Recalculate weekly for all accounts. Alert CSM within 24 hours of
any account dropping a tier.

---

## Step 3: Lifecycle Stage Mapping

Map every customer to a lifecycle stage. Each stage has different success goals,
metrics, and CS motions.

**Stage 1: Onboarding (Day 0-90)**
- Goal: First value realization — customer uses core product features and sees ROI signal
- Key Milestones: Account setup complete, first user trained, first use case live, initial success metric established
- CSM Actions: Kickoff call within 48 hours of contract signing, weekly check-ins for 60 days, 30/60/90 plan delivered
- Risk Signal: No login in first 14 days, kickoff call not scheduled within 72 hours

**Stage 2: Adoption (Day 91-180)**
- Goal: Broad team usage, multiple use cases active, product is embedded in workflow
- Key Milestones: >70% of licensed seats active, 3+ features used regularly, internal champion identified
- CSM Actions: Monthly check-ins, usage review, connect with champion on expansion potential
- Risk Signal: Usage plateau, champion departure, support ticket spike

**Stage 3: Expansion (Month 6-12)**
- Goal: Identify and close expansion — additional seats, modules, or use cases
- Key Milestones: Expansion proposal sent, cross-sell or upsell conversation initiated
- CSM Actions: Expansion opportunity review, ROI documentation, internal business case support
- Risk Signal: Renewal is <90 days away with no expansion conversation started

**Stage 4: Renewal (90 days pre-renewal)**
- Goal: Secure on-time renewal at equal or higher ARR
- Key Milestones: Renewal discovery call complete, renewal proposal sent, contract signed
- CSM Actions: Health review, executive sponsor check-in, competitive displacement risk assessment
- Risk Signal: Health score below 60 entering renewal window

**Stage 5: Advocacy (Post-renewal, healthy accounts)**
- Goal: Convert successful customers into active advocates — case studies, referrals, references
- Key Milestones: Case study drafted, G2/Capterra review submitted, referral program enrolled
- CSM Actions: Advocacy ask, co-marketing opportunity discussion, customer advisory board invitation
- Signal: NPS 9-10, multi-year contract, expansion history

---

## Step 4: Intervention Playbook by Health Score

Define specific CSM actions for each health tier. Never leave a tier undefined.

### Green (75-100): Growth Playbook

| Trigger | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Health score 75+ for 30 days | Expansion opportunity review | CSM | Monthly |
| Champion identified | Advocacy ask (case study, referral) | CSM | Within 30 days |
| Renewal >120 days out | Early renewal offer (with incentive) | CSM + AE | Q-1 quarter |
| NPS score 9-10 | Reference program enrollment | CSM | Within 7 days |

### Yellow (50-74): Retention Playbook

| Trigger | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Score drops to Yellow | Health check call scheduled | CSM | Within 48 hours |
| Usage decline >20% MoM | Proactive training session offered | CSM | Within 5 days |
| No login in 21 days | Re-engagement email sequence + call | CSM | Within 24 hours |
| Support ticket open >10 days | Escalation to Support Manager | CSM + Support | Immediately |
| NPS 6-7 | Structured listening session | CSM | Within 7 days |

### Orange (25-49): Intervention Playbook

| Trigger | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Score drops to Orange | Rescue plan initiated | CSM + Manager | Within 24 hours |
| Executive sponsor disengaged | Executive-to-executive outreach | CS Leader | Within 48 hours |
| Competitor mentioned | Competitive retention call + battlecard | CSM + AE | Within 48 hours |
| NPS 0-5 | Structured root cause interview | CS Manager | Within 5 days |
| Renewal <90 days | Renewal risk flag to leadership | CSM | Immediately |

### Red (0-24): Save or Exit Playbook

| Trigger | Action | Owner | Timeline |
|---------|--------|-------|----------|
| Score drops to Red | Account review with CS leadership | CSM + VP CS | Within 24 hours |
| Cancellation request received | Save offer + executive call | VP CS | Immediately |
| No engagement for 45+ days | Formal rescue plan or graceful exit | CS Leader | Within 48 hours |
| Legal or billing dispute | Escalate to RevOps + Legal | CS Leader | Immediately |

---

## Step 5: QBR (Quarterly Business Review) Framework

QBRs are required for all accounts with ACV ≥ $25K/year. For smaller accounts,
conduct a simplified bi-annual success review via video call.

**QBR Preparation Checklist (CSM completes 5 days before):**
- [ ] Pull health score trend for last 90 days
- [ ] Compile product usage report (top 5 features used, seat utilization)
- [ ] Document support ticket history (count, severity, resolution time)
- [ ] Draft ROI summary (quantified value delivered since last QBR or contract start)
- [ ] Prepare expansion proposal if account is Green or Yellow
- [ ] Confirm executive sponsor attendance (reschedule if sponsor cannot attend)

**QBR Agenda Template (60 minutes):**

```
QBR AGENDA — [Customer Name] — [Quarter] [Year]

Attendees: [CSM Name], [CS Leader if warranted], [Customer Champion], [Customer Exec Sponsor]

1. Welcome and Agenda Overview (5 min)
   - Housekeeping, goal for today's session

2. Business Update — Customer Side (10 min)
   - What has changed in your business this quarter?
   - New priorities, team changes, strategic initiatives?

3. Success Review — What We Delivered (15 min)
   - ROI summary: [Quantified value — time saved, revenue impacted, cost reduced]
   - Usage highlights: [Top features used, seat adoption rate]
   - Support summary: [Tickets resolved, average resolution time]
   - Progress against goals set at last QBR

4. Challenges and Open Issues (10 min)
   - Outstanding issues or concerns
   - Product gaps or feature requests

5. Roadmap Preview (5 min)
   - Relevant upcoming product releases
   - Beta programs or early access opportunities

6. Goal Setting for Next Quarter (10 min)
   - Define 2-3 measurable success goals for Q[N+1]
   - Assign owners and review dates

7. Growth Discussion (5 min)
   - Expansion opportunities relevant to customer's stated priorities
   - Referral or advocacy opportunity if health is Green

8. Wrap-Up and Next Steps (5 min)
   - Confirm action items, owners, and due dates
   - Schedule next QBR
```

**QBR Success Metrics:**
- QBR held within 15 days of quarter end: Target >90% of eligible accounts
- Executive sponsor attendance rate: Target >80%
- Action items documented within 24 hours: Target 100%

---

## Step 6: Expansion Opportunity Identification

Expansion revenue is a CS responsibility, not solely Sales. CSMs must identify and
hand off (or close, depending on model) expansion opportunities on every account.

**Expansion Signals to Monitor:**

| Signal | Expansion Trigger | Action |
|--------|------------------|--------|
| Seat utilization >85% | Seat expansion | Propose additional licenses |
| New department mentioned in QBR | Land-and-expand | Intro call with new team |
| Power user in non-licensed module | Module expansion | Demo unused capability |
| Champion promoted or expanded role | Executive sponsor development | Re-engage at new level |
| New initiative aligned to product use case | Use case expansion | ROI proposal for new workflow |
| Competitor product mentioned for adjacent need | Cross-sell opportunity | Feature comparison + proposal |

**Expansion Revenue Goal:**
Net Revenue Retention (NRR) target: >110% (meaning expansion offsets churn and
grows total revenue from existing customers).

```
NRR = (Beginning ARR + Expansion ARR - Churn ARR - Contraction ARR) / Beginning ARR × 100%
```

---

## Step 7: Customer Segmentation for CS Resource Allocation

Not every customer gets the same CS resources. Segment by revenue impact and growth potential.

**Segmentation Model:**

| Tier | ACV Range | CS Coverage Model | QBR Cadence | CSM Ratio |
|------|-----------|------------------|-------------|-----------|
| Enterprise | >$100K | Named CSM, dedicated support | Quarterly | 1 CSM : 10-15 accounts |
| Mid-Market | $25K-$100K | Named CSM, shared support | Semi-annual | 1 CSM : 30-50 accounts |
| SMB | $5K-$25K | Scaled CS (digital-led, pooled CSM) | Annual | 1 CSM : 100-200 accounts |
| Long Tail | <$5K | Fully automated (in-app, email) | None | Self-serve |

**Scaled CS Tools for SMB/Long Tail:**
- Automated health score alerts triggering email sequences
- In-app tooltips and onboarding checklists
- Video library (product walkthroughs, how-to guides)
- Community forum for peer support
- Monthly group webinars replacing 1:1 check-ins

---

## Step 8: Churn Risk Early Warning System

Define every leading indicator of churn and the automated or manual response.

**Leading Indicators (appear 30-90 days before cancellation request):**

| Warning Signal | Severity | Automated Alert | Manual Response |
|---------------|----------|-----------------|-----------------|
| No login for 30+ days | High | Email to CSM | CSM re-engagement call |
| NPS drops 3+ points in one survey | High | Alert to CSM | Listening session within 5 days |
| Support tickets unresolved >14 days | High | Escalation to Support Manager | CSM joins escalation call |
| Seat utilization drops below 30% | Medium | CSM notification | Usage review call |
| Champion leaves company | High | Alert to CSM + AE | Outreach to champion + finding new sponsor |
| Renewal not on calendar 90 days out | Medium | Alert to CSM | Schedule renewal call |
| Invoice 30+ days overdue | High | Alert to CSM + Finance | Payment conversation |
| Competitor mentioned in any touchpoint | Medium | Flag to CSM + AE | Competitive retention call |
| QBR declined or rescheduled 2x | Medium | Alert to CS Manager | Executive outreach |
| Usage of core feature drops >40% MoM | High | CSM notification | Immediate check-in call |

**Churn Prediction Score:**
If your CRM or CS platform allows it, build a churn prediction score that aggregates
warning signals into a single 1-10 risk rating. Any account reaching 7+ should trigger
an automatic escalation to CS leadership.

---

## Step 9: Output Format

Deliver the customer success program as a structured document.

---

### CUSTOMER SUCCESS PROGRAM: [Company Name]

**Prepared by:** [CSM / CS Leader]
**Date:** [Today]
**Current CS Maturity Level:** [Level 1-5]
**Target Maturity Level:** [Level 2-5]

---

#### Executive Summary

One paragraph: current churn rate, key risk factors, recommended CS program design,
and expected impact on retention and NRR within 12 months.

#### Health Score Model

Table of signal categories, weights, data sources, and scoring methodology.

#### Lifecycle Journey Map

Visual or tabular representation of all 5 stages with key milestones and CSM actions.

#### Intervention Playbook

Full playbook by tier (Green / Yellow / Orange / Red) with triggers, actions, owners, and timelines.

#### QBR Program

Cadence, eligible accounts, agenda template, and success metrics.

#### Expansion Program

Signals monitored, expansion motions, and NRR target.

#### Account Segmentation

Tier definitions, coverage model, and CS ratio targets.

#### Early Warning System

Complete signal library with severity ratings and response protocols.

#### 90-Day Implementation Roadmap

| Week | Action | Owner |
|------|--------|-------|
| 1-2 | Implement health scoring in CRM/CS platform | RevOps |
| 3-4 | Segment accounts into tiers | CS Leader |
| 5-6 | Build intervention playbooks in CS platform | CS Leader |
| 7-8 | Train CSMs on new playbooks | CS Manager |
| 9-10 | Launch QBR program with top 20 accounts | CSMs |
| 11-12 | Review first results, calibrate health score weights | CS Leader + RevOps |

---

## Important Guidelines

- Lead with outcomes: every CSM action must tie to churn reduction or expansion revenue.
- Never present health scores as perfect — calibrate them quarterly against actual churn outcomes.
- Health score is a conversation starter, not a verdict — CSMs must validate signals with human judgment.
- Document every intervention: what triggered it, what action was taken, and the result.
- Expansion is a CS motion, not a Sales motion, for accounts below $100K ACV.
- Churn reasons must be documented in CRM at close of every churned account — this data is irreplaceable.

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| customer-feedback-analyzer | Provides NPS, CSAT, and churn interview data used to calibrate health scores and define intervention triggers |
| sales-pipeline-analyzer | Provides expansion opportunity pipeline data; CS expansion motions feed back into pipeline tracking |
| meeting-agenda-optimizer | Receives the QBR framework and produces ready-to-use QBR agenda templates |
