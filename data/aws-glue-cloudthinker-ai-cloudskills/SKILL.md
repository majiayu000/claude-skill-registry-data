---
name: aws-glue
description: |
  Use when working with Aws Glue — aWS Glue crawler management, ETL job run
  analysis, Data Catalog exploration, and schema registry management. Covers
  crawler schedules, job performance metrics, database and table inventory,
  partition analysis, and connection health.
connection_type: aws
preload: false
---

# AWS Glue Skill

Analyze AWS Glue ETL jobs and Data Catalog with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-glue/` → Glue-specific analysis (crawlers, jobs, catalog, schema registry)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for job in $jobs; do
  get_job_runs "$job" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List Glue jobs
list_jobs() {
  aws glue get-jobs \
    --output text \
    --query 'Jobs[].[Name,Command.Name,GlueVersion,MaxCapacity,WorkerType,NumberOfWorkers,LastModifiedOn]'
}

# Get recent job runs
get_job_runs() {
  local job_name=$1 max=${2:-10}
  aws glue get-job-runs --job-name "$job_name" --max-results "$max" \
    --output text \
    --query 'JobRuns[].[JobName,JobRunState,StartedOn,CompletedOn,ExecutionTime,MaxCapacity,WorkerType,NumberOfWorkers,ErrorMessage]'
}

# List crawlers
list_crawlers() {
  aws glue get-crawlers \
    --output text \
    --query 'Crawlers[].[Name,State,Schedule.ScheduleExpression,LastCrawl.Status,LastCrawl.StartTime,DatabaseName]'
}

# List databases in Data Catalog
list_databases() {
  aws glue get-databases \
    --output text \
    --query 'DatabaseList[].[Name,CreateTime,LocationUri]'
}

# List tables in a database
list_tables() {
  local database=$1
  aws glue get-tables --database-name "$database" \
    --output text \
    --query 'TableList[].[Name,TableType,StorageDescriptor.InputFormat,StorageDescriptor.Location,UpdateTime]' | head -30
}

# Get table details
get_table() {
  local database=$1 table=$2
  aws glue get-table --database-name "$database" --name "$table" \
    --output text \
    --query 'Table.[Name,TableType,StorageDescriptor.InputFormat,StorageDescriptor.Location,StorageDescriptor.Columns[].Name,PartitionKeys[].Name]'
}

# List connections
list_connections() {
  aws glue get-connections \
    --output text \
    --query 'ConnectionList[].[Name,ConnectionType,CreationTime,LastUpdatedTime]'
}
```

## Common Operations

### 1. Job Inventory with Last Run Status

```bash
#!/bin/bash
export AWS_PAGER=""
JOBS=$(aws glue get-jobs --output text --query 'Jobs[].Name')
for job in $JOBS; do
  aws glue get-job-runs --job-name "$job" --max-results 1 \
    --output text \
    --query "JobRuns[].[\"$job\",JobRunState,StartedOn,ExecutionTime,ErrorMessage]" &
done
wait
```

### 2. Crawler Health and Schedule

```bash
#!/bin/bash
export AWS_PAGER=""
aws glue get-crawlers \
  --output text \
  --query 'Crawlers[].[Name,State,Schedule.ScheduleExpression,LastCrawl.Status,LastCrawl.StartTime,LastCrawl.LogGroup,DatabaseName]'
```

### 3. Job Failure Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
JOBS=$(aws glue get-jobs --output text --query 'Jobs[].Name')
for job in $JOBS; do
  aws glue get-job-runs --job-name "$job" --max-results 5 \
    --output text \
    --query "JobRuns[?JobRunState=='FAILED'].[\"$job\",JobRunState,StartedOn,ExecutionTime,ErrorMessage]" &
done
wait
```

### 4. Data Catalog Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
DATABASES=$(aws glue get-databases --output text --query 'DatabaseList[].Name')
for db in $DATABASES; do
  {
    table_count=$(aws glue get-tables --database-name "$db" --output text --query 'length(TableList)')
    printf "%s\tTables:%s\n" "$db" "$table_count"
  } &
done
wait
```

### 5. Job Performance Trends

```bash
#!/bin/bash
export AWS_PAGER=""
JOB_NAME=$1
aws glue get-job-runs --job-name "$JOB_NAME" --max-results 20 \
  --output text \
  --query 'JobRuns[].[StartedOn,JobRunState,ExecutionTime,MaxCapacity,DPUSeconds]' | sort -k1
```

## Anti-Hallucination Rules

1. **DPU vs Workers** - Older Glue jobs use `MaxCapacity` (DPU count). Newer jobs use `WorkerType` + `NumberOfWorkers`. These are mutually exclusive configurations.
2. **Worker types** - Valid values: Standard (default), G.1X (1 DPU per worker), G.2X (2 DPU per worker), G.025X (0.25 DPU). Do not invent other types.
3. **Job run states** - STARTING, RUNNING, STOPPING, STOPPED, SUCCEEDED, FAILED, TIMEOUT, ERROR, WAITING. Do not fabricate states.
4. **Crawler vs Job** - Crawlers populate the Data Catalog (schema discovery). Jobs perform ETL transformations. They are separate resources.
5. **Partition keys** - Glue Data Catalog partitions map to physical directories in S3 (e.g., `year=2024/month=01/`). Partitions reduce data scanned by Athena.

## Output Format

Present results as a structured report:
```
Aws Glue Report
═══════════════
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

- **DPU pricing**: Glue charges per DPU-hour. Standard worker = 1 DPU ($0.44/hour). G.2X = 2 DPU per worker ($0.88/hour per worker).
- **Job bookmarks**: Enable job bookmarks to avoid reprocessing data. If disabled, jobs reprocess all data each run.
- **Crawler classification**: Crawlers may misclassify data formats. Verify table schemas in the Data Catalog after crawling.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Schema registry**: Glue Schema Registry is separate from the Data Catalog. It provides schema versioning for streaming data (Kinesis, Kafka).
