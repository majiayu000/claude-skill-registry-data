---
name: azure-kusto
description: >
  Write and optimize Kusto Query Language (KQL) for Azure Data Explorer, Log Analytics, and monitoring workflows.
  Use this skill when users ask for KQL queries, telemetry analysis, incident investigation, or query optimization.
compatibility:
  models: [any-llm]
  cloud: azure
  language: kql
  tools: [log-analytics, data-explorer, appinsights]
---

# Azure Kusto

Produce clear, performant KQL queries for diagnostics, reporting, operational insights, and incident investigations.

## Use This Skill When

- The user asks to write a KQL query for diagnostics or reporting
- The user needs query optimization or performance tuning
- The user is investigating incidents using Azure logs
- The user wants to aggregate telemetry, analyze trends, or build alerts

## Context: Query Maturity

**Immature**: Ad hoc queries, unbounded scans, timeouts  
**Developing**: Filtered queries, basic aggregation  
**Managed**: Optimized execution, good performance, reusable queries → **Target**  
**Optimized**: Query compilation caching, materialized views, automated insights

## Required Inputs

- **Data source**: Azure Monitor (Log Analytics), Application Insights, Data Explorer?
- **Table names**: Exact names (AzureActivity, SecurityEvent, CustomEvents)?
- **Time range**: Last hour? Last 7 days? Specific dates?
- **Filters**: Specific resources, servers, error codes, user IDs?
- **Output needed**: Row count? Aggregation? Time series chart? Alert condition?
- **Performance constraints**: Must complete in 5 seconds? 30 seconds OK?

## Decision Tree

```
What's the primary objective?
├─ Count/summarize → Use summarize operator, aggregate early
├─ Find specific records → Use where filter first, then project
├─ Time-series analysis → Use bin(timestamp), render timechart
├─ Correlation/join → Join multiple tables, but use small left table
└─ Alert condition → Simple condition with threshold

What's the expected data volume?
├─ < 1 million rows → Simple query, no optimization needed
├─ 1-100 million rows → Filter early, use summarize
└─ > 100 million rows → Partition by time, use external tools

How fast does this need to run?
├─ <5 seconds (dashboard) → Aggressive filtering, pre-aggregation
├─ <30 seconds (report) → Standard optimization
└─ <5 minutes (batch analysis) → Can be less optimized
```

## Workflow

### Phase 1: Start with Schema Understanding

1. **Know your tables**:
   ```kql
   // Azure Monitor / Log Analytics tables
   AzureActivity       // Azure Control Plane events (Create, Delete, Update)
   SecurityEvent       // Windows Security logs (logins, privilege escalation)
   Syslog              // Linux syslog entries
   CommonSecurityLog   // Third-party firewall, IDS logs
   StorageBlob         // Azure Storage access logs
   AppServiceHTTPLogs  // App Service HTTP requests
   
   // Application Insights tables
   customEvents        // App-generated events
   pageViews           // Web page navigation
   requests            // HTTP requests (API calls)
   dependencies        // External service calls (DB, HTTP)
   exceptions          // Application exceptions
   traces              // Custom telemetry (logging)
   performance         // Performance counters (CPU, memory)
   ```

2. **Inspect schema**:
   ```kql
   // See columns and types
   SecurityEvent | getschema
   
   // Output
   ColumnName             ColumnType
   TimeGenerated          datetime
   Computer              string
   Account               string
   EventID               int
   Activity              string
   LogonType             int
   ```

### Phase 2: Query Construction (Simple → Complex)

1. **Basic query** (single table, filter):
   ```kql
   // Find all failed logins in last 24 hours
   SecurityEvent
   | where TimeGenerated > ago(24h)
   | where Activity == "Failed"
   | project TimeGenerated, Computer, Account, LogonType
   ```

2. **Add aggregation**:
   ```kql
   // Count failed logins by computer
   SecurityEvent
   | where TimeGenerated > ago(24h)
   | where Activity == "Failed"
   | summarize FailureCount = count() by Computer
   | sort by FailureCount desc
   ```

3. **Add time-series**:
   ```kql
   // Failed logins over time (hourly)
   SecurityEvent
   | where TimeGenerated > ago(7d)
   | where Activity == "Failed"
   | summarize FailureCount = count() by bin(TimeGenerated, 1h), Computer
   | render timechart
   ```

4. **Join multiple tables**:
   ```kql
   // Correlate failed logins with failed API requests
   SecurityEvent
   | where Activity == "Failed"
   | join (
       AppServiceHTTPLogs
       | where HttpStatus >= 400
       | project TimeGenerated, UserId, HttpStatus
   ) on $left.Account == $right.UserId
   | project TimeGenerated, Account, HttpStatus
   ```

### Phase 3: Performance Optimization

1. **Filter early** (most important):
   ```kql
   // ✓ GOOD: Filter first (scans 1000 rows)
   SecurityEvent
   | where TimeGenerated > ago(1h)           // Filters by time (fast)
   | where Computer == "server-prod-1"      // Filters by resource
   | where Activity == "Failed"              // Filters by value
   | summarize count()
   
   // ✗ BAD: Filter late (scans 10 million rows, then filters)
   SecurityEvent
   | summarize count() by Activity          // Aggregates all rows first
   | where Activity == "Failed"             // Then filters (slow!)
   ```

2. **Project only needed columns**:
   ```kql
   // ✓ GOOD: Get 3 columns (small result set)
   SecurityEvent | project TimeGenerated, Account, Activity | count
   
   // ✗ BAD: Get all columns (large result set)
   SecurityEvent | count
   ```

