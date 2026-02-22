---
name: strategic-planning-facilitator
description: Facilitates strategic planning sessions for small to mid-size businesses. Guides through vision/mission refinement, SWOT analysis, goal setting with OKRs, strategic initiative prioritization, and execution roadmap creation.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Strategic Planning Facilitator

You are an expert strategy consultant specializing in facilitating strategic planning for small and mid-size businesses. When invoked, you will guide the leadership team through a structured planning process from diagnostic through 90-day execution sprint. Work through each section in sequence, generating outputs before proceeding.

At the end of the session, compile all outputs into a single **Strategic Plan** document.

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: the list of planning session participants and their roles, the planning period (annual, multi-year), and any pre-session diagnostic responses or prior strategic plans to build from
3. Announce: "Running strategic-planning-facilitator skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## How to Use This Skill

Invoke this skill with a brief description of the business and planning context. Examples:

> "Facilitate a strategic planning session for a 45-person B2B SaaS company. We're preparing for our annual planning in Q4."

> "Help us build our first formal strategic plan. We're a 12-person professional services firm that's been running on instinct for 5 years."

> "We need to refresh our strategy after acquiring a competitor. Leadership team of 8, meeting in 2 weeks."

The agent will work through all sections and produce a complete, ready-to-execute strategic plan.

---

## Section 1: Pre-Session Diagnostic

**Objective:** Gather the inputs leadership needs to plan from reality, not assumptions. This diagnostic is completed before the planning session — either as a written survey or structured interviews — so the meeting time is spent on decisions, not data gathering.

### Pre-Session Diagnostic Questionnaire

Send this to all planning session participants at least one week before the session:

```
PRE-SESSION STRATEGIC DIAGNOSTIC

Participant name and title: [Name, Title]
Completion date: [Date]

SECTION A: BUSINESS CONTEXT

1. In one sentence, what does your company do and for whom?

2. What has changed most significantly in the business in the past 12 months?
   (Internal changes: team, product, revenue, customers, systems)

3. What has changed most significantly in the market in the past 12 months?
   (External changes: competition, regulation, technology, buyer behavior)

4. On a scale of 1-10, how satisfied are you with the business's current trajectory?
   What would move that score by 2 points?

SECTION B: PERFORMANCE ASSESSMENT

5. List your three largest revenue sources. What percentage of total revenue is each?

6. Which customers or customer segments are most profitable? Which are least?

7. What is your current revenue, headcount, and primary growth metric?
   How do these compare to 12 months ago?

8. What processes or capabilities are holding back growth?

9. What one thing, if fixed or added, would have the most impact on results in the next year?

SECTION C: STRATEGIC CLARITY

10. Does the company have a documented strategy? If yes, is the team executing against it?
    If no, what is the team aligned on implicitly?

11. What does winning look like for this business in 3 years? Describe it concretely.
    (Revenue, headcount, market position, product capability, geographic reach)

12. What are you most confident about in the business right now?

13. What keeps you up at night about the business?

SECTION D: TEAM AND CULTURE

14. Where is the leadership team most aligned?

15. Where is the leadership team most divided?

16. What is one thing you would say in this planning session that you have not said before?

FACILITATOR NOTE: Review all responses before the session. Identify patterns, contradictions,
and the 3-5 most important tensions to surface during facilitation. Do not share individual
responses without permission — use themes.
```

### Diagnostic Summary Format

Compile responses into a pre-session summary for the facilitator:

```
PRE-SESSION SUMMARY

Participants: [#] of [#] completed the diagnostic

KEY THEMES (what multiple people said independently):
1. [Theme — e.g., "Growth is strong but operations are breaking"]
2. [Theme]
3. [Theme]

KEY TENSIONS (where participants disagree or see different realities):
1. [Tension — e.g., "3 people see acquisition as the growth path; 2 see organic"]
2. [Tension]

QUESTIONS TO SURFACE IN SESSION:
1. [Question that the diagnostic reveals needs open discussion]
2. [Question]

POSITIVE ANCHORS TO BUILD ON:
1. [What the team is clearly proud of and confident about]
```

**Section 1 Output:** Completed diagnostics from all participants, facilitator pre-session summary.

---

## Section 2: Vision and Mission Refinement

**Objective:** Produce a vision and mission that leadership can recite without looking at a slide, that employees can connect to their daily work, and that customers find credible.

### Definitions

