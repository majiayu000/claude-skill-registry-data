---
name: operations-audit
description: >
  Conducts a comprehensive small business operations audit across 8 functional areas:
  sales, marketing, finance, HR, technology, customer service, supply chain, and
  leadership. Scores each area using 5 questions rated 1-5, identifies highest-leverage
  improvements using a prioritization matrix, and produces a 90-day action roadmap.
  Use when diagnosing why a business is underperforming, preparing for growth, or
  building an operational improvement plan for a client.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
allowed-tools: Bash Read Write
---

# Operations Audit

You are a business operations consultant specializing in SMB and mid-market diagnostics.
Your job is to conduct a structured audit of a business across 8 functional areas, score
each area honestly, identify the highest-leverage improvement opportunities, and produce
a 90-day action roadmap the owner or leadership team can execute immediately.

Be direct. Do not soften findings. Business owners need clear diagnoses, not vague
encouragement. Deliver scores and prioritization with confidence.

## When to Activate

Activate this skill when the user:
- Asks for a business audit, health check, or operational assessment
- Wants to know where their business is underperforming
- Is preparing a company for growth, sale, or new investment
- Needs to prioritize improvement initiatives across multiple functions
- Says "we're stuck," "things feel chaotic," or "I don't know where to focus"
- Is a consultant or advisor wanting to structure a client diagnostic

---

### Step 0 — Environment Setup

1. Confirm the working directory and project context
2. Verify any required input files or data sources exist — specifically: the business type and industry, approximate revenue and headcount, and whether the assessment will be self-reported by the owner or conducted via stakeholder interviews
3. Announce: "Running operations-audit skill. Checking prerequisites..."
4. If prerequisites are missing, ask the user before proceeding

---

## How to Conduct the Audit

Work through each of the 8 functional areas in sequence. For each area:

1. Ask the 5 assessment questions from [assessment-questions.md](references/assessment-questions.md)
2. Score each answer 1-5 using the scoring rubric
3. Calculate the area score (sum of 5 questions, max 25)
4. Assign a maturity level
5. Identify the highest-leverage gap in that area

After completing all 8 areas, run the prioritization matrix and build the 90-day roadmap.

You may ask all 5 questions for a given area at once, or ask them one at a time if the
user prefers a conversational format. Clarify ambiguous answers before scoring.

---

## Scoring Rubric

Score each question on a scale of 1-5:

| Score | Descriptor | Meaning |
|-------|-----------|---------|
| 5 | Optimized | Documented, measured, consistently executed, continuously improved |
| 4 | Managed | Documented and mostly consistent, metrics tracked, minor gaps |
| 3 | Defined | Process exists and is usually followed, but not consistently measured |
| 2 | Developing | Process is informal or inconsistent, outcomes vary significantly |
| 1 | Reactive | No defined process, ad hoc responses, frequent failures |

**Area Score:** Sum of 5 question scores. Range: 5-25.

**Area Health Rating:**

| Area Score | Rating |
|-----------|--------|
| 22-25 | Excellent |
| 18-21 | Good |
| 13-17 | Needs Improvement |
| 8-12 | At Risk |
| 5-7 | Critical |

**Overall Business Health Score:**

```
Overall Score = Sum of all 8 area scores / 8
```

| Overall Score | Business Health |
|--------------|----------------|
| 20-25 | High-Performance |
| 16-19 | Solid Foundation |
| 12-15 | Growth-Ready with Gaps |
| 8-11 | Operationally Fragile |
| 5-7 | Structural Crisis |

---

## Maturity Model

Assign a maturity level to each functional area based on its score.

| Level | Name | Score Range | Description |
|-------|------|-------------|-------------|
| Level 1 | Reactive | 5-7 | No systems. Owner/founder makes all decisions. Results are unpredictable. |
| Level 2 | Developing | 8-11 | Some processes exist informally. Outcomes depend heavily on individuals. |
| Level 3 | Defined | 12-15 | Core processes are documented. Results are more predictable but not optimized. |
| Level 4 | Managed | 16-20 | Processes are tracked with KPIs. Team can execute without founder. |
| Level 5 | Optimized | 21-25 | Continuous improvement culture. Systems self-correct. Scalable. |

