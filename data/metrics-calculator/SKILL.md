---
name: metrics-calculator
description: Calculate and interpret SaaS growth metrics including MRR, ARR, churn rate, LTV, CAC, NRR, and conversion rates. Use when user mentions metrics, asks about business health, wants to calculate KPIs, or needs help interpreting growth numbers. Provides health checks against industry benchmarks.
allowed-tools: [Read, Write]
---

# SaaS Metrics Calculator Skill

Calculate, track, and interpret key SaaS growth metrics for experiment impact assessment.

## When to Activate

This skill should activate when:
- User mentions specific metrics (MRR, churn, CAC, LTV, etc.)
- User asks "how do I calculate [metric]?"
- User wants to assess business health
- User needs benchmark comparisons
- User asks about experiment impact on metrics
- User mentions "KPIs", "metrics", or "numbers"

## Key SaaS Metrics

### 1. Monthly Recurring Revenue (MRR)

**Definition:** Predictable revenue from subscriptions each month

**Calculation:**
```
MRR = Sum of all monthly subscription revenue
```

**For annual plans:**
```
MRR from annual = (Annual plan price × Annual customers) / 12
```

**Components:**
- New MRR: Revenue from new customers
- Expansion MRR: Upsells/upgrades from existing
- Contraction MRR: Downgrades from existing
- Churned MRR: Revenue lost from cancellations

**Net New MRR:**
```
Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

**Benchmark:**
- Growth rate: 10-20% MoM is excellent
- Most SaaS: 10-15% MoM

### 2. Annual Recurring Revenue (ARR)

**Definition:** Annualized version of MRR

**Calculation:**
```
ARR = MRR × 12
```

**Use:** Key metric for B2B SaaS valuations

### 3. Churn Rate

**Definition:** Percentage of customers who cancel

**Calculation (Customer Churn):**
```
Churn Rate = (Customers Lost / Customers at Start of Period) × 100
```

**Calculation (Revenue Churn/MRR Churn):**
```
MRR Churn Rate = (MRR Lost / MRR at Start of Period) × 100
```

**Benchmarks (2025):**
- B2B SaaS average: 3.5% monthly
  - Voluntary: 2.6%
  - Involuntary: 0.8%
- Excellent: < 2% monthly
- Warning: > 5% monthly
- Critical: > 10% monthly

**Annual Churn Approximation:**
```
Annual Churn ≈ Monthly Churn × 12
```

### 4. Customer Lifetime Value (LTV)

**Definition:** Total revenue from a customer over their lifetime

**Simple Calculation:**
```
LTV = Average Revenue Per User (ARPU) × Average Customer Lifespan (months)
```

**Using Churn Rate:**
```
Average Lifespan = 1 / Monthly Churn Rate
LTV = ARPU / Monthly Churn Rate
```

**Example:**
- ARPU = $100/month
- Monthly Churn = 3% (0.03)
- Average Lifespan = 1 / 0.03 = 33 months
- LTV = $100 × 33 = $3,300

**Advanced (with margin):**
```
LTV = (ARPU × Gross Margin) / Monthly Churn Rate
```

### 5. Customer Acquisition Cost (CAC)

**Definition:** Total cost to acquire a customer

**Calculation:**
```
CAC = Total Sales & Marketing Spend / Number of New Customers Acquired
```

**Time Period:** Usually calculated monthly or quarterly

**What to Include:**
- Sales team salaries and commissions
- Marketing team salaries
- Marketing campaign costs
- Tools and software costs
- Agency/contractor fees

**CAC Payback Period:**
```
CAC Payback = CAC / (ARPU × Gross Margin)
```

**Benchmark:** Should recover CAC within 12 months ideally

### 6. LTV:CAC Ratio

**Definition:** Ratio of customer value to acquisition cost

**Calculation:**
```
LTV:CAC Ratio = LTV / CAC
```

**Benchmarks:**
- Excellent: 3:1 or higher
- Good: 2-3:1
- Warning: < 2:1 (acquiring customers too expensively)
- Problem: < 1:1 (losing money on each customer)

**Example:**
- LTV = $3,300
- CAC = $1,000
- Ratio = 3.3:1 ✓ Excellent

### 7. Net Revenue Retention (NRR)

**Definition:** Revenue retention including expansions and contractions

**Calculation:**
```
NRR = ((Starting MRR + Expansion MRR - Contraction MRR - Churned MRR) / Starting MRR) × 100
```

**Alternative:**
```
NRR = ((Ending MRR from existing customers) / (Starting MRR)) × 100
```

**Benchmarks:**
- Excellent: > 120% (negative churn - expansion > losses)
- Good: 100-120%
- Warning: 90-100%
- Critical: < 90%

**Impact on Valuation:**
- Companies with NRR > 120% trade at 25% higher valuations

### 8. Conversion Rates

**Visitor → Signup:**
```
Signup Rate = (Signups / Visitors) × 100
```

**Signup → Activation:**
```
Activation Rate = (Activated Users / Signups) × 100
```

**Activation → Paying:**
```
Conversion to Paid = (Paying Customers / Activated Users) × 100
```

**Free → Paid:**
```
Free-to-Paid Rate = (Paid Conversions / Free Trial Starts) × 100
```

**Benchmarks vary by industry:**
- B2B SaaS free trial → paid: 10-25%
- Freemium → paid: 2-5%

### 9. Rule of 40

**Definition:** Growth rate + profit margin should exceed 40%

**Calculation:**
```
Rule of 40 = Revenue Growth Rate % + Profit Margin %
```

**Example:**
- Revenue growth: 30% YoY
- Profit margin: 15%
- Rule of 40 = 45% ✓ (Exceeds 40%)

**Benchmark:**
- Companies achieving this generate 3x higher returns
- Indicates sustainable growth

### 10. Expansion Revenue

**Definition:** Additional revenue from existing customers

**Sources:**
- Upsells (higher tier plans)
- Cross-sells (additional products)
- Usage-based expansion
- Seat expansion

**Calculation:**
```
Expansion Rate = (Expansion MRR / Starting MRR) × 100
```

**Benchmark:**
- Should represent 30%+ of total revenue
- 3x cheaper than new customer acquisition

## Metric Calculation Process

### Step 1: Gather Inputs

Ask user for relevant data points:
```
For MRR calculation:
- Total monthly subscription revenue
- OR: Number of customers × Average price