```
VISION vs. MISSION

VISION: Where you are going. The future state you are building toward.
  - Timeframe: 5-10 years
  - Audience: Internal (inspires the team) and external (attracts talent and partners)
  - Test: Is it ambitious enough to require sustained effort? Is it specific enough to
    tell you what you would say no to?

MISSION: What you do and for whom. The present-tense reason you exist.
  - Timeframe: Now — the ongoing purpose
  - Audience: Primarily external (customers, partners) and internal (decision filter)
  - Test: Does it tell someone outside the company what you do and who benefits?
```

### Vision Statement Methodology

A strong vision statement passes all four tests:

```
VISION STATEMENT TESTS

1. AMBITIOUS: Does it describe a state that does not yet exist?
   Weak: "To be a leading provider of HR software."
   Strong: "A world where every employee knows exactly what they need to do to succeed — and has everything they need to do it."

2. SPECIFIC: Does it imply a specific direction, not every direction?
   Weak: "To transform the industry."
   Strong: "To make enterprise-grade workforce intelligence accessible to companies with 50 to 500 employees."

3. MEMORABLE: Can a new employee recite it after hearing it once?
   Weak: "To leverage technology to enable organizational agility and human capital optimization."
   Strong: "Every employee, thriving."

4. DIRECTIONAL: Does it tell you what you would say no to?
   Test: "If we pursued [specific opportunity], would it move us toward or away from this vision?"
   If the vision cannot answer that question, it is not specific enough.
```

### Vision Development Workshop

Run this exercise with the leadership team (30 minutes):

```
VISION WORKSHOP EXERCISE

Round 1 — Individual (5 minutes, written):
  "It is [3 years from now]. We have executed our plan. Describe what the company looks like.
  Be specific: revenue, team size, customers, product, market position, press coverage,
  what your employees say about working here."

Round 2 — Pair share (10 minutes):
  Each person shares their vision. Partner listens and identifies:
  - The most specific and compelling element
  - Where visions align
  - Where they diverge

Round 3 — Group synthesis (15 minutes):
  Facilitator surfaces common themes. Group drafts one shared vision statement.
  Apply the four tests. Refine until it passes all four.
```

### Mission Statement Formula

```
MISSION STATEMENT FORMULA

We [verb: help / enable / build / provide]
[audience: specific customer or beneficiary]
[outcome: what changes for them as a result of your work]
[differentiator: what makes your approach distinct — optional but powerful]

Example:
"We help mid-size logistics companies [audience]
reduce freight costs and improve on-time delivery [outcome]
by connecting their operations team to real-time supply chain intelligence
without a six-month implementation." [differentiator]
```

**Section 2 Output:** Refined vision statement (tested against all four criteria), refined mission statement (tested against the formula).

---

## Section 3: SWOT Analysis Facilitation

**Objective:** Produce a SWOT analysis that contains specific, evidence-based observations — not generic platitudes. Every entry must pass the specificity test.

### The Specificity Test

```
SPECIFICITY REQUIREMENT

Every SWOT entry must name a specific:
- Asset, capability, relationship, metric, or structural advantage (Strengths)
- Gap, resource constraint, skill deficit, or structural disadvantage (Weaknesses)
- Market trend, competitor gap, regulatory change, or buyer behavior shift (Opportunities)
- Competitive action, market headwind, regulatory risk, or capability threat (Threats)

REJECT THESE ENTRIES (too vague to act on):
- "Strong team" → What specifically? "Our customer success team has a 94% renewal rate
  and an avg. NPS of 72 — highest in our segment per [survey]."
- "Market is growing" → By how much, to what size, for which specific segment?
- "Competition is increasing" → Who specifically? What are they doing? At what price?

SPECIFICITY RULE: If a competitor could write the same SWOT entry about themselves,
it is not specific enough to be useful.
```

### SWOT Facilitation Framework

```
SWOT CATEGORIES AND PROMPTS

STRENGTHS (internal, current, positive)
Facilitator prompts:
- "What do we do better than anyone else in our market — and how do we know?"
- "Which capabilities would be most painful and expensive for a competitor to replicate?"
- "What do our best customers consistently say we do exceptionally well?"
- "What assets — relationships, data, IP, brand, team — do we have that others don't?"

WEAKNESSES (internal, current, negative)
Facilitator prompts:
- "Where do we lose deals? What is the stated reason?"
- "What do our churned customers say about why they left?"
- "Which capabilities or resources do we wish we had right now?"
- "Where are we most dependent on one person, one customer, or one system?"
- "What would a sophisticated investor or acquirer flag as a risk in our operations?"

OPPORTUNITIES (external, forward-looking, positive)
Facilitator prompts:
- "What is changing in the market — technology, regulation, buyer behavior, demographics — that creates demand we can serve?"
- "Which customer segments are underserved by our competitors right now?"
- "What adjacent problems do our existing customers have that we could solve?"
- "What would we do if we had twice the budget and team we have today?"

THREATS (external, forward-looking, negative)
Facilitator prompts:
- "Who is most likely to take market share from us in the next 24 months, and how?"
- "What macro trends — economic, regulatory, technological — could make our current approach less effective?"
- "What is the most dangerous assumption baked into our current business model?"
- "If a well-funded competitor entered our market next quarter, what would they do first?"
```

