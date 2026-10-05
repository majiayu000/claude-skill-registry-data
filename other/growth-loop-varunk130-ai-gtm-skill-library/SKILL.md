---
name: growth-loop
description: 'Retention, expansion, and advocacy strategy that maximizes customer lifetime value through structured lifecycle programs. Use when: retention strategy, customer retention, expansion strategy, churn prevention, customer success, NRR, upsell, advocacy program.'
---

# Growth Loop (ANCHOR System)

A structured lifecycle engine that designs every phase of post-acquisition customer engagement -- from initial activation through renewal and advocacy. ANCHOR maximizes net revenue retention by combining health scoring, trigger-based expansion plays, and systematic advocacy development into a unified retention and growth system.

## When to Use
- Designing a post-launch customer success and retention strategy
- Building a customer health scoring model to predict and prevent churn
- Creating expansion playbooks for upsell and cross-sell motions
- Developing customer advocacy programs (case studies, referrals, advisory boards)
- Improving net revenue retention (NRR) and reducing logo churn
- Structuring the handoff from launch/acquisition to ongoing customer success
- Building automated lifecycle programs with trigger-based interventions

## What You'll Need

**Critical inputs (ask if not provided):**
- Product name, pricing model, and customer segments
- Current retention and churn rates (or estimates)
- Key value moments and activation milestones in the product
- Customer support and success team structure
- Expansion products or tiers available for upsell/cross-sell
- Revenue targets (NRR, expansion revenue, logo retention)

**Nice-to-have:**
- Customer journey maps (from journey-architect)
- Product usage analytics and feature adoption data
- NPS or CSAT baseline scores
- Existing health scoring model (if any)
- Competitive switching triggers (from battle-scanner)
- Launch metrics framework (from launch-pulse)

## Process

### Step 1: Map the ANCHOR Lifecycle Stages

Define six lifecycle stages with specific timeframes, goals, and success criteria.

| Stage | Timeframe | Goal | Key Metric | Exit Criteria |
|-------|----------|------|-----------|---------------|
| **A** - Activate | Days 0-7 | First value moment achieved | Time to Value (TTV) | User completes core activation action |
| **N** - Nurture | Days 7-30 | Expand usage breadth and depth | Feature adoption rate | 3+ features adopted, regular usage pattern |
| **C** - Champion | Days 30-90 | Identify and cultivate internal advocates | Champion score | At least 1 identified champion per account |
| **H** - Habituate | Days 90-180 | Embed product into daily workflows | DAU/WAU ratio | Stickiness ratio >50%, multi-team usage |
| **O** - Optimize | Days 180-365 | Demonstrate and quantify business ROI | ROI documentation | ROI report delivered, value validated |
| **R** - Renew | 60 days pre-renewal | Secure renewal and identify expansion | Renewal rate | Renewal committed, expansion opportunity identified |

### Step 2: Design Stage-Specific Programs

For each ANCHOR stage, define the specific touchpoints, content, and automation.

**A -- Activate (Days 0-7)**

| Day | Touchpoint | Channel | Content | Owner | Trigger |
|-----|-----------|---------|---------|-------|---------|
| 0 | Welcome email sequence | Email | Onboarding guide, quick-start video | Lifecycle | Account created |
| 1 | In-app onboarding flow | Product | Guided tour, setup wizard | Product | First login |
| 2 | Activation check | Email | "Complete your setup" with specific CTA | Lifecycle | Setup incomplete |
| 3 | Tip of the day | In-app | Feature highlight relevant to segment | Product | Login |
| 5 | CS check-in (enterprise) | Email/Call | Personal welcome, needs assessment | CSM | Enterprise tier |
| 7 | Activation milestone | Email | Congratulations + next steps, or re-engagement | Lifecycle | Activated or not |

**At-Risk Trigger (Activate stage):** No login within 48 hours of signup --> immediate re-engagement sequence.

**N -- Nurture (Days 7-30)**

| Week | Touchpoint | Channel | Content | Trigger |
|------|-----------|---------|---------|---------|
| 2 | Feature discovery | In-app | "Have you tried [feature]?" based on segment | Login + not used feature |
| 2 | Best practices email | Email | Top 3 tips from power users | Day 10 |
| 3 | Webinar invitation | Email | "Getting more from [Product]" live session | Day 15 |
| 3 | Usage milestone | In-app | Celebrate usage achievement | Hits usage threshold |
| 4 | Value checkpoint | Email/Call | "Here is what you have accomplished so far" | Day 25 |

**C -- Champion (Days 30-90)**

