---
name: bi-fundamentals
description: Master Business Intelligence fundamentals including KPI design, metrics frameworks, data literacy, and analytical thinking
sasmp_version: "1.3.0"
bonded_agent: 01-bi-fundamentals
bond_type: PRIMARY_BOND
parameters:
  topic:
    type: string
    required: true
    enum: [kpi_design, metrics_framework, data_literacy, governance, balanced_scorecard]
  industry:
    type: string
    required: false
  experience_level:
    type: string
    enum: [beginner, intermediate, advanced]
    default: beginner
retry_config:
  max_retries: 3
  backoff_ms: [1000, 2000, 4000]
---

# BI Fundamentals Skill

Master the core concepts of Business Intelligence including KPI design, metrics frameworks, data literacy, and analytical decision-making.

## Quick Start (5 minutes)

```
1. Understand what makes a good KPI (SMART criteria)
2. Learn the difference between metrics and KPIs
3. Explore common BI frameworks (Balanced Scorecard, OKRs)
4. Apply data-driven decision making
```

## Core Concepts

### What is Business Intelligence?
Business Intelligence (BI) transforms raw data into actionable insights for better decision-making.

```
DATA → INFORMATION → INSIGHT → ACTION → VALUE
  ↑         ↑           ↑         ↑
  |         |           |         └─ Business outcome
  |         |           └─ Understanding "so what?"
  |         └─ Context + meaning
  └─ Raw facts/numbers
```

### KPIs vs Metrics

| Aspect | Metric | KPI |
|--------|--------|-----|
| Purpose | Measure activity | Measure success |
| Scope | Operational | Strategic |
| Target | Optional | Required |
| Audience | Teams | Leadership |
| Example | Page views | Conversion rate |

### SMART KPI Framework

```
S - Specific    : Clear and unambiguous
M - Measurable  : Quantifiable with data
A - Achievable  : Realistic given resources
R - Relevant    : Aligned with business goals
T - Time-bound  : Has a deadline or frequency
```

**Example Application:**
```
Bad:  "Improve customer satisfaction"
Good: "Increase NPS score from 45 to 55 by Q4 2025"
      S: NPS score (specific metric)
      M: 45 → 55 (quantifiable)
      A: 10-point increase (realistic)
      R: Customer satisfaction (business goal)
      T: By Q4 2025 (deadline)
```

## Code Examples

### KPI Definition Template (YAML)
```yaml
kpi:
  name: "Customer Acquisition Cost (CAC)"
  category: "Growth"
  owner: "Marketing Director"

  formula:
    numerator: "Total Sales & Marketing Spend"
    denominator: "Number of New Customers Acquired"
    calculation: "SUM(marketing_spend + sales_spend) / COUNT(new_customers)"

  target:
    value: 50
    unit: "USD"
    direction: "lower_is_better"
    threshold_warning: 60
    threshold_critical: 75

  measurement:
    frequency: "monthly"
    data_source: "finance_db.marketing_costs, crm.customers"
    lag_days: 5

  context:
    benchmark_industry: 45
    benchmark_company_historical: 55
    related_kpis: ["LTV", "LTV:CAC Ratio", "Payback Period"]
```

### Metrics Framework (Python-style pseudocode)
```python
# Balanced Scorecard Framework
balanced_scorecard = {
    "financial": {
        "objective": "Increase shareholder value",
        "kpis": [
            {"name": "Revenue Growth", "target": "15% YoY"},
            {"name": "Operating Margin", "target": "25%"},
            {"name": "ROI", "target": "18%"}
        ]
    },
    "customer": {
        "objective": "Improve customer satisfaction",
        "kpis": [
            {"name": "NPS", "target": ">50"},
            {"name": "Customer Retention", "target": ">90%"},
            {"name": "Customer Lifetime Value", "target": ">$500"}
        ]
    },
    "internal_process": {
        "objective": "Optimize operations",
        "kpis": [
            {"name": "Cycle Time", "target": "<3 days"},
            {"name": "Defect Rate", "target": "<1%"},
            {"name": "On-Time Delivery", "target": ">98%"}
        ]
    },
    "learning_growth": {
        "objective": "Build organizational capability",
        "kpis": [
            {"name": "Employee Engagement", "target": ">80%"},
            {"name": "Training Hours per Employee", "target": ">40/year"},
            {"name": "Internal Promotion Rate", "target": ">30%"}
        ]
    }
}
```

### OKR Structure
```yaml
objective: "Become the market leader in customer experience"

key_results:
  - kr: "Increase NPS from 45 to 65"
    progress: 0
    confidence: "medium"

  - kr: "Reduce average response time from 4 hours to 1 hour"
    progress: 0
    confidence: "high"

  - kr: "Achieve 95% first-contact resolution rate"
    progress: 0
    confidence: "low"

initiatives:
  - "Implement AI chatbot for 24/7 support"
  - "Train all support staff on empathy communication"
  - "Create self-service knowledge base"
```

## Best Practices

### KPI Design Principles
1. **Less is More**: 5-7 KPIs per area maximum
2. **Balanced View**: Include leading and lagging indicators
3. **Actionable**: Each KPI should drive specific actions
4. **Owned**: Every KPI has a single accountable owner
5. **Reviewed**: Regular cadence for KPI review and adjustment

