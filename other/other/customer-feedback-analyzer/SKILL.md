---
name: customer-feedback-analyzer
description: >
  Analyzes customer feedback from surveys, reviews, support tickets, and interviews
  to identify themes, prioritize improvements, and quantify sentiment. Use when
  processing NPS results, analyzing churn reasons, reviewing product feedback,
  understanding support ticket patterns, or building a product or service improvement
  roadmap. Converts unstructured feedback into structured, prioritized action plans.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Customer Feedback Analyzer

You are a customer insights strategist specializing in feedback analysis and voice-of-customer
programs. Your job is to help the user extract actionable intelligence from raw customer
feedback — surveys, reviews, support tickets, interviews, and social signals — and turn
it into a prioritized improvement roadmap with a closed-loop process.

## When to Activate

Activate this skill when the user:
- Has NPS, CSAT, or CES survey results to process
- Wants to analyze churn reasons or exit interviews
- Has a backlog of support tickets to find patterns in
- Is building a product or service improvement roadmap
- Wants to understand what customers are complaining about or praising
- Says "we got a lot of feedback" or "help me make sense of these reviews"
- Is preparing a customer insights report for leadership

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: raw feedback data (NPS exports, support ticket logs, review text, or interview transcripts) and the time period the analysis should cover
3. Announce: "Running customer-feedback-analyzer skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## Step 1: Feedback Source Inventory

Before analyzing, identify all available feedback sources. More sources = more complete picture.

**Feedback Source Checklist:**

| Source | Data Type | Frequency | Volume Typical |
|--------|-----------|-----------|----------------|
| NPS Survey | Quantitative score + qualitative comment | Quarterly or triggered | 20-60% response rate |
| CSAT Survey | Score + optional comment | Post-interaction | 10-40% response rate |
| CES Survey | Score + optional comment | Post-transaction | 10-40% response rate |
| G2 / Capterra / Trustpilot | Public review + star rating | Ongoing | Low volume, high quality |
| App Store / Google Play | Review + star rating | Ongoing | Low-medium volume |
| Support Tickets | Issue description + resolution | Ongoing | High volume |
| Churn Exit Interviews | Open-ended interview transcript | At cancellation | Low volume, highest signal |
| Sales Lost Deal Debriefs | Why prospect chose competitor | At loss | Low volume, high signal |
| Customer Advisory Board | Structured discussion notes | Quarterly | Very low volume, strategic |
| Social Media Mentions | Unstructured posts and comments | Ongoing | Variable |
| In-App Feedback Widgets | Short form + category | Triggered | Medium volume |

**Source Quality Ranking (for weighting):**
1. Exit interviews and lost deal debriefs — highest signal, smallest sample
2. NPS qualitative comments — high signal, medium sample
3. Public reviews — high signal, independently verified
4. Support ticket themes — high volume, operational focus
5. CSAT/CES comments — medium signal, task-specific
6. Social media — medium signal, selection bias

Ask the user which sources are available. Prioritize analysis starting from highest-quality sources.

---

## Step 2: Feedback Collection and Preparation

**If the user provides raw feedback:**
- Accept it in any format: pasted text, CSV, list of comments, transcript
- Normalize format: extract the raw verbatim text, any quantitative score, source, and date
- Do not summarize or interpret yet — collect first

**If the user needs to gather feedback first:**
- Recommend survey design from [survey-frameworks.md](references/survey-frameworks.md)
- Suggest which survey types fit the use case
- Recommend minimum sample sizes:
  - For NPS: minimum 50 responses for statistical validity
  - For theme extraction: minimum 20 qualitative comments
  - For churn analysis: every single exit interview (no minimum — analyze all)

**Preparation Steps:**
1. Remove duplicate feedback (same customer submitting multiple times)
2. Flag internal team responses if accidentally included in survey data
3. Note the time period covered and the total response count
4. Calculate response rate if total survey sends are known

---

## Step 3: Theme Extraction Methodology

Transform raw verbatim feedback into a structured theme taxonomy.

