---
name: kql
description: "KQL language expertise for writing correct, efficient Kusto Query Language queries. Covers syntax gotchas, join patterns, dynamic types, datetime pitfalls, regex patterns, serialization, memory management, result-size discipline, and advanced functions (geo, vector, graph). USE THIS SKILL whenever writing, debugging, or reviewing KQL queries — even simple ones — because the gotchas section prevents the most common errors that waste tool calls and cause expensive retry cascades. Trigger on: KQL, Kusto, ADX, Azure Data Explorer, Fabric Real-Time Intelligence, EventHouse, Log Analytics, log analysis, data exploration, time series, anomaly detection, summarize, where clause, join, extend, project, let statement, parse operator, extract function, any mention of pipe-forward query syntax."
---

# KQL Mastery

> **Try it yourself**: All `✅` examples in this skill can be run against the public help cluster:
> `https://help.kusto.windows.net`, database `Samples` (contains `StormEvents`, `SimpleGraph_Nodes`/`Edges`, `nyc_taxi`, and more).

## 1. KQL Basics

Kusto Query Language (KQL) is a pipe-forward query language for exploring data. It is the native query language for Azure Data Explorer (ADX), Microsoft Fabric Real-Time Intelligence (EventHouse), Azure Monitor Log Analytics, Microsoft Sentinel, and other Microsoft data services.

### Pipe-forward syntax

KQL queries are a chain of operators separated by `|`. Data flows left to right:

```kql
StormEvents                          // start with a table
| where State == "TEXAS"             // filter rows
| summarize count() by EventType     // aggregate
| top 5 by count_ desc              // limit results
```

### Query vs management commands

KQL has two execution planes:

| Plane | Starts with | Examples |
|-------|-------------|----------|
| **Query** | Table name, `let`, `print`, `datatable` | `StormEvents \| where State == "TEXAS"` |
| **Management** | `.show`, `.create`, `.set`, `.drop`, `.alter` | `.show tables`, `.show table T schema` |

Management commands can be followed by query operators (the output is tabular), but the entire request runs on the management plane. You cannot start with a query and pipe into a management command.

```kql
// ✅ WORKS — management command piped to query operators
.show tables | project TableName | where TableName has "Events"

// ❌ WRONG — query piped into management command
StormEvents | take 5 | .show tables
```

When in doubt: if the first token starts with `.`, it's a management command. For a full catalog of schema exploration commands, see `references/discovery-queries.md`.

## 2. Dynamic Type Discipline

KQL's `dynamic` type is flexible but strict in certain contexts. A common mistake is using a dynamic column in `summarize by`, `order by`, or `join on` without casting.

**The rule**: Any time you use a dynamic-typed column in `by`, `on`, or `order by`, wrap it in an explicit cast.

```kql
// ❌ ERROR: "Summarize group key ... is of a 'dynamic' type"
StormEvents | summarize count() by StormSummary.Details.Location

// ✅ FIX
StormEvents | summarize count() by tostring(StormSummary.Details.Location)
```

```kql
// ❌ ERROR: "order operator: key can't be of dynamic type"
StormEvents | order by StormSummary.TotalDamages desc

// ✅ FIX
StormEvents | order by tolong(StormSummary.TotalDamages) desc
```

```kql
// ❌ ERROR in join: dynamic join key
StormEvents | join kind=inner (PopulationData) on $left.StormSummary == $right.State

// ✅ FIX — cast both sides
StormEvents
| extend State_str = tostring(StormSummary.Details.Location)
| join kind=inner (PopulationData) on $left.State_str == $right.State
```

**Self-correction**: When you see "is of a 'dynamic' type" in an error, add `tostring()`, `tolong()`, or `todouble()`.

## 3. Join Patterns & Pitfalls

KQL joins have constraints that differ from SQL.

### Equality only
KQL join conditions support **only `==`**. No `<`, `>`, `!=`, or function calls in join predicates.

```kql
// ❌ ERROR: "Only equality is allowed in this context"
StormEvents | join (nyc_taxi) on geo_distance_2points(BeginLon, BeginLat, pickup_longitude, pickup_latitude) < 1000

// ✅ WORKAROUND — pre-bucket into spatial cells, then join on cell ID
StormEvents
| extend cell = geo_point_to_s2cell(BeginLon, BeginLat, 8)
| join kind=inner (nyc_taxi | extend cell = geo_point_to_s2cell(pickup_longitude, pickup_latitude, 8)) on cell
```

For range joins, pre-bin values: `| extend bin_val = bin(Value, 100)`, then join on `bin_val`. Note: values near bin boundaries may land in adjacent bins — consider checking neighboring bins or overlapping the range for precision.

### Left/right attribute matching
Both sides of a join `on` clause must reference **column entities only** — not expressions, not aggregates.

