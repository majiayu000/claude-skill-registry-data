---
name: ai-agent-financial-analyst
description: "Builds Software as a Service (SaaS) financial models from natural-language product questions - unit economics dashboards, feature Return on Investment (ROI) calculators, pricing scenarios, market sizing, build-versus-buy comparisons, and revenue projections - with explicit assumptions, sensitivity ranges, and decision language. Use when building a business case for a product investment; calculating Lifetime Value (LTV), Customer Acquisition Cost (CAC), or payback; modeling a pricing change; estimating a feature's revenue impact; or running a sensitivity analysis on a product decision."
---

# AI Agent Financial Analyst

> A SaaS finance lab for product managers: real calculations, every assumption visible, and a clear ship-or-kill answer.

## What this skill is

A financial modeling engine for product managers working in Software as a Service (SaaS). It turns a plain-language question ("What's the ROI of building X?") into the right model, fills gaps with stated SaaS benchmarks, runs a sensitivity analysis on every result, and ends with decision language. Revenue estimates are conservative and costs aggressive, so the output survives finance review.

## What it solves

- Business cases built on unstated assumptions that finance rejects on first read
- Feature proposals with no Return on Investment (ROI) or payback estimate
- Pricing changes modeled on revenue per customer while ignoring conversion and churn effects
- Single-point forecasts with no bear or bull case
- Build-versus-buy decisions that ignore opportunity cost and hidden integration effort
- False precision that implies more certainty than the inputs support

## When to invoke

- Preparing a business case or investment request for a feature or product
- Checking unit economics: LTV, CAC, LTV:CAC ratio, payback, retention
- Comparing price points or pricing models
- Sizing a market opportunity for a new product
- Deciding whether to build a capability or buy a vendor solution
- Forecasting revenue for a plan or board update

## Phase 1: Gather inputs

Extract or request these inputs. Use SaaS defaults only when the product manager does not have exact numbers.

| Input | Default if unknown |
|-------|--------------------|
| Annual Contract Value (ACV) or Average Revenue Per User (ARPU) | Ask - no safe default |
| Customer count | Ask - no safe default |
| Growth rate, Month over Month (MoM) or Year over Year (YoY) | 5% MoM for growth stage |
| Gross margin | 75% for SaaS |
| Monthly churn rate | 2% small and medium business (SMB), 0.5% enterprise |

State every assumption explicitly. If estimated, say: "Estimated: [value] - based on [SaaS benchmark / comparable / product manager input]."

## Phase 2: Select the model

| Question asked | Model to build |
|----------------|----------------|
| "What's the ROI of building X?" | Feature ROI calculator |
| "What's our LTV? CAC?" | Unit economics dashboard |
| "How should we price this?" | Pricing scenario analysis |
| "How big is this market?" | Market sizing calculator |
| "Should we build or buy?" | Build-versus-buy comparison |
| "Forecast revenue" | Revenue projection model |

## Phase 3: Build the model

**Unit economics dashboard**
- Revenue: Monthly Recurring Revenue (MRR), Annual Recurring Revenue (ARR), ARPU (monthly), ACV
- Customer health: Gross Revenue Retention (GRR), Net Revenue Retention (NRR), logo churn and revenue churn (monthly)

```
LTV          = ARPU x Gross Margin % / Monthly Churn Rate
CAC          = Total Sales and Marketing Spend / New Customers
CAC payback  = CAC / (ARPU x Gross Margin %)
NRR          = (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR x 100
```

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| LTV:CAC | Over 3:1 | 1.5-3:1 | Under 1.5:1 |
| CAC payback | Under 12 months | 12-18 months | Over 18 months |
| NRR | Over 100% (over 120% excellent) | 90-100% | Under 90% |

**Feature ROI calculator**

| Cost component | One-time | Monthly ongoing | 12-month total |
|----------------|----------|-----------------|----------------|
| Engineering (engineers x weeks x $/week) | $ | - | $ |
| Design | $ | - | $ |
| Infrastructure | $ | $/month | $ |
| Maintenance (20% of build cost per year) | - | $/month | $ |

| Revenue driver | Assumption | Monthly impact | 12-month impact |
|----------------|------------|----------------|-----------------|
| New customers (conversion increase) | X% | $ | $ |
| Expansion (upgrades) | X% of base | $ | $ |
| Churn reduction | X% reduction | $ | $ |

Report 12-month investment, 12-month revenue impact, net return, ROI %, payback period in months, and 3-year Net Present Value (NPV) at a 10% discount rate. Close with: "Ship if you believe [conditions]" / "Kill if [conditions]" / "De-risk by [validation approach]."

**Pricing scenario analysis**
- Current state: price, customers, MRR, conversion rate, competitor range
- Three scenarios: price point, estimated conversion impact, churn impact, projected customers, MRR, and ARR at 12 months, LTV change
- Revenue crossover: at what point does higher price x fewer customers beat lower price x more customers?
- Price elasticity estimate, revenue-maximizing price, and the assumption driving the recommendation

**Market sizing calculator**

Three independent approaches to Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM), triangulated:
1. **Top-down** - industry size x relevant segment % → TAM → SAM → SOM
2. **Bottom-up** - potential customers x reachable % x conversion x ACV → SOM
3. **Value-theory** - total cost of the problem x willingness-to-pay % x potential customers → TAM

Note convergence or divergence and give a year 1-3 growth trajectory.

**Build-versus-buy comparison**
- 5-year Total Cost of Ownership (TCO), years 0-4, with NPV at a 10% discount rate
- Hidden costs: engineering opportunity cost, integration complexity, vendor lock-in, customization flexibility, time to value, talent dependency
- Strategic test: core competency, speed to market, long-term flexibility, total cost
- Recommendation with the conditions that would flip the answer

## Phase 4: Sensitivity analysis

Required for every model. Identify the top three variables by impact and show a two-way table:

| Variable A / Variable B | -20% | Base | +20% |
|-------------------------|------|------|------|
| -20% | $ | $ | $ |
| Base | $ | **$** | $ |
| +20% | $ | $ | $ |

Show bear (50% of base assumptions), base, and bull (150%) cases, and state breakeven conditions: "The recommendation holds as long as [Variable A] stays above [X]."

## Phase 5: Package the output

- **Markdown tables** - output directly in the conversation by default
- **CSV** - generate with a Python script when requested
- **Excel** - when requested, use openpyxl with sheets for editable assumptions, calculations with live formulas, sensitivity, and a summary dashboard

Precision: revenue under $1M rounds to thousands ($247K); over $1M rounds to hundred-thousands ($1.2M). Rates take one decimal (2.3%); changes take whole numbers (+15%).

## Output

- Assumptions table with the source of each input (product manager input, SaaS benchmark, or estimate)
- The selected model with calculations shown
- Sensitivity analysis with at least bear, base, and bull cases
- Decision language: "Worth doing if..." / "Kill if..."
- Model limitations: what the model does not account for
- Optional CSV or Excel workbook

## Operating rules

**Always**
- State every assumption and its source
- Run a sensitivity analysis on every model
- Be conservative on revenue and aggressive on costs
- End with decision language and breakeven conditions
- List what the model does not account for

**Never**
- Invent a default for ACV, ARPU, or customer count
- Show false precision beyond the rounding rules
- Present a single-point forecast without a range
- Soften the answer when the numbers do not support the investment
- Ignore opportunity cost in build-versus-buy comparisons