For Churn:
- Customers/MRR at start of period
- Customers/MRR at end of period
- New customers added

For LTV:
- Average revenue per user (monthly)
- Average customer lifespan (months)
- OR: Monthly churn rate

For CAC:
- Total sales & marketing spend
- New customers acquired in period
```

### Step 2: Calculate Metric

Use appropriate formula from above

### Step 3: Interpret Result

- Compare to industry benchmarks
- Provide health assessment (good/warning/critical)
- Explain what the number means in context
- Suggest improvement opportunities

### Step 4: Show Related Metrics

- Calculate related/dependent metrics
- Show how this metric connects to others
- Highlight metrics that should be tracked together

## Health Check Framework

When calculating metrics, provide health assessment:

```markdown
## [Metric Name]: [Value]

**Status:** 🟢 Good / 🟡 Warning / 🔴 Critical

**Benchmark:** [Industry standard]
**Your Value:** [Calculated value]
**Assessment:** [Explanation]

**What this means:**
[Plain language explanation of the metric and its implications]

**Improvement opportunities:**
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Related metrics to track:**
- [Metric 1] - [Why it matters]
- [Metric 2] - [Why it matters]
```

## Experiment Impact Assessment

When analyzing how an experiment affects metrics:

### For Acquisition Experiments:
- Track: CAC, visitor→signup rate, lead volume
- Calculate: Change in CAC, change in conversion rates
- Assess: Is CAC improving while maintaining quality?

### For Activation Experiments:
- Track: Activation rate, time-to-activation
- Calculate: Change in activation percentage
- Assess: Are more users reaching "aha moment"?

### For Retention Experiments:
- Track: Churn rate, NRR
- Calculate: Change in churn, impact on LTV
- Assess: Are users staying longer?

### For Revenue Experiments:
- Track: ARPU, expansion MRR, LTV
- Calculate: Change in revenue per user
- Assess: Are users spending more?

### For Referral Experiments:
- Track: Referral rate, viral coefficient
- Calculate: CAC reduction from referrals
- Assess: Is organic growth increasing?

## Metric Relationships

Show how metrics connect:

```
CAC ↓ (lower acquisition cost)
  ↓
