---
name: queries
description: Build and execute semantic queries with filters, time dimensions, aggregations, and ordering in drizzle-cube. Use when querying analytics data, filtering results, working with date ranges, aggregating measures, or building reports with drizzle-cube.
---

# Drizzle Cube Queries

This skill helps you build and execute semantic queries using Drizzle Cube's query API. Queries combine measures, dimensions, filters, and time dimensions to retrieve analytics data.

## Core Concept

A **query** in Drizzle Cube specifies:
- **Measures** - What to aggregate (counts, sums, averages, etc.)
- **Dimensions** - How to group/categorize the results
- **TimeDimensions** - Time-based filtering and grouping
- **Filters** - Conditions to filter the data
- **Order** - Sorting of results
- **Limit/Offset** - Pagination

## Basic Query Structure

```typescript
const query = {
  measures: ['CubeName.measureName'],
  dimensions: ['CubeName.dimensionName'],
  timeDimensions: [{
    dimension: 'CubeName.timeDimension',
    granularity: 'day',
    dateRange: ['2024-01-01', '2024-12-31']
  }],
  filters: [{
    member: 'CubeName.field',
    operator: 'equals',
    values: ['value']
  }],
  order: { 'CubeName.field': 'asc' },
  limit: 100,
  offset: 0
}

// Execute the query
const result = await semanticLayer.execute(query, securityContext)
```

## Measures

Measures are aggregated values calculated across your data.

### Single Measure

```typescript
const query = {
  measures: ['Employees.count']
}

// Result: Total employee count
```

### Multiple Measures

```typescript
const query = {
  measures: [
    'Employees.count',
    'Employees.avgSalary',
    'Employees.totalSalary'
  ]
}

// Result: Multiple aggregations in one query
```

### Cross-Cube Measures

```typescript
const query = {
  measures: [
    'Employees.count',
    'Departments.count',
    'Projects.count'
  ]
}

// Result: Aggregations from multiple cubes (automatic JOINs)
```

## Dimensions

Dimensions categorize and group your data.

### Single Dimension

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: ['Employees.department']
}

// Result: Employee count grouped by department
```

### Multiple Dimensions

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: [
    'Employees.department',
    'Employees.isActive'
  ]
}

// Result: Employee count grouped by department and active status
```

### Cross-Cube Dimensions

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: [
    'Employees.name',
    'Departments.name' // Dimension from joined cube
  ]
}

// Result: Uses automatic JOIN to include department name
```

## Time Dimensions

Time dimensions enable temporal filtering and grouping.

### Basic Time Dimension

```typescript
const query = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'day' // Group by day
  }]
}
```

### Time Granularities

```typescript
// Supported granularities:
const granularities = [
  'second',
  'minute',
  'hour',
  'day',
  'week',
  'month',
  'quarter',
  'year'
]

// Example: Monthly grouping
const query = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'month'
  }]
}
```

### Date Range Filtering with Time Grouping

Time dimensions with `dateRange` filter AND group data by time. The dimension appears in the output grouped by the specified granularity.

```typescript
// Absolute date range (array format)
const query = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'week',
    dateRange: ['2024-01-01', '2024-12-31']
  }]
}
// Result: Weekly employee counts from Jan 1 to Dec 31, 2024

// Single date (becomes full day range)
const query2 = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'hour',
    dateRange: '2024-01-15'
  }]
}
// Result: Hourly counts for January 15, 2024

// Relative date range
const query3 = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'day',
    dateRange: 'last 30 days'
  }]
}
// Result: Daily counts for the last 30 days
```

**All Supported Date Range Patterns:**

```typescript
// Fixed relative ranges
const fixedRanges = [
  'today',              // Current day
  'yesterday',          // Previous day
  'this week',          // Current week (Monday-Sunday)
  'this month',         // Current month
  'this quarter',       // Current quarter (Q1-Q4)
  'this year',          // Current year
  'last week',          // Previous week
  'last month',         // Previous month
  'last quarter',       // Previous quarter
  'last year',          // Previous year
  'last 7 days',        // Last 7 days from now
  'last 30 days',       // Last 30 days from now
  'last 12 months'      // Last 12 months from now
]

