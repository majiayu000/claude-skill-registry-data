---
name: aws-waf
description: |
  Use when working with Aws Waf — aWS WAF web ACL management, rule analysis,
  traffic metrics, and IP set management. Covers WAF rule group inspection,
  rate-based rule configuration, managed rule group analysis, logging status,
  and blocked request investigation.
connection_type: aws
preload: false
---

# AWS WAF Skill

Analyze AWS WAF web ACLs and rules with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-waf/` → WAF-specific analysis (web ACLs, rules, IP sets, logging)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for acl_id in $acl_ids; do
  get_web_acl_details "$acl_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List web ACLs (regional)
list_web_acls() {
  local scope=${1:-REGIONAL}
  aws wafv2 list-web-acls --scope "$scope" \
    --output text \
    --query 'WebACLs[].[Name,Id,ARN]'
}

# Get web ACL details
get_web_acl() {
  local name=$1 scope=$2 id=$3
  aws wafv2 get-web-acl --name "$name" --scope "$scope" --id "$id" \
    --output text \
    --query 'WebACL.[Name,DefaultAction,Rules[].Name]'
}

# List IP sets
list_ip_sets() {
  local scope=${1:-REGIONAL}
  aws wafv2 list-ip-sets --scope "$scope" \
    --output text \
    --query 'IPSets[].[Name,Id,ARN]'
}

# Get WAF metrics
get_waf_metrics() {
  local web_acl=$1 rule=$2 days=${3:-7}
  local end_time start_time
  end_time=$(date -u +"%Y-%m-%dT%H:%M:%S")
  start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%S")
  aws cloudwatch get-metric-statistics \
    --namespace AWS/WAFV2 --metric-name BlockedRequests \
    --dimensions Name=WebACL,Value="$web_acl" Name=Rule,Value="$rule" Name=Region,Value=us-east-1 \
    --start-time "$start_time" --end-time "$end_time" \
    --period $((days * 86400)) --statistics Sum \
    --output text --query 'Datapoints[0].Sum'
}

# List managed rule groups
list_managed_rule_groups() {
  local scope=${1:-REGIONAL}
  aws wafv2 list-available-managed-rule-groups --scope "$scope" \
    --output text \
    --query 'ManagedRuleGroups[].[VendorName,Name,Description]' | head -30
}
```

## Common Operations

### 1. Web ACL Inventory

```bash
#!/bin/bash
export AWS_PAGER=""
echo "=== REGIONAL Web ACLs ==="
aws wafv2 list-web-acls --scope REGIONAL \
  --output text \
  --query 'WebACLs[].[Name,Id,ARN]' &

echo "=== CLOUDFRONT Web ACLs ==="
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1 \
  --output text \
  --query 'WebACLs[].[Name,Id,ARN]' &
wait
```

### 2. Rule Analysis per Web ACL

```bash
#!/bin/bash
export AWS_PAGER=""
SCOPE=REGIONAL
ACLS=$(aws wafv2 list-web-acls --scope "$SCOPE" --output text --query 'WebACLs[].[Name,Id]')
echo "$ACLS" | while read name id; do
  aws wafv2 get-web-acl --name "$name" --scope "$SCOPE" --id "$id" \
    --output text \
    --query "WebACL.[Name,DefaultAction,VisibilityConfig.SampledRequestsEnabled,Rules[].[Name,Priority,Action,OverrideAction]]" &
done
wait
```

### 3. Blocked Request Metrics

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")
ACLS=$(aws wafv2 list-web-acls --scope REGIONAL --output text --query 'WebACLs[].Name')
for acl in $ACLS; do
  {
    blocked=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/WAFV2 --metric-name BlockedRequests \
      --dimensions Name=WebACL,Value="$acl" Name=Rule,Value=ALL \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    allowed=$(aws cloudwatch get-metric-statistics \
      --namespace AWS/WAFV2 --metric-name AllowedRequests \
      --dimensions Name=WebACL,Value="$acl" Name=Rule,Value=ALL \
      --start-time "$START" --end-time "$END" \
      --period 604800 --statistics Sum \
      --output text --query 'Datapoints[0].Sum')
    printf "%s\tAllowed:%s\tBlocked:%s\n" "$acl" "${allowed:-0}" "${blocked:-0}"
  } &
done
wait
```

### 4. IP Set Review

```bash
#!/bin/bash
export AWS_PAGER=""
SCOPE=REGIONAL
IP_SETS=$(aws wafv2 list-ip-sets --scope "$SCOPE" --output text --query 'IPSets[].[Name,Id]')
echo "$IP_SETS" | while read name id; do
  aws wafv2 get-ip-set --name "$name" --scope "$SCOPE" --id "$id" \
    --output text \
    --query "[Name,IPAddressVersion,length(Addresses)]" &
done
wait
```

### 5. Logging Configuration

```bash
#!/bin/bash
export AWS_PAGER=""
ACLS=$(aws wafv2 list-web-acls --scope REGIONAL --output text --query 'WebACLs[].ARN')
for arn in $ACLS; do
  {
    logging=$(aws wafv2 get-logging-configuration --resource-arn "$arn" \
      --output text \
      --query 'LoggingConfiguration.[ResourceArn,LogDestinationConfigs[0]]' 2>/dev/null || echo "$arn NO_LOGGING")
    printf "%s\n" "$logging"
  } &
done
wait
```

## Anti-Hallucination Rules

1. **WAFv2 vs WAF Classic** - Always use `wafv2` commands. WAF Classic (`waf` and `waf-regional`) is legacy. Do not mix APIs.
2. **Scope matters** - REGIONAL for ALB/API Gateway/AppSync. CLOUDFRONT for CloudFront distributions (must use us-east-1 region).
3. **Rule actions** - Valid actions: Allow, Block, Count, CAPTCHA, Challenge. Managed rule groups use OverrideAction (Count or None), not Action.
4. **Metric dimensions** - WAFv2 CloudWatch metrics require Region dimension even for REGIONAL scope. Use the actual AWS region, not "Global".
5. **Sampled requests** - WAF retains sampled requests for only 3 hours. For historical analysis, use WAF logging (to S3, CloudWatch Logs, or Kinesis).

## Output Format

Present results as a structured report:
```
Aws Waf Report
══════════════
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

- **CloudFront WAF region**: CLOUDFRONT-scoped web ACLs MUST be queried from us-east-1 region: `--region us-east-1`.
- **Lock token**: Update operations require a lock token from the get operation. Always fetch before modifying.
- **Rate-based rules**: Rate limits are evaluated per 5-minute window. A limit of 100 means 100 requests per 5 minutes per IP.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Managed rule group versions**: Managed rule groups auto-update by default. Pin versions for stability with `Version` parameter.
