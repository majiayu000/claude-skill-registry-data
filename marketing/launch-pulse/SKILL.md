---
name: launch-pulse
description: 'GTM analytics and measurement framework that builds metrics architecture, dashboard specs, and alert systems. Use when: GTM metrics, launch metrics, measurement framework, KPIs, dashboard design, what should we measure, analytics framework.'
---

# Launch Pulse (VITAL Metrics Architecture)

A comprehensive measurement framework engine that designs the full analytics stack for tracking launch success -- from metric definitions through dashboard specifications to automated alert systems. VITAL ensures you measure what matters, detect problems early, and attribute results accurately across channels and touchpoints.

## When to Use
- Designing the measurement framework for an upcoming launch
- Defining KPIs and success criteria for GTM initiatives
- Building dashboard specifications for different stakeholder audiences
- Setting up alert systems to detect launch issues early
- Choosing an attribution model for multi-channel campaigns
- Establishing baselines and targets before a launch
- Creating a metrics review cadence and reporting rhythm

## What You'll Need

**Critical inputs (ask if not provided):**
- Product name and launch type (GA, beta, feature, expansion)
- Target audience and customer segments
- Business objectives and success criteria (revenue, adoption, pipeline targets)
- Marketing channels being activated (from demand-engine)
- Sales motion (PLG, sales-led, hybrid)
- Analytics tools and data infrastructure in use

**Nice-to-have:**
- Historical baselines for similar launches or products
- Current analytics setup and gaps
- Dashboard tools and BI platforms available
- Data team capacity and timeline
- Attribution tools currently deployed
- Customer journey maps (from journey-architect)

## Process

### Step 1: Build the VITAL Metrics Pyramid

The VITAL pyramid organizes metrics into five layers, each building on the one below. Start from the base (Volume) and work upward to Loyalty.

| Layer | Focus | Time Horizon | Audience | Signal Type |
|-------|-------|-------------|----------|-------------|
| **V** - Volume | Reach and awareness | Daily | Marketing | Leading |
| **I** - Intent | Engagement and interest | Daily/Weekly | Marketing + Sales | Leading |
| **T** - Traction | Pipeline and conversion | Weekly | Sales + Revenue | Leading/Lagging |
| **A** - Adoption | Product usage and value | Weekly/Monthly | Product + CS | Lagging |
| **L** - Loyalty | Retention and advocacy | Monthly/Quarterly | CS + Executive | Lagging |

### Step 2: Define Metrics Per Layer

For each VITAL layer, define 4-8 specific metrics with full specifications.

**V -- Volume Metrics (Top of Funnel)**

| # | Metric | Definition | Source | Frequency | Owner | Leading/Lagging |
|---|--------|-----------|--------|-----------|-------|-----------------|
| V1 | Website Traffic | Unique visitors to launch/product pages | GA4 | Daily | Marketing | Leading |
| V2 | Impressions | Total ad impressions across paid channels | Ad platforms | Daily | Demand Gen | Leading |
| V3 | Social Reach | Unique accounts reached on social platforms | Social tools | Daily | Social | Leading |
| V4 | PR Mentions | Press coverage and article mentions | Media monitoring | Daily | Comms | Leading |
| V5 | Content Views | Blog, video, and resource page views | CMS/GA4 | Daily | Content | Leading |
| V6 | Event Registrations | Webinar/event signups | Event platform | Weekly | Events | Leading |

**I -- Intent Metrics (Mid-Funnel)**

| # | Metric | Definition | Source | Frequency | Owner | Leading/Lagging |
|---|--------|-----------|--------|-----------|-------|-----------------|
| I1 | MQLs | Marketing qualified leads by scoring criteria | MAP | Daily | Demand Gen | Leading |
| I2 | Demo Requests | Inbound requests for product demonstration | CRM | Daily | Sales | Leading |
| I3 | Trial Signups | Free trial or freemium account creations | Product | Daily | Growth | Leading |
| I4 | Content Engagement | Downloads, time-on-page, return visits | GA4/MAP | Weekly | Content | Leading |
| I5 | Email Engagement | Open rate, click rate, reply rate | MAP | Weekly | Email | Leading |
| I6 | Pricing Page Views | Visits to pricing/packaging pages | GA4 | Daily | Marketing | Leading |

**T -- Traction Metrics (Pipeline)**

