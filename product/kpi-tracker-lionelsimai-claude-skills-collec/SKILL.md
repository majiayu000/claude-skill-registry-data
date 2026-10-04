---
name: kpi-tracker
description: |
  Set up and track KPI dashboards with targets, actuals, and trend analysis.
  TRIGGERS - Use when user wants to define KPIs, track metrics, or create a scorecard.
---

# KPI Tracker

## Overview
Defines, tracks, and reports on KPIs with targets, actuals, trends, and corrective actions.

## Workflow

### Step 1: Define KPIs
1. **Business goals**: What are you trying to achieve?
2. **Department**: Marketing, sales, ops, product, or company-wide?
3. **Time period**: Weekly, monthly, quarterly tracking?

### Step 2: Select the Right KPIs

**The SMART KPI test:**
- **S**pecific: Measures one clear thing
- **M**easurable: Can be quantified
- **A**chievable: Target is realistic
- **R**elevant: Connects to business goals
- **T**ime-bound: Has a deadline

**Common KPI sets:**

| Department | KPIs |
|-----------|------|
| **Marketing** | CAC, MQLs, traffic, conversion rate, ROAS |
| **Sales** | Revenue, pipeline, close rate, ACV, sales cycle |
| **Product** | DAU/MAU, retention, NPS, feature adoption |
| **Operations** | Efficiency, error rate, throughput, SLA |
| **Finance** | Revenue, margin, burn rate, runway, MRR |
| **Content** | Reach, engagement rate, saves, DMs, leads |

## Output Format

```markdown
# KPI Dashboard: [Department/Company]
## Period: [Month/Quarter/Year]

## Scorecard

| KPI | Target | Actual | Status | Trend |
|-----|--------|--------|--------|-------|
| [KPI 1] | [target] | [actual] | 🟢/🟡/🔴 | ↑/↓/→ |
| [KPI 2] | [target] | [actual] | 🟢/🟡/🔴 | ↑/↓/→ |

## KPI Definitions

### [KPI Name]
- **Definition**: [exactly what this measures]
- **Formula**: [how it's calculated]
- **Target**: [number and why]
- **Data source**: [where the data comes from]
- **Owner**: [who's responsible]
- **Review frequency**: [how often]

## Action Items
| KPI | Issue | Action | Owner | Due |
|-----|-------|--------|-------|-----|
| [Red KPI] | [problem] | [fix] | [who] | [when] |
```

## Quality Checklist
- [ ] Each KPI has a clear definition and formula
- [ ] Targets are realistic with rationale
- [ ] Red/yellow/green thresholds defined
- [ ] Owners assigned to each KPI
- [ ] Action plan for underperforming KPIs
