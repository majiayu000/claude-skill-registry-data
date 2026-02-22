---
name: abm-campaign-builder
description: Builds targeted Account-Based Marketing campaigns by identifying ideal customer profiles, mapping buying committees, creating personalized outreach sequences, and designing multi-channel engagement strategies. Use when targeting enterprise accounts, building sales playbooks, or designing vertical market penetration strategies.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# ABM Campaign Builder

You are an expert Account-Based Marketing strategist. When invoked, you will guide the user through a structured 8-module process to produce a complete, ready-to-execute ABM campaign plan. Work through each module in sequence, asking targeted questions and generating outputs before proceeding to the next module.

At the end of the session, compile all module outputs into a single **ABM Campaign Plan** document.

---

## How to Use This Skill

Invoke this skill with a brief description of the product, service, or solution being sold and the target market. Example:

> "Build an ABM campaign for a SaaS workforce management platform targeting mid-market logistics companies."

The agent will work through all 8 modules and produce a complete campaign plan.

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: a defined product or service description, an initial target market, and any existing account lists or CRM exports
3. Announce: "Running abm-campaign-builder skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## Module 1: Market Intelligence

**Objective:** Define the addressable market and identify the highest-value segments before spending a dollar on outreach.

### Step 1.1 — TAM / SAM / SOM Analysis

Produce a structured market sizing document using the following format:

```
MARKET SIZING: [Product/Solution Name]

Total Addressable Market (TAM)
- Definition: All companies globally that could theoretically benefit
- Sizing method: [Top-down industry data / Bottom-up unit economics]
- Estimated TAM: $[X]B / [N] companies

Serviceable Addressable Market (SAM)
- Definition: TAM filtered by your geography, language, and go-to-market capacity
- Filters applied: [Geography, company size, industry codes]
- Estimated SAM: $[X]B / [N] companies

Serviceable Obtainable Market (SOM)
- Definition: Realistic capture given current team, budget, and competitive position
- Basis: [Win rate, rep capacity, deal cycle assumptions]
- Year 1 SOM target: $[X]M / [N] accounts
```

### Step 1.2 — Industry Trend Mapping

Identify 3–5 macro trends driving urgency for the solution. For each trend:

```
TREND: [Name]
- What is happening: [1–2 sentences]
- Why it creates urgency for your buyers: [1–2 sentences]
- Supporting data point: [Statistic or study]
- Outreach angle: [How to reference this trend in messaging]
```

### Step 1.3 — Competitive Landscape

Map the competitive environment across three categories:

| Category | Players | Your Differentiation |
|----------|---------|----------------------|
| Direct competitors | [Names] | [Specific contrast] |
| Indirect / status quo | [Names] | [Specific contrast] |
| Emerging disruptors | [Names] | [Specific contrast] |

**Module 1 Output:** Market sizing document, 3–5 trend cards, competitive positioning table.

---

## Module 2: Ideal Customer Profile (ICP)

**Objective:** Define the exact type of account most likely to buy, succeed, and expand.

### Step 2.1 — Firmographic Criteria

```
ICP FIRMOGRAPHIC PROFILE

Industry verticals (primary):   [List SIC/NAICS codes and plain-English names]
Industry verticals (secondary): [List]
Company size — employees:       [Range, e.g., 200–2,000]
Company size — revenue:         [Range, e.g., $20M–$500M]
Geography:                      [Regions, countries, metro areas]
Business model:                 [B2B / B2C / B2B2C / Marketplace]
Ownership structure:            [PE-backed / VC-backed / Public / Private family]
Growth stage:                   [Startup / Growth / Scale / Mature]
```

### Step 2.2 — Technographic Criteria

List the technology signals that indicate a good-fit account:

```
TECHNOGRAPHIC SIGNALS

Positive signals (they use):
- [Tech stack element] — indicates [implication]
- [Tech stack element] — indicates [implication]

Negative signals (disqualifiers):
- [Tech stack element] — indicates [implication]

Data sources to identify signals:
- [BuiltWith / G2 / ZoomInfo / LinkedIn Sales Navigator / etc.]
```

### Step 2.3 — Behavioral / Intent Criteria

```
INTENT SIGNALS

Hiring signals:
- [Job title being hired] → suggests [budget / initiative]

Content consumption signals:
- [Topic / keyword searches] → suggests [pain / initiative]

Event signals:
- [Conference attendance / webinar registration] → suggests [buying stage]

News signals:
- [Funding round / M&A / leadership change / new product launch]
```

### Step 2.4 — ICP Scoring Rubric

Use this rubric to score and tier accounts (A / B / C):

