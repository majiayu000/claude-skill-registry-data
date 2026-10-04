---
name: financial-modeling
description: >
  Build 3-scenario financial models (Base/Bull/Bear) for startups with templates by business model (SaaS/Marketplace/Commerce), unit economics (CAC/LTV), cohort analysis, and runway calculations.
  Triggers on "financial model", "3-year projection", "unit economics", "runway", "financial forecast",
  "재무 모델", "3년 예측", "유닛 이코노믹스", "런웨이 계산", "재무 전망" requests.
---

# Startup Financial Modeling

Investors speak in numbers. This skill provides a framework for building compelling financial models for fundraising — 3-scenario forecasts, business-model-specific templates, unit economics analysis, and transparent assumption documentation.

## Connectors (Optional)

| Connector | Additional Functionality |
|-----------|--------------------------|
| **~~spreadsheet** | Auto-generate models in Google Sheets or Excel with real-time collaboration |
| **~~knowledge base** | Auto-reference historical financial data and metrics history |
| **~~analytics** | Auto-collect actual data, forecast vs actuals reconciliation |
| **~~CRM** | Revenue forecasts based on sales pipeline |

> **No connectors?** You can build solid financial models with web research and user input alone. Output results as markdown tables or CSV and copy to your spreadsheet.

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                   FINANCIAL MODELING                              │
├─────────────────────────────────────────────────────────────────┤
│  Core Features (Standalone)                                      │
│  ✓ 3-scenario forecasts (Base/Bull/Bear) 3-5 years               │
│  ✓ Business-model templates (SaaS/Marketplace/Commerce/Services) │
│  ✓ Unit economics (CAC/LTV/Payback/LTV:CAC)                     │
│  ✓ Cohort-based revenue modeling                                │
│  ✓ Runway & burn rate calculations                              │
│  ✓ Assumption documentation & sensitivity analysis              │
├─────────────────────────────────────────────────────────────────┤
│  Enhanced Mode (With Connectors)                                 │
│  + ~~spreadsheet: Auto-generate in Google Sheets/Excel          │
│  + ~~knowledge base: Auto-reference historical data              │
│  + ~~analytics: Auto-collect actual data                        │
│  + ~~CRM: Revenue forecasts from sales pipeline                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Getting Started

```bash
"3-year financial model - SaaS, MRR ₩10M, CAC ₩300K"
"Calculate unit economics - CAC, LTV, Payback"
"Calculate runway - current cash ₩500M, monthly burn ₩50M"
"Marketplace financial model - GMV-based"
```

---

## Output Format

### 3-Scenario Financial Model Summary

