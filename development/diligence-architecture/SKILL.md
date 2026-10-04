---
name: Diligence Architecture
description: Build a structured due diligence workplan with workstream owners, DDQ templates, key risk checklist, and a risk-ranked issues log ready for the IC memo.
---

# Diligence Architecture

## When to use

Use this skill after completing the CIM teardown and before the first management meeting. The output is the workplan that coordinates your deal team (internal associates, external advisors, specialist consultants) across all diligence workstreams. It ensures nothing material falls through the gaps and that every risk identified in the teardown is owned by a specific workstream with a specific deliverable.

## What it does

Produces: (1) a structured diligence workplan with workstreams, owners, and key deliverables; (2) a due diligence questionnaire (DDQ) tailored to the specific business model and thesis; (3) a key-man and management risk checklist; and (4) a risk-ranked issues log template that tracks findings from first management meeting through final IC memo.

## Method

### Step 1 -- Define workstreams

A standard PE diligence architecture covers eight workstreams. Activate each based on relevance to the specific target:

**Financial and accounting diligence (FDD/QoE):** Owned by external accounting firm or in-house VP. Deliverable: Quality of Earnings report with adjusted EBITDA, normalised working capital, net debt, and covenant analysis.

**Commercial / market diligence:** Owned by external commercial diligence firm or deal team with primary research. Deliverable: market sizing, competitive landscape, customer reference findings, win/loss analysis, and growth thesis validation.

**Legal diligence:** Owned by legal counsel. Deliverable: corporate structure, material contracts, IP ownership, employment agreements, litigation history, regulatory compliance, and data privacy.

**Technology and IT diligence (for software or tech-enabled businesses):** Owned by technology advisor. Deliverable: code quality assessment, architecture review, technical debt quantification, data security posture, and SLA compliance history.

**Tax diligence:** Owned by tax advisor. Deliverable: tax structure, deferred tax positions, transfer pricing, and potential tax liabilities.

**Management and HR diligence:** Owned by deal team VP with external reference checks. Deliverable: management assessment, retention plan, key-man risk, organisational structure, and compensation benchmarking.

**Environmental, Social, and Governance (ESG):** Owned by deal team or ESG advisor. Deliverable: environmental risk flags, social compliance, governance structures, and LP ESG reporting requirements.

**Insurance and operational risk:** Owned by insurance advisor for complex assets. Deliverable: coverage gaps, claims history, and operational risk exposures.

For each activated workstream, define:
- Workstream lead (internal role or external advisor)
- Key deliverable
- Deadline (relative to signing: e.g., Day 15, Day 30, Day 45)
- Information requests outstanding

### Step 2 -- Build the DDQ

A DDQ (Due Diligence Questionnaire) is sent to management after the first meeting. Structure it by workstream. Each question should be specific, answerable with a document or data extract, and traceable to a risk identified in the teardown.

**Financial DDQ (core questions):**
- Monthly P&L for the last 3 full fiscal years and LTM, by revenue segment
- Monthly ARR or MRR bridge for the last 24 months (if SaaS or subscription)
- Full add-back schedule with supporting documentation for each item
- Customer-level revenue for the last 3 years (top 20 customers minimum)
- Working capital bridge: average, peak, and trough monthly net working capital
- Capital expenditure schedule: maintenance vs growth capex, by year
- Debt schedule and covenant compliance certificates
- Management accounts for the most recent 3 months

**Commercial DDQ (core questions):**
- Customer contract templates and any bespoke terms for top 10 customers
- Win/loss log for the last 24 months
- Pipeline report as of the most recent month end
- Churn data: customer count and revenue by cohort, by year
- Pricing history: any price increases and renewal rate changes in the last 3 years
- Competitive displacement examples: wins and losses vs specific named competitors

**Legal DDQ (core questions):**
- Corporate structure chart with ownership percentages
- Material contracts: list of all contracts above a threshold (e.g., $500K annual value)
- IP schedule: owned, licensed-in, and licensed-out; any open-source usage
- Employment agreements for all C-suite and VP-level employees
- Any litigation, regulatory action, or threatened claims in the last 5 years
- Data processing agreements and privacy compliance documentation