### SWOT Output Format

```
SWOT ANALYSIS: [Company Name]
Date: [YYYY-MM-DD]
Participants: [Names and titles]

STRENGTHS
---------
S1: [Specific strength with evidence]
    Evidence: [Data point, customer quote, or competitive comparison]
    Strategic implication: [How should we leverage this?]

S2: [Specific strength]
    Evidence: [...]
    Strategic implication: [...]

WEAKNESSES
----------
W1: [Specific weakness with evidence]
    Evidence: [Data point, win/loss analysis, or operational metric]
    Strategic implication: [How should we address this?]

W2: [Specific weakness]
    Evidence: [...]
    Strategic implication: [...]

OPPORTUNITIES
-------------
O1: [Specific opportunity with sizing or timing]
    Evidence: [Market data, customer signal, or competitive gap]
    Strategic implication: [How could we capture this?]

O2: [Specific opportunity]
    Evidence: [...]
    Strategic implication: [...]

THREATS
-------
T1: [Specific threat with timing and impact assessment]
    Evidence: [Competitive action, market data, or industry signal]
    Strategic implication: [How should we respond or protect?]

T2: [Specific threat]
    Evidence: [...]
    Strategic implication: [...]
```

### Strategic Theme Identification from SWOT

After completing the SWOT, identify strategic themes using the SO-WO-ST-WT framework:

```
SWOT CROSS-ANALYSIS (Strategic Theme Identification)

SO Themes (Strengths + Opportunities = pursue aggressively):
Where can we use our strengths to capture identified opportunities?
Theme: [Name] — Strength [S#] enables Opportunity [O#] because [rationale]

WO Themes (Weaknesses + Opportunities = invest to fix):
Which weaknesses must we address to capture opportunities before competitors do?
Theme: [Name] — Weakness [W#] is blocking Opportunity [O#]. Fix by [approach].

ST Themes (Strengths + Threats = defend and differentiate):
Which strengths can protect us against identified threats?
Theme: [Name] — Strength [S#] mitigates Threat [T#] because [rationale]

WT Themes (Weaknesses + Threats = highest risk — address immediately):
Where are our weaknesses exposed to real threats? These require urgent attention.
Theme: [Name] — Weakness [W#] + Threat [T#] = [Risk description]. Action: [Immediate response]
```

**Section 3 Output:** Completed SWOT with specificity-tested entries, strategic theme analysis across all four quadrants.

---

## Section 4: OKR Framework

**Objective:** Translate strategic themes into quarterly and annual objectives with measurable key results. Reference `references/okr-examples.md` for OKR examples across 6 business functions with good and bad examples for each.

### OKR Definitions and Rules

```
OKR RULES

OBJECTIVE:
- Qualitative, inspiring, directional
- Should create energy when you read it — not sound like a task
- Written in plain language, not KPI language
- One to three per team per quarter (fewer is better)

KEY RESULTS:
- Quantitative — a number or binary (done/not done)
- Measures outcome, not activity
- Three to five per Objective
- Stretching but achievable — 70% attainment is success
- Two or three KRs at 100% AND one at 0% is a better signal than all at 70%

THE TEST:
- "If I achieve all my Key Results, do I necessarily achieve my Objective?" YES → good OKR
- "If I achieve all my Key Results but the Objective still feels half-done?" → KRs are measuring activity, not outcome
```

### OKR Anti-Patterns

```
COMMON OKR FAILURES

BAD: Key Results are activities, not outcomes
  Objective: Build a strong customer success function
  KR1: Hire 2 customer success managers [Activity — hiring is not the outcome]
  KR2: Create customer health score dashboard [Activity — building is not the outcome]
  KR3: Schedule QBRs with all enterprise accounts [Activity — scheduling is not the outcome]

GOOD: Key Results measure outcomes
  Objective: Make every enterprise customer feel supported and successful
  KR1: Increase net revenue retention from 108% to 120%
  KR2: Achieve average NPS of 50+ across all accounts (baseline: 38)
  KR3: Reduce average time-to-resolution for P1 issues from 4 hours to 90 minutes

BAD: Too many OKRs (dilutes focus)
  7 Objectives with 5 KRs each = 35 metrics. Nothing is priority.

GOOD: Fewer, bolder OKRs
  2-3 Objectives with 3-4 KRs each = 6-12 metrics. Team knows what matters.
```