// Flexible relative ranges (N can be any number)
const flexibleRanges = [
  'last N days',        // e.g., 'last 45 days', 'last 90 days'
  'last N weeks',       // e.g., 'last 8 weeks', 'last 12 weeks'
  'last N months',      // e.g., 'last 3 months', 'last 18 months'
  'last N quarters',    // e.g., 'last 2 quarters', 'last 4 quarters'
  'last N years'        // e.g., 'last 2 years', 'last 5 years'
]

// Examples of flexible patterns
const examples = {
  measures: ['Sales.revenue'],
  timeDimensions: [{
    dimension: 'Sales.date',
    granularity: 'week',
    dateRange: 'last 12 weeks'  // Last 12 weeks grouped by week
  }]
}

// All patterns are case-insensitive
'Last 30 Days' === 'last 30 days' === 'LAST 30 DAYS'
```

### Time Dimension with Granularity and Range

```typescript
const query = {
  measures: ['Employees.count'],
  timeDimensions: [{
    dimension: 'Employees.createdAt',
    granularity: 'week',
    dateRange: 'last 90 days'
  }]
}

// Result: Weekly employee counts for the last 90 days
```

## Filters

Filters restrict which data is included in the query.

### Simple Filters

#### Equals Filter

```typescript
const query = {
  measures: ['Employees.count'],
  filters: [{
    member: 'Employees.department',
    operator: 'equals',
    values: ['Engineering']
  }]
}
```

#### Multiple Values (IN clause)

```typescript
const query = {
  measures: ['Employees.count'],
  filters: [{
    member: 'Employees.department',
    operator: 'equals',
    values: ['Engineering', 'Sales', 'Marketing']
  }]
}
```

### String Operators

```typescript
// Contains
{
  member: 'Employees.name',
  operator: 'contains',
  values: ['John']
}

// Not contains
{
  member: 'Employees.email',
  operator: 'notContains',
  values: ['@competitor.com']
}

// Starts with
{
  member: 'Employees.name',
  operator: 'startsWith',
  values: ['Dr.']
}

// Ends with
{
  member: 'Employees.email',
  operator: 'endsWith',
  values: ['@company.com']
}

// Not equals
{
  member: 'Employees.status',
  operator: 'notEquals',
  values: ['terminated']
}
```

### Numeric Operators

```typescript
// Greater than
{
  member: 'Employees.salary',
  operator: 'gt',
  values: [100000]
}

// Greater than or equal
{
  member: 'Employees.salary',
  operator: 'gte',
  values: [50000]
}

// Less than
{
  member: 'Employees.yearsOfService',
  operator: 'lt',
  values: [5]
}

// Less than or equal
{
  member: 'Employees.age',
  operator: 'lte',
  values: [65]
}

// Between (range)
{
  member: 'Employees.salary',
  operator: 'between',
  values: [50000, 150000]
}
```

### Null/Empty Operators

```typescript
// Is set (not null)
{
  member: 'Employees.departmentId',
  operator: 'set'
}

// Not set (is null)
{
  member: 'Employees.terminationDate',
  operator: 'notSet'
}

// Is empty (null or empty string)
{
  member: 'Employees.middleName',
  operator: 'isEmpty'
}

// Is not empty
{
  member: 'Employees.email',
  operator: 'isNotEmpty'
}
```

### Date Operators

```typescript
// In date range
{
  member: 'Employees.createdAt',
  operator: 'inDateRange',
  values: ['2024-01-01', '2024-12-31']
}

// Before date
{
  member: 'Employees.createdAt',
  operator: 'beforeDate',
  values: ['2024-06-01']
}

