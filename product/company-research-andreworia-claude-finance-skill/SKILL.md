---
name: company-research
description: Builds a fast, deep company profile across financials, drivers, and positioning, for when you need a baseline on a target or client before deeper work.
---

# Company Research Agent

## When to use
Use this agent when you need a fast, deep baseline on a target or client before valuation, diligence, or a pitch. It is the first pass that gets you fluent on a company: what it does, how it makes money, how healthy the financials are, and where it sits competitively. Reach for it when a deal lands on your desk and you need to be conversant by the next morning.

## What it does
It returns a company profile that combines the quantitative picture (financials, segments, unit economics) with the qualitative picture (business model, drivers, positioning, and risks), so you have a grounded baseline to build on.

## Method
The agent runs a company-profiling routine, quantitative and qualitative:

1. Establish identity: what the company sells, to whom, its scale, ownership and structure, and how it is organized into business segments.
   - Note whether it is public, sponsor-owned, or founder-held, since that shapes both data availability and deal dynamics.

2. Decompose the business model: the revenue model, how the company charges, recurring versus one-time mix, and the core unit economics that drive margin.
   - Good looks like being able to state the profit made on one unit of the core product or one customer.

3. Read the financials: revenue trajectory and growth rate, gross and operating margins, profitability trend, cash generation, and the shape of the balance sheet including leverage.
   - Check cash conversion against reported earnings; a wide gap is a flag worth chasing.

4. Break out segments: revenue and profit by segment or geography, so mix effects and the true growth engine are visible rather than buried in the consolidated total.
   - Pitfall: a healthy consolidated margin can hide one segment subsidizing a structurally weak one.

5. Identify the value drivers: the two to four levers that most move the company's revenue and margin, such as volume, price, retention, utilization, or input cost.
   - Rank the drivers by sensitivity, so the reader knows which lever matters most.

6. Map positioning: main competitors, relative scale, sources of advantage or disadvantage, and share trend where it can be inferred.
   - Distinguish a real, defensible advantage from a temporary lead that rivals can copy.

7. Compute orientation metrics: a few standard reference points such as EV/EBITDA and revenue growth versus the peer set, to place the company on the map.
   - Use these to locate the company relative to peers, not to conclude a valuation, which is a separate exercise.

8. Surface risks and questions: the key vulnerabilities and the open diligence questions the profile cannot yet answer.
   - Separate answerable-with-more-data questions from genuine structural risks.

9. Synthesize: a short verdict on financial health and competitive standing, framed for the decision at hand.
   - Tie the verdict back to the purpose the profile was requested for.

## Inputs
- The company name and, if relevant, the specific entity or segment in focus.
- The purpose (valuation prep, diligence, pitch, client baseline).
- Any financials, filings, or investor materials already in hand.
- The peer set to benchmark against, if known.
- The ownership status, if known, and any known constraints.
- The depth and length expected for the profile.

## Output format
Claude returns a profile with these named sections:
- Snapshot: what the company is, in three lines.
- Business Model: how it charges and where margin comes from.
- Financial Picture: growth, margins, cash, and leverage, with the key figures called out in prose rather than a grid.
- Segments: the split of revenue and profit and where the growth engine sits.
- Value Drivers: the ranked levers that move revenue and margin.
- Competitive Positioning: rivals, relative scale, and advantage.
- Risks and Open Questions: vulnerabilities and unresolved diligence items.
- Verdict: financial health and competitive standing for the decision at hand.
- Confidence Note: where figures are estimated or data was unavailable. Any peer or multiple comparison is written as sentences, not a table.

## Example
Company: fictional Northwind Logistics, a regional freight and warehousing operator, sponsor-owned. Snapshot: asset-light freight brokerage plus owned warehousing, serving mid-market shippers across three regions. Business Model: brokerage earns a spread per load and warehousing earns recurring storage and handling fees, giving a mixed one-time and recurring profile. Financial Picture: revenue growing at a mid-teens rate with operating margins in the high single digits, solid cash conversion, and moderate leverage. Segments: warehousing is smaller but higher-margin and growing faster than brokerage, so it is the true growth engine despite brokerage carrying more revenue. Value Drivers, ranked: warehouse utilization, brokerage spread, and load volume. Competitive Positioning: sub-scale versus national carriers but strong in its home region on service and relationships. Risks and Open Questions: brokerage spread is cyclical and customer concentration is unclear. Verdict: financially healthy and a plausible roll-up platform, pending confirmation of customer concentration and contract durability.
