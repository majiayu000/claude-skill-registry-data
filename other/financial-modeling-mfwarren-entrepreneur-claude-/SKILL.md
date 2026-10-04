---
name: financial-modeling
version: 1.0.0
category: Finance & Fundraising
domain: financial-modeling
author: Matt Warren
license: MIT
status: production
updated: 2026-02-07
activation_triggers:
  - "financial model"
  - "revenue forecast"
  - "financial projection"
  - "cash flow"
  - "P&L"
  - "profit and loss"
  - "expense forecast"
  - "scenario analysis"
  - "runway"
tools: []
---

# Financial Modeling

Revenue forecasts, expense modeling, cash flow projections, and scenario analysis.

## Purpose

Build financial models that help founders make decisions — not impress investors with hockey sticks. Focus on the assumptions that matter and the scenarios that could kill the business.

## Workflow

### Step 1: Gather Context
- Business model and revenue streams
- Current monthly revenue and expenses (or estimates)
- Growth assumptions and drivers
- Planned hires or major expenses
- Funding status and runway needs

### Step 2: Revenue Model
Build bottom-up from drivers:
- Customers x ARPU = Revenue (SaaS)
- Traffic x Conversion Rate x AOV = Revenue (e-commerce)
- Clients x Project Value x Utilization = Revenue (services)
- Units x Price = Revenue (CPG/product)

Monthly projections for 12-24 months.

### Step 3: Expense Model
Categorize:
- Fixed costs (rent, salaries, SaaS tools)
- Variable costs (COGS, commissions, shipping)
- Growth investments (marketing spend, new hires)

### Step 4: Cash Flow
- Revenue - Expenses = Net burn/profit
- Cash balance projection
- Runway calculation: Cash / Monthly Burn = Months of runway

### Step 5: Scenario Analysis
Three scenarios:
- **Base case:** Realistic assumptions
- **Upside case:** Things go well (what changes)
- **Downside case:** Things go badly (what breaks)

For each: when do you run out of cash? When do you break even?

### Step 6: Key Metrics Dashboard
- Monthly Recurring Revenue (MRR)
- Burn rate
- Runway
- Gross margin
- Growth rate (MoM)

## Output Format
```markdown
## Financial Model: [Business Name]

### Revenue Projections (12 months)
| Month | Revenue | Expenses | Net | Cash Balance |
|-------|---------|----------|-----|-------------|

### Key Assumptions
[Listed and explained]

### Scenario Analysis
| Scenario | Break-even | Runway | Key Risk |
|----------|-----------|--------|----------|

### Dashboard Metrics
[Current key metrics]
```

## Constraints
- Always label assumptions explicitly — the model is only as good as its inputs
- Don't project beyond what's reasonable for the business stage
- Flag when the user's growth assumptions are unrealistic
- Note that this is a planning tool, not a guarantee
- Cash flow matters more than P&L for startups — always include it