```markdown
# Financial Model: [Company Name] - [Business Model]
**Date:** [Date] | **Forecast Period:** [Start Month] ~ [End Month] (3-year/5-year) | **Scenarios:** Base/Bull/Bear

---

## Executive Summary

| Scenario | Year 3 Revenue | Year 3 EBITDA | Burn | Additional Funding Needed |
|----------|----------------|---------------|------|---------------------------|
| Bull | [Amount] | [Amount] | [Amount] | [None/₩X] |
| Base | [Amount] | [Amount] | [Amount] | [₩X] |
| Bear | [Amount] | [Amount] | [Amount] | [₩X] |

**Key Assumptions:**
- Base: [Realistic growth rate — market average level]
- Bull: [Aggressive growth rate — top 25% benchmark]
- Bear: [Conservative growth rate — risk-adjusted]

---

## Scenario Details

### 📊 Base Scenario (Most Likely)

**Revenue (Unit: ₩)**
| Year | Y1 | Y2 | Y3 | YoY Growth |
|------|----|----|----|-----------||
| Revenue | X | Y | Z | Y2→Y3: +W% |

**Key Drivers:**
- [Driver 1]: [Assumption and rationale]
- [Driver 2]: [Assumption and rationale]

**P&L Structure:**
| Line Item | Y1 | Y2 | Y3 | Y3 % of Revenue |
|-----------|----|----|----|-----------------||
| Revenue | X | Y | Z | 100% |
| COGS | -A | -B | -C | -D% |
| Gross Profit | E | F | G | +H% |
| OpEx | -I | -J | -K | -L% |
| EBITDA | M | N | O | +/-P% |

---

### 🚀 Bull Scenario (Upside Case)

**Key Differences:**
- [Major difference vs Base 1]
- [Major difference vs Base 2]

**Revenue (Unit: ₩)**
[Simplified table — key metrics only]

---

### ⚠️ Bear Scenario (Downside Case)

**Risk Factors:**
- [Major risk 1 + impact]
- [Major risk 2 + impact]

**Revenue (Unit: ₩)**
[Simplified table — key metrics only]

---

## Unit Economics

| Metric | Year 1 | Year 2 | Year 3 | Target/Benchmark |
|--------|--------|--------|--------|-------------------|
| CAC | [Amount] | [Amount] | [Amount] | [Benchmark] |
| LTV | [Amount] | [Amount] | [Amount] | [Benchmark] |
| LTV:CAC | [Ratio] | [Ratio] | [Ratio] | 3:1+ |
| Payback | [Months] | [Months] | [Months] | <12 months |
| Gross Margin | [%] | [%] | [%] | >70% (SaaS) |

**Interpretation:**
- [Health assessment]
- [Areas for improvement]

---

## Funding Plan

**Current State (Base Scenario):**
- Current cash: [Amount]
- Monthly burn rate: [Amount]
- Runway: [X months] ([End date])

**Additional Funding Required:**
- [Round]: [Amount] by [Timing]
- Use of funds: [1. Item — Amount], [2. Item — Amount]

**Funding Needs by Scenario:**
- Bull: [None or modest amount]
- Base: [Planned amount]
- Bear: [Larger amount or earlier timing]

---

## Key Assumptions

### Revenue Assumptions
- [Assumption 1]: [Value] — [Rationale]
- [Assumption 2]: [Value] — [Rationale]

### Cost Assumptions
- [Assumption 1]: [Value] — [Rationale]
- [Assumption 2]: [Value] — [Rationale]

### Sensitivity Analysis
Most sensitive variables:
1. [Variable 1]: 10% change → Year 3 revenue [X]% impact
2. [Variable 2]: 10% change → Year 3 EBITDA [Y]% impact

---

## Next Steps

- [ ] Build detailed monthly model in spreadsheet
- [ ] Perform sensitivity analysis by scenario
- [ ] Generate summary charts for board/investors
- [ ] Set up performance tracking dashboard
```

---

## Execution Flow

### Step 1: Identify Business Model

```
Checklist:
- Business model: SaaS / Marketplace / E-commerce / Services?
- Current stage: Pre-revenue / Early traction / Growth?
- Revenue model: Subscription / Transaction fees / Product sales / Hourly?
- Key metrics: MRR / GMV / Transaction volume / Number of projects?
```

Select appropriate template by business model → see `references/model-templates.md`

### Step 2: Collect Current State Data

```
Core Data:
- Current revenue (MRR, GMV, monthly revenue, etc.)
- Customer count & growth rate
- Unit economics (CAC, LTV — if available)
- Team size & payroll
- Current cash & burn rate

Enhanced (With Connectors):
- ~~analytics: Auto-collect actual metrics
- ~~CRM: Sales pipeline data
- ~~knowledge base: Historical financial data
```

### Step 3: Design Scenarios

**Base Scenario (50-60% probability):**
```
Principles:
- Realistic and achievable growth rate
- Based on market average or comparable company benchmarks
- Reflect known risks, but exclude severe shocks
- "Most likely" outcome

Example Assumptions:
- Customer growth: +10-15%/month (market average)
- Churn: 3-5% (benchmark)
- CAC: Maintain current level or modest improvement
```

**Bull Scenario (20-30% probability):**
```
Principles:
- Growth when everything goes well
- Top 25% benchmark
- Strong product-market fit, successful channel optimization
- "Optimistic but realistic" outcome

Example Assumptions:
- Customer growth: +20-30%/month (aggressive marketing)
- Churn: ≤2% (product improvements)
- CAC: 20-30% reduction (channel optimization)
```

**Bear Scenario (10-20% probability):**
```
Principles:
- Key risks materialize
- Conservative assumptions
- Market slowdown, increased competition, execution challenges
- "Difficult but not worst-case" outcome

Example Assumptions:
- Customer growth: +5%/month (market slowdown)
- Churn: 8-10% (intensified competition)
- CAC: 20% increase (channel efficiency decline)
```