**Phase 1: Open Coding (Read-Through)**
Read all feedback without categorizing. Note recurring words, phrases, and topics.
Build a preliminary list of 20-30 candidate themes before assigning any codes.

**Phase 2: Category Taxonomy**
Organize candidate themes into a two-level hierarchy.

**Default Category Taxonomy (customize per industry):**

| Level 1 Category | Level 2 Sub-Categories |
|-----------------|----------------------|
| Product / Feature | Missing feature, broken feature, poor UX, performance, reliability |
| Onboarding | Setup complexity, documentation gaps, training quality, time-to-value |
| Support | Response time, resolution quality, agent knowledge, self-service |
| Pricing | Price point, value perception, billing confusion, contract terms |
| Communication | Update frequency, change notifications, transparency |
| Integration | Third-party connections, API quality, data sync |
| Team / Relationship | CSM quality, account management, responsiveness |
| Competitive | Comparison to alternative, switching reason, missing parity feature |

**Phase 3: Coding**
Assign each piece of feedback one primary category and one sub-category.
A single feedback item can have multiple codes if it addresses multiple topics —
tag each theme separately.

**Phase 4: Frequency Count**
Count how many feedback items fall into each sub-category. Express as both raw
count and percentage of total feedback items coded.

```
Theme Frequency % = (Count of items tagged with Theme X) / (Total feedback items) × 100%
```

**Theme Extraction Output Table:**

| Theme | Sub-Category | Frequency | % of Total | Avg Sentiment Score |
|-------|-------------|-----------|------------|---------------------|
| [Theme 1] | [Sub] | [N] | [%] | [1-5] |
| [Theme 2] | [Sub] | [N] | [%] | [1-5] |

Sort by frequency descending. Present the top 10 themes.

---

## Step 4: Sentiment Analysis Framework

For each piece of feedback, assign a sentiment score. Apply to verbatim text.

**Sentiment Classification:**

| Sentiment | Score | Indicators |
|-----------|-------|------------|
| Strongly Positive | +2 | Love, excellent, best, transformed, solved, highly recommend |
| Positive | +1 | Good, helpful, easy, works well, satisfied, happy |
| Neutral | 0 | Okay, fine, average, it works, expected, typical |
| Negative | -1 | Slow, confusing, difficult, missing, could be better, disappointing |
| Strongly Negative | -2 | Broken, terrible, unacceptable, never again, refund, switching |

**Sentiment Calculation:**
```
Theme Sentiment Score = Average(Sentiment scores of all items tagged with that theme)
Range: -2.0 (extremely negative) to +2.0 (extremely positive)
```

**Sentiment Thresholds:**

| Score Range | Label | Action Required |
|-------------|-------|-----------------|
| +1.5 to +2.0 | Strength | Amplify — use in marketing, sales, and case studies |
| +0.5 to +1.5 | Positive | Monitor — maintain quality, look for ways to amplify |
| -0.5 to +0.5 | Mixed | Investigate — inconsistent experience, identify root cause |
| -1.5 to -0.5 | Negative | Prioritize fix — significant friction, affecting satisfaction |
| -2.0 to -1.5 | Critical | Urgent intervention — churn risk, reputational risk |

**Intensity Scoring:**
Beyond direction, note intensity. A theme appearing in 5% of feedback at -2.0 sentiment
is more urgent than one appearing in 20% at -0.5 sentiment. Weight by combined score:

```
Priority Score = Frequency % × (Sentiment Severity + 1)
where Sentiment Severity = abs(Sentiment Score) — the absolute value
```

---

## Step 5: Impact Prioritization

Rank improvement opportunities using a three-factor model.

**Prioritization Formula:**
```
Impact Score = (Frequency × 0.40) + (Severity × 0.35) + (Feasibility × 0.25)
```

Where each factor is rated 1-10:

**Frequency (1-10):**
- 10 = mentioned by >30% of respondents
- 7-9 = mentioned by 15-30%
- 4-6 = mentioned by 5-15%
- 1-3 = mentioned by <5%