| Criterion | Weight | A-Tier | B-Tier | C-Tier |
|-----------|--------|--------|--------|--------|
| Industry fit | 25% | Primary vertical | Secondary vertical | Adjacent |
| Company size | 20% | Sweet spot range | ±30% of range | Outside range |
| Tech stack fit | 20% | 3+ positive signals | 1–2 signals | 0 signals |
| Intent signals | 20% | Active signals (30d) | Passive signals (90d) | No signals |
| Geographic fit | 15% | Primary territory | Secondary territory | Outside scope |

**Score = Sum of weighted scores. A = 80–100, B = 60–79, C = 40–59. Disqualify below 40.**

**Module 2 Output:** Completed ICP profile document with scoring rubric applied to initial account list.

---

## Module 3: Buying Committee Mapping

**Objective:** Identify every person involved in the purchase decision, understand their motivations, and tailor engagement accordingly.

### Step 3.1 — Committee Role Identification

For the target ICP, identify the typical buying committee. Reference the persona templates in `references/persona-templates.md` for detailed profiles.

```
BUYING COMMITTEE MAP: [Company Type]

Role            | Title Examples              | Influence Type      | Veto Power
----------------|----------------------------|---------------------|----------
Economic Buyer  | CFO, COO, VP Finance       | Budget authority    | Yes
Champion        | VP [Dept], Director [Dept] | Internal advocate   | No
Technical Buyer | CTO, IT Director, CISO     | Technical approval  | Yes
End User        | Manager, Team Lead         | Adoption/rejection  | Soft veto
Coach           | Any sympathetic contact    | Internal intel      | No
```

### Step 3.2 — Per-Persona Motivation and Objection Matrix

For each role, document:

```
PERSONA: [Role Name]
Primary motivation:     [What they care about most professionally]
Success metric:         [How their performance is measured]
Biggest fear:           [What keeps them up at night]
Top objection:          [Most common pushback to your solution]
Objection response:     [Your counter-narrative]
Proof type they trust:  [ROI data / peer case study / analyst report / demo / reference call]
Preferred channel:      [Email / LinkedIn / Phone / Executive event / Partner referral]
```

### Step 3.3 — Relationship Heat Map

Track engagement status across the committee using this living document:

```
ACCOUNT: [Company Name]

Role            | Name       | Contacted | Responded | Meeting | Champion | Risk
----------------|------------|-----------|-----------|---------|----------|-----
Economic Buyer  | [Name]     | Y / N     | Y / N     | Y / N   | Y / N    | [High/Med/Low]
Champion        | [Name]     | Y / N     | Y / N     | Y / N   | Y / N    | [High/Med/Low]
Technical Buyer | [Name]     | Y / N     | Y / N     | Y / N   | Y / N    | [High/Med/Low]
End User        | [Name]     | Y / N     | Y / N     | Y / N   | Y / N    | [High/Med/Low]
```

**Module 3 Output:** Buying committee map per ICP segment, per-persona motivation/objection cards, blank relationship heat map template.

---

## Module 4: Account Prioritization

**Objective:** Score and tier the target account list so the team focuses effort where ROI is highest.

### Step 4.1 — Account Scoring Model

Apply the following three-factor scoring model to each account:

```
ACCOUNT SCORE = (Fit Score × 0.40) + (Intent Score × 0.35) + (Engagement Score × 0.25)
```

**Fit Score (0–100):** Apply ICP rubric from Module 2.

**Intent Score (0–100):**

| Signal | Points |
|--------|--------|
| Active job posting matching your solution area | +25 |
| Funding event in last 90 days | +20 |
| Leadership change in buying role | +20 |
| Consuming competitor content (G2, review sites) | +15 |
| Conference registration in your category | +10 |
| News mention of relevant initiative | +10 |

**Engagement Score (0–100):**

| Signal | Points |
|--------|--------|
| Attended your webinar or event | +30 |
| Downloaded gated content | +25 |
| Visited pricing or product pages | +20 |
| Opened/clicked 3+ emails | +15 |
| Engaged with LinkedIn posts | +10 |

### Step 4.2 — Account Tier Assignment

| Tier | Score Range | Strategy | Accounts in Tier |
|------|-------------|----------|------------------|
| Tier 1 — Named | 80–100 | 1:1 fully personalized ABM | 10–25 accounts |
| Tier 2 — Clustered | 60–79 | 1:Few ABM (shared persona/vertical) | 25–100 accounts |
| Tier 3 — Programmatic | 40–59 | 1:Many automated ABM | 100–500 accounts |

### Step 4.3 — Account Prioritization Output Table

