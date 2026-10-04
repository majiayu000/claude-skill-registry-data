---
name: Commercial Analysis
description: Structured commercial due diligence covering TAM/SAM/SOM sizing, competitive positioning using Porter's Five Forces, customer concentration analysis, and growth thesis validation.
---

# Commercial Analysis

## When to use

Use this skill during the commercial diligence workstream -- typically weeks 2-4 of a process. It applies to any business where the investment thesis depends on market growth, competitive positioning, or the ability to expand into adjacent markets. It is particularly important for technology, services, and consumer businesses where the moat is not always visible in the financials. This skill synthesises publicly available information and management inputs; it does not replace primary customer reference interviews, but it structures the framework those interviews should test.

## What it does

Produces a commercial analysis memo covering: market definition and sizing, competitive landscape mapped against Porter's Five Forces, company positioning and differentiation, customer and revenue concentration analysis, growth thesis assessment, and key commercial risks with diligence recommendations.

## Method

### Step 1 -- Market definition

Before sizing a market, define it with precision. Vague market definitions lead to inflated TAM figures and unvalidatable growth rate claims.

Apply the substitution test: which products or services would a buyer choose if this company did not exist? That defines the competitive set and the market boundary.

Define the market at three levels:
- **Vertical market:** The specific use case this product addresses for the specific buyer type. Example: "workforce analytics for mid-market manufacturers" not "HR software."
- **Horizontal adjacency:** Adjacent use cases the company is expanding into (or the seller is claiming it will expand into). Note these separately -- they are expansion optionality, not current market.
- **Geographic scope:** Where the company operates and where it is claimed the market exists. TAM figures from research firms often include geographies the company does not serve.

State the market definition in one sentence. This becomes the anchor for all sizing work.

### Step 2 -- Market sizing (TAM/SAM/SOM)

**Top-down approach:**
- Identify the broadest defensible TAM using named, attributable data (industry report, government statistics, or a logical first-principles calculation).
- Apply filters for geography, customer segment, and use case to arrive at SAM (serviceable addressable market).
- Apply the company's current or achievable market share to arrive at SOM (serviceable obtainable market).

**Bottom-up cross-check:**
- Count the total number of potential buyers (establishments, enterprises, or individuals depending on the model).
- Multiply by realistic average spend per buyer per year.
- Cross-check against top-down SAM. If the two figures diverge by more than 2-3x, the market definition or the assumptions are flawed. Investigate before proceeding.

**Growth rate validation:**
- Identify the claimed market growth rate (from CIM or management).
- Test against three leading indicators: (a) number of new entrants over the last 3 years, (b) public company revenue growth rates in the sector, (c) customer spend trend from the company's own data (NRR as a proxy for category spend growth).
- Flag if the claimed growth rate is materially higher than the cross-checks imply.

### Step 3 -- Porter's Five Forces analysis

Apply Porter's Five Forces specifically to this company in this market -- not to the sector generically.

**Threat of new entrants:**
- What are the barriers to entry? (capital requirements, network effects, regulatory approval, proprietary data, switching costs)
- How long would it take a well-funded new entrant to reach competitive parity? If less than 18 months, the moat is weak.
- Are there any recent or announced entrants that validate the market and threaten the incumbent?

**Bargaining power of buyers:**
- How concentrated is the customer base? (use the customer concentration analysis from Step 4)
- What is the cost of switching to a competitor? High switching costs (deep integrations, data migration burden, retraining) shift power back to the supplier.
- Are buyers becoming more sophisticated or price-sensitive over time?

**Bargaining power of suppliers:**
- Does the business depend on a small number of critical third-party inputs (cloud providers, data licensors, specialist contractors)?
- What is the cost of switching suppliers? Are there single-source dependencies?

**Threat of substitutes:**
- Could buyers solve this problem with a different category of product? (e.g., internal headcount instead of SaaS, generic software instead of specialised tool)
- Is the current solution category at risk of being disrupted by AI, automation, or platform consolidation?

