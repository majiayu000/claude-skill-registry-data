---
name: power-bi
description: Master Power BI development including DAX formulas, Power Query M, data modeling, and report optimization
sasmp_version: "1.3.0"
bonded_agent: 04-excel-power-bi
bond_type: PRIMARY_BOND
parameters:
  task:
    type: string
    required: true
    enum: [dax_measure, power_query, data_model, visualization, performance]
  complexity:
    type: string
    enum: [basic, intermediate, advanced]
    default: intermediate
  context:
    type: string
    enum: [row, filter, query]
    default: filter
retry_config:
  max_retries: 3
  backoff_ms: [1000, 2000, 4000]
---

# Power BI Skill

Master Microsoft Power BI development including DAX formulas, Power Query transformations, data modeling, and report optimization.

## Quick Start (5 minutes)

```dax
// 3 essential DAX patterns:

// 1. Basic measure
Total Sales = SUM(Sales[Amount])

// 2. Time intelligence
Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])

// 3. Safe division
Profit Margin = DIVIDE([Profit], [Revenue], 0)
```

## Core Concepts

### DAX Evaluation Context

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTEXT IN DAX                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ROW CONTEXT                    FILTER CONTEXT              │
│  ────────────                   ──────────────              │
│  Created by:                    Created by:                 │
│  • Calculated columns           • Slicers                   │
│  • Iterators (SUMX, etc.)       • Filters                   │
│  • Row-level security           • Rows/Columns in visual    │
│                                 • CALCULATE                  │
│  Accesses:                      Accesses:                   │
│  • Current row values           • Filtered table            │
│                                                             │
│  CALCULATE triggers CONTEXT TRANSITION                      │
│  (Row context → Filter context)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Measure vs Calculated Column

| Aspect | Measure | Calculated Column |
|--------|---------|-------------------|
| Calculated | Query time | Refresh time |
| Storage | None | In model |
| Context | Filter | Row |
| Use when | Aggregations | Row-level values |
| Performance | Better for large data | Impacts model size |

### CALCULATE Deep Dive

```dax
// CALCULATE structure
CALCULATE(
    <expression>,           // What to calculate
    <filter1>,              // Modify filter context
    <filter2>,              // Additional filters
    ...
)

// CALCULATE actions:
// 1. Context transition (row → filter)
// 2. Apply filters (modify filter context)
// 3. Evaluate expression (in new context)

// Examples:
Sales All Products = CALCULATE([Total Sales], ALL(Products))
Sales Current Region = CALCULATE([Total Sales], REMOVEFILTERS())
Sales Top Category = CALCULATE([Total Sales], TOPN(1, Categories, [Total Sales]))
```

## Code Examples

### Time Intelligence Measures
```dax
// Year-to-Date
Sales YTD =
TOTALYTD(
    [Total Sales],
    'Date'[Date]
)

// Prior Year
Sales PY =
CALCULATE(
    [Total Sales],
    SAMEPERIODLASTYEAR('Date'[Date])
)

// Year-over-Year Growth
YoY Growth % =
VAR CurrentSales = [Total Sales]
VAR PriorSales = [Sales PY]
RETURN
DIVIDE(
    CurrentSales - PriorSales,
    PriorSales,
    BLANK()
)

// Rolling 12 Months
Sales Rolling 12M =
CALCULATE(
    [Total Sales],
    DATESINPERIOD(
        'Date'[Date],
        MAX('Date'[Date]),
        -12,
        MONTH
    )
)

// Month-to-Date
Sales MTD =
TOTALMTD(
    [Total Sales],
    'Date'[Date]
)

// Previous Month
Sales PM =
CALCULATE(
    [Total Sales],
    PREVIOUSMONTH('Date'[Date])
)
```