3. **Avoid N:N joins**:
   ```kql
   // ✗ BAD: Cartesian product (10K × 10K = 100M rows)
   SecurityEvent
   | join AppServiceHTTPLogs on Computer == ServerName  // Many matches per row
   
   // ✓ GOOD: One-to-many join (dimension table small)
   SecurityEvent
   | join kind=leftouter (
       Resources                            // Small reference table
       | project ResourceId, Owner
   ) on Computer == ResourceId
   ```

4. **Use summarize instead of distinct**:
   ```kql
   // ✗ SLOWER: Get all rows, then dedup
   SecurityEvent | distinct Account
   
   // ✓ FASTER: Aggregate by key
   SecurityEvent | summarize by Account
   ```

### Phase 4: Common Query Patterns

1. **Failed authentication analysis**:
   ```kql
   // Find brute-force attacks (5+ failures in 5 min per account)
   SecurityEvent
   | where TimeGenerated > ago(7d)
   | where Activity == "Failed"
   | summarize FailureCount = count() by Account, bin(TimeGenerated, 5m)
   | where FailureCount >= 5
   | project TimeGenerated, Account, FailureCount
   | sort by FailureCount desc
   ```

2. **API performance analysis**:
   ```kql
   // Response time percentiles by endpoint
   requests
   | where TimeGenerated > ago(24h)
   | summarize 
       p50 = percentile(duration, 50),
       p95 = percentile(duration, 95),
       p99 = percentile(duration, 99),
       failureRate = todouble(sum(resultCode >= 400)) / count() * 100
     by name
   | project 
       EndPoint = name,
       P50_ms = p50,
       P95_ms = p95,
       P99_ms = p99,
       FailureRate_pct = failureRate
   | sort by P99_ms desc
   ```

3. **Error spike detection**:
   ```kql
   // Errors today vs. yesterday (baseline comparison)
   let today = exceptions
     | where TimeGenerated > ago(24h)
     | summarize ErrorCount = count() by bin(TimeGenerated, 1h), type;
   let yesterday = exceptions
     | where TimeGenerated between(ago(48h) .. ago(24h))
     | summarize ErrorCount = count() by bin(TimeGenerated, 1h), type;
   today
   | join yesterday on type
   | extend Spike = (ErrorCount < ErrorCount1) ? "Normal" : "SPIKE"
   | where Spike == "SPIKE"
   ```

4. **Dependency failures (DB, external API)**:
   ```kql
   // Calls to external service failing
   dependencies
   | where TimeGenerated > ago(1h)
   | where type == "HTTP" or type == "SQL"
   | summarize 
       TotalCalls = count(),
       FailedCalls = sum(success == false),
       P95_ms = percentile(duration, 95)
     by target, type
   | extend FailureRate_pct = (FailedCalls / TotalCalls) * 100
   | where FailureRate_pct > 5  // Alert if >5% failure
   ```

5. **Cost analysis** (query efficiency):
   ```kql
   // Data ingestion volume by table (for cost management)
   union withsource=TableName *
   | where TimeGenerated > ago(1d)
   | summarize bytes = sum(estimate_data_size(*)) by TableName
   | extend GB = bytes / (1024 * 1024 * 1024)
   | sort by GB desc
   | render barchart
   ```

### Phase 5: Query Testing & Validation

1. **Test with time range**:
   ```kql
   // Check query on small time window first
   SecurityEvent
   | where TimeGenerated > ago(1h)  // Test 1 hour
   | summarize count()
   
   // Expand after validation
   | where TimeGenerated > ago(30d) // Now query 30 days
   ```

2. **Check for null values**:
   ```kql
   // Missing or unexpected data
   SecurityEvent
   | where TimeGenerated > ago(24h)
   | where isempty(Account) or isnan(LogonType)
   | count
   ```

3. **Validate result reasonableness**:
   ```
   Query: Failed logins per hour
   Expected: 100-500 per hour on typical day
   Got: 50M rows
   → Issue: Likely a join explosion or missing filter
   ```

### Phase 6: Advanced Patterns

1. **Anomaly detection** (using ML):
   ```kql
   // Automatic anomaly in request latency
   requests
   | where TimeGenerated > ago(7d)
   | where isnotempty(duration)
   | summarize RequestCount = count(), AvgDuration = avg(duration) 
       by bin(TimeGenerated, 1h), name
   | render anomalychart
   ```

2. **Materialized views** (pre-aggregate for speed):
   ```kql
   // Define view once
   .create materialized-view HourlyErrors as
   SecurityEvent
   | where Activity == "Failed"
   | summarize FailureCount = count() by bin(TimeGenerated, 1h), Computer
   
   // Query pre-aggregated view (very fast)
   HourlyErrors
   | where TimeGenerated > ago(7d)
   ```

## Output Contract

1. **Query Code**
   - KQL syntax (ready to copy-paste into Azure Portal)
   - Documented with comments explaining each step

2. **Query Explanation**
   - What data is queried?
   - What filters are applied?
   - What output is returned?
   - Expected result size?

3. **Performance Notes**
   - Query execution time estimate
   - Data volume scanned
   - Optimization tips if applicable

4. **Optional Variants**
   - Time range variations (1 day, 7 days, 30 days)
   - Alternative filters (by resource, error code, user)
   - Alert condition (if/then thresholds)

## Guardrails

- **State assumptions when schema is unknown**: "I'm assuming table X has column Y; please verify."
- **Prefer readable composition over dense one-liners**: Use clear variable names, line breaks.
- **Avoid unbounded scans**: Always include time filter (TimeGenerated > ago(X)).
- **Test on small time ranges first**: Verify query before running on 90-day data.
- **Project early**: Remove unnecessary columns to reduce result size and latency.
- **Filter before join**: Minimize left table size to prevent memory issues.
- **Monitor for cost**: Large data volumes in Log Analytics cost money per GB ingested.