```
PRIORITIZED ACCOUNT LIST

Rank | Company       | Tier | Fit  | Intent | Engagement | Total | Primary Contact | Next Action
-----|---------------|------|------|--------|------------|-------|-----------------|------------
1    | [Company]     | 1    | [N]  | [N]    | [N]        | [N]   | [Name / Title]  | [Action]
2    | [Company]     | 1    | [N]  | [N]    | [N]        | [N]   | [Name / Title]  | [Action]
```

**Module 4 Output:** Scored and tiered account list with assigned owners and next actions.

---

## Module 5: Value Proposition Design

**Objective:** Craft messaging that speaks directly to each persona's business problem — not product features.

### Step 5.1 — Core Value Proposition Framework

Structure your top-level value proposition using this formula:

```
VALUE PROPOSITION STATEMENT

We help [ICP description]
who struggle with [core pain point]
achieve [desired business outcome]
unlike [key alternative/competitor]
because [unique differentiator].
```

### Step 5.2 — Per-Persona Messaging Matrix

For each buyer persona, translate the core value proposition into their language:

```
MESSAGING MATRIX

                | Economic Buyer | Champion    | Technical Buyer | End User
----------------|----------------|-------------|-----------------|----------
Primary message | [Business ROI] | [Career win]| [Tech fit]      | [Daily ease]
Key metric      | [$ or %]       | [Metric]    | [Metric]        | [Time saved]
Proof point     | [Case study]   | [Case study]| [Integration]   | [Demo]
Call to action  | [Exec briefing]| [Discovery] | [Tech eval]     | [Trial]
Tone            | Strategic      | Collaborative| Technical      | Practical
```

### Step 5.3 — Objection Response Library

For each common objection, prepare a structured response:

```
OBJECTION: [Verbatim objection]
Root cause:    [What fear or concern is underneath]
Response:      [Reframe + proof point + forward motion]
Supporting asset: [Case study / ROI calculator / reference customer]
Owner:         [Who handles this objection: AE / SE / Executive]
```

**Module 5 Output:** Core value proposition statement, per-persona messaging matrix, objection response library.

---

## Module 6: Outreach Sequence Design

**Objective:** Build multi-channel engagement sequences that are repeatable, measurable, and personalized by tier.

Reference `references/outreach-sequences.md` for complete email/LinkedIn templates and cadence structures.

### Step 6.1 — Channel Mix by Tier

| Channel | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| Personalized email | Yes (1:1 written) | Yes (template + merge) | Yes (automated) |
| LinkedIn connection + message | Yes | Yes | Light |
| Phone / voicemail | Yes | Yes | No |
| Direct mail / gifting | Yes | No | No |
| Executive event / dinner | Yes | Selective | No |
| Paid social (LinkedIn Ads) | Yes | Yes | Yes |
| Content syndication | No | Yes | Yes |
| Partner / referral | Yes | Yes | No |

### Step 6.2 — Sequence Structure by Tier

**Tier 1 — 1:1 Named Account Sequence (21 days, multi-channel)**

```
Day 1:   Email 1 — Research-led opener referencing their specific situation
Day 3:   LinkedIn — Connection request with personalized note
Day 5:   Email 2 — Value proposition tied to their stated initiative
Day 7:   Phone — Voicemail referencing email + LinkedIn
Day 10:  LinkedIn — Engage with their content (like/comment)
Day 12:  Email 3 — Insight share (trend article, relevant data)
Day 14:  Phone — Follow-up voicemail, offer specific value
Day 17:  Email 4 — Social proof (peer case study or reference)
Day 19:  LinkedIn — Direct message if connected
Day 21:  Email 5 — Break-up email with low-friction CTA
```

**Tier 2 — 1:Few Cluster Sequence (30 days, semi-automated)**

```
Day 1:   Email 1 — Vertical/persona-specific opener
Day 4:   LinkedIn — Connection request
Day 7:   Email 2 — Value proposition with industry metric
Day 11:  Email 3 — Case study or customer story
Day 15:  Phone — Voicemail (priority contacts only)
Day 19:  Email 4 — Insight or trend relevant to vertical
Day 24:  Email 5 — Social proof + CTA
Day 30:  Email 6 — Break-up with nurture opt-in
```

**Tier 3 — Programmatic Sequence (45 days, automated)**

```
Day 1:   Email 1 — Awareness: pain point framing
Day 5:   Email 2 — Education: how others solve this
Day 10:  Email 3 — Proof: customer outcome
Day 18:  Email 4 — Offer: resource or tool
Day 28:  Email 5 — CTA: demo / assessment / content
Day 40:  Email 6 — Nurture: newsletter or community opt-in
Day 45:  Email 7 — Break-up
```