| Trigger | Action | Channel | Owner |
|---------|--------|---------|-------|
| Power user identified (top 10% usage) | Invite to champion program | Email | CSM |
| Multiple team members active | Celebrate team growth, offer admin tools | In-app | Product |
| Positive support interaction | Request testimonial quote | Email | CSM |
| Feature request submitted | Acknowledge, share roadmap context | Email | Product |

**H -- Habituate (Days 90-180)**

| Milestone | Action | Channel | Owner |
|-----------|--------|---------|-------|
| Multi-department usage detected | Cross-team best practices guide | Email | CSM |
| Integration with other tools | Integration deepening guide | In-app | Product |
| Workflow automation created | Showcase advanced capabilities | Email | CSM |
| 90-day review | QBR with usage data and ROI preview | Call | CSM |

**O -- Optimize (Days 180-365)**

| Activity | Timing | Deliverable | Owner |
|----------|--------|-------------|-------|
| ROI data collection | Day 180 | Usage metrics, time savings, business outcomes | CSM |
| ROI report creation | Day 200 | Branded ROI report with quantified value | CSM + PMM |
| Executive presentation | Day 210 | ROI presentation for executive sponsor | CSM |
| Case study qualification | Day 220 | Assess willingness for public case study | CSM + PMM |

**R -- Renew (60 Days Pre-Renewal)**

| Day (before renewal) | Action | Owner |
|---------------------|--------|-------|
| -60 | Internal renewal review: health score, usage, risks | CSM |
| -45 | Renewal + expansion conversation with champion | CSM |
| -30 | Proposal delivered: renewal terms + expansion options | CSM + Sales |
| -15 | Negotiation and procurement support | CSM + Sales |
| -7 | Final approval and signature | Sales |
| 0 | Renewal confirmed, next-year success plan created | CSM |

### Step 3: Build the Health Scoring Model

The health score predicts account risk and expansion potential on a 0-100 scale.

**Health Score Components:**

| Component | Weight | Inputs | Scoring Logic |
|-----------|--------|--------|---------------|
| Usage Depth | 30% | Core feature usage frequency, actions per session | 0-25: <1x/week; 25-50: 1-3x/week; 50-75: daily; 75-100: multiple daily |
| Usage Breadth | 20% | Number of features adopted out of total available | 0-25: <20% features; 25-50: 20-40%; 50-75: 40-70%; 75-100: >70% |
| Engagement | 20% | Login frequency, support interactions, event attendance | 0-25: monthly; 25-50: weekly; 50-75: multiple weekly; 75-100: daily |
| Sentiment | 15% | NPS score, CSAT, support sentiment, survey responses | 0-25: detractor; 25-50: passive-low; 50-75: passive-high; 75-100: promoter |
| Business Impact | 15% | ROI documented, executive sponsor, business case | 0-25: no ROI; 25-50: anecdotal; 50-75: quantified; 75-100: exec-validated |

**Health Score Calculation:**

```
Health_Score = (Usage_Depth x 0.30) + (Usage_Breadth x 0.20) + (Engagement x 0.20)
             + (Sentiment x 0.15) + (Business_Impact x 0.15)
```

### Step 4: Define Health Bands and Automated Interventions

Each health band triggers specific actions and escalation paths.

| Band | Score Range | Label | Account % Target | Intervention | Cadence | Owner |
|------|-----------|-------|-----------------|-------------|---------|-------|
| A | 80-100 | Thriving | 30%+ | Advocacy cultivation, expansion conversation | Quarterly QBR | CSM |
| B | 60-79 | Healthy | 40%+ | Continue nurture, feature adoption push | Monthly check-in | CSM |
| C | 40-59 | At Risk | <20% | Risk mitigation, exec re-engagement, rescue plan | Bi-weekly | CSM + Manager |
| D | 0-39 | Critical | <10% | Emergency intervention, exec-to-exec outreach | Weekly | CS Leader + Exec |

**Automated Interventions by Band:**

| Trigger | Band A Action | Band B Action | Band C Action | Band D Action |
|---------|-------------|-------------|-------------|-------------|
| Score drops 10+ pts in 30 days | Monitor | CSM alert | Manager alert, call scheduled | Exec escalation, rescue plan |
| No login in 7 days | N/A (unlikely) | In-app re-engage | CSM call + email | Emergency outreach |
| Support ticket (negative) | Thank + resolve | Thank + resolve + CSM note | CSM review + follow-up | CSM call within 24h |
| NPS detractor response | CSM follow-up | CSM call within 48h | CSM call within 24h | Exec call within 24h |
| Usage spike (positive) | Expansion signal | Expansion signal | Recovery signal | Recovery signal |

### Step 5: Build the Expansion Playbook

Trigger-based expansion motions with conversation templates and timing.

**Expansion Signal Detection:**