### Step 4: Model by Business Model

Each business model has unique drivers and metrics. See `references/model-templates.md` for detailed templates.

**SaaS:**
```
Core Drivers:
- New MRR (New Customers)
- Expansion MRR (Upsell/Cross-sell)
- Churn MRR (Cancellations)
- Net MRR = Prior + New + Expansion - Churn

Cohort-based Revenue:
- Monthly new customer cohorts
- Retention curve per cohort
- Monthly ARPU changes
```

**Marketplace:**
```
Core Drivers:
- GMV (Gross Merchandise Value)
- Take Rate (commission rate)
- Revenue = GMV × Take Rate
- Two-sided supply/demand growth

Liquidity Metrics:
- Transaction completion rate
- Repeat purchase rate
- Demand per supplier
```

**E-commerce:**
```
Core Drivers:
- Monthly order volume
- AOV (Average Order Value)
- Repeat purchase rate
- Revenue = Order Count × AOV

Cohort Analysis:
- First purchase cohorts
- Repeat purchase patterns
- LTV calculation
```

**Services/Agency:**
```
Core Drivers:
- Billable headcount
- Hourly billing rate
- Utilization rate
- Revenue = Headcount × Hours × Billing Rate × Utilization

Project-based:
- Average project size
- Monthly project count
```

### Step 5: Model Cost Structure

**COGS (Cost of Goods Sold):**
```
SaaS:
- Hosting costs (AWS, GCP)
- Third-party API costs
- Customer support costs (partial)
Target: Gross Margin 70-80%

Marketplace:
- Payment processing fees
- Fraud prevention costs
- Customer support
Target: Gross Margin 60-70%

E-commerce:
- Product COGS
- Shipping costs
- Inventory management
Target: Gross Margin 40-60%
```

**Operating Expenses:**
```
R&D / Product:
- Engineer salaries (25-35% of revenue)
- Tools & infrastructure

Sales & Marketing:
- CAC budget (New customers × CAC)
- Marketing team salaries
Target: 30-50% of revenue (growth stage)

G&A (General & Administrative):
- Executive salaries
- Legal, accounting, office
Target: 10-15% of revenue
```

### Step 6: Document & Validate Assumptions

**Assumption Documentation Structure:**
```markdown
## Key Assumptions Document

### 1. Customer Acquisition
- **Assumption:** [X] new customers/month
- **Rationale:** [Past 3-month avg Y customers × growth rate Z%]
- **Risk:** [CAC increase, channel saturation]
- **Validation:** [Monthly performance tracking]

### 2. Churn Rate
- **Assumption:** [X]%/month
- **Rationale:** [Past 6-month avg + benchmark]
- **Risk:** [Product gaps, intensified competition]
- **Validation:** [Cohort analysis]

[Repeat for all major assumptions]
```

**Sensitivity Analysis:**
```
Top 3 most impactful variables:
1. Customer growth rate: ±10% → Year 3 revenue ±X%
2. Churn rate: ±2%p → Year 3 revenue ±Y%
3. CAC: ±20% → Profitability achievement ±Z months
```

---

## Business Model Considerations

### SaaS (Software as a Service)

**Core Metrics:**
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- Net Revenue Retention (NRR)
- CAC Payback Period
- Rule of 40 (Growth rate + EBITDA margin)

**Modeling Approach:**
- Cohort-based MRR buildup
- Separate expansion & contraction
- Annual vs monthly contract mix

**Detailed Template:** `references/model-templates.md` → SaaS section

### Marketplace

**Core Metrics:**
- GMV (Gross Merchandise Value)
- Take Rate (commission rate)
- Liquidity (transaction completion rate)
- Repeat transaction rate

**Modeling Approach:**
- Two-sided supply/demand growth model
- Liquidity curve (low initially → high at maturity)
- Take rate progression (low initially → increases with brand strength)

**Detailed Template:** `references/model-templates.md` → Marketplace section

### E-commerce

**Core Metrics:**
- GMV
- AOV (Average Order Value)
- Repeat Purchase Rate
- Inventory Turnover

**Modeling Approach:**
- Separate new vs repeat customers
- Incorporate seasonality
- Inventory turnover & cash conversion cycle