| # | Metric | Definition | Source | Frequency | Owner | Leading/Lagging |
|---|--------|-----------|--------|-----------|-------|-----------------|
| T1 | SQLs | Sales qualified leads accepted by sales | CRM | Weekly | Sales | Leading |
| T2 | Pipeline Created | Dollar value of new pipeline from launch | CRM | Weekly | Revenue | Leading |
| T3 | Win Rate | Deals won / deals in pipeline | CRM | Monthly | Sales | Lagging |
| T4 | Sales Cycle Length | Average days from SQL to closed-won | CRM | Monthly | Sales | Lagging |
| T5 | Deal Size | Average contract value of launch deals | CRM | Monthly | Revenue | Lagging |
| T6 | MQL-to-SQL Rate | Conversion rate from MQL to SQL | CRM/MAP | Weekly | RevOps | Leading |

**A -- Adoption Metrics (Product)**

| # | Metric | Definition | Source | Frequency | Owner | Leading/Lagging |
|---|--------|-----------|--------|-----------|-------|-----------------|
| A1 | Activation Rate | % of signups completing key onboarding action | Product analytics | Weekly | Product | Lagging |
| A2 | Time to Value | Median time from signup to first value moment | Product analytics | Weekly | Product | Lagging |
| A3 | DAU/WAU Ratio | Daily active / weekly active users (stickiness) | Product analytics | Weekly | Product | Lagging |
| A4 | Feature Adoption | % of users using launch feature within 30 days | Product analytics | Weekly | Product | Lagging |
| A5 | Usage Depth | Actions per session or per user per week | Product analytics | Weekly | Product | Lagging |

**L -- Loyalty Metrics (Retention)**

| # | Metric | Definition | Source | Frequency | Owner | Leading/Lagging |
|---|--------|-----------|--------|-----------|-------|-----------------|
| L1 | NPS | Net Promoter Score from post-launch survey | Survey tool | Monthly | CS | Lagging |
| L2 | Retention Rate | % of users/accounts active after 30/60/90 days | Product analytics | Monthly | CS | Lagging |
| L3 | Expansion Revenue | Upsell/cross-sell revenue from launch cohort | CRM | Monthly | Revenue | Lagging |
| L4 | Referral Rate | % of customers generating referrals | CRM/Product | Monthly | Growth | Lagging |
| L5 | Support Satisfaction | CSAT score on support interactions | Support tool | Weekly | Support | Lagging |

### Step 3: Set Targets and Thresholds

For each metric, establish baselines and progressive targets with RAG thresholds.

**Target-Setting Template:**

| Metric | Baseline | 30-Day Target | 90-Day Target | 365-Day Target | Red (<) | Yellow | Green (>) |
|--------|----------|--------------|---------------|----------------|---------|--------|-----------|
| V1: Website Traffic | | | | | | | |
| I1: MQLs | | | | | | | |
| T2: Pipeline | | | | | | | |
| A1: Activation Rate | | | | | | | |
| L2: Retention Rate | | | | | | | |

**RAG Threshold Guidelines:**

| Level | Definition | Action Required |
|-------|-----------|----------------|
| RED | Below 70% of target for 3+ consecutive periods | Immediate investigation, escalation to leadership, corrective action plan |
| YELLOW | 70-90% of target for 2+ consecutive periods | Root-cause analysis, optimization plan within 1 week |
| GREEN | 90%+ of target | Continue execution, look for scale opportunities |
| BLUE (bonus) | 120%+ of target | Investigate why, document learnings, consider increasing investment |

### Step 4: Design Dashboard Architecture

Build four dashboard tiers for different audiences and cadences.

**Dashboard Tier Map:**

| Dashboard | Audience | Metrics Count | Refresh | Format |
|-----------|----------|--------------|---------|--------|
| Executive | C-suite, VPs | 5-7 top-level | Weekly | One-page scorecard |
| Operations | Marketing, Sales leads | 15-20 operational | Daily | Multi-tab dashboard |
| Campaign | Channel managers | Per-channel deep dive | Real-time | Channel-specific views |
| Product | Product, Engineering | Adoption and usage | Daily | Product analytics tool |

**Executive Dashboard Specification (5 metrics):**

| Position | Metric | Visualization | Comparison | Alert |
|----------|--------|--------------|------------|-------|
| Hero | Pipeline Created (T2) | Number + trend line | vs. target, vs. last launch | < 70% of target |
| Top-left | MQLs (I1) | Number + bar chart | vs. target by week | < 70% of target |
| Top-right | Activation Rate (A1) | Percentage gauge | vs. baseline | < 50% |
| Bottom-left | Win Rate (T3) | Percentage + trend | vs. company average | < historical -10pp |
| Bottom-right | NPS (L1) | Score + distribution | vs. baseline, vs. industry | < 20 |