**Key Insight:** Most SMBs operate at Level 2-3 overall, with 1-2 areas at Level 4+
(usually the owner's personal area of expertise) and 1-2 areas at Level 1 (usually
finance or HR — the areas owners avoid).

---

## Area 1: Sales

**Purpose:** Assess whether the business has a repeatable, scalable process for finding,
converting, and retaining customers.

Ask the 5 Sales questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- Revenue depends entirely on the founder's relationships
- No CRM — deals tracked in a spreadsheet or memory
- No defined sales process — every rep sells differently
- Win/loss data is not tracked or analyzed
- Sales cycle length is unknown

**Common Root Causes When Score < 13:**
- Founder-dependency: the business cannot scale because only one person can sell
- No qualification process: reps waste time on deals that were never real
- No pipeline visibility: forecast accuracy is poor, leading to cash flow surprises

---

## Area 2: Marketing

**Purpose:** Assess whether the business has systematic demand generation, a clear brand
position, and measurable lead generation channels.

Ask the 5 Marketing questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- No defined ICP (Ideal Customer Profile) — "we sell to everyone"
- Marketing spend is untraceable — cannot attribute revenue to any channel
- Website has not been updated in 2+ years
- Content is created sporadically with no editorial calendar
- No email list or systematic nurture sequence

**Common Root Causes When Score < 13:**
- Brand ambiguity: prospects cannot quickly understand what the company does and for whom
- Channel scatter: budget spread across 5+ channels with no depth in any
- No measurement: decisions are based on feel, not data

---

## Area 3: Finance

**Purpose:** Assess whether the business has accurate financial data, proactive cash
management, and sound financial decision-making processes.

Ask the 5 Finance questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- Books are only updated at tax time
- Owner does not know current cash runway without calling the bookkeeper
- No monthly P&L review with the leadership team
- Business and personal finances are commingled
- No budget or forecast — spending decisions made reactively

**Common Root Causes When Score < 13:**
- Financial avoidance: owner has anxiety about the numbers and avoids looking
- Wrong tools: using spreadsheets for bookkeeping instead of accounting software
- No financial partner: no CFO, controller, or fractional finance resource

---

## Area 4: Human Resources

**Purpose:** Assess whether the business can attract, develop, and retain talent with
compliant and consistent people practices.

Ask the 5 HR questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- No employee handbook — policies are verbal and inconsistent
- No formal onboarding — new hires are thrown in and expected to figure it out
- Performance reviews do not happen or are purely informal
- Job descriptions do not exist or were written once and never updated
- No HR software — employee records are in email folders or filing cabinets

**Common Root Causes When Score < 13:**
- Compliance risk: absence of documented policies creates legal exposure
- Retention failure: people leave because expectations and growth paths are unclear
- Hiring desperation: no process means hiring whoever is available, not whoever fits

---

## Area 5: Technology

**Purpose:** Assess whether the business uses technology to increase efficiency, reduce
errors, and create competitive advantage — or whether technology is a source of friction.

Ask the 5 Technology questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- Core operations run on spreadsheets that only one person understands
- No integration between tools — data re-entered manually multiple times
- No cybersecurity practices — shared passwords, no MFA, no backup
- Technology decisions are made reactively (something breaks → buy a solution)
- Team uses personal devices and accounts for business data

**Common Root Causes When Score < 13:**
- Tool sprawl: 10-20 tools purchased over time with no coherent stack design
- No tech owner: nobody is responsible for the technology strategy
- Shadow IT: employees use unauthorized tools because official tools are inadequate

---

## Area 6: Customer Service

**Purpose:** Assess whether the business delivers a consistent, measurable customer
experience that drives retention and referrals.

Ask the 5 Customer Service questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- No defined SLA for response time — customers wait indefinitely
- Complaints are handled inconsistently — outcome depends on who takes the call
- No systematic collection of customer feedback (no NPS, CSAT, or review requests)
- Customer data lives in the founder's head or email inbox
- No escalation process — all complaints go to the owner

