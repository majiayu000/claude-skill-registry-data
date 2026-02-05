---
name: tableau
description: Master Tableau development including calculated fields, LOD expressions, table calculations, and dashboard design
sasmp_version: "1.3.0"
bonded_agent: 05-tableau
bond_type: PRIMARY_BOND
parameters:
  task:
    type: string
    required: true
    enum: [calculation, lod_expression, table_calc, dashboard_action, performance]
  data_source:
    type: string
    enum: [extract, live, published]
    default: extract
  complexity:
    type: string
    enum: [basic, intermediate, advanced]
    default: intermediate
retry_config:
  max_retries: 3
  backoff_ms: [1000, 2000, 4000]
---

# Tableau Skill

Master Tableau development including calculated fields, LOD expressions, table calculations, dashboard actions, and performance optimization.

## Quick Start (5 minutes)

```tableau
// 3 essential Tableau patterns:

// 1. Basic calculated field
[Profit Margin] = [Profit] / [Sales]

// 2. LOD Expression (FIXED)
[Customer First Order] = { FIXED [Customer ID] : MIN([Order Date]) }

// 3. Table Calculation
[Running Total] = RUNNING_SUM(SUM([Sales]))
```

## Core Concepts

### Order of Operations

```
┌─────────────────────────────────────────────────────────────┐
│                 TABLEAU ORDER OF OPERATIONS                  │
├─────────────────────────────────────────────────────────────┤
│  1. Extract Filters (data source)                           │
│  2. Data Source Filters                                     │
│  3. Context Filters          ◄── Set BEFORE LOD             │
│  4. FIXED LOD Expressions    ◄── Computed here              │
│  5. Set/Top N Filters                                       │
│  6. Dimension Filters                                       │
│  7. INCLUDE/EXCLUDE LOD      ◄── Computed here              │
│  8. Measure Filters                                         │
│  9. Table Calculations       ◄── Computed last              │
│ 10. Trend Lines, Reference Lines                            │
└─────────────────────────────────────────────────────────────┘
```

### LOD Expression Types

```
┌──────────────────────────────────────────────────────────────┐
│                    LOD EXPRESSIONS                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  FIXED: Calculate at SPECIFIED level                         │
│  { FIXED [Customer] : SUM([Sales]) }                        │
│  → Always at customer level, regardless of view              │
│                                                              │
│  INCLUDE: Add dimension to calculation                       │
│  { INCLUDE [Product] : AVG([Price]) }                       │
│  → Include product even if not in view                      │
│                                                              │
│  EXCLUDE: Remove dimension from calculation                  │
│  { EXCLUDE [Region] : SUM([Sales]) }                        │
│  → Calculate without region grouping                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Table Calculation Addressing

```
Compute Using: Controls HOW the calculation traverses

Table (across)     → Left to right
Table (down)       → Top to bottom
Table (across then down) → Left-right, then next row
Pane (across)      → Within each pane left-right
Cell               → Each cell individually
Specific Dimensions → Custom control

PARTITIONING: Dimensions that DEFINE the scope
ADDRESSING: Dimensions that TRAVERSE for calculation
```

## Code Examples

### LOD Expressions
```tableau
// Customer's First Purchase Date
[Customer First Order] =
{ FIXED [Customer ID] : MIN([Order Date]) }

// Customer Lifetime Value
[Customer LTV] =
{ FIXED [Customer ID] : SUM([Sales]) }

// Is New Customer (Boolean)
[Is New Customer] =
[Order Date] = [Customer First Order]

// Days Since First Order
[Customer Tenure] =
DATEDIFF('day', [Customer First Order], [Order Date])

// Percent of Customer Total
[% of Customer Sales] =
SUM([Sales]) / [Customer LTV]

// Cohort Month
[Cohort Month] =
{ FIXED [Customer ID] : MIN(DATETRUNC('month', [Order Date])) }

// Average Order Value per Customer (then aggregate)
[Avg Order Value per Customer] =
{ FIXED [Customer ID] : AVG([Sales]) }
// Use AVG([Avg Order Value per Customer]) to get average across customers

// New vs Returning Segment
[Customer Type] =
IF [Order Date] = [Customer First Order]
THEN "New"
ELSE "Returning"
END
```

### Table Calculations
```tableau
// Running Total
[Running Total Sales] =
RUNNING_SUM(SUM([Sales]))
// Compute using: specific date dimension

