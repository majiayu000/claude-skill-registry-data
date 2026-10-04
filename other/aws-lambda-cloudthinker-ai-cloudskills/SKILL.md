---
name: aws-lambda
description: |
  Use when working with Aws Lambda — aWS Lambda function analysis, invocation
  metrics, cold start analysis, layer management, and concurrency tracking.
  Covers function configuration review, error rate analysis, duration
  percentiles, provisioned concurrency utilization, and deployment package
  optimization.
connection_type: aws
preload: false
---

# AWS Lambda Skill

Analyze AWS Lambda functions with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-lambda/` → Lambda-specific analysis (functions, layers, concurrency)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

# CORRECT: Parallel metric fetching
for func in $functions; do
  get_lambda_metrics "$func" &
done
wait
```

**FORBIDDEN**: Sequential loops like `for func in $functions; do aws lambda get-function "$func"; done`

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List all Lambda functions with key details
list_lambda_functions() {
  aws lambda list-functions \
    --output text \
    --query 'Functions[].[FunctionName,Runtime,MemorySize,Timeout,CodeSize,LastModified]'
}

# Get function configuration and state
get_function_config() {
  local func_name=$1
  aws lambda get-function-configuration \
    --function-name "$func_name" \
    --output text \
    --query '[FunctionName,Runtime,MemorySize,Timeout,State,LastUpdateStatus,Handler,CodeSize,Architectures[0]]'
}

# Get invocation metrics for a function (last N days)
get_invocation_metrics() {
  local func_name=$1 days=${2:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")

  aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Invocations \
    --dimensions Name=FunctionName,Value="$func_name" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].[Sum]' &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Errors \
    --dimensions Name=FunctionName,Value="$func_name" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].[Sum]' &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Duration \
    --dimensions Name=FunctionName,Value="$func_name" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Average Maximum \
    --output text --query 'Datapoints[0].[Average,Maximum]' &

  aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name Throttles \
    --dimensions Name=FunctionName,Value="$func_name" \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].[Sum]' &

  wait
}

# Get concurrent executions
get_concurrency_metrics() {
  local func_name=$1 days=${2:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")

  aws cloudwatch get-metric-statistics \
    --namespace AWS/Lambda \
    --metric-name ConcurrentExecutions \
    --dimensions Name=FunctionName,Value="$func_name" \
    --start-time "$start_time" --end-time "$end_time" \
    --period 3600 --statistics Maximum \
    --output text --query 'Datapoints[*].[Timestamp,Maximum]' \
    | sort -k1 | tail -10
}

# List layers for a function
get_function_layers() {
  local func_name=$1
  aws lambda get-function-configuration \
    --function-name "$func_name" \
    --output text \
    --query 'Layers[].[Arn,CodeSize]'
}
```

## Common Operations

### 1. Function Inventory with Runtime Distribution

```bash
#!/bin/bash
export AWS_PAGER=""
aws lambda list-functions \
  --output text \
  --query 'Functions[].[Runtime]' \
  | sort | uniq -c | sort -rn
```

### 2. Cold Start Analysis (Init Duration)

```bash
#!/bin/bash
export AWS_PAGER=""
# Query CloudWatch Logs Insights for init durations
FUNCTIONS=$(aws lambda list-functions --output text --query 'Functions[].FunctionName')
for func in $FUNCTIONS; do
  aws logs filter-log-events \
    --log-group-name "/aws/lambda/$func" \
    --filter-pattern "REPORT" \
    --start-time $(($(date +%s) - 86400))000 \
    --max-items 50 \
    --output text \
    --query 'events[].message' \
    | grep -o 'Init Duration: [0-9.]*' | head -5 &
done
wait
```

### 3. Error Rate Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
FUNCTIONS=$(aws lambda list-functions --output text --query 'Functions[].FunctionName')
for func in $FUNCTIONS; do
  {
    invocations=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/Lambda --metric-name Invocations \
      --dimensions Name=FunctionName,Value="$func" \
      --start-time "$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -v-7d +%Y-%m-%dT%H:%M:%S)" \
      --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    errors=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/Lambda --metric-name Errors \
      --dimensions Name=FunctionName,Value="$func" \
      --start-time "$(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S 2>/dev/null || date -u -v-7d +%Y-%m-%dT%H:%M:%S)" \
      --end-time "$(date -u +%Y-%m-%dT%H:%M:%S)" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\t%s\t%s\n" "$func" "${invocations:-0}" "${errors:-0}"
  } &
done
wait
```

### 4. Layer Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
aws lambda list-layers --output text \
  --query 'Layers[].[LayerName,LatestMatchingVersion.Version,LatestMatchingVersion.CompatibleRuntimes[0]]'
```

### 5. Provisioned Concurrency Status

```bash
#!/bin/bash
export AWS_PAGER=""
FUNCTIONS=$(aws lambda list-functions --output text --query 'Functions[].FunctionName')
for func in $FUNCTIONS; do
  aws lambda list-provisioned-concurrency-configs \
    --function-name "$func" \
    --output text \
    --query "ProvisionedConcurrencyConfigs[].[\"$func\",RequestedProvisionedConcurrentExecutions,AvailableProvisionedConcurrentExecutions,AllocatedProvisionedConcurrentExecutions,Status]" 2>/dev/null &
done
wait
```

## Anti-Hallucination Rules

1. **Never guess runtimes** - Always query `list-functions` to get actual runtime values. Valid runtimes change over time.
2. **Duration != Cold Start** - `Duration` metric is execution time only. Cold start is `Init Duration` from REPORT logs. Do not conflate them.
3. **Memory != Allocated Memory** - `MemorySize` is configured max. Actual usage requires CloudWatch `max_memory_used` from REPORT logs.
4. **Throttles != Errors** - Throttled invocations are NOT counted as errors. They are separate metrics.
5. **CodeSize is compressed** - The `CodeSize` field is the deployment package size (zip), not uncompressed code size.

## Output Format

Present results as a structured report:
```
Aws Lambda Report
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

- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum` (NOT `Average,Maximum`)
- **Log group naming**: Lambda log groups follow `/aws/lambda/{function-name}` convention. Do not guess other patterns.
- **Concurrent execution limits**: Account default is 1000. Check with `aws lambda get-account-settings`.
- **Qualifier matters**: When checking aliases/versions, always specify `--qualifier`. Unqualified calls go to `$LATEST`.
- **ARM vs x86**: Check `Architectures` field. arm64 functions have different pricing. Do not assume x86_64.