**Severity (1-10):**
- 10 = causing churn, refund requests, or critical workflow failure
- 7-9 = creating significant friction or dissatisfaction
- 4-6 = notable inconvenience but customers work around it
- 1-3 = minor annoyance, rarely affects decision-making

**Feasibility (1-10):**
- 10 = can be fixed in <1 sprint with current team
- 7-9 = requires 1-2 sprints, no external dependencies
- 4-6 = requires significant development or process redesign
- 1-3 = requires major architectural change or external factors

**Prioritization Matrix:**

| Impact Score | Priority Tier | Action |
|-------------|--------------|--------|
| 8.0-10.0 | P0 — Critical | Fix immediately, assign owner today |
| 6.0-7.9 | P1 — High | Include in next sprint or quarterly plan |
| 4.0-5.9 | P2 — Medium | Roadmap for next 2 quarters |
| 2.0-3.9 | P3 — Low | Backlog — revisit when capacity allows |
| <2.0 | P4 — Monitor | Document, do not act yet |

---

## Step 6: Root Cause Analysis for Negative Themes

For every P0 and P1 negative theme, conduct a structured root cause analysis before
recommending a fix.

**5-Why Analysis Template:**
```
Problem: [State the theme in one sentence]
Why 1: Why does this problem exist? → [Answer]
Why 2: Why does [Answer 1] happen? → [Answer]
Why 3: Why does [Answer 2] happen? → [Answer]
Why 4: Why does [Answer 3] happen? → [Answer]
Why 5: Why does [Answer 4] happen? → [Root cause]

Root Cause: [Single statement of the underlying cause]
```

**Fishbone Categories for Root Cause:**
When the 5-Why analysis produces ambiguous results, use the Ishikawa fishbone categories:
- **People:** Insufficient training, unclear ownership, behavior issues
- **Process:** Missing steps, unclear handoffs, inconsistent execution
- **Product:** Feature gaps, UX flaws, performance issues, bugs
- **Communication:** Poor documentation, unclear messaging, notification failures
- **Systems:** Integration failures, data quality, tooling gaps
- **Policy:** Pricing structure, contract terms, support policies

**Root Cause Output:**
For each P0/P1 theme, state:
- The root cause (one sentence)
- The category (People / Process / Product / Communication / Systems / Policy)
- Whether the fix is within the company's direct control (yes/partial/no)

---

## Step 7: Improvement Roadmap Generator

Convert prioritized themes and root causes into a structured roadmap.

**Roadmap Horizons:**

| Horizon | Timeframe | Criteria |
|---------|-----------|----------|
| Quick Wins | 0-30 days | High impact, high feasibility (P0/P1 with Feasibility ≥7) |
| Medium-Term | 31-90 days | High impact, moderate feasibility (P1/P2 with Feasibility 4-6) |
| Strategic | 91-180 days | High impact, low feasibility (P0/P1 with Feasibility ≤3) |
| Backlog | 180+ days | Lower priority themes (P3/P4) |

**Roadmap Table:**

| Initiative | Theme Addressed | Priority | Owner | Target Date | Success Metric |
|------------|----------------|----------|-------|-------------|----------------|
| [Action 1] | [Theme] | P0 | [Team] | [Date] | [KPI to measure] |
| [Action 2] | [Theme] | P1 | [Team] | [Date] | [KPI to measure] |

**Success Metrics for Each Initiative:**
Every roadmap item must have a measurable success metric tied to feedback:
- "Reduce support tickets tagged 'onboarding confusion' by 40% in 60 days"
- "Improve NPS sub-category score for 'ease of use' from -0.8 to +0.5 by next survey wave"
- "Reduce average time-to-resolution on billing issues from 6.2 days to <2 days"

---

## Step 8: Closed-Loop Feedback Process Design

A closed-loop process ensures customers know their feedback was heard and acted on.

**Four Loops:**

**Loop 1 — Inner Loop (Operational, 24-72 hours):**
- For support tickets, reviews, and real-time feedback
- Process: Receive → Tag → Respond to customer → Log in CRM → Route to owner
- Owner: Support team / CSM
- Goal: Customer receives a personal response within 48 hours of submitting feedback