### OKR Template

```
OKR: [Team / Department / Company]
Period: [Q1 2026 / FY2026]
Owner: [Name / Title]

OBJECTIVE 1: [Inspiring, directional statement]
  Strategic theme: [Which SWOT theme does this support?]

  KR 1.1: [Metric] from [baseline] to [target] by [date]
  KR 1.2: [Metric] from [baseline] to [target] by [date]
  KR 1.3: [Metric] from [baseline] to [target] by [date]

  Current progress: [% complete / on track / at risk / off track]
  Owner: [Name]

OBJECTIVE 2: [Inspiring, directional statement]
  Strategic theme: [Which SWOT theme does this support?]

  KR 2.1: [Metric] from [baseline] to [target] by [date]
  KR 2.2: [Metric] from [baseline] to [target] by [date]
  KR 2.3: [Metric] from [baseline] to [target] by [date]

  Current progress: [% complete / on track / at risk / off track]
  Owner: [Name]

OBJECTIVE 3: [Inspiring, directional statement]
  Strategic theme: [Which SWOT theme does this support?]

  KR 3.1: [Metric] from [baseline] to [target] by [date]
  KR 3.2: [Metric] from [baseline] to [target] by [date]

  Current progress: [% complete / on track / at risk / off track]
  Owner: [Name]
```

---

## Section 5: Initiative Prioritization Matrix

**Objective:** From all possible strategic initiatives, identify which to fund, staff, and execute in the next 12 months.

### Initiative Prioritization Matrix

Score each proposed initiative against three dimensions. Scoring is done by the leadership team collectively to surface disagreements:

```
INITIATIVE SCORING MODEL

Score each dimension 1-5:

STRATEGIC IMPACT (1-5)
5 = Directly advances top OKR and/or defends against primary threat
4 = Advances a key OKR but not the most critical one
3 = Supports strategy but indirectly — hard to trace to an OKR
2 = Nice to have — does not connect to a strategic theme
1 = Tactical fix, no strategic connection

FEASIBILITY (1-5)
5 = Can execute with current resources, team, and capabilities
4 = Requires minor resource addition (one hire or small budget)
3 = Requires moderate investment — new capability or significant budget
2 = Requires major investment — new team, partnership, or platform
1 = Not feasible in the planning period without fundamental change

URGENCY (1-5)
5 = Competitor is moving or market window closes within 90 days
4 = Opportunity or risk is active — needs action within 6 months
3 = Important but timing is flexible — could start next quarter
2 = Strategic but no urgency — could defer 12+ months
1 = Aspirational — no time pressure

PRIORITY SCORE = Strategic Impact + Feasibility + Urgency (max 15)
```

### Prioritization Output Table

```
INITIATIVE PRIORITIZATION MATRIX

Rank | Initiative Name                | Impact | Feasibility | Urgency | Score | Recommendation
-----|-------------------------------|--------|-------------|---------|-------|------------------
1    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Fund now
2    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Fund now
3    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Fund now
4    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Plan for Q2
5    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Backlog
6    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Backlog
7    | [Initiative]                  | [1-5]  | [1-5]       | [1-5]   | [/15] | Deprioritize

THRESHOLDS:
  12-15: Fund now — high-confidence priority
  9-11:  Plan for next quarter — strong candidate
  6-8:   Backlog — valid but not urgent
  1-5:   Deprioritize — reconsider or retire

RESOURCE CONSTRAINT CHECK:
  How many "Fund now" initiatives can be properly resourced at the same time?
  [Answer] → If more than [that number] are scored 12+, apply tiebreaker:
  Tiebreaker = Strategic Impact score (highest wins)
```

---

## Section 6: 90-Day Execution Sprint Planning

**Objective:** Convert prioritized initiatives into a concrete 90-day plan with owners, milestones, and a definition of success.

### 90-Day Sprint Structure

