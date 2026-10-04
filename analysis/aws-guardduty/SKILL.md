---
name: aws-guardduty
description: |
  Use when working with Aws Guardduty — aWS GuardDuty finding analysis, detector
  management, suppression rule review, and member account oversight. Covers
  threat detection summary, finding severity distribution, finding type
  breakdown, trusted IP lists, and organization-wide security posture.
connection_type: aws
preload: false
---

# AWS GuardDuty Skill

Analyze AWS GuardDuty findings and detectors with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-guardduty/` → GuardDuty-specific analysis (findings, detectors, suppression)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for detector_id in $detectors; do
  get_detector_findings "$detector_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List detectors
list_detectors() {
  aws guardduty list-detectors --output text --query 'DetectorIds[]'
}

# Get detector details
get_detector() {
  local detector_id=$1
  aws guardduty get-detector --detector-id "$detector_id" \
    --output text \
    --query '[Status,FindingPublishingFrequency,DataSources.S3Logs.Status,DataSources.CloudTrail.Status,DataSources.DNSLogs.Status]'
}

# List findings with criteria
list_findings() {
  local detector_id=$1
  aws guardduty list-findings --detector-id "$detector_id" \
    --finding-criteria '{"Criterion":{"service.archived":{"Eq":["false"]}}}' \
    --sort-criteria '{"AttributeName":"severity","OrderBy":"DESC"}' \
    --max-results 50 \
    --output text --query 'FindingIds[]'
}

# Get finding details (batch)
get_findings() {
  local detector_id=$1
  shift
  local finding_ids="$@"
  aws guardduty get-findings --detector-id "$detector_id" --finding-ids $finding_ids \
    --output text \
    --query 'Findings[].[Id,Type,Severity,Title,Description,UpdatedAt]'
}

# List member accounts
list_members() {
  local detector_id=$1
  aws guardduty list-members --detector-id "$detector_id" \
    --output text \
    --query 'Members[].[AccountId,Email,RelationshipStatus,DetectorId,InvitedAt]'
}
```

## Common Operations

### 1. Detector Health Check

```bash
#!/bin/bash
export AWS_PAGER=""
DETECTORS=$(aws guardduty list-detectors --output text --query 'DetectorIds[]')
for det in $DETECTORS; do
  aws guardduty get-detector --detector-id "$det" \
    --output text \
    --query "[\"$det\",Status,FindingPublishingFrequency,CreatedAt]" &
done
wait
```

### 2. Finding Severity Summary

```bash
#!/bin/bash
export AWS_PAGER=""
DETECTOR=$(aws guardduty list-detectors --output text --query 'DetectorIds[0]')
FINDING_IDS=$(aws guardduty list-findings --detector-id "$DETECTOR" \
  --finding-criteria '{"Criterion":{"service.archived":{"Eq":["false"]}}}' \
  --max-results 50 --output text --query 'FindingIds[]')
[ -z "$FINDING_IDS" ] && echo "No active findings" && exit 0
aws guardduty get-findings --detector-id "$DETECTOR" --finding-ids $FINDING_IDS \
  --output text \
  --query 'Findings[].[Severity,Type]' \
  | awk '{sev=$1; if(sev>=7) level="HIGH"; else if(sev>=4) level="MEDIUM"; else level="LOW"; print level "\t" $2}' \
  | sort | uniq -c | sort -rn
```

### 3. Finding Type Breakdown

```bash
#!/bin/bash
export AWS_PAGER=""
DETECTOR=$(aws guardduty list-detectors --output text --query 'DetectorIds[0]')
FINDING_IDS=$(aws guardduty list-findings --detector-id "$DETECTOR" \
  --finding-criteria '{"Criterion":{"service.archived":{"Eq":["false"]}}}' \
  --max-results 50 --output text --query 'FindingIds[]')
[ -z "$FINDING_IDS" ] && echo "No active findings" && exit 0
aws guardduty get-findings --detector-id "$DETECTOR" --finding-ids $FINDING_IDS \
  --output text \
  --query 'Findings[].Type' | tr '\t' '\n' | sort | uniq -c | sort -rn
```

### 4. Suppression Rule Review

```bash
#!/bin/bash
export AWS_PAGER=""
DETECTOR=$(aws guardduty list-detectors --output text --query 'DetectorIds[0]')
aws guardduty list-filters --detector-id "$DETECTOR" \
  --output text \
  --query 'FilterNames[]'
FILTERS=$(aws guardduty list-filters --detector-id "$DETECTOR" --output text --query 'FilterNames[]')
for filter in $FILTERS; do
  aws guardduty get-filter --detector-id "$DETECTOR" --filter-name "$filter" \
    --output text \
    --query '[Name,Action,Rank,FindingCriteria]' &
done
wait
```

### 5. Member Account Status

```bash
#!/bin/bash
export AWS_PAGER=""
DETECTOR=$(aws guardduty list-detectors --output text --query 'DetectorIds[0]')
aws guardduty list-members --detector-id "$DETECTOR" \
  --output text \
  --query 'Members[].[AccountId,Email,RelationshipStatus,UpdatedAt]'
```

## Anti-Hallucination Rules

1. **Severity is numeric** - GuardDuty severity is 0-10 scale. High: 7-8.9, Medium: 4-6.9, Low: 1-3.9. Do not use text labels without mapping.
2. **Finding IDs are required for details** - `list-findings` returns IDs only. You must call `get-findings` with those IDs to get details.
3. **Archived vs active** - By default, `list-findings` may include archived findings. Always filter with `service.archived Eq false` for active findings.
4. **One detector per region** - Each region has at most one GuardDuty detector. `list-detectors` returns 0 or 1 IDs.
5. **Data sources** - GuardDuty analyzes CloudTrail, VPC Flow Logs, DNS logs, S3 data events, EKS audit logs, and more. Not all sources are enabled by default.

## Output Format

Present results as a structured report:
```
Aws Guardduty Report
════════════════════
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

- **get-findings batch limit**: `get-findings` accepts max 50 finding IDs per call. Chunk larger lists.
- **Finding criteria syntax**: Uses `Criterion` with `Eq`, `Neq`, `Gt`, `Gte`, `Lt`, `Lte` operators. Syntax is JSON, not JMESPath.
- **Organization delegation**: In AWS Organizations, GuardDuty has a delegated administrator. Members may have limited API access.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Findings are regional**: GuardDuty findings are per-region. For organization-wide view, query each region or use aggregation via Security Hub.
