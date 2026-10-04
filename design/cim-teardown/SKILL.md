---
name: CIM Teardown
description: Systematic extraction and critical analysis of a Confidential Information Memorandum, identifying deal thesis, EBITDA bridge, management assertions, and the questions every diligence workstream must answer.
---

# CIM Teardown

## When to use

Use this skill after you have received a full CIM from a sell-side advisor and before you have convened the internal deal team for the first time. The teardown converts a 60-120 page marketing document into a structured analytical brief: what is the seller claiming, what is verifiable, what is optimistic, and what must be stress-tested in diligence. It is the starting document for your DDQ and your diligence architecture.

## What it does

Produces a CIM teardown memo covering: deal overview, stated investment thesis (in the seller's own terms), business model decomposition, financial analysis with EBITDA bridge reconstruction, management claim tracker, identified risks, and an ordered list of diligence priorities. The output is designed to be shared directly with deal team members as their briefing document for management meetings and workstream kickoffs.

## Method

### Step 1 -- Deal overview extraction

Pull the following from the CIM without interpretation:
- Business description (one paragraph, seller's own words)
- Founded, HQ, number of employees
- Products or services offered
- Customer segments served
- Geographies of operation
- Ownership structure and process type (proprietary sale, auction, carve-out, secondary buyout)
- Stated financials: revenue, EBITDA, growth rates for the last 2-3 years and forward projections
- Stated entry valuation range or process parameters

Do not rephrase or editorialize at this stage. Accuracy of extraction matters more than elegance.

### Step 2 -- Stated investment thesis

Identify the 3-5 core thesis pillars the CIM is built around. Common CIM thesis structures include:
- Large and growing TAM with low penetration
- Mission-critical product with high switching costs
- Proven management team with M&A track record
- Multiple expansion potential (re-rating from services to software multiple)
- Platform for consolidation in a fragmented market
- Margin expansion through operational leverage or pricing power

For each pillar: (a) state the seller's claim verbatim or near-verbatim, (b) note whether it is supported by data in the CIM or is an assertion, and (c) assign a confidence level (high / medium / low) based on the evidence presented.

### Step 3 -- Business model decomposition

Break the revenue model into its components:
- Revenue streams: list each distinct revenue line, its approximate contribution to total revenue, and its growth rate
- Pricing model: per-seat, usage-based, project-based, recurring subscription, or mixed
- Go-to-market: direct sales, channel partners, inbound, field sales -- and the cost structure of each
- Revenue recognition: when and how revenue is recognised (particularly important for software, long-term contracts, or milestone-based services)
- Renewal and churn: stated gross and net retention rates; if not stated, flag as a critical diligence question

Identify the one or two revenue lines that drive the majority of growth and margin. These are the diligence focus areas.

### Step 4 -- EBITDA bridge reconstruction

Reconstruct the seller's EBITDA path from revenue to EBITDA margin:
- Start with reported revenue
- Identify gross margin (stated or implied by cost of goods sold)
- Identify operating expense structure: S&M, R&D, G&A as % of revenue
- Arrive at stated EBITDA and margin
- List all stated add-backs and their descriptions
- Categorise each add-back as: (a) clearly one-time and legitimate, (b) recurring but reclassified, or (c) requires QoE scrutiny

Apply a preliminary Quality of Earnings (QoE) frame: list the 3-5 add-backs or normalisation items that are most likely to be challenged by your accounting diligence team, and estimate the potential EBITDA impact if they are rejected or haircut.

Flag if reported EBITDA and cash-on-cash conversion diverge significantly -- this often indicates working capital traps, deferred revenue burn, or elevated maintenance capex not visible in the headline EBITDA.

### Step 5 -- Management assertions tracker

Create a two-column tracker: Claim | Evidence Provided. Walk through each section of the CIM and extract every quantified or qualified assertion management is making about the business. Examples:

- "NRR of 112% over the last 3 years" -- supported by a chart / not supported / supported only for one year
- "Market growing at 18% CAGR" -- cite (Gartner, internal estimate, unnamed source?)
- "No customer represents more than 10% of revenue" -- exact figure in financials / stated but no breakdown
- "Management team has delivered 3x MOIC on prior PE-backed exits" -- names and transaction listed / assertion only

This tracker becomes the backbone of your DDQ.

### Step 6 -- Risk identification

Using the CIM as the primary source, identify risks across three categories:

**Risks the CIM acknowledges (disclosed risks):** Competition, regulatory, customer concentration, dependence on key personnel. Note how the CIM characterises each and whether the mitigation described is credible.

**Risks the CIM downplays or omits (implicit risks):** Look for: rapid revenue growth without corresponding margin improvement (suggests scaling investment not fully captured in EBITDA), high add-back density, limited customer reference data, vague forward projections without a bottoms-up build, or absence of segment-level disclosure.

**Structural risks:** Carve-out complexity (stranded costs, TSA dependencies), secondary buyout (prior sponsor already extracted easy value), or management rollover terms not yet agreed.

### Step 7 -- Diligence priority list

Based on Steps 2-6, produce an ordered list of the top 10 diligence questions that must be answered before the IC memo is written. Format each question as:

- Question (one sentence)
- Workstream owner (financial, commercial, legal, technical/IT, management reference)
- Data required to answer it
- Risk if unanswered

Prioritise by: (a) questions that could cause a pass decision if answered negatively, and (b) questions where the CIM's evidence is weakest.

## Inputs

- Full CIM document text (paste the executive summary and key sections, or upload the document)
- Fund sector and return parameters (so the analyst can calibrate what "good" looks like)
- Any initial screening note or deal summary already prepared (to avoid duplication)

## Output format

A CIM teardown memo with seven sections:
1. Deal overview (structured bullets)
2. Stated investment thesis (pillar-by-pillar with confidence rating)
3. Business model decomposition (revenue stream breakdown as prose)
4. EBITDA bridge reconstruction (bridge as prose, add-back analysis as bullet list)
5. Management assertions tracker (claim / evidence / gap columns described as prose)
6. Risk identification (three categories, bullets per risk)
7. Diligence priority list (10 items, each with workstream, data needed, risk)

Total length: 900-1,400 words. Designed to be read in 10 minutes by a senior deal partner.

## Example

**Input excerpt from CIM:** "The company has achieved 95% gross revenue retention over the last three years, with net revenue retention of 114% driven by strong upsell performance. Management attributes this to the platform's deep integration with customers' ERP systems."

**Teardown output (assertions tracker entry):**
- Claim: GRR 95%, NRR 114% over 3 years.
- Evidence provided: Single chart covering 2022-2024; no cohort-level breakdown; upsell contribution to NRR not separately quantified.
- Diligence gap: Confirm by customer cohort -- is NRR driven by a small number of large upsells, or is it broad-based? Request monthly retention data by cohort, not annual average. Verify ERP integration depth with 3 customer reference calls.