```kql
// ❌ ERROR: "for each left attribute, right attribute should be selected"
StormEvents | join kind=inner (PopulationData) on $left.State

// ✅ FIX — specify both sides explicitly
StormEvents | join kind=inner (PopulationData) on $left.State == $right.State
```

### Cardinality check before large joins
**Always** check cardinality before joining tables with >10K rows. A cross-join explosion was the source of the single `E_RUNAWAY_QUERY` error (25K × 195 = potential 4.8M rows).

```kql
// Before joining, check how many rows each side contributes
StormEvents | summarize dcount(State)        // → 67 distinct states
PopulationData | summarize dcount(State)     // → 52 — safe to join
```

## 4. Regex in KQL

KQL handles regex natively — no need for Python.

### The `extract_all` gotcha
Unlike Python's `re.findall()`, KQL's `extract_all` **requires capturing groups** in the regex:

```kql
// ❌ ERROR: "extractall(): argument 2 must be a valid regex with [1..16] matching groups"
StormEvents | extend words = extract_all(@"[a-zA-Z]{3,}", EventNarrative)

// ✅ FIX — add parentheses around the pattern
StormEvents | extend words = extract_all(@"([a-zA-Z]{3,})", EventNarrative)
```

### Regex toolkit — don't fall back to Python
| Function | Use case | Example |
|----------|----------|---------|
| `extract(regex, group, source)` | Single match | `extract(@"User '([^']+)'", 1, Msg)` |
| `extract_all(regex, source)` | All matches (needs `()`) | `extract_all(@"(\w+)", Text)` |
| `parse` | Structured extraction | `parse Msg with * "User '" Sender "' sent" *` |
| `matches regex` | Boolean filter | `where Url matches regex @"^https?://"` |
| `replace_regex` | Find and replace | `replace_regex(Text, @"\s+", " ")` |

## 5. Serialization Requirements

Window functions need serialized (ordered) input.

```kql
// ❌ ERROR: "Function 'row_cumsum' cannot be invoked. The row set must be serialized."
StormEvents
| where State == "TEXAS"
| summarize DailyCount = count() by bin(StartTime, 1d)
| extend CumulativeCount = row_cumsum(DailyCount)

// ✅ FIX — add | serialize (or | order by, which implicitly serializes)
StormEvents
| where State == "TEXAS"
| summarize DailyCount = count() by bin(StartTime, 1d)
| order by StartTime asc
| extend CumulativeCount = row_cumsum(DailyCount)
```

Functions requiring serialization: `row_number()`, `row_cumsum()`, `prev()`, `next()`, `row_window_session()`.

## 6. Memory-Safe Query Patterns

The most common memory error. Caused by scanning too much data without pre-filtering.

### The progression of safety
```
Safest ──────────────────────────────────────────────── Most dangerous
| count    | take 10    | where + summarize    | summarize (no filter)    | full scan
```

### Rules for large tables (>1M rows)

1. **Always start with `| count`** to understand table size
2. **Always `| where` before `| summarize`** — filter time range, partition key, or category first
3. **Never `dcount()` on high-cardinality columns** without pre-filtering
4. **Check join cardinality** before executing (see Section 3)
5. **Use `materialize()`** for subqueries referenced multiple times

```kql
// ❌ OUT OF MEMORY — large table, no filter, many group-by columns
StormEvents
| summarize dcount(EventType), count() by StartTime, State, Source
| where dcount_EventType > 1

// ✅ SAFE — filter first, then aggregate
StormEvents
| where StartTime between (datetime(2007-04-15) .. datetime(2007-04-16))
| summarize dcount(EventType) by State, Source
| where dcount_EventType > 1
```

### When you see `E_LOW_MEMORY_CONDITION`
The query touched too much data. Your options:
- Add `| where` filters (time range, partition key)
- Reduce the number of `by` columns in `summarize`
- Break into smaller time windows and union results
- Use `| sample 10000` for exploratory work instead of full scans

### When you see `E_RUNAWAY_QUERY`
A join or aggregation produced too many output rows. Check join cardinality — one or both sides is too large.

## 7. Result Size Discipline

Large results slow down analysis. Prevention:

| Query type | Safeguard |
|-----------|-----------|
| Exploratory | Always end with `\| take 10` or `\| take 20` |
| Aggregation | Use `\| top 20 by ...` not unbounded `summarize` |
| Wide rows (vectors, JSON) | `\| project` only needed columns |
| `make_list()` / `make_set()` | Avoid on high-cardinality groups (produces huge cells) |
| Unknown size | Run `\| count` first |

**The vector trap**: Tables with embedding columns (1536-dim float arrays) produce ~30KB per row. Even `| take 20` yields 600KB. Always `| project` away vector columns unless you specifically need them.

## 8. String Comparison Strictness