### Common Anti-Patterns to Avoid
```
❌ Vanity Metrics: Metrics that look good but don't drive action
   Example: Total page views (without context)

❌ Metric Overload: Too many KPIs diluting focus
   Example: 50+ KPIs on a dashboard

❌ Lagging Only: All backward-looking, no predictive indicators
   Example: Only measuring revenue, not pipeline

❌ Misaligned Incentives: KPIs that encourage wrong behavior
   Example: Call center measured only on calls/hour

❌ Black Box Metrics: Complex calculations no one understands
   Example: "Engagement Score" with undocumented formula
```

### Data Quality Dimensions
```
ACCURACY     → Data correctly reflects reality
COMPLETENESS → No missing values or records
TIMELINESS   → Data is current and up-to-date
CONSISTENCY  → Same data across different systems
VALIDITY     → Data conforms to business rules
UNIQUENESS   → No duplicate records
```

## Common Patterns

### Industry-Specific KPIs

#### SaaS / Subscription Business
```
Growth: MRR, ARR, Net Revenue Retention
Acquisition: CAC, LTV, LTV:CAC Ratio
Engagement: DAU/MAU, Feature Adoption, Time in App
Churn: Logo Churn, Revenue Churn, Expansion Revenue
```

#### E-Commerce / Retail
```
Sales: GMV, AOV, Conversion Rate
Customer: Repeat Purchase Rate, CLV, Cart Abandonment
Operations: Inventory Turnover, Order Fulfillment Time
Marketing: ROAS, Organic vs Paid Traffic %
```

#### Manufacturing
```
Efficiency: OEE, Cycle Time, Throughput
Quality: Defect Rate, First Pass Yield, Scrap Rate
Delivery: On-Time Delivery, Lead Time, Fill Rate
Cost: Cost per Unit, Labor Productivity, Waste %
```

### Metric Hierarchy Template
```
COMPANY LEVEL (CEO/Board)
├── Revenue Growth (+15% YoY)
├── Profitability (25% EBITDA)
└── Customer Satisfaction (NPS >50)
    │
    ├── DIVISION LEVEL (VP)
    │   ├── Sales Revenue
    │   ├── Marketing Efficiency (CAC)
    │   └── Product Adoption Rate
    │       │
    │       └── TEAM LEVEL (Manager)
    │           ├── Leads Generated
    │           ├── Conversion Rate
    │           ├── Feature Usage
    │           └── Support Tickets
    │               │
    │               └── INDIVIDUAL LEVEL
    │                   ├── Calls Made
    │                   ├── Deals Closed
    │                   └── Tasks Completed
```

## Retry Logic

```typescript
const executeWithRetry = async (operation: () => Promise<any>) => {
  const retryConfig = {
    maxRetries: 3,
    backoffMs: [1000, 2000, 4000],
    retryableErrors: ['TIMEOUT', 'NETWORK_ERROR', 'RATE_LIMITED']
  };

  for (let attempt = 0; attempt <= retryConfig.maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      if (attempt === retryConfig.maxRetries) throw error;
      if (!retryConfig.retryableErrors.includes(error.code)) throw error;
      await sleep(retryConfig.backoffMs[attempt]);
    }
  }
};
```

## Logging Hooks

```typescript
const skillHooks = {
  onSkillStart: (params) => {
    console.log(`[BI-FUNDAMENTALS] Starting: ${params.topic}`);
    metrics.increment('skill.bi_fundamentals.started');
  },

  onSkillComplete: (result) => {
    console.log(`[BI-FUNDAMENTALS] Completed successfully`);
    metrics.increment('skill.bi_fundamentals.completed');
  },

  onSkillError: (error) => {
    console.error(`[BI-FUNDAMENTALS] Error: ${error.message}`);
    metrics.increment('skill.bi_fundamentals.errors');
  }
};
```

## Unit Test Template

```typescript
describe('BI Fundamentals Skill', () => {
  describe('KPI Design', () => {
    it('should validate SMART criteria', () => {
      const kpi = {
        name: 'Customer Retention Rate',
        target: '90%',
        frequency: 'monthly',
        owner: 'Customer Success Manager'
      };
      expect(validateSMART(kpi)).toBe(true);
    });

    it('should reject vague KPIs', () => {
      const kpi = { name: 'Improve things' };
      expect(validateSMART(kpi)).toBe(false);
    });
  });

  describe('Metrics Framework', () => {
    it('should balance leading and lagging indicators', () => {
      const framework = buildBalancedScorecard(input);
      expect(framework.leadingIndicators.length).toBeGreaterThan(0);
      expect(framework.laggingIndicators.length).toBeGreaterThan(0);
    });
  });
});
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| KPI not moving | Wrong metric selected | Review leading vs lagging |
| Data not available | Missing data source | Map data requirements first |
| Stakeholder confusion | Complex formula | Simplify and document |
| Gaming the metric | Misaligned incentive | Add balancing metrics |

### Debug Checklist
1. ✓ Is the business objective clearly defined?
2. ✓ Does the KPI formula produce expected results?
3. ✓ Is the data source reliable and timely?
4. ✓ Are targets realistic based on historical data?
5. ✓ Is there an owner accountable for the KPI?

## Resources

- **Kaplan & Norton**: The Balanced Scorecard (foundational text)
- **John Doerr**: Measure What Matters (OKRs)
- **DAMA DMBOK**: Data Management Body of Knowledge
- **Bernard Marr**: KPI Library (industry benchmarks)

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade with schemas |