// Year-over-Year Growth
[YoY Growth] =
(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))
// Compute using: Year

// Percent of Total
[% of Total] =
SUM([Sales]) / TOTAL(SUM([Sales]))

// Rank
[Sales Rank] =
RANK(SUM([Sales]))
// Compute using: Product

// Moving Average (3 periods)
[3-Period MA] =
WINDOW_AVG(SUM([Sales]), -2, 0)

// Cumulative Percent (Pareto)
[Cumulative %] =
RUNNING_SUM(SUM([Sales])) / TOTAL(SUM([Sales]))

// Index (normalized 0-100)
[Sales Index] =
(SUM([Sales]) - WINDOW_MIN(SUM([Sales]))) /
(WINDOW_MAX(SUM([Sales])) - WINDOW_MIN(SUM([Sales]))) * 100

// Period-over-Period Comparison
[MoM Change] =
ZN(SUM([Sales])) - LOOKUP(ZN(SUM([Sales])), -1)
```

### Advanced Calculated Fields
```tableau
// Fiscal Year (April Start)
[Fiscal Year] =
IF MONTH([Order Date]) >= 4
THEN YEAR([Order Date])
ELSE YEAR([Order Date]) - 1
END

// Business Days Between Dates (excluding weekends)
[Business Days] =
DATEDIFF('day', [Start Date], [End Date])
- (DATEDIFF('week', [Start Date], [End Date]) * 2)
- IF DATEPART('weekday', [Start Date]) = 1 THEN 1 ELSE 0 END
- IF DATEPART('weekday', [End Date]) = 7 THEN 1 ELSE 0 END

// Dynamic Date Granularity
[Dynamic Date] =
CASE [Date Granularity Parameter]
    WHEN 'Day' THEN STR(DAY([Order Date])) + ' ' + DATENAME('month', [Order Date])
    WHEN 'Week' THEN 'Week ' + STR(DATEPART('week', [Order Date]))
    WHEN 'Month' THEN DATENAME('month', [Order Date]) + ' ' + STR(YEAR([Order Date]))
    WHEN 'Quarter' THEN 'Q' + STR(DATEPART('quarter', [Order Date])) + ' ' + STR(YEAR([Order Date]))
    WHEN 'Year' THEN STR(YEAR([Order Date]))
END

// Safe Division with NULL handling
[Safe Margin] =
IF ISNULL([Revenue]) OR [Revenue] = 0
THEN NULL
ELSE ([Revenue] - [Cost]) / [Revenue]
END
```

## Best Practices

### Calculation Naming Convention
```
Prefix by type:
• agg_    : Aggregate calculations
• lod_    : LOD expressions
• tc_     : Table calculations
• param_  : Parameter-dependent
• bool_   : Boolean/filter fields
• calc_   : General calculations

Examples:
• agg_Total Sales
• lod_Customer First Order
• tc_Rank by Category
• param_Selected Date Range
• bool_Is Current Year
• calc_Profit Margin
```

### Performance Optimization
```
✓ DO:
• Use extracts for large data
• Use context filters for LOD
• Aggregate at data source level
• Limit marks to <10,000 per view
• Use data source filters

✗ DON'T:
• Nest multiple LODs deeply
• Use live connections for large data
• Create complex string calculations
• Use CONTAINS for exact matches
• Include unused fields in view
```

### Filter Best Practices
```
1. Context Filters: Use when LOD needs filtering
2. Data Source Filters: Apply at connection level
3. Extract Filters: Reduce extract size
4. Dimension Filters: Most common, after LOD
5. Measure Filters: After aggregation
6. Table Calc Filters: Applied last
```

## Common Patterns

### Dashboard Actions Configuration
```yaml
Filter Action:
  name: "Select Category"
  source_sheet: "Category Overview"
  target_sheets:
    - "Product Detail"
    - "Trend Chart"
  run_on: "Select"
  clearing: "Show all values"
  source_fields: ["Category"]
  target_fields: ["Category"]

Highlight Action:
  name: "Highlight Region"
  source_sheet: "Regional Map"
  target_sheets: "All sheets in dashboard"
  run_on: "Hover"
  target_highlighting: true

URL Action:
  name: "Open Product Page"
  source_sheet: "Product Table"
  run_on: "Menu"
  url: "https://products.example.com/<Product ID>"
  url_target: "New Tab"