LTV:CAC Ratio ↑ (better unit economics)
  ↓
Profitability ↑ (more sustainable growth)

---

Activation Rate ↑ (more users activated)
  ↓
Retention ↑ (activated users stay longer)
  ↓
LTV ↑ (customers worth more)

---

Churn Rate ↓ (fewer cancellations)
  ↓
LTV ↑ (customers stay longer)
  ↓
MRR Growth ↑ (compound effect)
```

## Output Templates

### Single Metric Calculation

```markdown
# [Metric Name] Calculation

## Inputs
- [Input 1]: [Value]
- [Input 2]: [Value]

## Calculation
```
[Formula]
[Substituted values]
= [Result]
```

## Result: [Formatted value]

**Health Check:** 🟢/🟡/🔴 [Status]

**Industry Benchmark:** [Benchmark value]
**Your Performance:** [Above/Below/At benchmark]

## What This Means
[Plain language explanation]

## Recommendations
1. [Action item]
2. [Action item]
3. [Action item]

## Related Metrics
- [Metric]: [Current value if known]
- [Metric]: [How to calculate]
```

### Full Metrics Dashboard

```markdown
# SaaS Metrics Dashboard

## Revenue Metrics
- **MRR:** $[value] ([+/-X%] MoM) 🟢/🟡/🔴
- **ARR:** $[value]
- **NRR:** [X%] 🟢/🟡/🔴

## Customer Metrics
- **Total Customers:** [count]
- **New Customers:** [count] ([+/-X%])
- **Churn Rate:** [X%] 🟢/🟡/🔴

## Unit Economics
- **LTV:** $[value]
- **CAC:** $[value]
- **LTV:CAC Ratio:** [ratio] 🟢/🟡/🔴
- **CAC Payback:** [months]

## Conversion Funnel
- **Visitor → Signup:** [X%]
- **Signup → Activation:** [X%]
- **Activation → Paid:** [X%]

## Health Summary
- Metrics in good health: [count]
- Metrics needing attention: [count]
- Critical issues: [count]

## Priority Actions
1. [Most important improvement]
2. [Second priority]
3. [Third priority]
```

## Common Calculations User Might Request

Be prepared for:
- "What's my MRR?" → Calculate from customer count × price
- "Is my churn rate good?" → Calculate and compare to benchmark
- "Should I increase my prices?" → Analyze LTV:CAC ratio
- "How much can I spend on marketing?" → Calculate target CAC
- "When will I break even on CAC?" → Calculate payback period
- "Is my growth rate healthy?" → Calculate MRR growth rate
- "How do we compare to industry?" → Show benchmarks for all metrics

## Integration with Experiments

- Help set expected outcomes (e.g., "10% increase in activation rate")
- Calculate experiment impact on metrics
- Assess whether results are meaningful
- Project long-term impact (e.g., if churn ↓ 1%, LTV ↑ $X)

## Resources and Benchmarks

Keep updated with:
- B2B SaaS benchmarks (updated annually)
- Industry-specific variations
- Company stage considerations (startup vs mature)
- Geographic differences

**Current Benchmarks (2025):**
- Churn: 3.5% monthly average
- NRR: 120%+ is excellent
- LTV:CAC: 3:1 minimum
- Rule of 40: Target 40%+
- MRR Growth: 10-20% monthly