### Dynamic Segmentation
```dax
// Customer Segment based on Sales
Customer Segment =
VAR CustomerSales = [Total Sales]
RETURN
SWITCH(
    TRUE(),
    CustomerSales >= 100000, "Platinum",
    CustomerSales >= 50000, "Gold",
    CustomerSales >= 10000, "Silver",
    "Bronze"
)

// ABC Analysis (Pareto)
ABC Category =
VAR CurrentProduct = SELECTEDVALUE(Products[ProductName])
VAR AllProducts =
    ADDCOLUMNS(
        ALLSELECTED(Products[ProductName]),
        "@Sales", [Total Sales]
    )
VAR RankedProducts =
    ADDCOLUMNS(
        AllProducts,
        "@Rank", RANKX(AllProducts, [@Sales],, DESC, DENSE),
        "@CumSales", SUMX(
            FILTER(AllProducts, RANKX(AllProducts, [@Sales],, DESC, DENSE) <= RANKX(AllProducts, [@Sales],, DESC, DENSE)),
            [@Sales]
        )
    )
VAR TotalSales = SUMX(AllProducts, [@Sales])
VAR CumPct =
    MAXX(
        FILTER(RankedProducts, [Products[ProductName]] = CurrentProduct),
        [@CumSales] / TotalSales
    )
RETURN
SWITCH(
    TRUE(),
    CumPct <= 0.8, "A",
    CumPct <= 0.95, "B",
    "C"
)
```

### Power Query M Patterns
```powerquery
// Incremental Refresh Setup
let
    Source = Sql.Database("server", "database"),
    // RangeStart and RangeEnd are incremental refresh parameters
    FilteredRows = Table.SelectRows(
        Source,
        each [ModifiedDate] >= RangeStart and [ModifiedDate] < RangeEnd
    )
in
    FilteredRows

// Dynamic Column Pivoting
let
    Source = Excel.CurrentWorkbook(){[Name="Data"]}[Content],
    Unpivoted = Table.UnpivotOtherColumns(
        Source,
        {"Product"},
        "Attribute",
        "Value"
    )
in
    Unpivoted

// Error Handling
let
    Source = try Sql.Database("server", "db")
             otherwise #table({"Status"}, {{"Connection Failed"}}),
    Result = if Table.RowCount(Source) > 0
             then Source
             else error "No data returned"
in
    Result

// Custom Function
let
    CalculateMargin = (Revenue as number, Cost as number) as number =>
        if Revenue = 0 then 0 else (Revenue - Cost) / Revenue
in
    CalculateMargin
```

## Best Practices

### DAX Formatting Standard
```dax
// Format: Sentence case with units
Revenue per Customer ($) =
VAR TotalRevenue = SUM(Sales[Revenue])
VAR CustomerCount = DISTINCTCOUNT(Sales[CustomerID])
RETURN
DIVIDE(
    TotalRevenue,
    CustomerCount,
    0  // Alternate result for division by zero
)
```

### Model Optimization Checklist
```
□ Remove unused columns
□ Disable Auto Date/Time
□ Use star schema (avoid snowflake)
□ Create a proper Date table (mark as date table)
□ Use integer keys for relationships
□ Avoid bidirectional filtering (use only when necessary)
□ Set column data types correctly
□ Hide foreign key columns from report view
□ Group measures in display folders
□ Add descriptions to measures
```

### Performance Anti-Patterns
```dax
// ❌ AVOID: FILTER with large tables
Sales Filtered =
CALCULATE([Total Sales], FILTER(ALL(Products), Products[Category] = "A"))

// ✓ BETTER: Direct filter
Sales Filtered =
CALCULATE([Total Sales], Products[Category] = "A")

// ❌ AVOID: SUMX over entire table
Total Margin =
SUMX(Sales, Sales[Revenue] - Sales[Cost])

// ✓ BETTER: Pre-calculated column or simpler aggregate
Total Margin =
SUM(Sales[Revenue]) - SUM(Sales[Cost])
```

## Common Patterns

### Conditional Formatting Values
```dax
// Return values for conditional formatting
Status Icon =
VAR Actual = [Total Sales]
VAR Target = [Target]
VAR Variance = DIVIDE(Actual - Target, Target)
RETURN
SWITCH(
    TRUE(),
    Variance >= 0.1, "▲",  // Green up
    Variance >= 0, "●",    // Yellow neutral
    "▼"                    // Red down
)

// Background color value
KPI Color =
VAR Variance = [Variance %]
RETURN
SWITCH(
    TRUE(),
    Variance >= 0.1, "#22C55E",
    Variance >= 0, "#F59E0B",
    "#EF4444"
)
```