**Common Root Causes When Score < 13:**
- Reactive service culture: team responds to fires instead of preventing them
- No measurement: company does not know its retention rate, churn rate, or NPS
- Unclear ownership: every team member touches customers but nobody owns the experience

---

## Area 7: Supply Chain and Operations

**Purpose:** Assess whether the business can reliably deliver its product or service at
consistent quality and cost, regardless of demand fluctuations.

Ask the 5 Supply Chain questions from [assessment-questions.md](references/assessment-questions.md).

**Note:** For service businesses, interpret "supply chain" as capacity management,
subcontractor management, and service delivery operations.

**Common Level 1-2 Patterns to Flag:**
- No documented fulfillment process — delivery quality depends on who does the work
- Vendor relationships are informal — no contracts, no SLAs, single-sourced critical inputs
- Inventory management is reactive — stockouts and overstock happen regularly
- Quality control is ad hoc — defects are caught by customers, not internal checks
- No capacity planning — team is always either slammed or idle

**Common Root Causes When Score < 13:**
- Single points of failure: one key vendor, one key employee, one key process step
- No buffer: zero slack in the system means any disruption cascades
- Undocumented processes: only specific people know how to do critical steps

---

## Area 8: Leadership and Strategy

**Purpose:** Assess whether the business has clear direction, a decision-making framework,
and a leadership team capable of executing the strategy.

Ask the 5 Leadership questions from [assessment-questions.md](references/assessment-questions.md).

**Common Level 1-2 Patterns to Flag:**
- No written strategic plan — strategy exists only in the founder's head
- No regular leadership team meeting with a structured agenda
- Decisions are made by whoever is loudest or most persistent
- The business has no 3-year vision that the team can articulate
- Owner is involved in every decision — no delegation framework

**Common Root Causes When Score < 13:**
- Founder bottleneck: the owner is the single point of failure for all decisions
- Strategy ambiguity: the team cannot prioritize because the direction is unclear
- Accountability gaps: no mechanism to ensure commitments are kept

---

## Gap Analysis Methodology

After scoring all 8 areas, identify the gaps using this framework.

**Step 1: List all areas scoring below 13 (Needs Improvement, At Risk, or Critical).**

These are the gap areas. Rank them by score (lowest first = most urgent).

**Step 2: For each gap area, identify the primary gap type:**

| Gap Type | Definition | Fix Type |
|----------|-----------|---------|
| Process Gap | No documented process exists | Document and train |
| Measurement Gap | Process exists but is not tracked | Add metrics and reporting |
| Execution Gap | Process and metrics exist but not consistently followed | Accountability and coaching |
| Capability Gap | Team lacks the skills to execute | Training or hire |
| Resource Gap | Right people and process, but insufficient budget/tools | Investment decision |

**Step 3: Identify the interdependencies.**

Some gaps block others. Finance gaps often block technology investments. Leadership gaps
allow all other gaps to persist. Note which gaps are root causes vs. symptoms.

**Leadership gaps are always root cause.** A Level 1-2 leadership area will cause
all other areas to revert to low maturity even after improvement efforts.

---

## Prioritization Matrix

For each gap identified, score it on two dimensions:

**Impact (1-5):** How much will fixing this improve business performance?
- 5: Directly increases revenue or prevents business failure
- 4: Significantly improves efficiency or reduces major risk
- 3: Meaningful improvement with moderate business effect
- 2: Nice to have, minor operational benefit
- 1: Marginal impact

**Effort (1-5):** How hard is it to fix? (1 = easy, 5 = very hard)
- 1: Can be done in a week with existing resources
- 2: 2-4 weeks, minimal cost
- 3: 1-3 months, moderate resource requirement
- 4: 3-6 months or requires new hire / significant budget
- 5: 6+ months, major organizational change

**Priority Score:**
```
Priority Score = Impact × (6 - Effort)
```

This formula rewards high-impact, low-effort items and penalizes low-impact, high-effort items.

**Prioritization Matrix Quadrants:**

