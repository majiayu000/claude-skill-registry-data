---
name: aws-config
description: |
  Use when working with Aws Config — aWS Config compliance dashboard, rule
  evaluation status, conformance pack management, and resource timeline
  analysis. Covers configuration recorder status, compliance summary,
  non-compliant resource investigation, remediation tracking, and aggregator
  management.
connection_type: aws
preload: false
---

# AWS Config Skill

Analyze AWS Config compliance and resource configuration with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-config/` → Config-specific analysis (rules, compliance, conformance packs)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for rule in $rules; do
  get_compliance_details "$rule" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# Get configuration recorder status
get_recorder_status() {
  aws configservice describe-configuration-recorder-status \
    --output text \
    --query 'ConfigurationRecordersStatus[].[name,recording,lastStatus,lastStatusChangeTime]'
}

# List Config rules
list_config_rules() {
  aws configservice describe-config-rules \
    --output text \
    --query 'ConfigRules[].[ConfigRuleName,ConfigRuleState,Source.Owner,Source.SourceIdentifier]'
}

# Get compliance summary by rule
get_compliance_summary() {
  aws configservice describe-compliance-by-config-rule \
    --output text \
    --query 'ComplianceByConfigRules[].[ConfigRuleName,Compliance.ComplianceType]'
}

# Get non-compliant resources for a rule
get_non_compliant_resources() {
  local rule_name=$1
  aws configservice get-compliance-details-by-config-rule \
    --config-rule-name "$rule_name" \
    --compliance-types NON_COMPLIANT \
    --output text \
    --query 'EvaluationResults[].[EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId,EvaluationResultIdentifier.EvaluationResultQualifier.ResourceType,ResultRecordedTime]' | head -20
}

# List conformance packs
list_conformance_packs() {
  aws configservice describe-conformance-packs \
    --output text \
    --query 'ConformancePackDetails[].[ConformancePackName,ConformancePackState,LastUpdateRequestedTime]'
}
```

## Common Operations

### 1. Configuration Recorder and Delivery Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws configservice describe-configuration-recorder-status \
  --output text \
  --query 'ConfigurationRecordersStatus[].[name,recording,lastStatus,lastStatusChangeTime]' &

aws configservice describe-delivery-channel-status \
  --output text \
  --query 'DeliveryChannelsStatus[].[name,configSnapshotDeliveryInfo.lastStatus,configHistoryDeliveryInfo.lastStatus,configStreamDeliveryInfo.lastStatus]' &
wait
```

### 2. Compliance Dashboard

```bash
#!/bin/bash
export AWS_PAGER=""
echo "=== Compliance Summary ==="
aws configservice get-compliance-summary-by-config-rule \
  --output text \
  --query 'ComplianceSummary.[CompliantResourceCount.CappedCount,NonCompliantResourceCount.CappedCount]'

echo "=== Per-Rule Compliance ==="
aws configservice describe-compliance-by-config-rule \
  --output text \
  --query 'ComplianceByConfigRules[].[ConfigRuleName,Compliance.ComplianceType]' | sort -k2
```

### 3. Non-Compliant Resource Investigation

```bash
#!/bin/bash
export AWS_PAGER=""
NON_COMPLIANT_RULES=$(aws configservice describe-compliance-by-config-rule \
  --compliance-types NON_COMPLIANT \
  --output text \
  --query 'ComplianceByConfigRules[].ConfigRuleName')
for rule in $NON_COMPLIANT_RULES; do
  aws configservice get-compliance-details-by-config-rule \
    --config-rule-name "$rule" --compliance-types NON_COMPLIANT \
    --output text \
    --query "EvaluationResults[].[\"$rule\",EvaluationResultIdentifier.EvaluationResultQualifier.ResourceId,EvaluationResultIdentifier.EvaluationResultQualifier.ResourceType]" | head -5 &
done
wait
```

### 4. Conformance Pack Status

```bash
#!/bin/bash
export AWS_PAGER=""
aws configservice describe-conformance-pack-compliance \
  --conformance-pack-name "$1" \
  --output text \
  --query 'ConformancePackRuleComplianceList[].[ConfigRuleName,ComplianceType]' | sort -k2
```

### 5. Resource Configuration Timeline

```bash
#!/bin/bash
export AWS_PAGER=""
RESOURCE_TYPE=$1  # e.g., AWS::EC2::Instance
RESOURCE_ID=$2
aws configservice get-resource-config-history \
  --resource-type "$RESOURCE_TYPE" --resource-id "$RESOURCE_ID" \
  --limit 10 \
  --output text \
  --query 'configurationItems[].[configurationItemCaptureTime,configurationItemStatus,resourceType,resourceId]'
```

## Anti-Hallucination Rules

1. **Config recorder must be on** - If the recorder is not recording, compliance data is stale. Always check recorder status first.
2. **Compliance types** - Valid types: COMPLIANT, NON_COMPLIANT, NOT_APPLICABLE, INSUFFICIENT_DATA. Do not invent other states.
3. **CappedCount** - Compliance summary counts are capped at 25. If count is 25, the actual number may be higher. Use detailed queries for exact counts.
4. **AWS-managed vs custom rules** - `Source.Owner` is AWS for managed rules, CUSTOM_LAMBDA for custom rules. Different remediation approaches apply.
5. **Resource types use CloudFormation format** - Resource types follow `AWS::Service::Resource` format (e.g., `AWS::EC2::Instance`). Do not use API resource names.

## Output Format

Present results as a structured report:
```
Aws Config Report
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

- **Multi-region**: Config rules and recorders are regional. For organization-wide view, use Config Aggregators.
- **Evaluation frequency**: Periodic rules evaluate on a schedule (1h, 3h, 6h, 12h, 24h). Change-triggered rules evaluate on resource changes. Recent changes may not be reflected.
- **Conformance packs vs rules**: Conformance packs are collections of rules deployed together. Individual rule compliance is tracked separately.
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Resource timeline retention**: Config retains configuration history based on delivery channel settings. Default retention varies by resource type.
