---
name: unit-economics
version: 1.0.0
category: Finance & Fundraising
domain: unit-economics
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "unit economics"
  - "CAC"
  - "LTV"
  - "customer acquisition cost"
  - "lifetime value"
  - "payback period"
  - "contribution margin"
  - "break even"
  - "churn rate"
  - "economics of my business"
tools: []
---

# Unit Economics

Calculate and analyze CAC, LTV, payback period, contribution margin, and break-even for any business model. Turn raw numbers into decisions.

## Purpose

Unit economics tell you whether your business model actually works — not in theory, but per customer, per transaction. This skill takes the user's numbers and produces a clear picture of profitability, sustainability, and where to focus.

## Workflow

### Step 1: Identify Business Model

Ask the user:
- **Model type:** SaaS, e-commerce, marketplace, services, CPG, other
- **Revenue model:** Subscription, one-time purchase, usage-based, hybrid
- **Current stage:** Pre-revenue, early, growth, mature

### Step 2: Gather the Numbers

Based on model type, collect:

**For SaaS / Subscription:**
- Monthly revenue per customer (ARPU)
- Monthly churn rate (%)
- Customer acquisition cost (CAC) — or marketing spend + sales spend / new customers
- Gross margin (%)

**For E-commerce / CPG:**
- Average order value (AOV)
- Purchase frequency (orders per year)
- Cost of goods sold (COGS) per unit
- Customer acquisition cost
- Repeat purchase rate

**For Services:**
- Average contract value
- Gross margin on delivery
- Sales cycle length
- Customer acquisition cost
- Retention / renewal rate

If the user doesn't have exact numbers, help them estimate from what they do know.

### Step 3: Calculate Core Metrics

**Customer Acquisition Cost (CAC)**
```
CAC = Total Sales & Marketing Spend / New Customers Acquired
```

**Lifetime Value (LTV)**
- SaaS: `LTV = ARPU x Gross Margin / Monthly Churn Rate`
- E-commerce: `LTV = AOV x Purchase Frequency x Avg Customer Lifespan x Gross Margin`
- Services: `LTV = Avg Contract Value x Gross Margin x Avg Renewals`

**LTV:CAC Ratio**
```
LTV:CAC = LTV / CAC
```
- Below 1:1 = Losing money on every customer
- 1:1 to 3:1 = Unsustainable or early stage
- 3:1 to 5:1 = Healthy
- Above 5:1 = Under-investing in growth (or CAC will rise)

**Payback Period**
```
Payback Period = CAC / (ARPU x Gross Margin)
```
- Under 6 months = excellent
- 6-12 months = healthy
- 12-18 months = needs monitoring
- 18+ months = cash flow problem

**Contribution Margin**
```
Contribution Margin = (Revenue - Variable Costs) / Revenue
```

**Break-even Point**
```
Break-even = Fixed Costs / Contribution Margin per Unit
```

### Step 4: Analyze and Interpret

For each metric, provide:
- The calculated number
- What it means in plain language
- How it compares to benchmarks for their business type
- What lever to pull to improve it

### Step 5: Scenario Modeling

Show impact of changes:
- "If you reduce churn by 2%, LTV increases by $X"
- "If you increase AOV by 15%, payback period drops to X months"
- "If you cut CAC by 20% (through organic channels), LTV:CAC hits X:1"

### Step 6: Recommendations

Based on the numbers, recommend:
1. The single biggest lever for profitability
2. Warning signs (if any)
3. What to track monthly

## Output Format

```markdown
## Unit Economics: [Business Name / Product]

### Key Metrics
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| CAC | $XX | $XX-XX | [healthy/warning/critical] |
| LTV | $XX | $XX-XX | [healthy/warning/critical] |
| LTV:CAC | X:1 | 3:1-5:1 | [healthy/warning/critical] |
| Payback Period | X months | <12 mo | [healthy/warning/critical] |
| Contribution Margin | XX% | XX-XX% | [healthy/warning/critical] |
| Monthly Churn | X% | X-X% | [healthy/warning/critical] |

### Calculations
[Show the math for each metric]

### Scenario Analysis
| Change | Impact on LTV | Impact on LTV:CAC |
|--------|--------------|-------------------|
| [Scenario 1] | +$XX | X:1 → X:1 |
| [Scenario 2] | +$XX | X:1 → X:1 |

### Recommendations
1. **Biggest lever:** [What to focus on]
2. **Warning:** [If applicable]
3. **Track monthly:** [Key metrics to watch]
```

## Constraints

- Always show the math — don't just give a number without the calculation
- Label assumptions clearly — "Assuming 5% monthly churn" not just "LTV = $2,400"
- Use industry benchmarks but note they vary widely
- Don't give false precision — if inputs are estimates, outputs are estimates too
- Flag when the user doesn't have enough data for reliable calculations
- Never present unit economics as a guarantee of business viability