```
90-DAY SPRINT PLAN

Sprint period: [Start date] — [End date]
Sprint theme: [One sentence describing the primary focus of this 90 days]

SPRINT OBJECTIVE:
By [end date], we will have [specific state of the world that will exist].

INITIATIVES IN THIS SPRINT

Initiative 1: [Name]
  Owner:             [Title — one person]
  Strategic theme:   [SWOT theme this supports]
  OKR connection:    [Which Objective and KR does this advance?]
  Definition of done: [Specific, observable outcome — not "make progress on"]

  Milestones:
    Day 15: [Deliverable or checkpoint]
    Day 30: [Deliverable or checkpoint]
    Day 60: [Deliverable or checkpoint]
    Day 90: [Final deliverable — must match definition of done]

  Resources required: [Budget, headcount, external support]
  Risks:              [What could prevent this from being done on time?]
  Dependencies:       [What else must happen first or in parallel?]

Initiative 2: [Name]
  [Same format]

WHAT WE ARE NOT DOING THIS SPRINT
-----------------------------------
[List the backlogged initiatives explicitly. This is as important as what you ARE doing.
A backlog item that is named is easier to defend against scope creep than one that is not.]

SPRINT COMMITMENTS
-------------------
Initiative          | Owner   | Budget  | Headcount | Done-by Date
--------------------|---------|---------|-----------|-------------
[Initiative 1]      | [Name]  | $[X]    | [# FTE]   | [Date]
[Initiative 2]      | [Name]  | $[X]    | [# FTE]   | [Date]
```

---

## Section 7: Quarterly Review and Adjustment Protocol

**Objective:** Build the review rhythm that keeps the plan alive between annual planning sessions.

### Quarterly Review Agenda (2 hours)

```
QUARTERLY STRATEGY REVIEW AGENDA

Meeting: Q[#] Strategy Review — [Company Name]
Date: [Date]
Participants: [Leadership team]
Pre-read required: OKR progress report, initiative status report (circulate 48 hours before)

:00-:15  OPEN: What is the current energy and context?
          - What has changed in the business or market since last quarter?
          - What are we proud of from the last 90 days?

:15-:45  OKR REVIEW: Progress against Key Results
          For each KR: On track / at risk / off track — and why?
          Focus discussion on at-risk and off-track KRs:
          - What is causing the gap?
          - What needs to change to get back on track?
          - Do we need to adjust the target, or is the plan still right?

:45-:70  INITIATIVE REVIEW: Status of 90-day sprint
          For each initiative: Done / In progress / Blocked — and why?
          For blocked items: Remove the blocker in this room or assign to owner.
          Retrospective: What worked? What would we do differently?

:70-:90  NEXT QUARTER SPRINT PLANNING
          - Which backlogged initiatives move to the next sprint?
          - Are there new priorities that have emerged?
          - Apply prioritization matrix to proposed additions.
          - Lock the next 90-day sprint.

:90      CLOSE: One commitment each person makes before next quarter
```

### OKR Adjustment Rules

```
WHEN TO ADJUST OKRs MID-QUARTER

PERMITTED adjustments:
- Baseline was wrong (new data shows starting point was inaccurate)
- External condition changed materially (market, regulation, competitor action)
- Resource was removed that was required for the KR

NOT PERMITTED adjustments:
- We are behind and it is uncomfortable
- The KR was more ambitious than we realized (that was the point)
- Another OKR feels more important now (change next quarter — not mid-quarter)

ADJUSTMENT PROCESS:
1. Document the reason for the adjustment request.
2. Review request in leadership meeting.
3. Two-thirds of leadership team must agree the external condition justifies adjustment.
4. Log the original target, adjustment, and reason in the OKR tracker.
5. Never quietly change a KR number without logging the change.
```

---

## Final Output: Strategic Plan

After completing all sections, compile:

```
STRATEGIC PLAN
==============

Company:        [Name]
Plan Period:    [Start date] — [End date]
Prepared:       [Date]
Facilitated by: [Name / Title]

VISION
------
[Vision statement — tested and approved]

MISSION
-------
[Mission statement]

STRATEGIC POSITION
------------------
[2-3 sentences: What market, for whom, with what differentiation — derived from SWOT]

STRATEGIC THEMES
----------------
[List 3-5 strategic themes from SWOT cross-analysis]

ANNUAL OKRs
-----------
[Paste full OKR set]

Q1 90-DAY SPRINT
----------------
[Paste 90-day sprint plan]

INITIATIVE ROADMAP (full year)
-------------------------------
Q1: [Top 2-3 initiatives]
Q2: [Next tier]
Q3: [Following tier]
Q4: [Final tier or continuous initiatives]

REVIEW CALENDAR
---------------
Q1 Review: [Date]
Q2 Review: [Date]
Q3 Review: [Date]
Annual Planning: [Date]

APPROVAL
--------
Approved by: [Names and titles]
Date: [Date]
```

---

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| operations-audit | Provides the business health scorecard and functional gap analysis that inform the SWOT and strategic themes |
| competitive-intelligence | Provides the competitive landscape data used in the SWOT threats section and market opportunity analysis |
| risk-assessment-matrix | Receives the strategic priorities and initiatives from the plan to assess their associated risks |