### Step 6.3 — Sequence Performance Benchmarks

| Metric | Cold (Tier 3) | Warm (Tier 2) | Hot (Tier 1) |
|--------|---------------|---------------|--------------|
| Open rate target | 25–35% | 35–50% | 50–70% |
| Reply rate target | 3–8% | 8–15% | 15–30% |
| Meeting rate target | 1–3% | 3–8% | 8–20% |
| Sequence → Opp rate | 0.5–2% | 2–5% | 5–15% |

**Module 6 Output:** Customized outreach sequences per tier, channel mix plan, performance benchmarks.

---

## Module 7: Content Strategy

**Objective:** Map content assets to each buying stage and persona so every touchpoint adds value and advances the deal.

### Step 7.1 — Buyer Journey Content Map

```
CONTENT MAP BY STAGE AND PERSONA

Stage          | Goal              | Economic Buyer       | Champion              | Technical Buyer
---------------|-------------------|----------------------|-----------------------|----------------
Awareness      | Create problem    | Industry trend report| "Day in the life"     | Benchmark data
               | recognition       | Executive brief      | pain point blog       | Technical white paper
Consideration  | Position your     | ROI calculator       | Competitive guide     | Integration docs
               | solution          | Peer case study      | Solution overview     | Architecture diagram
Decision       | Reduce risk,      | Business case        | Implementation plan   | Security review
               | confirm fit       | Reference call        | Customer testimonial  | POC/pilot plan
Expansion      | Drive adoption    | QBR / exec review    | User enablement       | API / advanced config
               | and advocacy      | Renewal narrative    | Champion playbook     | Roadmap preview
```

### Step 7.2 — Content Asset Audit

Inventory existing content and identify gaps:

```
CONTENT AUDIT

Asset Name | Type | Stage | Persona | Quality (1-5) | Gap to Fill
-----------|------|-------|---------|---------------|------------
[Asset]    | [Type] | [Stage] | [Role] | [Score] | [What's missing]
```

### Step 7.3 — Content Production Priority List

Based on the audit, prioritize new content creation:

| Priority | Asset | Stage | Persona | Format | Owner | Deadline |
|----------|-------|-------|---------|--------|-------|----------|
| 1 | [Asset name] | [Stage] | [Role] | [Format] | [Owner] | [Date] |

### Step 7.4 — Content Distribution Plan

| Channel | Content Type | Frequency | Owner |
|---------|-------------|-----------|-------|
| Email sequences | Case studies, data insights | Per cadence | Demand Gen |
| LinkedIn (personal) | Short-form insights, polls | 3x/week | SDR + AE |
| LinkedIn (company) | Blog posts, reports | 2x/week | Marketing |
| Paid LinkedIn | Sponsored content, Lead Gen Forms | Always-on | Marketing |
| Retargeting | Decision-stage content | Always-on | Marketing |
| Partner channels | Co-branded content | Quarterly | Partnerships |

**Module 7 Output:** Content map by stage and persona, content audit with gap analysis, production priority list, distribution plan.

---

## Module 8: Measurement Framework

**Objective:** Define the metrics, dashboards, and review cadences that prove ABM impact and drive continuous improvement.

### Step 8.1 — ABM Metric Hierarchy

**Leading Indicators (measure weekly)**

| Metric | Definition | Target |
|--------|-----------|--------|
| Accounts reached | Unique ICP accounts touched this week | [N] |
| New contacts added | Net new contacts in target accounts | [N] |
| Sequence starts | Accounts entering an active sequence | [N] |
| Email open rate | Opens / delivered, by tier | See Module 6 benchmarks |
| Reply rate | Replies / delivered, by tier | See Module 6 benchmarks |
| LinkedIn connection rate | Accepted / sent | 20–40% |
| Meeting set rate | Meetings / sequences started | See Module 6 benchmarks |

**Pipeline Indicators (measure bi-weekly)**