// After date
{
  member: 'Employees.createdAt',
  operator: 'afterDate',
  values: ['2023-01-01']
}
```

### Date Range Filters (Filter Without Time Grouping)

**NEW**: Use `dateRange` in filters to filter by date WITHOUT adding time dimensions to the output. This is perfect for KPI cards, summaries, and any query where you want to filter by time period but don't need time-series data.

**Key Differences from timeDimensions:**
- **filters.dateRange**: Filters data only, NO time columns in output
- **timeDimensions.dateRange**: Filters AND groups data, time columns appear in output

#### Basic Filter with dateRange

```typescript
// Filter employees created in last 30 days
// Time dimension does NOT appear in output
const query = {
  measures: ['Employees.count', 'Employees.avgSalary'],
  dimensions: ['Employees.department'],
  filters: [{
    member: 'Employees.createdAt',
    operator: 'inDateRange',    // REQUIRED operator
    dateRange: 'last 30 days'   // NEW property
  }]
}

// Result: Department-level stats filtered to last 30 days
// Output columns: department, count, avgSalary (NO createdAt column)
```

#### All dateRange Formats Work in Filters

```typescript
// Absolute date range (array)
{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: ['2024-01-01', '2024-12-31']
}

// Single date (full day)
{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: '2024-01-15'
}

// Fixed relative ranges
{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'today'
}

{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'this month'
}

{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'last quarter'
}

// Flexible relative ranges
{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'last 90 days'
}

{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'last 12 weeks'
}

{
  member: 'Orders.createdAt',
  operator: 'inDateRange',
  dateRange: 'last 6 months'
}
```

#### When to Use filters.dateRange vs timeDimensions.dateRange

**Use filters.dateRange when:**
- Building KPI cards (total sales this month)
- Showing summary statistics for a time period
- You need to filter by date but don't want time columns in output
- Creating comparison queries (this month vs last month using separate queries)
- Dashboard widgets showing single metrics

**Use timeDimensions.dateRange when:**
- Creating time-series charts (line charts, area charts)
- Showing trends over time (weekly signups, monthly revenue)
- Need time dimension in output (day, week, month columns)
- Comparing periods in a single query with time grouping

#### Comparison Table

| Feature | filters.dateRange | timeDimensions.dateRange |
|---------|-------------------|--------------------------|
| **Filters data** | ✅ Yes | ✅ Yes |
| **Groups by time** | ❌ No | ✅ Yes |
| **Time column in output** | ❌ No | ✅ Yes |
| **Requires granularity** | ❌ No | ✅ Yes |
| **Requires operator** | ✅ `inDateRange` | ❌ N/A |
| **Best for** | KPIs, summaries | Charts, trends |

#### Practical Examples

```typescript
// Example 1: KPI Card - Total sales this month (NO time grouping)
const thisMonthSales = {
  measures: ['Orders.totalRevenue', 'Orders.count'],
  filters: [{
    member: 'Orders.createdAt',
    operator: 'inDateRange',
    dateRange: 'this month'
  }]
}
// Output: { totalRevenue: 150000, count: 342 }

// Example 2: Time-series chart - Daily sales last 30 days (WITH time grouping)
const dailySalesChart = {
  measures: ['Orders.totalRevenue'],
  timeDimensions: [{
    dimension: 'Orders.createdAt',
    granularity: 'day',
    dateRange: 'last 30 days'
  }]
}
// Output: [
//   { 'Orders.createdAt': '2024-01-01', totalRevenue: 5000 },
//   { 'Orders.createdAt': '2024-01-02', totalRevenue: 5500 },
//   ...
// ]

// Example 3: Department summary for Q1 (NO time grouping)
const q1Summary = {
  measures: ['Employees.count', 'Employees.avgSalary'],
  dimensions: ['Employees.department'],
  filters: [{
    member: 'Employees.createdAt',
    operator: 'inDateRange',
    dateRange: 'this quarter'
  }]
}
// Output: [
//   { department: 'Engineering', count: 50, avgSalary: 120000 },
//   { department: 'Sales', count: 30, avgSalary: 90000 }
// ]