KQL sometimes requires explicit casts when comparing computed string values — even when both sides are already strings.

```kql
// ❌ ERROR: "Cannot compare values of types string and string. Try adding explicit casts"
StormEvents | where geo_point_to_s2cell(BeginLon, BeginLat, 16) == other_cell

// ✅ FIX — wrap both sides in tostring()
StormEvents | where tostring(geo_point_to_s2cell(BeginLon, BeginLat, 16)) == tostring(other_cell)
```

This is most common with computed values from `geo_point_to_s2cell()` and `strcat()` comparisons. When in doubt, cast with `tostring()`.

## 9. Advanced Functions

KQL handles these natively — no need for Python:

### Vector similarity
```kql
// try it! — cosine similarity on Iris feature vectors
let target = pack_array(5.1, 3.5, 1.4, 0.2);
Iris
| extend Vec = pack_array(SepalLength, SepalWidth, PetalLength, PetalWidth)
| extend sim = series_cosine_similarity(Vec, target)
| top 5 by sim desc
```

### Geo operations
```kql
// Distance between two points (meters)
StormEvents | extend dist = geo_distance_2points(BeginLon, BeginLat, EndLon, EndLat)

// Spatial bucketing for joins
StormEvents | extend cell = geo_point_to_s2cell(BeginLon, BeginLat, 8)
```

### Graph queries
```kql
// Persistent graph model — try it on the help cluster!
graph("Simple")
| graph-match (src)-[e*1..3]->(dst)
  where src.name == "Alice"
  project src.name, dst.name, path_length = array_length(e)

// Transient graph — build inline with make-graph
SimpleGraph_Edges
| make-graph source --> target with SimpleGraph_Nodes on id
| graph-match (src)-[e*1..5]->(dst)
  where src.name == "Alice"
  project src.name, dst.name, path_length = array_length(e)
```

### Time series
```kql
// try it! — create a time series and detect anomalies
StormEvents
| make-series count() default=0 on StartTime step 1d
| extend anomalies = series_decompose_anomalies(count_)
```

For detailed examples and patterns, consult `references/advanced-patterns.md`.

## 10. Self-Correction Lookup Table

When you encounter an error, look it up here before retrying:

| Error message contains | Likely cause | Fix |
|---|---|---|
| `is of a 'dynamic' type` | Dynamic column in `by`/`on`/`order by` | Wrap in `tostring()`/`tolong()` |
| `Only equality is allowed` | Range predicate in join condition | Pre-bucket with S2/H3 cells or `bin()` |
| `extractall(): matching groups` | Missing `()` in regex | Add `()`: `@"(\w+)"` not `@"\w+"` |
| `row set must be serialized` | Window function on unsorted data | Add `\| serialize` or `\| order by` before it |
| `Cannot compare values of types string and string` | Computed string comparison | Add `tostring()` on both sides |
| `Failed to resolve column named 'X'` | Wrong column name or wrong table | Run `.show table T schema` to check column names |
| `E_LOW_MEMORY_CONDITION` | Query touched too much data | Add `\| where` filters, reduce time range, break into steps |
| `E_RUNAWAY_QUERY` | Join/aggregation produced too many rows | Check cardinality before joining; add pre-filters |
| `for each left attribute, right attribute` | Join `on` clause incomplete | Use explicit form: `on $left.X == $right.Y` |
| `needs to be bracketed` | Reserved word used as identifier | Use `['keyword']` syntax |
| `plugin doesn't exist` | Unavailable plugin on this cluster | Fall back to equivalent function or Python |
| `Expected string literal in datetime()` | Bare integer in datetime literal | Use `datetime(2024-01-01)` not `datetime(2024)` |
| `Unexpected token` after `by` | Complex expression in summarize by-clause | `extend` the expression first, then `summarize by` the column |
| `not recognized` / `unknown operator` | Operator not available on this engine | Check operator support; try equivalent (`order by` = `sort by`) |

## 11. Datetime Pitfalls

Datetime literals are a common source of errors. A wrong literal format can cascade into completely different approaches instead of fixing the small issue.

### Literal format
```kql
// ❌ WRONG — bare year is not a valid datetime
StormEvents | where StartTime > datetime(2007)

// ✅ RIGHT — always use full date format
StormEvents | where StartTime > datetime(2007-01-01)
```

### Filtering by year, month, or hour
```kql
// ❌ WRONG — comparing datetime column to integer
StormEvents | where StartTime == 2007

// ✅ RIGHT — use datetime_part() to extract components
StormEvents | where datetime_part("year", StartTime) == 2007

// ✅ ALSO RIGHT — use between with datetime range
StormEvents | where StartTime between (datetime(2007-01-01) .. datetime(2007-12-31T23:59:59))
```

