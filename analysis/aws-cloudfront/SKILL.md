---
name: aws-cloudfront
description: |
  Use when working with Aws Cloudfront — aWS CloudFront distribution analysis,
  cache hit ratio monitoring, origin health checks, invalidation management, and
  performance optimization. Covers distribution inventory, behavior
  configuration, SSL certificate status, geo-restriction, and real-time metrics.
connection_type: aws
preload: false
---

# AWS CloudFront Skill

Analyze AWS CloudFront distributions with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-cloudfront/` → CloudFront-specific analysis (distributions, caching, origins)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for dist_id in $distributions; do
  get_distribution_details "$dist_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List all distributions
list_distributions() {
  aws cloudfront list-distributions \
    --output text \
    --query 'DistributionList.Items[].[Id,DomainName,Status,Enabled,Origins.Items[0].DomainName]'
}

# Get distribution details
get_distribution_config() {
  local dist_id=$1
  aws cloudfront get-distribution --id "$dist_id" \
    --output text \
    --query 'Distribution.[Id,DomainName,Status,DistributionConfig.Enabled,DistributionConfig.DefaultCacheBehavior.ViewerProtocolPolicy]'
}

# Get cache hit ratio metrics
get_cache_hit_ratio() {
  local dist_id=$1 days=${2:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/CloudFront --metric-name CacheHitRate \
    --dimensions Name=DistributionId,Value="$dist_id" Name=Region,Value=Global \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Average \
    --output text --query 'Datapoints[0].Average'
}

# Get request count
get_request_count() {
  local dist_id=$1 days=${2:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/CloudFront --metric-name Requests \
    --dimensions Name=DistributionId,Value="$dist_id" Name=Region,Value=Global \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].Sum'
}

# List recent invalidations
list_invalidations() {
  local dist_id=$1
  aws cloudfront list-invalidations --distribution-id "$dist_id" \
    --max-items 10 \
    --output text \
    --query 'InvalidationList.Items[].[Id,CreateTime,Status]'
}
```

## Common Operations

### 1. Distribution Inventory with Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws cloudfront list-distributions \
  --output text \
  --query 'DistributionList.Items[].[Id,DomainName,Status,Enabled,HttpVersion,PriceClass,Origins.Quantity]'
```

### 2. Cache Performance Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
DISTS=$(aws cloudfront list-distributions --output text --query 'DistributionList.Items[].Id')
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")
for dist in $DISTS; do
  {
    hit_rate=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/CloudFront --metric-name CacheHitRate \
      --dimensions Name=DistributionId,Value="$dist" Name=Region,Value=Global \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    requests=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/CloudFront --metric-name Requests \
      --dimensions Name=DistributionId,Value="$dist" Name=Region,Value=Global \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tHitRate:%.1f%%\tRequests:%s\n" "$dist" "${hit_rate:-0}" "${requests:-0}"
  } &
done
wait
```

### 3. Origin Health Check

```bash
#!/bin/bash
export AWS_PAGER=""
DISTS=$(aws cloudfront list-distributions --output text --query 'DistributionList.Items[].Id')
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1d +"%Y-%m-%dT%H:%M:%S")
for dist in $DISTS; do
  {
    errors4xx=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/CloudFront --metric-name 4xxErrorRate \
      --dimensions Name=DistributionId,Value="$dist" Name=Region,Value=Global \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    errors5xx=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/CloudFront --metric-name 5xxErrorRate \
      --dimensions Name=DistributionId,Value="$dist" Name=Region,Value=Global \
      --start-time "$START" --end-time "$END" \
      --period 86400 --statistics Average \
      --output text --query 'Datapoints[0].Average')
    printf "%s\t4xx:%.2f%%\t5xx:%.2f%%\n" "$dist" "${errors4xx:-0}" "${errors5xx:-0}"
  } &
done
wait
```

### 4. SSL Certificate Expiry Check

```bash
#!/bin/bash
export AWS_PAGER=""
aws cloudfront list-distributions \
  --output text \
  --query 'DistributionList.Items[].[Id,DomainName,ViewerCertificate.CertificateSource,ViewerCertificate.Certificate]'
```

### 5. Invalidation History

```bash
#!/bin/bash
export AWS_PAGER=""
DISTS=$(aws cloudfront list-distributions --output text --query 'DistributionList.Items[].Id')
for dist in $DISTS; do
  aws cloudfront list-invalidations --distribution-id "$dist" --max-items 5 \
    --output text \
    --query "InvalidationList.Items[].[\"$dist\",Id,CreateTime,Status]" &
done
wait
```

## Anti-Hallucination Rules

1. **CloudFront metrics require Region=Global** - CloudFront metrics use `Region=Global` as a dimension, not a specific AWS region. Omitting this returns no data.
2. **Cache hit rate is a percentage** - CacheHitRate is 0-100, not 0-1. Do not multiply by 100.
3. **Invalidation costs money** - First 1000 paths/month are free, then $0.005/path. Do not create invalidations unnecessarily.
4. **Distribution deployment takes 15-20 min** - Status "InProgress" is normal after changes. Do not report this as an error.
5. **Price class affects edge locations** - PriceClass_All uses all edges. PriceClass_100/200 limits to cheaper regions. This affects latency.

## Output Format

Present results as a structured report:
```
Aws Cloudfront Report
═════════════════════
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

- **CloudFront API is us-east-1 only**: All CloudFront API calls go to us-east-1 regardless of your configured region.
- **Aliases vs DomainName**: The `DomainName` is the CloudFront domain (d123.cloudfront.net). Custom domains are in `Aliases`.
- **Behavior order matters**: CloudFront matches behaviors by path pattern in order. The default (*) behavior is the fallback.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Real-time metrics**: Standard CloudFront metrics have 1-minute granularity. Real-time metrics require additional configuration.