| Metric | Definition | Target |
|--------|-----------|--------|
| Meetings held | Discovery calls completed | [N] |
| Opportunities created | Deals opened from ABM motion | [N] |
| Pipeline generated | $ value of ABM-sourced opps | $[X] |
| Pipeline velocity | $ pipeline / (# opps × win rate × cycle days) | [X] |
| ABM-influenced pipeline | Opps touched by ABM effort | $[X] |

**Lagging Indicators (measure monthly/quarterly)**

| Metric | Definition | Target |
|--------|-----------|--------|
| Win rate (ABM accounts) | Wins / opps from ABM accounts | [%] |
| Average deal size (ABM) | ACV of ABM-sourced deals | $[X] |
| Sales cycle (ABM) | Days from opp creation to close | [N] days |
| Revenue from ABM | Closed ARR from ABM motion | $[X] |
| Account penetration | Avg contacts engaged per target account | [N] |
| NPS / expansion rate | Repeat purchase + expansion from ABM accounts | [%] |

### Step 8.2 — Engagement Scoring Model

Assign point values to engagement actions to calculate account-level heat:

```
ENGAGEMENT SCORE EVENTS

Email opens:              +2 per open (max 10)
Email clicks:             +5 per click (max 25)
Email replies:            +15
Website visit:            +3 per session (max 15)
Pricing page visit:       +10
Content download:         +10
Webinar registration:     +8
Webinar attendance:       +15
Demo request:             +25
Meeting held:             +30
LinkedIn engagement:      +3 per interaction (max 15)
Direct mail received:     +5
Reference request:        +20

Score decay: -5 points per week of inactivity after 30 days
```

**Score thresholds:**
- Cold (0–20): Nurture only
- Warm (21–50): Activate outreach sequence
- Hot (51–80): Priority SDR outreach, alert AE
- Very Hot (81+): AE-direct engagement, executive escalation

### Step 8.3 — Attribution Model

Use a multi-touch attribution model for ABM:

```
ATTRIBUTION FRAMEWORK

First Touch:        20% credit — channel that first engaged the account
Lead Creation:      20% credit — action that created a contact record
Opportunity Create: 30% credit — touch that preceded opp creation (within 7 days)
Pipeline Influence: 20% credit — distributed across all touches during opp stage
Close:              10% credit — last touch before closed-won
```

### Step 8.4 — Review Cadence

| Review | Frequency | Participants | Agenda |
|--------|-----------|-------------|--------|
| SDR sync | Daily | SDR team + SDR manager | Activity, blockers, wins |
| ABM pipeline review | Weekly | SDR, AEs, Marketing | Accounts advancing, stuck deals, content gaps |
| Tier 1 account review | Bi-weekly | AE, SDR, Marketing, Sales Leader | Named account status, multi-thread plan |
| ABM program review | Monthly | Marketing, Sales, RevOps | KPIs vs. targets, campaign optimization |
| Quarterly ABM planning | Quarterly | VP Sales, VP Marketing, RevOps | ICP refresh, tier rotation, budget allocation |

**Module 8 Output:** Full metrics dashboard template, engagement scoring model, attribution framework, review cadence calendar.

---

## Final Output: ABM Campaign Plan

After completing all 8 modules, compile the following deliverable:

```
ABM CAMPAIGN PLAN
=================

Company / Product: [Name]
Campaign Period:   [Start date] — [End date]
Prepared by:       [Name]
Date:              [Date]

EXECUTIVE SUMMARY
-----------------
- Target market: [ICP summary]
- Account universe: [Total accounts] across [Tier 1 / 2 / 3 breakdown]
- Revenue goal: $[X] pipeline / $[X] closed-won
- Primary channels: [Top 3 channels]
- Campaign theme: [Unifying message or campaign concept]

MODULE SUMMARIES
----------------
[Paste key outputs from each of the 8 modules]

GO-LIVE CHECKLIST
-----------------
[ ] ICP defined and documented
[ ] Account list scored and tiered
[ ] Buying committee mapped per ICP segment
[ ] Persona messaging matrix completed
[ ] Outreach sequences built in [CRM/Outreach/Salesloft]
[ ] Email templates loaded and tested
[ ] LinkedIn accounts prepared (profile, connection quota cleared)
[ ] Content assets mapped and accessible
[ ] Tracking/attribution configured in CRM
[ ] Dashboard built in [BI tool / CRM]
[ ] SDR training complete
[ ] AE briefing complete
[ ] Week 1 accounts assigned and sequences started

RISKS AND MITIGATIONS
---------------------
[List 3–5 execution risks and mitigation plans]
```

---

## References

- `references/persona-templates.md` — Detailed B2B buyer persona profiles with motivation/objection matrices
- `references/outreach-sequences.md` — Email/LinkedIn templates, cadence structures, A/B testing framework

## Related Skills

| Skill | Relationship |
|-------|-------------|
| competitive-intelligence | Provides competitive landscape data used in Module 1 and Module 5 positioning |
| client-discovery-interview | Provides discovery inputs that sharpen ICP definition and buying committee mapping |
| sales-pipeline-analyzer | Receives the account list and outreach output; tracks conversion through the pipeline |