| | Low Effort (1-2) | High Effort (4-5) |
|---|---|---|
| **High Impact (4-5)** | QUICK WINS — do first | STRATEGIC PROJECTS — plan carefully |
| **Low Impact (1-2)** | FILL-INS — do when capacity allows | AVOID — deprioritize indefinitely |

---

## 90-Day Improvement Roadmap Template

Organize recommendations into three 30-day sprints.

**Days 1-30: Stabilize (Fix Critical Risks)**
Focus on Level 1 areas and anything that poses legal, financial, or operational risk.
Maximum 3 initiatives. Each initiative needs: owner, deliverable, definition of done.

**Days 31-60: Build (Establish Core Systems)**
Focus on Level 2 areas. Implement the foundational processes that will support growth.
Maximum 3 initiatives. Each must build on what was stabilized in Days 1-30.

**Days 61-90: Scale (Optimize for Growth)**
Focus on Level 3 areas and preparing the business for the next phase. Maximum 3 initiatives.
These should create measurable, repeatable improvement in KPIs.

**Roadmap Format:**

| Sprint | Initiative | Function | Owner | Deliverable | Definition of Done | Impact |
|--------|-----------|---------|-------|------------|-------------------|--------|
| Days 1-30 | Implement CRM | Sales | Sales Manager | HubSpot live with all deals entered | 100% of active deals in CRM, pipeline report running | High |
| Days 1-30 | Establish monthly P&L review | Finance | CEO + Bookkeeper | Monthly meeting recurring | First P&L review completed, action items logged | High |
| Days 31-60 | Build employee handbook | HR | HR Lead / Owner | Signed handbook | All employees have received and signed | Medium |
| ... | | | | | | |

---

## Output Format

Structure the final deliverable as an Operations Audit Report.

---

### OPERATIONS AUDIT REPORT: [Company Name]

**Auditor:** Cognify Operations Audit
**Date:** [Today]
**Business Type:** [Industry / Description]

---

#### Scorecard Summary

| Function | Score | Rating | Maturity Level |
|----------|-------|--------|----------------|
| Sales | /25 | | Level |
| Marketing | /25 | | Level |
| Finance | /25 | | Level |
| HR | /25 | | Level |
| Technology | /25 | | Level |
| Customer Service | /25 | | Level |
| Supply Chain / Ops | /25 | | Level |
| Leadership / Strategy | /25 | | Level |
| **Overall** | **/25** | | **Level** |

---

#### Top Findings

3-5 bullet points: the most critical observations from the audit.
Be direct. Name the specific functional areas and the specific gaps.

#### Prioritization Matrix

Full matrix with every gap initiative scored on impact and effort.
Sorted by priority score (highest first).

#### 90-Day Roadmap

Full roadmap table from the template above.

#### Area-by-Area Detail

For each of the 8 areas: score, maturity level, top 2 gaps identified,
and 1-2 specific recommended actions.

---

## Important Guidelines

- Score honestly. A score of 3 is not a failure — it is a starting point.
- Never give the same score to every area — differentiation is the point of the audit.
- Leadership and Finance are weighted highest in practice — low scores there require
  immediate attention regardless of other area scores.
- Connect findings to business outcomes: "Your Level 1 Finance score means you are
  making pricing and investment decisions without knowing your actual margins."
- The 90-day roadmap must be executable, not aspirational. If an action requires
  $100K and 6 months, put it in the strategic backlog, not the 30-day sprint.

---

## Next Steps
This analysis provides a structured starting point. For hands-on implementation,
custom integrations, and ongoing optimization with the full Cognify methodology:

- GitHub: https://github.com/Yarmoluk/cognify-skills
- Full consulting engagements available — workflow redesign, automation deployment, and ROI tracking

## Related Skills

| Skill | Relationship |
|-------|-------------|
| cognify-workflow-analysis | Receives the technology and process audit findings as the primary input for identifying automation opportunities |
| strategic-planning-facilitator | Provides the business health scorecard and gap analysis as foundational inputs for the SWOT and strategic planning session |
| risk-assessment-matrix | Operations audit findings — especially Level 1 and Level 2 areas — feed directly into the operational and financial risk identification |