### Step 5: Configure Alert System

Define threshold-based alerts with escalation paths and response protocols.

**Alert Configuration Matrix:**

| Alert Name | Metric | Trigger Condition | Severity | Channel | Recipient | Response Protocol |
|-----------|--------|------------------|----------|---------|-----------|-------------------|
| Pipeline Drop | T2 | <70% weekly target, 2 weeks | Critical | Slack + Email | VP Sales, VP Marketing | Emergency pipeline review within 24h |
| Activation Cliff | A1 | <50% activation rate | Critical | Slack + Email | VP Product, PM | UX investigation, onboarding audit |
| MQL Drought | I1 | <60% daily target, 5 days | High | Slack | Demand Gen lead | Channel audit, budget reallocation |
| CAC Spike | T1/Budget | CAC >150% of target | High | Email | Marketing, Finance | Channel pause, spend review |
| Churn Signal | L2 | Retention <80% at 30 days | High | Slack + Email | CS lead, Product | Churn cohort analysis, intervention |
| Traffic Surge | V1 | >200% of daily average | Info | Slack | Marketing | Investigate source, capitalize if organic |

**Escalation Ladder:**

| Severity | First Response | Escalation | Timeline |
|----------|---------------|-----------|----------|
| Critical | Metric owner + VP | C-suite if unresolved | 24h to action plan, 48h to resolution |
| High | Metric owner + manager | VP if unresolved | 48h to action plan, 1 week to resolution |
| Medium | Metric owner | Manager if unresolved | 1 week to action plan |
| Info | Metric owner (log only) | No escalation | Document and review in weekly sync |

### Step 6: Attribution Model Design

Define how credit is assigned across channels and touchpoints.

**Attribution Model Comparison:**

| Model | How It Works | Best For | Limitation |
|-------|-------------|----------|-----------|
| First-Touch | 100% credit to first interaction | Understanding awareness drivers | Ignores nurture and conversion |
| Last-Touch | 100% credit to final interaction | Understanding conversion drivers | Ignores awareness and nurture |
| Linear | Equal credit across all touches | Fair distribution when unsure | Overweights low-impact touches |
| Time-Decay | More credit to recent touches | Shorter sales cycles | Undervalues awareness |
| Position-Based | 40% first, 40% last, 20% middle | Balanced, most recommended | Arbitrary weighting |
| Self-Reported | Ask buyers "how did you hear about us?" | Dark social, word-of-mouth | Recall bias, limited scale |

**Recommended Approach:**
- **Primary:** Position-based (40/20/40) for automated attribution
- **Secondary:** Self-reported "How did you hear about us?" on signup and demo forms
- **Validation:** Compare models quarterly -- if they diverge significantly, investigate

**Attribution Data Requirements:**

| Requirement | Tool/Source | Status | Gap |
|------------|-----------|--------|-----|
| UTM tracking on all links | URL builder + GA4 | | |
| CRM-MAP integration | CRM + MAP | | |
| Multi-touch tracking | Attribution tool | | |
| Self-reported field | Form builder | | |
| Offline event tracking | CRM manual + import | | |

## Output

Save to `outputs/launch-pulse/`

### Deliverables:
1. **VITAL Metrics Framework** -- Complete pyramid with 25-30 defined metrics, each with definition, source, frequency, owner, baseline, targets (30/90/365), RAG thresholds, and leading/lagging classification
2. **Dashboard Specifications** -- Four-tier dashboard architecture (Executive, Operations, Campaign, Product) with metric placement, visualization types, comparison logic, and refresh cadences
3. **Alert Rules** -- Threshold-based alert system with trigger conditions, severity levels, notification channels, recipients, response protocols, and escalation ladders
4. **Attribution Model** -- Recommended multi-model attribution approach with data requirements, implementation checklist, and quarterly validation protocol

## Chain Connections
- **Receives from:** launch-command (launch plan and workstreams), demand-engine (channel strategy and targets), budget-allocator (spend allocation for ROI tracking)
- **Feeds into:** growth-loop (adoption and retention metrics), signal-radar (market performance signals), launch-debrief (actuals vs targets)
- **Enhanced by:** journey-architect (touchpoint mapping for attribution), financial-analyst (unit economics for ROI thresholds)