// Example 4: Combining filters.dateRange with other filters
const activeEmployeesLast6Months = {
  measures: ['Employees.count'],
  dimensions: ['Employees.department'],
  filters: [{
    and: [
      {
        member: 'Employees.createdAt',
        operator: 'inDateRange',
        dateRange: 'last 6 months'
      },
      {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      },
      {
        member: 'Employees.salary',
        operator: 'gte',
        values: [50000]
      }
    ]
  }]
}
```

#### Important Notes

1. **Operator is mandatory**: When using `dateRange` in filters, you MUST use `operator: 'inDateRange'`
2. **Time dimensions only**: `dateRange` only works with time dimensions (type: 'time'), not regular dimensions
3. **Precedence**: If both `dateRange` and `values` are provided, `dateRange` takes precedence
4. **Validation**: Invalid date ranges will throw an error during query execution

```typescript
// ❌ WRONG: Missing operator
{
  member: 'Employees.createdAt',
  dateRange: 'last 30 days'
  // ERROR: Missing operator: 'inDateRange'
}

// ❌ WRONG: Wrong operator
{
  member: 'Employees.createdAt',
  operator: 'equals',
  dateRange: 'last 30 days'
  // ERROR: Must use 'inDateRange' operator with dateRange
}

// ❌ WRONG: Non-time dimension
{
  member: 'Employees.name',  // String dimension, not time
  operator: 'inDateRange',
  dateRange: 'last 30 days'
  // ERROR: Can only use dateRange with time dimensions
}

// ✅ CORRECT
{
  member: 'Employees.createdAt',
  operator: 'inDateRange',
  dateRange: 'last 30 days'
}
```

### Compound Filters (AND)

```typescript
const query = {
  measures: ['Employees.count'],
  filters: [
    {
      and: [
        {
          member: 'Employees.department',
          operator: 'equals',
          values: ['Engineering']
        },
        {
          member: 'Employees.isActive',
          operator: 'equals',
          values: [true]
        },
        {
          member: 'Employees.salary',
          operator: 'gte',
          values: [100000]
        }
      ]
    }
  ]
}

// Result: Active engineers making >= $100k
```

### Compound Filters (OR)

```typescript
const query = {
  measures: ['Employees.count'],
  filters: [
    {
      or: [
        {
          member: 'Employees.department',
          operator: 'equals',
          values: ['Engineering']
        },
        {
          member: 'Employees.department',
          operator: 'equals',
          values: ['Data Science']
        }
      ]
    }
  ]
}

// Result: Employees in either Engineering or Data Science
```

### Nested Compound Filters

```typescript
const query = {
  measures: ['Employees.count'],
  filters: [
    {
      and: [
        {
          member: 'Employees.isActive',
          operator: 'equals',
          values: [true]
        },
        {
          or: [
            {
              member: 'Employees.salary',
              operator: 'gte',
              values: [100000]
            },
            {
              member: 'Employees.yearsOfService',
              operator: 'gte',
              values: [10]
            }
          ]
        }
      ]
    }
  ]
}

// Result: Active employees who either earn >= $100k OR have >= 10 years service
```

## Ordering

Sort query results by dimensions or measures.

### Order by Dimension

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: ['Employees.department'],
  order: {
    'Employees.department': 'asc'
  }
}
```

### Order by Measure

```typescript
const query = {
  measures: ['Employees.count', 'Employees.avgSalary'],
  dimensions: ['Employees.department'],
  order: {
    'Employees.count': 'desc' // Sort by employee count descending
  }
}
```

### Multiple Order Fields

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: ['Employees.department', 'Employees.isActive'],
  order: {
    'Employees.department': 'asc',
    'Employees.count': 'desc'
  }
}