| # | Signal | Data Source | Confidence | Expansion Type | Suggested Action |
|---|--------|-----------|-----------|---------------|-----------------|
| 1 | Hitting usage/seat limits | Product analytics | High | Tier upgrade | Proactive outreach before hard limit |
| 2 | New team members added | Product analytics | High | Seat expansion | Celebrate growth, offer team onboarding |
| 3 | New use case adopted | Feature analytics | Medium | Cross-sell | Share relevant case study, offer workshop |
| 4 | Executive sponsor change | CRM/CSM note | Medium | Re-engage | Exec intro, value recap presentation |
| 5 | Budget cycle approaching | Calendar/CRM | Medium | Any expansion | QBR with ROI data, proposal |
| 6 | Competitor contract expiring | Intel/CRM | High | Displacement | Competitive battle card, migration offer |
| 7 | Industry event trigger | Signal radar | Low-Med | Awareness | Relevant content, event invitation |

**Expansion Conversation Framework:**

| Phase | Timing | Approach | Template |
|-------|--------|---------|----------|
| Signal detected | Day 0 | Internal: Review account, prep data | Pull usage data, ROI metrics, growth trajectory |
| Soft open | Day 1-3 | Share insight: "I noticed [signal]..." | Value-first, no pitch, ask about their experience |
| Value quantification | Day 5-10 | Present ROI: "Here is what you have achieved..." | ROI report, usage growth chart, peer benchmarks |
| Proposal | Day 10-15 | Recommend next step: "Based on your growth..." | Specific tier/product recommendation with business case |
| Negotiation | Day 15-30 | Handle objections, involve champion | Mutual action plan, procurement checklist |

### Step 6: Design the Advocacy Engine

Systematically develop customer advocates across four programs.

**Advocacy Programs:**

| Program | Target Audience | Ask Level | Reward | Pipeline Goal |
|---------|---------------|-----------|--------|-------------|
| Case Study Pipeline | Band A, 6+ months, ROI documented | High (time, approval) | Co-marketing, early access | 2-4 per quarter |
| Referral Program | Band A or B, NPS 9-10 | Medium (introduction) | Credit, gift, mutual benefit | 5-10 per quarter |
| Champion Program | Power users, internal advocates | Medium (ongoing) | Exclusive community, swag, events | 10-20 per quarter |
| Advisory Board | Strategic accounts, industry leaders | High (strategic input) | Influence roadmap, executive access | 6-10 members |

**Case Study Pipeline Process:**

| Stage | Action | Owner | Timeline | Deliverable |
|-------|--------|-------|----------|-------------|
| Identify | Flag Band A accounts with quantified ROI | CSM | Ongoing | Candidate list |
| Qualify | Confirm willingness, get internal approval | CSM + PMM | 1-2 weeks | Signed release |
| Interview | 45-minute structured interview | PMM | 1 week | Raw transcript |
| Draft | Write case study with customer review | PMM | 2 weeks | Draft document |
| Approve | Customer legal/marketing sign-off | CSM | 1-2 weeks | Approved final |
| Publish | Multi-format distribution | Marketing | 1 week | PDF, web, video, social |

**Referral Program Structure:**

| Element | Design |
|---------|--------|
| Who can refer | NPS 9-10 promoters, Band A and B accounts |
| How to refer | In-app widget, email template, unique referral link |
| Reward (referrer) | Account credit, premium feature access, gift |
| Reward (referee) | Extended trial, onboarding bonus, discount |
| Tracking | Unique codes, CRM attribution, dashboard |
| Goal | 10% of new pipeline from referrals within 12 months |

## Output

Save to `outputs/growth-loop/`

### Deliverables:
1. **ANCHOR Lifecycle Playbook** -- Six-stage lifecycle program with touchpoints, content, channels, triggers, and automation specs for each stage from Activate through Renew
2. **Health Scoring Model** -- 0-100 health score with five weighted components, scoring logic, four health bands (Thriving/Healthy/At Risk/Critical), and automated intervention protocols per band
3. **Expansion Playbook** -- Seven trigger-based expansion signals with confidence levels, suggested actions, conversation framework, and templates from soft open through negotiation
4. **Advocacy Program Design** -- Four-program advocacy engine (Case Studies, Referrals, Champions, Advisory Board) with processes, targets, rewards, and pipeline goals

## Chain Connections
- **Receives from:** journey-architect (customer journey stages), launch-pulse (adoption and retention metrics), launch-command (post-launch handoff)
- **Feeds into:** signal-radar (customer signals and advocacy data), demand-engine (referral pipeline, case studies for content)
- **Enhanced by:** battle-scanner (competitive switching intel), enablement-forge (CS enablement materials), financial-analyst (LTV and unit economics)