### Dynamic Top N
```dax
// With parameter table
Top N Sales =
VAR TopNValue = SELECTEDVALUE('Parameters'[TopN], 10)
VAR RankedProducts =
    ADDCOLUMNS(
        SUMMARIZE(Sales, Products[ProductName]),
        "@Sales", [Total Sales],
        "@Rank", RANKX(ALL(Products[ProductName]), [Total Sales],, DESC)
    )
RETURN
SUMX(
    FILTER(RankedProducts, [@Rank] <= TopNValue),
    [@Sales]
)
```

### Disconnected Table Pattern
```dax
// Create slicer options without relationships
// DateGranularity table: Day, Week, Month, Quarter, Year

Selected Granularity Label =
VAR Selection = SELECTEDVALUE('DateGranularity'[Granularity], "Month")
RETURN
SWITCH(
    Selection,
    "Day", FORMAT([Date], "MMM DD, YYYY"),
    "Week", "Week " & WEEKNUM([Date]),
    "Month", FORMAT([Date], "MMM YYYY"),
    "Quarter", "Q" & QUARTER([Date]) & " " & YEAR([Date]),
    "Year", FORMAT([Date], "YYYY")
)
```

## Retry Logic

```typescript
const refreshDataset = async (datasetId: string) => {
  const retryConfig = {
    maxRetries: 3,
    backoffMs: [60000, 120000, 300000]  // 1min, 2min, 5min
  };

  for (let attempt = 0; attempt <= retryConfig.maxRetries; attempt++) {
    try {
      return await powerBIService.refreshDataset(datasetId);
    } catch (error) {
      if (attempt === retryConfig.maxRetries) throw error;
      if (error.code === 'REFRESH_ALREADY_IN_PROGRESS') {
        await waitForRefreshComplete(datasetId);
        return;
      }
      await sleep(retryConfig.backoffMs[attempt]);
    }
  }
};
```

## Logging Hooks

```typescript
const powerBIHooks = {
  onMeasureEvaluate: (measureName, duration) => {
    console.log(`[DAX] ${measureName} evaluated in ${duration}ms`);
    if (duration > 1000) {
      console.warn(`[DAX] Slow measure: ${measureName}`);
    }
  },

  onRefreshStart: (datasetId) => {
    console.log(`[REFRESH] Starting: ${datasetId}`);
  },

  onRefreshComplete: (datasetId, status, duration) => {
    console.log(`[REFRESH] ${datasetId}: ${status} in ${duration}s`);
  }
};
```

## Unit Test Template

```typescript
describe('Power BI Skill', () => {
  describe('DAX Measures', () => {
    it('should calculate YoY correctly', async () => {
      const result = await evaluateMeasure('YoY Growth %', {
        'Date[Year]': 2024
      });
      expect(result).toBeCloseTo(0.15, 2);
    });

    it('should handle division by zero', async () => {
      const result = await evaluateMeasure('Profit Margin', {
        'Sales[Amount]': 0
      });
      expect(result).toBe(0);  // Not error
    });
  });

  describe('Data Model', () => {
    it('should have star schema structure', () => {
      const relationships = getModelRelationships();
      const factsToFacts = relationships.filter(
        r => r.fromTable.startsWith('Fact_') && r.toTable.startsWith('Fact_')
      );
      expect(factsToFacts.length).toBe(0);
    });
  });
});
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Circular dependency | Self-referencing | Use VAR or EARLIER() |
| Wrong totals | Filter context leakage | Use ALL() or REMOVEFILTERS() |
| Slow visuals | Complex iterator | Use SUMMARIZECOLUMNS |
| Blank results | Missing relationship | Check model relationships |
| #ERROR | Division by zero | Use DIVIDE() function |

## Resources

- **SQLBI**: DAX Patterns and best practices
- **DAX Guide**: Complete function reference
- **Power Query M Reference**: Microsoft documentation
- **DAX Studio**: Performance analysis tool

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade with optimization |