**Technology DDQ (for tech-enabled businesses):**
- System architecture diagram
- Third-party software dependencies and licensing
- Incident log for the last 24 months: outages, breaches, SLA misses
- Technical debt register if maintained
- Penetration test results or SOC 2 Type II report

Customise the DDQ based on the specific risk flags from the CIM teardown. Prioritise questions that bear directly on the investment thesis -- if growth is the thesis, the commercial DDQ questions are the most critical. If margin expansion is the thesis, the financial DDQ questions on cost structure are the most critical.

### Step 3 -- Key-man and management risk checklist

Evaluate management along five dimensions:

**Continuity risk:** Identify the 3-5 individuals most critical to business performance (founder-CEO, head of sales, lead engineer or product owner). For each: Is their departure survivable? What is the succession plan? Is there a retention package tied to the transaction?

**Sponsor-backed experience:** Has this team operated inside a PE-owned company before? If not, what specific gaps (financial reporting cadence, board governance, covenant compliance) might emerge post-close?

**Incentive alignment:** What equity or synthetic equity does management hold? What is the rollover plan? If management is taking significant liquidity at close, flag this as a potential misalignment risk.

**Reference quality:** Plan 3-5 external references per key executive: former employers, board members, and at least one customer or partner who has worked with them professionally. Structure reference call questions to probe: decision-making under pressure, integrity, ability to manage a PE board relationship.

**Organisational depth:** Is there a layer below the C-suite that can execute independently? In sub-$50M EBITDA businesses, key-man risk is often the single most underappreciated risk.

### Step 4 -- Issues log

The issues log is a living document maintained from first management meeting through IC memo. Structure it as:

- Issue ID (sequential number for easy reference)
- Description (one sentence)
- Workstream (financial, commercial, legal, tech, HR)
- Severity (high, medium, low -- where high = potential deal stopper)
- Status (open, resolved, monitoring)
- Resolution or mitigant
- Impact on EBITDA or valuation if unresolved

Start the log immediately after the CIM teardown with the risks identified in Step 6 of the CIM teardown skill. Update it after every management meeting, advisor call, and data room session. The IC memo's risk section is built directly from this log.

### Step 5 -- Workplan timeline

Map each workstream against the expected timeline. Standard PE diligence timelines:
- Expedited process (auction): 4-6 weeks from CIM to indicative bid, 4-6 weeks to final bid
- Bilateral process: 8-12 weeks from exclusivity to signing
- Complex carve-out: 12-16 weeks minimum

Identify the critical path -- the workstream whose completion is necessary before the IC memo can be finalised. In most transactions, this is FDD/QoE (because the adjusted EBITDA underpins the returns model) and commercial diligence (because the growth thesis underpins the exit multiple assumption).

## Inputs

- CIM teardown memo (or the CIM itself)
- Target business description and model type (SaaS, services, manufacturing, etc.)
- Anticipated deal timeline
- Names and roles of internal deal team and external advisors already engaged
- Any risks already identified from initial screening or management meetings

## Output format

Four deliverables in sequence:
1. Workstream plan (workstream name, lead, deliverable, deadline -- in a structured prose list)
2. DDQ by workstream (questions in numbered list format, grouped by workstream)
3. Management risk checklist (5 dimensions, each as a paragraph)
4. Issues log template (blank structure with column headers described in prose, with the first 3-5 entries pre-populated from the CIM teardown risks)

## Example

**Deal context:** Software-as-a-Service business, $12M EBITDA, founder-led, 24-month runway to exit, acquired in bilateral process.

**Critical path determination:** Commercial diligence is the critical path because the deal thesis rests on TAM expansion into an adjacent vertical. FDD is standard and expected to close in 3 weeks. Commercial diligence requires 6-8 customer interviews and a market sizing exercise -- it should begin at the same time as FDD, targeting completion by Day 30.

**Management risk note:** Founder-CEO holds 100% of common equity pre-close, rolling 30%. CFO was hired 14 months ago, no prior sponsor experience. Recommend: (a) 3-year retention package for CFO tied to EBITDA milestones, (b) COO hire plan within 90 days post-close as succession mitigation, (c) minimum 3 external reference calls on founder-CEO before signing.