### Time bucketing in summarize
```kql
// This works, but can be harder to read and reuse in complex queries
StormEvents | summarize count() by startofmonth(StartTime)

// Clearer — extend first, then summarize by the computed column
StormEvents
| extend Month = startofmonth(StartTime)
| summarize count() by Month
| order by Month asc
```

### Useful datetime functions
| Function | Purpose | Example |
|----------|---------|---------|
| `bin(ts, 1h)` | Round down to bucket boundary | `bin(Timestamp, 1d)` |
| `startofmonth(ts)` | First day of month | `startofmonth(Timestamp)` |
| `datetime_part("hour", ts)` | Extract component | `datetime_part("year", Timestamp)` |
| `format_datetime(ts, fmt)` | Format as string | `format_datetime(Timestamp, "yyyy-MM")` |
| `ago(1d)` | Relative time | `where Timestamp > ago(1d)` |
| `between(a .. b)` | Range filter (inclusive) | `where Timestamp between (datetime(2024-01-01) .. datetime(2024-01-31T23:59:59))` |
| `todatetime(str)` | Parse string → datetime | `todatetime("2024-01-15T10:30:00Z")` |
| `totimespan(str)` | Parse string → timespan | `totimespan("01:30:00")` |

## 12. Operator Naming & Equality

KQL has subtle differences from SQL syntax.

### Naming conventions

| Entity | Convention | Example |
|--------|-----------|---------|
| Tables | UpperCamelCase | `StormEvents`, `NetworkLogs` |
| Columns | UpperCamelCase | `StartTime`, `EventType` |
| Variables (`let`) | snake_case | `let filtered_events = ...` |
| Built-in functions | snake_case | `format_bytes()`, `geo_distance_2points()` |
| Stored functions | UpperCamelCase | `.create function GetTopUsers` |

### Equality operators
```kql
// In where clauses, == is case-sensitive, =~ is case-insensitive
StormEvents | where State == "TEXAS" | count        // exact match
StormEvents | where State =~ "texas" | count        // case-insensitive

// In joins, use == only
StormEvents | join kind=inner (PopulationData) on State
```

### sort vs order
Both `sort by` and `order by` work identically in KQL — they are aliases. Use whichever you prefer, but be consistent.

### contains vs has
```kql
// contains: substring match (slower)
StormEvents | where EventNarrative contains "tree"   // finds "trees", "treetop" too

// has: term/word match (faster, uses index)
StormEvents | where EventNarrative has "tree"        // matches word boundaries only

// For exact prefix/suffix
StormEvents | where EventType startswith "Thunder"
StormEvents | where Source endswith "Spotter"
```

## 13. Error Recovery Strategy

When a first KQL query fails, the temptation is to abandon the entire approach and try something completely different. The correct response is almost always to **fix the specific error**, not change strategy.

### The pattern to avoid
```
Query 1: extract(@"pattern", 1, col)  → Parse error
Query 2: todynamic(col)               → Different error  
Query 3: parse_json(col)              → Another error
Query 4: Python script                → Works but 10x tokens
```

### The correct pattern
```
Query 1: extract(@"pattern", 1, col)  → Parse error (bad escaping)
Query 2: extract(@"pattern", 1, col)  → Fix the specific escaping issue → Success
```

**Rules for error recovery:**
1. Read the error message carefully — it almost always tells you exactly what's wrong
2. Fix the **specific** syntax/escaping issue, don't switch approaches
3. Use the self-correction table (Section 10) to map errors to fixes
4. Only switch approaches after 2 failed fixes of the same query
5. The `parse` operator is often simpler than `extract()` for structured text:

```kql
// Instead of complex regex on TraceLogs:
// extract(@"file path: \"\"([^\"]+)\"\"", 1, Message)

// Use parse for structured extraction (try it on help cluster, SampleLogs db):
cluster("help").database("SampleLogs").TraceLogs
| where Message has "file path"
| parse Message with * "file path: \"\"" FilePath "\"\"" *
| project Timestamp, FilePath
| take 5
```

## 14. Query Writing Checklist

Before running any KQL query, mentally check:

1. **Pre-filtered?** Large tables have a `| where` before any `| summarize`
2. **Result bounded?** Exploratory queries end with `| take N` or `| top N`
3. **Dynamic columns cast?** Any dynamic column in `by`/`on`/`order by` is wrapped
4. **Regex has groups?** `extract_all` patterns have `()` around what you want to capture
5. **Join cardinality safe?** Both sides checked with `dcount()` before joining
6. **Needed columns only?** Wide tables get `| project` to drop unneeded columns
7. **Datetime literals valid?** Using `datetime(2024-01-01)` not `datetime(2024)` or bare integers
8. **Complex by-expressions?** Use `| extend` first, then `| summarize by` the computed column
9. **Error recovery plan?** If a query fails, fix the specific error — don't change strategy
