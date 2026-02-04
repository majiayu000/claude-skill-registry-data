---
name: data-insights
description: Generate actionable insights from transaction data. Use when implementing insight generators, anomaly detection, or data analysis features for financial/tax tracking applications.
---

# Data Insights Skill

This skill provides patterns for generating actionable insights from transaction data, specifically designed for tax and expense tracking applications.

## When to Use This Skill

- Implementing insight generators for dashboards
- Detecting spending anomalies and patterns
- Computing aggregated statistics over time ranges
- Building ranked insight cards with drill-down capabilities

## Core Insight Types

### 1. Quiet Leaks (Small Recurring Expenses)

Detects small, frequent purchases that add up significantly.

**Trigger Rules:**
- Transaction appears 3+ times in the range
- Individual amounts ≤ $20
- Cumulative total ≥ $50

**Severity Calculation:**
```typescript
severity = Math.min(10, Math.floor(cumulativeTotal / 25))
```

**Query Pattern:**
```typescript
// Group by merchant, count occurrences, sum totals
const quietLeaks = transactions
  .filter(t => parseFloat(t.totalAmount) <= 20)
  .reduce((acc, t) => {
    const key = t.merchant || 'Unknown';
    if (!acc[key]) acc[key] = { count: 0, total: 0, transactions: [] };
    acc[key].count++;
    acc[key].total += parseFloat(t.totalAmount);
    acc[key].transactions.push(t.id);
    return acc;
  }, {});

// Filter to those with 3+ occurrences and $50+ total
return Object.entries(quietLeaks)
  .filter(([_, data]) => data.count >= 3 && data.total >= 50)
  .map(([merchant, data]) => ({
    type: 'QUIET_LEAK',
    title: `${merchant} adds up`,
    summary: `${data.count} purchases totaling $${data.total.toFixed(2)}`,
    severityScore: Math.min(10, Math.floor(data.total / 25)),
    supportingTransactionIds: data.transactions
  }));
```

### 2. Tax Drag (High Tax Rate Merchants)

Identifies merchants or categories with unusually high effective tax rates.

**Trigger Rules:**
- Effective tax rate > 9% (above typical sales tax)
- At least $100 spent at merchant

**Severity Calculation:**
```typescript
severity = Math.min(10, Math.floor((effectiveTaxRate - 0.08) * 100))
```

**Query Pattern:**
```typescript
const taxDrag = transactions.reduce((acc, t) => {
  const key = t.merchant || 'Unknown';
  const taxRate = parseFloat(t.taxAmount) / parseFloat(t.totalAmount);
  if (!acc[key]) acc[key] = { totalSpent: 0, totalTax: 0, transactions: [] };
  acc[key].totalSpent += parseFloat(t.totalAmount);
  acc[key].totalTax += parseFloat(t.taxAmount);
  acc[key].transactions.push(t.id);
  return acc;
}, {});

return Object.entries(taxDrag)
  .filter(([_, data]) => {
    const effectiveRate = data.totalTax / data.totalSpent;
    return effectiveRate > 0.09 && data.totalSpent >= 100;
  })
  .map(([merchant, data]) => {
    const effectiveRate = data.totalTax / data.totalSpent;
    return {
      type: 'TAX_DRAG',
      title: `High tax burden at ${merchant}`,
      summary: `${(effectiveRate * 100).toFixed(1)}% effective tax rate on $${data.totalSpent.toFixed(2)}`,
      severityScore: Math.min(10, Math.floor((effectiveRate - 0.08) * 100)),
      supportingTransactionIds: data.transactions
    };
  });
```

### 3. Spikes/Anomalies (Unusual Spending)

Detects month-over-month jumps, duplicates, or unusual amounts.

**Trigger Rules:**
- Single transaction > 2x average transaction
- Month-over-month increase > 50%
- Duplicate-like entries (same merchant + amount within 24h)

**Severity Calculation:**
```typescript
// For outliers
severity = Math.min(10, Math.floor((amount / average - 1) * 2))

// For MoM spikes
severity = Math.min(10, Math.floor((percentIncrease - 50) / 10))
```

**Query Pattern:**
```typescript
const average = transactions.reduce((sum, t) => sum + parseFloat(t.totalAmount), 0) / transactions.length;

// Find outliers
const outliers = transactions
  .filter(t => parseFloat(t.totalAmount) > average * 2)
  .map(t => ({
    type: 'SPIKE',
    title: `Unusual expense: $${parseFloat(t.totalAmount).toFixed(2)}`,
    summary: `${t.merchant || 'Unknown'} - ${((parseFloat(t.totalAmount) / average - 1) * 100).toFixed(0)}% above average`,
    severityScore: Math.min(10, Math.floor((parseFloat(t.totalAmount) / average - 1) * 2)),
    supportingTransactionIds: [t.id]
  }));

// Find duplicates
const potentialDuplicates = findDuplicates(transactions);
```

## Output Format

All insight generators must return this standardized format:

```typescript
interface Insight {
  type: 'QUIET_LEAK' | 'TAX_DRAG' | 'SPIKE' | 'DUPLICATE' | 'MOM_INCREASE';
  title: string;       // Short, attention-grabbing headline
  summary: string;     // 1-2 sentence explanation
  severityScore: number; // 1-10 scale for ranking
  supportingTransactionIds: string[]; // For drill-down
}
```

## Implementation Structure

```
src/lib/insights/
├── index.ts              # Main getInsights() function
├── types.ts              # Insight interface definitions
├── generators/
│   ├── quiet-leaks.ts    # detectQuietLeaks()
│   ├── tax-drag.ts       # detectTaxDrag()
│   └── spikes.ts         # detectSpikes()
└── __tests__/
    ├── quiet-leaks.test.ts
    ├── tax-drag.test.ts
    └── spikes.test.ts
```

## Best Practices

1. **Pure Functions**: Each insight generator should be a pure function taking transactions and returning insights
2. **Configurable Thresholds**: Make trigger thresholds configurable via parameters
3. **Efficient Queries**: Compute all insights in a single pass when possible
4. **Test with Edge Cases**: Empty data, single transaction, all same merchant, etc.
5. **Sort by Severity**: Return insights sorted by severityScore descending