**Competitive rivalry:**
- How many direct competitors exist, and what are their approximate market shares?
- Is competition primarily on price, product features, service quality, or brand?
- Is the market consolidating (few large players gaining share) or fragmenting (many niche players)?

Summarise the Five Forces in one paragraph: what does this analysis imply about the durability of the company's competitive position and pricing power?

### Step 4 -- Customer concentration analysis

Customer concentration is one of the most underappreciated risks in PE transactions. Analyse:

- Revenue contribution of top 1, 3, 5, and 10 customers as % of total revenue
- Contract terms for top customers: length, auto-renewal, termination rights, pricing escalators
- Age of relationship: how long has the top customer been a customer?
- Dependency risk: is the business's product embedded in the customer's mission-critical operations, or is it easily replaceable?
- Concentration trend: is the customer base becoming more or less concentrated over time?

Industry benchmarks vary, but general flags:
- Top customer above 15% of revenue: high concentration risk, flag for IC memo
- Top 5 customers above 50% of revenue: meaningful concentration risk in most contexts
- Any single customer that is also a strategic or industry partner (e.g., distribution partnership): assess whether this is a customer relationship or a channel dependency

### Step 5 -- Growth thesis assessment

Identify the seller's stated growth drivers and stress-test each:

**Organic growth drivers:** New customer acquisition, upsell to existing customers, price increases, geographic expansion, new product lines. For each: what is the historical evidence that this driver has worked? What is the constraint on its continued operation (sales capacity, product readiness, market penetration ceiling)?

**Inorganic growth drivers:** M&A-led consolidation in a fragmented market. For each: how many targets have been identified? What are realistic acquisition multiples? What is the integration capability of the management team?

**Growth ceiling check:** Project the company's revenue 5 years forward at the stated growth rate. Does the resulting market share imply the company will have penetrated more than 30-40% of its SAM? If so, the growth rate assumption requires market expansion beyond the current SAM, which changes the risk profile.

**Churn as a growth governor:** For recurring revenue businesses, model the gross customer acquisition needed to sustain the stated growth rate net of churn. If the required new customer acquisition is 2-3x the historical rate, the growth thesis requires a step change in sales execution.

### Step 6 -- Commercial risk summary

Consolidate the commercial risks identified across Steps 1-5 into a ranked list:

For each risk: state the risk in one sentence, the evidence basis from the analysis, the potential impact on the investment thesis if the risk materialises, and the recommended diligence action (customer reference call, primary research, data request to management).

## Inputs

- CIM (particularly the market section and growth thesis)
- Company's revenue data by customer, product, and geography (if available from DDQ)
- Any industry or market research already gathered
- Names of 3-5 customers Claude can reference by sector type (no identifying information required for the framework; customer-specific data is used only in the concentration analysis)

## Output format

A commercial analysis memo with six sections:
1. Market definition (one precise sentence, plus a paragraph of rationale)
2. Market sizing (top-down and bottom-up, cross-check, growth rate validation)
3. Porter's Five Forces (one paragraph per force, summary paragraph)
4. Customer concentration analysis (bullets with % figures, flag for high-risk items)
5. Growth thesis assessment (one paragraph per growth driver, growth ceiling check)
6. Commercial risk summary (ranked risk list, 5-7 risks)

Total length: 1,000-1,500 words. Analytical, not promotional.

## Example

**Growth thesis stress-test (excerpt):**
Management projects 25% revenue growth over the next 3 years, driven by: (a) 15% from new logo acquisition, (b) 7% from upsell, and (c) 3% from price increases. Historical new logo growth was 12% in 2022 and 18% in 2023 -- the 15% target is plausible but requires the sales team to grow headcount by 30% (4 net new AEs) in year 1. The current pipeline coverage ratio is 2.1x (stated), which is below the 3x typically required to sustain this growth rate with a 9-month average sales cycle. Recommend: request detailed pipeline by stage, rep productivity metrics, and hiring plan before accepting 25% as the base case.