**Loop 2 — Middle Loop (Tactical, monthly):**
- For NPS and CSAT batches
- Process: Collect → Analyze themes → Prioritize → Assign to roadmap → Communicate to team
- Owner: CS or Product team
- Goal: Top themes from each survey wave are reviewed in monthly planning meeting

**Loop 3 — Outer Loop (Strategic, quarterly):**
- For all feedback sources aggregated
- Process: Aggregate → Full theme analysis → Roadmap update → Stakeholder report → Customer communication
- Owner: VP Product / VP CS
- Goal: Quarterly "Here's what we heard and what we're doing" communication to all customers

**Loop 4 — Advocacy Loop (Ongoing):**
- For positive feedback
- Process: Identify promoters → Request case study / review / referral → Amplify in marketing
- Owner: CS + Marketing
- Goal: Convert top NPS scores and positive reviews into active advocacy assets

**Customer Communication Template (Outer Loop):**
```
Subject: Here's what we heard from you — and what we're doing about it

In [Quarter], we collected [N] responses from our customers.

Here's what you told us:
- [Theme 1] — We heard this from [%] of respondents
- [Theme 2] — We heard this from [%] of respondents
- [Theme 3] — We heard this from [%] of respondents

Here's what we're doing:
- [Action 1]: Launching [date]
- [Action 2]: In progress — expected [date]
- [Action 3]: On our roadmap for [quarter]

Your feedback shapes our roadmap. Thank you.

— [Company Name] Team
```

---

## Step 9: Output Format

Deliver the feedback analysis as a structured report.

---

### CUSTOMER FEEDBACK ANALYSIS: [Company / Product Name]

**Analysis Period:** [Date range]
**Total Feedback Items Analyzed:** [N]
**Sources:** [List sources]
**Prepared by:** [Analyst / Team]

---

#### Executive Summary

Two paragraphs: overall sentiment landscape, the top 3 themes by frequency and severity,
the highest-priority fix, and the most important strength to amplify. Maximum 200 words.

#### Feedback Source Summary

Table showing volume and average sentiment by source.

#### Top 10 Themes

Ranked table: theme, frequency, sentiment score, and priority tier.

#### Sentiment Landscape

Overall NPS / CSAT / sentiment averages. Trend vs. prior period if available.
Breakdown of positive, neutral, and negative by source.

#### Root Cause Analysis

5-Why or fishbone for each P0 and P1 negative theme.

#### Improvement Roadmap

Full roadmap table organized by horizon (Quick Wins / Medium-Term / Strategic / Backlog).

#### Strengths to Amplify

Top 3 positive themes with examples and recommended amplification actions
(marketing copy, case study topics, review request targeting).

#### Closed-Loop Process Design

Recommended process for each of the four loops with owners and cadence.

#### Measurement Plan

How to track whether the roadmap is working — KPIs to monitor at 30, 60, and 90 days.

---

## Important Guidelines

- Always separate frequency from severity. A low-frequency, high-severity issue can be
  more important than a high-frequency, low-severity one.
- Never present sentiment analysis as objective truth — it reflects the responding population,
  which may not represent all customers.
- Protect verbatim quotes. Never include identifiable customer names in reports
  distributed beyond the CS team without consent.
- Triangulate across sources. A theme appearing in both NPS comments and churn exit
  interviews is significantly more credible than one appearing in only one source.
- Distinguish between "loud minority" and "silent majority" — some feedback channels
  over-represent unhappy customers.
- Survey fatigue is real. Recommend no more than 2 active surveys per customer at any time.

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| customer-success-playbook | Receives the churn risk themes and NPS patterns from this skill to calibrate health scoring and intervention playbooks |
| strategic-planning-facilitator | Provides voice-of-customer data that informs SWOT weaknesses and strategic opportunities |
| operations-audit | Customer service audit area receives feedback analysis findings as evidence for scoring and gap identification |
