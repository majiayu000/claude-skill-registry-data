---
name: research-business-analysis
description: How to do research for benchmarking, financial and economic modeling, and other business analysis tasks.
---

# Skill

These are basic principles for conducting research for financial and economic modeling, benchmarking, and other business-analysis information-gathering tasks.


## Definition of modeling

A model is a simplified representation of a real-world (business) process, developed to solve a specific business problem and support a decision.

Key success factors:

- Clearly define the problem and success criteria.
- Choose the right level of simplification: not too simple to miss required precision; not so complex that it becomes overkill.


## Core modeling principles

Consider the following:

- MECE (Mutually Exclusive, Collectively Exhaustive): ensure categories do not overlap (exclusive) and cover all possibilities (exhaustive). Use MECE to eliminate double-counting and ensure no gaps in the analysis.
- SISO a.k.a. GIGO (Garbage In, Garbage Out): model output quality is bounded by input quality.
- Time sensitivity: facts are time-dependent. Example: in 2025, using a 2023 forecast as a “fact” is usually wrong unless explicitly treated as a forecast.


## Generic model structure

1. Inputs
   - Historical data: a digital representation of the real-world business process.
   - Assumptions (by scenario): educated guesses about how the business process may behave in the future.
2. Business logic: mathematical formulas based on the chosen methodology.
3. Outputs


## Modeling process

1. Plan the model
   - Identify the problem the model is intended to solve and the decision it will support.
   - Form hypotheses to test.
   - Define criteria (e.g., thresholds).
   - Define scope (e.g., geography, segments, timeframes), requirements (e.g., precision), and constraints (e.g., exclude re-export flows; include only maritime transport because it dominates).
   - Select a methodology/approach/framework. Prefer simpler approaches that meet requirements.
   - Design the model structure.
   - Identify required data.
   - Identify data sources.

2. Build the model
   - Gather data.
   - Prepare data.
   - Assess input data quality.
   - Build the business logic.
   - Generate outputs.

3. Use the model
   - Quality-control the outputs.
   - Test the hypotheses.
   - Answer the question.
   - Provide options or recommendations for the decision.
   - Communicate outcomes in an actionable format.


### 1. Plan the model

Convert the business problem into research questions (variables). Turn vague symptoms into testable hypotheses and measurable variables. Example pattern: “Sales not growing” → market growth? share loss? distribution? awareness? pricing? category saturation?

Avoid cherry-picking by design. Explore opposing views.


### 2. Build the model

As a research AI agent, your scope typically sits in the Build step (gathering and preparing data, and assessing data quality). Ensure you understand all items from the Plan step and align your work to them.


#### Gather data

For each source, assess:

- Authority: who produced it; incentives/conflicts.
- Methodology: definitions, sampling, coverage, collection method.
- Time: publication date, “as-of” date, period covered, revision history.
- Granularity: geography, segment, currency, unit (nominal/real).
- Consistency: does it reconcile with other sources? if not, why?

Data sources by reputability (descending):
1. Data provided by the client (if credible and internally consistent).
2. Public audited financial reporting.
3. Official government statistics.
4. Specialized analytics agencies (e.g., Argus, Platts for commodities).
5. General research agencies and statistics aggregators.
6. Business consulting firms.
7. Public media (press releases, expert interviews).
8. Expert interviews conducted by a business analyst.
9. Data collected by a business analyst via observation (e.g., 1–5 events).

Prefer primary sources. Example: if you find a consulting outlook, follow its references to the underlying primary sources and use those.

Assumptions by credibility (descending):
1. Forecasts from specialized analytics agencies.
2. Official government economic scenarios.
3. Inertial forecasts based on market dynamics.
4. Benchmarks (historical, cross-country) and proxies.
5. Expert opinions.
6. Forecasts from consulting firms.
7. Forecasts from companies in the sector.
8. Educated guesses.

While collecting data:
1. Use at least two independent sources and explain discrepancies (scope, units, timeframe, methodology, etc.).

2. Use triangulation:
   - Top-down (e.g., macro totals → segment shares).
   - Bottom-up (e.g., units × price × adoption).
   - Value theory (e.g., spend per user × number of users).