**Detailed Template:** `references/model-templates.md` → E-commerce section

### Services/Agency

**Core Metrics:**
- Billable headcount
- Utilization Rate
- Hourly billing rate
- Project size & duration

**Modeling Approach:**
- Headcount-based capacity model
- Project pipeline → revenue conversion
- Productization roadmap (services → SaaS transition)

**Detailed Template:** `references/model-templates.md` → Services section

---

## Unit Economics Framework

### Core Metric Definitions

**1. CAC (Customer Acquisition Cost)**
```
CAC = (Sales & Marketing Spend) / (New Customers)

Includes:
- Marketing campaign costs
- Sales team salaries (all or portion)
- Marketing tools & infrastructure
- Ad spend, events, content creation

Excludes:
- Customer Success (retention costs)
- Product development costs
```

**2. LTV (Lifetime Value)**
```
LTV = (ARPU × Gross Margin) / Churn Rate

SaaS Example:
- ARPU: ₩100K/month
- Gross Margin: 80%
- Churn: 3%/month
- LTV = (100K × 0.8) / 0.03 = ₩2.67M

Or:
LTV = ARPU × Avg. Customer Lifetime × Gross Margin
```

**3. LTV:CAC Ratio**
```
Healthy Ratios:
- 3:1+ → Healthy
- 2:1~3:1 → Needs improvement
- <2:1 → Risk (broken unit economics)

Investor Expectations:
- Seed: 2:1+ (prove initial efficiency)
- Series A: 3:1+ (scalability)
- Series B+: 4:1+ (maturity)
```

**4. CAC Payback Period**
```
Payback = CAC / (ARPU × Gross Margin)

Targets:
- SaaS: <12 months
- Marketplace: <6 months
- E-commerce: <3 months

Example:
- CAC: ₩300K
- ARPU: ₩100K
- Gross Margin: 80%
- Payback = 300K / (100K × 0.8) = 3.75 months
```

### Unit Economics Improvement Strategies

**Reduce CAC:**
- Strengthen organic channels (SEO, content, word-of-mouth)
- Optimize channels (eliminate low-efficiency ones)
- Improve funnel conversion rates

**Increase LTV:**
- Reduce churn (product improvements, stronger CS)
- Upsell/Cross-sell (increase ARPU)
- Expand usage (usage-based pricing)

---

## Runway & Burn Rate

### Basic Calculation

```
Runway (months) = Current Cash / Monthly Burn Rate

Burn Rate = Monthly Revenue - Monthly Costs

Example:
- Current cash: ₩500M
- Monthly revenue: ₩50M
- Monthly costs: ₩100M
- Burn: -₩50M
- Runway: 500M / 50M = 10 months
```

### Fundraising Timing

```
Rule of Thumb:
- Start next round when 6 months of runway remain
- Time to close: 3-6 months (Seed/Series A)

Example:
- Current runway: 12 months
- Start fundraising at month 6
- Close target: months 9-12
- Safety margin: Additional 3-6 months (for Bear case)
```

### Runway by Scenario

```
| Scenario | Burn Rate | Runway | Funding Needed | Timing |
|----------|-----------|--------|-----------------|--------|
| Bull | -₩30M | 16 months | None | - |
| Base | -₩50M | 10 months | ₩500M | Month 6 |
| Bear | -₩80M | 6 months | ₩1B | Immediately |

Decision Rules:
- If Bull probability is high → defer additional funding
- If Bear risk is high → secure funding now or reduce burn
```

---

## Assumption Documentation & Transparency

### Why Document Assumptions?

1. **Investor Confidence** — Investors evaluate your thinking process, not just numbers.
2. **Team Alignment** — Ensure everyone starts from the same premises.
3. **Traceability** — Validate assumptions against actual results.
4. **Agility** — Quickly adjust when assumptions prove wrong.

### Assumption Documentation Template

