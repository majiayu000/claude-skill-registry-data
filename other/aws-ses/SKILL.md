---
name: aws-ses
description: |
  Use when working with Aws Ses — aWS SES sending statistics, bounce and
  complaint rate analysis, identity management, configuration set monitoring,
  and deliverability tracking. Covers sending quota utilization, suppression
  list management, DKIM/SPF status, and reputation dashboard metrics.
connection_type: aws
preload: false
---

# AWS SES Skill

Analyze AWS SES email sending with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-ses/` → SES-specific analysis (identities, sending stats, bounce rates)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for identity in $identities; do
  get_identity_details "$identity" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# Get sending quota and statistics
get_send_quota() {
  aws sesv2 get-account \
    --output text \
    --query '[SendQuota.Max24HourSend,SendQuota.MaxSendRate,SendQuota.SentLast24Hours,SendingEnabled,ProductionAccessEnabled]'
}

# List email identities
list_identities() {
  aws sesv2 list-email-identities \
    --output text \
    --query 'EmailIdentities[].[IdentityType,IdentityName,SendingEnabled]'
}

# Get identity verification details
get_identity_details() {
  local identity=$1
  aws sesv2 get-email-identity --email-identity "$identity" \
    --output text \
    --query '[IdentityType,VerifiedForSendingStatus,DkimAttributes.Status,DkimAttributes.SigningEnabled]'
}

# List configuration sets
list_config_sets() {
  aws sesv2 list-configuration-sets \
    --output text \
    --query 'ConfigurationSets[]'
}

# Get configuration set details
get_config_set_details() {
  local config_set=$1
  aws sesv2 get-configuration-set --configuration-set-name "$config_set" \
    --output text \
    --query '[ConfigurationSetName,DeliveryOptions.SendingPoolName,ReputationOptions.ReputationMetricsEnabled,SendingOptions.SendingEnabled]'
}

# Get suppressed destinations
list_suppressed() {
  local reason=${1:-""}
  local reason_filter=""
  [ -n "$reason" ] && reason_filter="--reasons $reason"
  aws sesv2 list-suppressed-destinations $reason_filter \
    --output text \
    --query 'SuppressedDestinationSummaries[].[EmailAddress,Reason,LastUpdateTime]' | head -20
}
```

## Common Operations

### 1. Account Sending Overview

```bash
#!/bin/bash
export AWS_PAGER=""
aws sesv2 get-account \
  --output text \
  --query '[SendQuota.Max24HourSend,SendQuota.MaxSendRate,SendQuota.SentLast24Hours,SendingEnabled,ProductionAccessEnabled,EnforcementStatus]'
```

### 2. Identity Verification Status

```bash
#!/bin/bash
export AWS_PAGER=""
IDENTITIES=$(aws sesv2 list-email-identities --output text --query 'EmailIdentities[].IdentityName')
for id in $IDENTITIES; do
  aws sesv2 get-email-identity --email-identity "$id" \
    --output text \
    --query "[\"$id\",IdentityType,VerifiedForSendingStatus,DkimAttributes.Status,DkimAttributes.SigningEnabled,MailFromAttributes.MailFromDomainStatus]" &
done
wait
```

### 3. Bounce and Complaint Rate Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
END=$(date -u +"%Y-%m-%dT%H:%M:%S")
START=$(date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-7d +"%Y-%m-%dT%H:%M:%S")

aws cloudwatch get-metric-statistics \
  --namespace AWS/SES --metric-name Reputation.BounceRate \
  --start-time "$START" --end-time "$END" \
  --period 86400 --statistics Average Maximum \
  --output text --query 'Datapoints[*].[Timestamp,Average,Maximum]' | sort -k1 &

aws cloudwatch get-metric-statistics \
  --namespace AWS/SES --metric-name Reputation.ComplaintRate \
  --start-time "$START" --end-time "$END" \
  --period 86400 --statistics Average Maximum \
  --output text --query 'Datapoints[*].[Timestamp,Average,Maximum]' | sort -k1 &

aws cloudwatch get-metric-statistics \
  --namespace AWS/SES --metric-name Send \
  --start-time "$START" --end-time "$END" \
  --period 86400 --statistics Sum \
  --output text --query 'Datapoints[*].[Timestamp,Sum]' | sort -k1 &
wait
```

### 4. Configuration Set Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
CONFIG_SETS=$(aws sesv2 list-configuration-sets --output text --query 'ConfigurationSets[]')
for cs in $CONFIG_SETS; do
  aws sesv2 get-configuration-set --configuration-set-name "$cs" \
    --output text \
    --query "[ConfigurationSetName,ReputationOptions.ReputationMetricsEnabled,SendingOptions.SendingEnabled,TrackingOptions.CustomRedirectDomain]" &
done
wait
```

### 5. Suppression List Review

```bash
#!/bin/bash
export AWS_PAGER=""
echo "=== BOUNCE suppressions ==="
aws sesv2 list-suppressed-destinations --reasons BOUNCE \
  --output text \
  --query 'SuppressedDestinationSummaries[].[EmailAddress,Reason,LastUpdateTime]' | head -10 &

echo "=== COMPLAINT suppressions ==="
aws sesv2 list-suppressed-destinations --reasons COMPLAINT \
  --output text \
  --query 'SuppressedDestinationSummaries[].[EmailAddress,Reason,LastUpdateTime]' | head -10 &
wait
```

## Anti-Hallucination Rules

1. **SES v1 vs v2 API** - Use `sesv2` commands (SES v2 API) for all operations. The v1 `ses` commands are legacy and missing features.
2. **Bounce rate threshold** - AWS pauses sending if bounce rate exceeds 5%. Complaint rate threshold is 0.1%. These are hard limits.
3. **Sandbox mode** - New SES accounts are in sandbox. Can only send to verified identities. Check `ProductionAccessEnabled` field.
4. **DKIM status values** - Valid statuses: SUCCESS, FAILED, PENDING, TEMPORARY_FAILURE, NOT_STARTED. Do not fabricate other values.
5. **Sending quota is per 24 hours** - `Max24HourSend` is a rolling 24-hour window, not a daily reset.

## Output Format

Present results as a structured report:
```
Aws Ses Report
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

- **Regional service**: SES is regional. Identities verified in us-east-1 are not available in eu-west-1. Check the correct region.
- **Domain vs email identity**: Domain identities cover all addresses @domain. Email identities are individual addresses. Both can coexist.
- **Suppression list is account-level**: The suppression list applies to all configuration sets in the account/region.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Event destinations**: Configuration sets can route events to CloudWatch, SNS, Kinesis, or Pinpoint. Check event destination configuration for monitoring.
