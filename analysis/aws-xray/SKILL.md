---
name: aws-xray
description: |
  Use when working with Aws Xray — aWS X-Ray trace analysis, service map
  generation, fault and error analysis, sampling rule management, and latency
  investigation. Covers trace summaries, segment analysis, annotation-based
  filtering, and group configuration.
connection_type: aws
preload: false
---

# AWS X-Ray Skill

Analyze AWS X-Ray traces and service maps with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-xray/` → X-Ray-specific analysis (traces, service maps, sampling)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for group in $groups; do
  get_group_traces "$group" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# Get service graph (service map)
get_service_graph() {
  local hours=${1:-1}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$hours hours ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${hours}H +"%Y-%m-%dT%H:%M:%S")
  aws xray get-service-graph \
    --start-time "$start_time" --end-time "$end_time" \
    --output text \
    --query 'Services[].[Name,Type,State,SummaryStatistics.TotalCount,SummaryStatistics.FaultStatistics.TotalCount,SummaryStatistics.ErrorStatistics.TotalCount,ResponseTimeHistogram[0].Average]'
}

# Get trace summaries with filter
get_trace_summaries() {
  local filter=$1 hours=${2:-1}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$hours hours ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${hours}H +"%Y-%m-%dT%H:%M:%S")
  aws xray get-trace-summaries \
    --start-time "$start_time" --end-time "$end_time" \
    --filter-expression "$filter" \
    --output text \
    --query 'TraceSummaries[].[Id,Duration,HasFault,HasError,Http.HttpStatus,ResponseTime]' | head -20
}

# List sampling rules
list_sampling_rules() {
  aws xray get-sampling-rules \
    --output text \
    --query 'SamplingRuleRecords[].[SamplingRule.RuleName,SamplingRule.Priority,SamplingRule.FixedRate,SamplingRule.ReservoirSize,SamplingRule.ServiceName,SamplingRule.HTTPMethod,SamplingRule.URLPath]'
}

# List X-Ray groups
list_groups() {
  aws xray get-groups \
    --output text \
    --query 'Groups[].[GroupName,GroupARN,FilterExpression]'
}
```

## Common Operations

### 1. Service Map Overview

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
aws xray get-service-graph \
  --start-time "$START" --end-time "$END" \
  --output text \
  --query 'Services[].[Name,Type,SummaryStatistics.TotalCount,SummaryStatistics.FaultStatistics.TotalCount,SummaryStatistics.ErrorStatistics.TotalCount]'
```

### 2. Fault Analysis (5xx Errors)

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "6 hours ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-6H +"%Y-%m-%dT%H:%M:%S")
aws xray get-trace-summaries \
  --start-time "$START" --end-time "$END" \
  --filter-expression 'fault = true' \
  --output text \
  --query 'TraceSummaries[].[Id,Duration,Http.HttpStatus,Http.HttpURL,ResponseTime]' | head -20
```

### 3. Latency Investigation (Slow Traces)

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1H +"%Y-%m-%dT%H:%M:%S")
aws xray get-trace-summaries \
  --start-time "$START" --end-time "$END" \
  --filter-expression 'responsetime > 5' \
  --output text \
  --query 'TraceSummaries[].[Id,Duration,ResponseTime,Http.HttpURL]' | sort -k3 -rn | head -10
```

### 4. Sampling Rule Review

```bash
#!/bin/bash
export AWS_PAGER=""
aws xray get-sampling-rules \
  --output text \
  --query 'SamplingRuleRecords[].[SamplingRule.RuleName,SamplingRule.Priority,SamplingRule.FixedRate,SamplingRule.ReservoirSize,SamplingRule.ServiceName,SamplingRule.HTTPMethod,SamplingRule.URLPath,SamplingRule.Version]'
```

### 5. Error Rate by Service

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "6 hours ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-6H +"%Y-%m-%dT%H:%M:%S")
aws xray get-service-graph \
  --start-time "$START" --end-time "$END" \
  --output text \
  --query 'Services[].[Name,Type,SummaryStatistics.TotalCount,SummaryStatistics.FaultStatistics.TotalCount,SummaryStatistics.ErrorStatistics.TotalCount,SummaryStatistics.OkCount]' \
  | awk '{total=$3; faults=$4; errors=$5; if(total>0) printf "%s\t%s\tTotal:%s\tFaultRate:%.2f%%\tErrorRate:%.2f%%\n", $1, $2, total, faults/total*100, errors/total*100}'
```

## Anti-Hallucination Rules

1. **Fault vs Error** - In X-Ray, a fault is a 5xx server error. An error is a 4xx client error. Throttle is a 429 specifically. Do not conflate them.
2. **Filter expression syntax** - X-Ray uses its own filter expression syntax, NOT JMESPath. Use `service()`, `annotation.key`, `responsetime`, `fault`, `error` keywords.
3. **Trace retention** - X-Ray retains trace data for 30 days. Trace summaries are available for 30 days. Full trace data beyond this requires export to S3.
4. **Service graph time range** - Maximum time range for `get-service-graph` is 6 hours per call. For longer periods, make multiple calls and aggregate.
5. **Sampling affects completeness** - X-Ray samples traces. A 5% sampling rate means you see ~5% of actual requests. Do not report trace counts as request counts.

## Output Format

Present results as a structured report:
```
Aws Xray Report
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

- **Time range limits**: `get-trace-summaries` supports up to 6 hours per call. For longer analysis, paginate across time windows.
- **Group filter expressions**: Groups filter traces server-side. Different groups may show different subsets of the same traces.
- **Segment documents**: Full trace details require `batch-get-traces` with specific trace IDs. `get-trace-summaries` is a lightweight summary.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Active tracing vs passive**: Active tracing (X-Ray SDK) sends traces. Passive tracing (downstream services) only records if upstream sends trace headers.
