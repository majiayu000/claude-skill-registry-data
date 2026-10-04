---
name: aws-athena
description: |
  Use when working with Aws Athena — aWS Athena query execution analysis,
  workgroup management, Data Catalog integration, and cost-per-query tracking.
  Covers query history, performance optimization, workgroup quota management,
  saved queries, and data scanned analysis.
connection_type: aws
preload: false
---

# AWS Athena Skill

Analyze AWS Athena queries and workgroups with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-athena/` → Athena-specific analysis (queries, workgroups, cost tracking)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)
- `aws-glue/` → Data Catalog (databases, tables, partitions)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for workgroup in $workgroups; do
  get_workgroup_details "$workgroup" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List workgroups
list_workgroups() {
  aws athena list-work-groups \
    --output text \
    --query 'WorkGroups[].[Name,State,Description]'
}

# Get workgroup details
get_workgroup() {
  local workgroup=$1
  aws athena get-work-group --work-group "$workgroup" \
    --output text \
    --query 'WorkGroup.[Name,State,Configuration.ResultConfiguration.OutputLocation,Configuration.EnforceWorkGroupConfiguration,Configuration.BytesScannedCutoffPerQuery,Configuration.EngineVersion.SelectedEngineVersion]'
}

# List recent query executions
list_query_executions() {
  local workgroup=$1 max=${2:-20}
  local query_ids
  query_ids=$(aws athena list-query-executions --work-group "$workgroup" --max-results "$max" \
    --output text --query 'QueryExecutionIds[]')
  [ -z "$query_ids" ] && return
  aws athena batch-get-query-execution --query-execution-ids $query_ids \
    --output text \
    --query 'QueryExecutions[].[QueryExecutionId,Query,Status.State,Statistics.DataScannedInBytes,Statistics.EngineExecutionTimeInMillis,Status.SubmissionDateTime]' | head -20
}

# Get query execution details
get_query_execution() {
  local query_id=$1
  aws athena get-query-execution --query-execution-id "$query_id" \
    --output text \
    --query 'QueryExecution.[QueryExecutionId,Status.State,Statistics.DataScannedInBytes,Statistics.EngineExecutionTimeInMillis,Statistics.TotalExecutionTimeInMillis,ResultConfiguration.OutputLocation]'
}

# List named queries
list_named_queries() {
  local workgroup=$1
  local query_ids
  query_ids=$(aws athena list-named-queries --work-group "$workgroup" \
    --output text --query 'NamedQueryIds[]')
  [ -z "$query_ids" ] && return
  aws athena batch-get-named-query --named-query-ids $query_ids \
    --output text \
    --query 'NamedQueries[].[NamedQueryId,Name,Database,Description]'
}
```

## Common Operations

### 1. Workgroup Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
WORKGROUPS=$(aws athena list-work-groups --output text --query 'WorkGroups[].Name')
for wg in $WORKGROUPS; do
  aws athena get-work-group --work-group "$wg" \
    --output text \
    --query 'WorkGroup.[Name,State,Configuration.ResultConfiguration.OutputLocation,Configuration.BytesScannedCutoffPerQuery,Configuration.EngineVersion.SelectedEngineVersion]' &
done
wait
```

### 2. Query Cost Analysis (Data Scanned)

```bash
#!/bin/bash
export AWS_PAGER=""
WORKGROUP=${1:-primary}
QUERY_IDS=$(aws athena list-query-executions --work-group "$WORKGROUP" --max-results 50 \
  --output text --query 'QueryExecutionIds[]')
[ -z "$QUERY_IDS" ] && echo "No queries found" && exit 0
aws athena batch-get-query-execution --query-execution-ids $QUERY_IDS \
  --output text \
  --query 'QueryExecutions[].[QueryExecutionId,Status.State,Statistics.DataScannedInBytes,Statistics.EngineExecutionTimeInMillis]' \
  | awk '{scanned_gb=$3/1073741824; cost=scanned_gb*5; printf "%s\t%s\t%.3f_GB\t$%.4f\t%d_ms\n", $1, $2, scanned_gb, cost, $4}' \
  | sort -t$'\t' -k3 -rn | head -20
```

### 3. Failed Query Investigation

```bash
#!/bin/bash
export AWS_PAGER=""
WORKGROUP=${1:-primary}
QUERY_IDS=$(aws athena list-query-executions --work-group "$WORKGROUP" --max-results 50 \
  --output text --query 'QueryExecutionIds[]')
[ -z "$QUERY_IDS" ] && exit 0
aws athena batch-get-query-execution --query-execution-ids $QUERY_IDS \
  --output text \
  --query 'QueryExecutions[?Status.State==`FAILED`].[QueryExecutionId,Status.StateChangeReason,Status.SubmissionDateTime,Query]' | head -10
```

### 4. Workgroup Quota and Limits

```bash
#!/bin/bash
export AWS_PAGER=""
WORKGROUPS=$(aws athena list-work-groups --output text --query 'WorkGroups[].Name')
for wg in $WORKGROUPS; do
  aws athena get-work-group --work-group "$wg" \
    --output text \
    --query "WorkGroup.[Name,State,Configuration.BytesScannedCutoffPerQuery,Configuration.EnforceWorkGroupConfiguration,Configuration.RequesterPaysEnabled]" &
done
wait
```

### 5. Data Catalog Database and Table Summary

```bash
#!/bin/bash
export AWS_PAGER=""
CATALOG=${1:-AwsDataCatalog}
DATABASES=$(aws athena list-databases --catalog-name "$CATALOG" \
  --output text --query 'DatabaseList[].Name')
for db in $DATABASES; do
  {
    table_count=$(aws athena list-table-metadata --catalog-name "$CATALOG" --database-name "$db" \
      --output text --query 'length(TableMetadataList)' 2>/dev/null)
    printf "%s\tTables:%s\n" "$db" "${table_count:-0}"
  } &
done
wait
```

## Anti-Hallucination Rules

1. **Pricing is per data scanned** - Athena charges $5 per TB of data scanned. Minimum charge is 10 MB per query. Cancelled queries are charged for data scanned before cancellation.
2. **batch-get-query-execution limit** - Maximum 50 query IDs per `batch-get-query-execution` call. Chunk larger lists.
3. **Engine versions** - Athena engine version 2 uses Presto. Engine version 3 uses Trino. Query syntax differences exist between versions.
4. **Workgroup isolation** - Workgroups can enforce result location, encryption, and data scan limits. `EnforceWorkGroupConfiguration=true` overrides per-query settings.
5. **Query results in S3** - Athena writes query results to S3. These results accumulate and incur S3 storage costs. Clean up periodically.

## Output Format

Present results as a structured report:
```
Aws Athena Report
═════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **CTAS/INSERT INTO**: CREATE TABLE AS SELECT and INSERT INTO write data to S3. This incurs both Athena query charges AND S3 storage costs.
- **Partitioning reduces cost**: Queries on partitioned tables only scan relevant partitions. Always WHERE-filter on partition columns.
- **Data format matters**: Columnar formats (Parquet, ORC) scan less data than CSV/JSON. Compression (Snappy, ZSTD) further reduces scan.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Named queries are not cached results**: Named queries are saved SQL templates, not cached results. Each execution scans data again.