3. State ranges explicitly when applicable (e.g., 5–10%).

4. Address potential biases in data and assumptions:
   - Client-provided data may contain manipulation if not properly audited (e.g., “adjusted” KPIs).
   - Audited reporting can still be managed; trends may differ between IFRS and local standards (e.g., RAS).
   - Government data may reflect political incentives.
   - Specialized agencies can diverge due to methodology differences.
   - Generic aggregators may oversimplify or contain methodological errors.
   - Experts may be too conservative or too optimistic.
   - Consultants may cherry-pick to support commercial narratives.
   - Company forecasts may be optimized for investors or customers.

#### Prepare data

##### Assess data quality

###### Technical criteria

1. Completeness: data covers:
   - The full period.
   - All companies in the group/holding.
   - All items in scope (e.g., SKUs, segments).
   - Other context-specific requirements.

2. Accuracy: required analytical breakdowns are available in the extraction/report.

3. Integrity/consistency: data points can be linked unambiguously via identifiers, e.g.:
   - Business unit.
   - Company code (since company names may vary).
   - SKU code.

4. Clarity of values: meanings of all variables and fields are clear.

Based on this, estimate data reliability.

###### Business criteria

1. Correctness: how precisely the data reflects real business events (amounts, quantities).
2. Timeliness: how promptly events are recorded in the database.
3. Objectivity: independence from subjective judgment (e.g., experts, stakeholders, managers, business users).

Based on this, estimate data credibility.

##### Make the data suitable for analysis

1. Make figures comparable:
   - Units (including domain-specific units).
   - Scale (thousand/million/billion, etc.).
   - Currency.
   - Timeframe (calendar vs fiscal year).
   - Accounting standard.
   - Actual vs estimate vs forecast.
   - Inclusion/exclusion rules.
   - Nominal vs real prices.
   - For ranges: choose average or median based on methodology/context.

Log all conversions and state all coefficients used (e.g., FX rates, inflation assumptions).

2. Handle outliers.

3. Follow the “tidy data” principle:
   - Each observational unit forms a table.
   - Each variable forms a column.
   - Each observation forms a row.
   - No data in column names (e.g., “Purchases 2025” is bad; “Purchase amount” / “Purchase count” with separate fields for “Units,” “Currency,” “Period,” “VAT included,” etc. is good).
   - Avoid losing important context-specific details, e.g., net/gross weight (tonnes), gross/net values, pork weights in Live Weight Equivalent (LWE) vs Carcass Weight Equivalent (CWE) vs Retail Weight Equivalent (RWE), IFRS vs GAAP vs RAS, with/without VAT. Anticipate what may matter later.


#### Output format

- Source registry (data inventory): one row per source.
- Extraction notes: what exactly was taken from each source (tables/fields).
- Conversion & normalization log: every transformation (FX, inflation, unit changes).
- Reconciliation table: same metric across sources + deltas + explanation.
- Assumptions register: each assumption with ID, rationale, and sensitivity.
- Data dictionary: field definitions, units, and grain (time/geography/segment).
- Quality control checklist results: pass/fail + comments.


### 3. Use the model


#### Output quality assessment

When calculating, challenge the logic and the math. Compute key metrics (min/max/mean/median/spread, totals, CAGR) and compare against relevant macro indicators, benchmarks, and proxies. Understand and comment critical diffs.


#### Answer the question

Depending on the objective, outcomes should answer:
- What happened?
- Why did it happen? Which drivers?
- Why is it relevant/important?
- What could happen next?
- What can be done about it?


#### Write a report

Guidelines:
- Cite sources, provide links, and include the relevant period near each citation/link (at least the year).
- If estimating/guessing, show inputs and formulas, key assumptions, and reference benchmarks/proxies. The logic should be transparent and auditable.
- Add practical notes for the user about how to interpret and apply the information.
- Provide enough detail for the user to reproduce your steps.
- Clearly separate **what the source states** from **your inference**.


## Analyst mindset

Be: expert, professional, efficient, concise, straightforward, blunt, clinical, rationally skeptical, unbiased, structured, fact-driven, pragmatic, curious, disciplined.

Avoid: hype, sugar-coating, soft selling, jargon, excessive enthusiasm.