```markdown
# Financial Model Assumptions Document
**Model Version:** v1.3 | **Date:** 2024-11-15

---

## 1. Customer Acquisition

### 1.1 New Customers (Monthly)
- **Base:** 100 customers (+15% MoM)
- **Bull:** 150 customers (+25% MoM)
- **Bear:** 60 customers (+8% MoM)

**Rationale:**
- Past 3-month average: 85 customers/month
- Base: Double marketing budget → +15% growth (benchmark)
- Bull: Viral effect + channel optimization
- Bear: Market slowdown + higher CAC

**Risks:**
- CAC higher than expected → fewer customers
- Competitor aggressive marketing → market saturation

**Validation:**
- Monthly performance tracking
- CAC & conversion rate by channel

---

## 2. Churn Rate

### 2.1 Monthly Churn
- **Base:** 3.5%
- **Bull:** 2.0%
- **Bear:** 6.0%

**Rationale:**
- Past 6-month average: 4.2%
- Base: Product improvements + stronger CS → benchmark level
- Bull: Enterprise customers → half the churn
- Bear: Product gaps + intense competition

**Risks:**
- Product defects discovered
- Competitor launches strong alternative

**Validation:**
- Cohort retention tracking
- Churn reason interviews

[Repeat for all major assumptions]
```

---

## Investor Presentation Summary

### Financial Slides for Pitch Deck (3-4 slides)

**Slide 1: 3-Scenario Revenue Forecast**
```
Chart:
- X-axis: Year 0 → Year 3
- Y-axis: Revenue (₩)
- 3 lines: Bull (top), Base (middle), Bear (bottom)
- Highlight Year 3 numbers

Key Message:
"Base scenario: Year 3 revenue ₩[X], [Y]% CAGR"
```

**Slide 2: Unit Economics**
```
4 boxes:
┌─────────────┬─────────────┐
│ CAC         │ LTV         │
│ [Amount]    │ [Amount]    │
└─────────────┴─────────────┘
┌─────────────┬─────────────┐
│ LTV:CAC     │ Payback     │
│ [Ratio]     │ [Months]    │
└─────────────┴─────────────┘

Benchmark Comparison:
"Ours: 3.2:1 / Industry avg: 3:1"
```

**Slide 3: Use of Funds**
```
Waterfall or pie chart:
- Product Development: 40% (₩X)
- Sales & Marketing: 35% (₩Y)
- Team Expansion: 15% (₩Z)
- Operations & Contingency: 10% (₩W)

Milestones:
"Within 12 months: [3 key goals]"
"Within 24 months: [Next round readiness]"
```

**Slide 4: Cohort Economics (Optional)**
```
Cohort Retention Curve:
- Monthly cohorts (M0 → M12)
- Retention % or Revenue $

Key Message:
"12-month cohort: [X]% retention, [Y]x revenue expansion"
```

---

## Related Skills

Effective when used alongside this skill:

- **startup-metrics** — Define core metrics by business model
- **market-sizing** — Validate revenue ceiling with TAM/SAM/SOM
- **fundraising-process** — Financial requirements by funding round
- **pitch-craft** — Integrate financial slides into pitch deck
- **investor-update** — Include financial performance in monthly updates

---

## Tips

1. **Start simple** — Don't aim for a perfect model from day one. Focus on core drivers and refine progressively.

2. **Document assumptions** — Investors evaluate your thinking, not just numbers. Back up all major assumptions with reasoning.

3. **Base scenario must be realistic** — Bull/Bear are extremes, but Base should be the "most likely" outcome.

4. **Unit economics come first** — If one customer doesn't make economic sense, scaling only amplifies the problem.

5. **Build monthly models** — Annual summaries are for pitches; operations require monthly tracking.

6. **Think in cohorts** — Especially for SaaS/Marketplace, cohort-based revenue modeling is most accurate.

7. **Compare against actuals** — Your model is a living document. Update assumptions monthly based on results.

8. **Connect to spreadsheet** — Use ~~spreadsheet connector to auto-generate in Google Sheets for real-time team collaboration.

9. **Reference benchmarks** — Leverage industry averages, public comps, and VC benchmark reports.

10. **Do sensitivity analysis** — Identify which variables have the greatest impact and manage those intensively.

---

## Detailed Templates

For business-model-specific financial model templates, see:

📄 **`references/model-templates.md`**

Includes:
- SaaS financial model (MRR buildup, NRR, Rule of 40)
- Marketplace financial model (GMV, Take Rate, two-sided growth)
- E-commerce financial model (GMV, AOV, repeat rate, inventory)
- Services/Agency financial model (headcount, utilization, projects)
- Monthly detailed structure for each model
- Spreadsheet formula examples