Parameter Action:
  name: "Set Selected Customer"
  source_sheet: "Customer List"
  run_on: "Select"
  source_field: "Customer ID"
  target_parameter: "Selected Customer"
```

### Cohort Analysis Setup
```tableau
// Step 1: Create cohort dimension
[Cohort Month] = { FIXED [Customer ID] : MIN(DATETRUNC('month', [Order Date])) }

// Step 2: Calculate period number
[Periods Since Cohort] = DATEDIFF('month', [Cohort Month], DATETRUNC('month', [Order Date]))

// Step 3: Create retention calculation (as table calc)
[Retention Rate] = COUNTD([Customer ID]) / LOOKUP(COUNTD([Customer ID]), FIRST())
// Compute using: Periods Since Cohort

// Layout:
// Rows: Cohort Month
// Columns: Periods Since Cohort
// Color: Retention Rate
```

### Dynamic Parameter Selector
```tableau
// Parameter: Select Measure
// Allowable values: Revenue, Profit, Orders

// Calculated field using parameter
[Selected Measure] =
CASE [Select Measure Parameter]
    WHEN 'Revenue' THEN SUM([Sales])
    WHEN 'Profit' THEN SUM([Profit])
    WHEN 'Orders' THEN COUNTD([Order ID])
END

// Dynamic title
[Chart Title] = "Performance by Region: " + [Select Measure Parameter]
```

## Retry Logic

```typescript
const publishWorkbook = async (workbook: Workbook) => {
  const retryConfig = {
    maxRetries: 3,
    backoffMs: [5000, 15000, 30000]
  };

  for (let attempt = 0; attempt <= retryConfig.maxRetries; attempt++) {
    try {
      return await tableauServer.publish(workbook);
    } catch (error) {
      if (attempt === retryConfig.maxRetries) throw error;
      if (error.code === 'CONFLICT') {
        await resolveConflict(workbook);
      }
      await sleep(retryConfig.backoffMs[attempt]);
    }
  }
};
```

## Logging Hooks

```typescript
const tableauHooks = {
  onCalcCreate: (calcName, type) => {
    console.log(`[TABLEAU] Created ${type}: ${calcName}`);
  },

  onQueryExecute: (datasource, rowCount, duration) => {
    console.log(`[TABLEAU] Query on ${datasource}: ${rowCount} rows in ${duration}ms`);
    if (duration > 5000) {
      console.warn(`[TABLEAU] Slow query on ${datasource}`);
    }
  },

  onExtractRefresh: (extractName, status) => {
    console.log(`[TABLEAU] Extract ${extractName}: ${status}`);
  }
};
```

## Unit Test Template

```typescript
describe('Tableau Skill', () => {
  describe('LOD Expressions', () => {
    it('should calculate customer first order correctly', () => {
      const result = evaluateLOD('{ FIXED [Customer ID] : MIN([Order Date]) }');
      expect(result['CUST001']).toBe('2024-01-15');
    });
  });

  describe('Table Calculations', () => {
    it('should compute running total', () => {
      const data = [100, 200, 150];
      const result = runningSum(data);
      expect(result).toEqual([100, 300, 450]);
    });

    it('should rank correctly with ties', () => {
      const data = [100, 200, 200, 150];
      const result = rank(data, 'desc');
      expect(result).toEqual([4, 1, 1, 3]);
    });
  });

  describe('Filters', () => {
    it('should respect context filter order', () => {
      const result = evaluateWithFilters({
        context: [{ field: 'Region', value: 'West' }],
        lod: '{ FIXED [State] : SUM([Sales]) }'
      });
      expect(result).toContainStates(['CA', 'WA', 'OR']);
    });
  });
});
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cannot mix aggregate | Aggregate/row mismatch | Wrap with ATTR() or aggregate |
| LOD returns wrong values | Filter order | Use context filter |
| Table calc addressing wrong | Compute using incorrect | Manually set addressing |
| Slow dashboard | Too many marks | Reduce detail, use extract |
| Extract fails | Data type mismatch | Check null handling |

## Resources

- **Tableau Help**: Official calculation reference
- **LOD Expressions Deep Dive**: Tableau whitepaper
- **Performance Best Practices**: Tableau documentation
- **The Information Lab**: Advanced tutorials

## Version History
| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01 | Initial release |
| 2.0.0 | 2025-01 | Production-grade with LOD patterns |