// Result: Sorted by department (A-Z), then by count (high to low)
```

## Pagination

Limit results and implement pagination.

### Limit Results

```typescript
const query = {
  measures: ['Employees.count'],
  dimensions: ['Employees.name'],
  order: { 'Employees.count': 'desc' },
  limit: 10 // Top 10 only
}
```

### Pagination with Offset

```typescript
// Page 1 (first 20 results)
const page1 = {
  measures: ['Employees.count'],
  dimensions: ['Employees.name'],
  order: { 'Employees.name': 'asc' },
  limit: 20,
  offset: 0
}

// Page 2 (results 21-40)
const page2 = {
  measures: ['Employees.count'],
  dimensions: ['Employees.name'],
  order: { 'Employees.name': 'asc' },
  limit: 20,
  offset: 20
}

// Page 3 (results 41-60)
const page3 = {
  measures: ['Employees.count'],
  dimensions: ['Employees.name'],
  order: { 'Employees.name': 'asc' },
  limit: 20,
  offset: 40
}
```

## Complete Query Examples

### Example 1: Sales Report

```typescript
const salesReport = {
  measures: [
    'Orders.count',
    'Orders.totalRevenue',
    'Orders.avgOrderValue'
  ],
  dimensions: [
    'Orders.productCategory',
    'Customers.region'
  ],
  timeDimensions: [{
    dimension: 'Orders.createdAt',
    granularity: 'month',
    dateRange: 'this year'
  }],
  filters: [{
    and: [
      {
        member: 'Orders.status',
        operator: 'equals',
        values: ['completed']
      },
      {
        member: 'Orders.totalAmount',
        operator: 'gte',
        values: [100]
      }
    ]
  }],
  order: {
    'Orders.totalRevenue': 'desc'
  },
  limit: 100
}

const result = await semanticLayer.execute(salesReport, securityContext)
```

### Example 2: Employee Analytics

```typescript
const employeeAnalytics = {
  measures: [
    'Employees.count',
    'Employees.avgSalary',
    'Employees.totalSalary'
  ],
  dimensions: [
    'Departments.name',
    'Employees.seniorityLevel'
  ],
  filters: [{
    and: [
      {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      },
      {
        member: 'Employees.createdAt',
        operator: 'afterDate',
        values: ['2020-01-01']
      }
    ]
  }],
  order: {
    'Departments.name': 'asc',
    'Employees.avgSalary': 'desc'
  }
}

const result = await semanticLayer.execute(employeeAnalytics, securityContext)
```

### Example 3: Growth Metrics

```typescript
const growthMetrics = {
  measures: [
    'Users.count',
    'Users.newSignups',
    'Users.activeUsers'
  ],
  timeDimensions: [{
    dimension: 'Users.createdAt',
    granularity: 'week',
    dateRange: 'last 90 days'
  }],
  filters: [{
    member: 'Users.isVerified',
    operator: 'equals',
    values: [true]
  }],
  order: {
    'Users.createdAt': 'asc'
  }
}

const result = await semanticLayer.execute(growthMetrics, securityContext)
```

### Example 4: Top Performers

```typescript
const topPerformers = {
  measures: [
    'Employees.count',
    'Productivity.avgLinesOfCode',
    'Productivity.totalDeployments'
  ],
  dimensions: [
    'Employees.name',
    'Departments.name'
  ],
  timeDimensions: [{
    dimension: 'Productivity.date',
    dateRange: 'last 30 days'
  }],
  filters: [{
    and: [
      {
        member: 'Employees.isActive',
        operator: 'equals',
        values: [true]
      },
      {
        member: 'Productivity.totalDeployments',
        operator: 'gt',
        values: [0]
      }
    ]
  }],
  order: {
    'Productivity.totalDeployments': 'desc'
  },
  limit: 10
}

const result = await semanticLayer.execute(topPerformers, securityContext)
```

## Query Execution

### Basic Execution

```typescript
import { SemanticLayerCompiler } from 'drizzle-cube'

