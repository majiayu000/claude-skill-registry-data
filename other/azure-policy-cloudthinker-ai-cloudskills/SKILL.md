---
name: azure-policy
description: |
  Use when working with Azure Policy — azure Policy compliance assessment,
  policy and initiative assignment management, remediation task tracking, and
  definition analysis via Azure CLI.
connection_type: azure
preload: false
---

# Azure Policy Skill

Manage and analyze Azure Policy using `az policy` commands.

## Discovery-First Rule

**ALWAYS discover before acting.** Never assume policy names, assignment names, initiative names, or definition IDs.

```bash
# Discover policy assignments
az policy assignment list --output json \
  --query "[].{name:name, displayName:displayName, scope:scope, policyDefinitionId:policyDefinitionId, enforcementMode:enforcementMode, notScopes:notScopes}"

# Discover policy definitions (custom only)
az policy definition list --query "[?policyType=='Custom']" --output json \
  --query "[].{name:name, displayName:displayName, mode:mode, policyType:policyType}"
```

## Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
for assignment in $(echo "$assignments" | jq -c '.[]'); do
  {
    name=$(echo "$assignment" | jq -r '.name')
    az policy state summarize --policy-assignment "$name" --output json
  } &
done
wait
```

## Helper Functions

```bash
# Get compliance summary for an assignment
get_compliance_summary() {
  local assignment="$1"
  az policy state summarize --policy-assignment "$assignment" --output json \
    --query "value[0].{totalResources:results.totalResources, nonCompliant:results.nonCompliantResources, policyAssignments:policyAssignments[].{name:policyAssignmentId, nonCompliant:results.nonCompliantResources}}"
}

# List non-compliant resources
list_noncompliant() {
  local assignment="$1" top="${2:-50}"
  az policy state list --policy-assignment "$assignment" --filter "complianceState eq 'NonCompliant'" --top "$top" --output json \
    --query "[].{resourceId:resourceId, resourceType:resourceType, policyDefinitionAction:policyDefinitionAction, complianceState:complianceState, timestamp:timestamp}"
}

# Get remediation tasks
list_remediations() {
  az policy remediation list --output json \
    --query "[].{name:name, policyAssignmentId:policyAssignmentId, provisioningState:provisioningState, deploymentStatus:deploymentStatus, createdOn:createdOn}"
}

# Get policy definition details
get_policy_definition() {
  local name="$1"
  az policy definition show --name "$name" --output json \
    --query "{name:name, displayName:displayName, description:description, mode:mode, policyRule:policyRule, parameters:parameters}"
}
```

## Common Operations

### 1. Compliance Overview

```bash
# Overall compliance summary
az policy state summarize --output json \
  --query "value[0].{totalResources:results.totalResources, nonCompliant:results.nonCompliantResources, compliant:results.compliantResources}"

# Per-assignment compliance
assignments=$(az policy assignment list --output json --query "[].name")
for name in $(echo "$assignments" | jq -r '.[]'); do
  {
    echo "Assignment: $name"
    get_compliance_summary "$name"
  } &
done
wait
```

### 2. Non-Compliant Resource Investigation

```bash
# Top non-compliant resources across all policies
az policy state list --filter "complianceState eq 'NonCompliant'" --top 50 --output json \
  --query "[].{resource:resourceId, type:resourceType, policy:policyDefinitionName, action:policyDefinitionAction, complianceState:complianceState}"

# Non-compliant resources for a specific policy
list_noncompliant "$ASSIGNMENT_NAME" 100
```

### 3. Initiative (Policy Set) Analysis

```bash
# List initiative assignments
az policy assignment list --output json \
  --query "[?contains(policyDefinitionId, 'policySetDefinitions')].{name:name, displayName:displayName, initiative:policyDefinitionId, enforcementMode:enforcementMode}"

# Get initiative definition and included policies
az policy set-definition show --name "$INITIATIVE_NAME" --output json \
  --query "{name:name, displayName:displayName, policyCount:policyDefinitions | length(@), policies:policyDefinitions[].{definitionId:policyDefinitionId, parameters:parameters}}"
```

### 4. Remediation Task Management

```bash
# List all remediation tasks with status
list_remediations

# Check remediation deployment progress
az policy remediation show --name "$REMEDIATION" --output json \
  --query "{name:name, status:provisioningState, policyAssignment:policyAssignmentId, totalDeployments:deploymentStatus.totalDeployments, successfulDeployments:deploymentStatus.successfulDeployments, failedDeployments:deploymentStatus.failedDeployments}"

# List failed remediation deployments
az policy remediation deployment list --name "$REMEDIATION" --output json \
  --query "[?status=='Failed'].{resourceId:remediatedResourceId, status:status, error:error}"
```

### 5. Policy Enforcement Audit

```bash
# Check enforcement mode (DoNotEnforce means audit-only)
az policy assignment list --output json \
  --query "[].{name:displayName, enforcement:enforcementMode, scope:scope}" | jq '[.[] | select(.enforcement=="DoNotEnforce")]'

# Check for exemptions
az policy exemption list --output json \
  --query "[].{name:name, policyAssignment:policyAssignmentId, category:exemptionCategory, expiresOn:expiresOn, description:description}"
```

## Output Format

Present results as a structured report:
```
Azure Policy Report
═══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

1. **Enforcement mode**: `DoNotEnforce` means the policy only audits, it does not deny or deploy. Check enforcement mode before assuming resources are protected.
2. **Evaluation delay**: Policy compliance evaluation is not real-time. New resources may take up to 30 minutes to be evaluated. Trigger on-demand evaluation with `az policy state trigger-scan`.
3. **Scope inheritance**: Policies assigned at management group level apply to all child subscriptions. Check parent scopes for inherited policies.
4. **Exemptions vs exclusions**: `notScopes` excludes permanently; exemptions can have expiry dates. Use exemptions for temporary exceptions.
5. **DeployIfNotExists timing**: DINE policies only trigger on resource creation or update, not on existing non-compliant resources. Use remediation tasks for existing resources.