const semanticLayer = new SemanticLayerCompiler({ drizzle: db, schema })
semanticLayer.registerCube(employeesCube)

const result = await semanticLayer.execute(query, {
  organisationId: 'org-123',
  userId: 'user-456'
})

console.log(result.data) // Array of result rows
console.log(result.annotation) // Metadata about measures/dimensions
```

### Result Structure

```typescript
interface QueryResult {
  data: Array<Record<string, any>> // Result rows
  annotation: {
    measures: Record<string, MeasureAnnotation>
    dimensions: Record<string, DimensionAnnotation>
    timeDimensions: Record<string, TimeDimensionAnnotation>
  }
  requestId: string
  slowQuery: boolean
  query: any // Transformed query
}

// Example result
const result = {
  data: [
    {
      'Employees.department': 'Engineering',
      'Employees.count': 50,
      'Employees.avgSalary': 125000
    },
    {
      'Employees.department': 'Sales',
      'Employees.count': 30,
      'Employees.avgSalary': 95000
    }
  ],
  annotation: {
    measures: {
      'Employees.count': { title: 'Employee Count', type: 'count' },
      'Employees.avgSalary': { title: 'Average Salary', type: 'avg' }
    },
    dimensions: {
      'Employees.department': { title: 'Department', type: 'string' }
    }
  },
  requestId: 'req-abc123',
  slowQuery: false
}
```

## Best Practices

1. **Specify only needed fields** - Don't request all measures/dimensions unnecessarily
2. **Use filters early** - Apply filters to reduce data processed
3. **Limit large result sets** - Use `limit` and `offset` for pagination
4. **Order strategically** - Order by measures for "top N" queries
5. **Combine filters efficiently** - Use AND/OR appropriately to minimize data scanned
6. **Use time dimensions wisely** - Leverage granularity for time-series analysis
7. **Test security context** - Always validate multi-tenant isolation
8. **Choose the right dateRange approach**:
   - Use `filters.dateRange` for KPIs and summaries (no time grouping needed)
   - Use `timeDimensions.dateRange` for charts and trends (time grouping needed)
   - Leverage flexible patterns like `'last 90 days'` instead of hardcoded dates
9. **Prefer relative date ranges** - Use `'last 30 days'` instead of absolute dates for dynamic reports

## Common Pitfalls

- **Missing security context** - Every query requires a security context
- **Wrong operator** - Use `equals` not `=`, `gte` not `>=`
- **Invalid date format** - Use ISO format: `2024-01-01`
- **Mixing AND/OR incorrectly** - Nested compound filters need careful structure
- **Performance issues** - Large queries without limits can be slow
- **Missing `inDateRange` operator** - When using `dateRange` in filters, you MUST specify `operator: 'inDateRange'`
- **Using dateRange on non-time dimensions** - `dateRange` only works with time dimensions (type: 'time')
- **Confusing filters.dateRange vs timeDimensions.dateRange**:
  - Wrong: Using `timeDimensions.dateRange` for a KPI card (adds unnecessary time column to output)
  - Wrong: Using `filters.dateRange` for a time-series chart (no time grouping, can't create chart)
- **Invalid relative date patterns** - Use exact patterns like `'last 30 days'` not `'past 30 days'` or `'previous 30 days'`

## All Available Filter Operators

```typescript
// String operators
'equals', 'notEquals', 'contains', 'notContains', 'startsWith', 'endsWith'

// Numeric operators
'gt', 'gte', 'lt', 'lte', 'between'

// Array operators
'in', 'notIn'

// Null operators
'set', 'notSet', 'isEmpty', 'isNotEmpty'

// Date operators
'inDateRange', 'beforeDate', 'afterDate'

// Pattern operators
'like', 'ilike', 'regex'
```

## Next Steps

- Create **charts** from your queries with the chart skills
- Build **dashboards** with the `dashboard` skill
- Learn about **cube definitions** with the `cube-definition` skill
- Set up **server APIs** with the `server-setup` skill
