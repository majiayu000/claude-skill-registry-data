---
name: managing-nops
description: |
  Use when working with Nops — nOps AWS cloud optimization and cost management
  platform. Covers ShareSave automated savings, commitment management,
  well-architected reviews, idle resource detection, and AWS cost optimization.
  Use when optimizing AWS spend, managing reserved instances and savings plans,
  or running well-architected reviews.
connection_type: nops
preload: false
---

# nOps Management Skill

Manage AWS cloud optimization and automated savings with nOps.

## MANDATORY: Discovery-First Pattern

**Always list connected AWS accounts and optimization status before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

nops_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $NOPS_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.nops.io/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $NOPS_API_TOKEN" \
            "https://api.nops.io/v1/${endpoint}"
    fi
}

echo "=== Connected AWS Accounts ==="
nops_api GET "accounts" | jq -r '
    .items[] | "\(.id)\t\(.name)\t\(.awsAccountId)\t\(.status)"
' | column -t

echo ""
echo "=== Optimization Summary ==="
nops_api GET "dashboard/summary" | jq '{
    totalMonthlySpend: .totalMonthlySpend,
    totalSavings: .totalSavings,
    savingsPercent: .savingsPercent,
    activeRecommendations: .activeRecommendations
}'

echo ""
echo "=== ShareSave Status ==="
nops_api GET "sharesave/status" | jq -r '
    .items[] | "\(.accountName)\tSavings: $\(.monthlySavings | . * 100 | round / 100)\tCommitments: \(.activeCommitments)"
' | column -t | head -10
```

## Core Helper Functions

```bash
#!/bin/bash

nops_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Authorization: Bearer $NOPS_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.nops.io/v1/${endpoint}" -d "$data"
    else
        curl -s -X "$method" -H "Authorization: Bearer $NOPS_API_TOKEN" \
            "https://api.nops.io/v1/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to extract savings and optimization summaries
- Round costs and savings to 2 decimal places

## Common Operations

### ShareSave Analysis

```bash
#!/bin/bash
echo "=== ShareSave Savings Summary ==="
nops_api GET "sharesave/savings" | jq '{
    totalSavingsThisMonth: .totalSavingsThisMonth,
    totalSavingsAllTime: .totalSavingsAllTime,
    activeCommitments: .activeCommitments,
    savingsPlansActive: .savingsPlansActive,
    riActive: .riActive
}'

echo ""
echo "=== ShareSave by Service ==="
nops_api GET "sharesave/savings/breakdown" | jq -r '
    .items[] | "\(.service)\tSavings: $\(.monthlySavings | . * 100 | round / 100)\tCoverage: \(.coveragePercent | round)%"
' | sort -t'$' -k2 -rn | column -t | head -15
```

### Commitment Management

```bash
#!/bin/bash
echo "=== Active Commitments ==="
nops_api GET "commitments" | jq -r '
    .items[] |
    "\(.type)\t\(.service)\tExpires: \(.expirationDate[0:10])\tUtilization: \(.utilizationPercent | round)%\tMonthly: $\(.monthlyAmount | . * 100 | round / 100)"
' | column -t | head -20

echo ""
echo "=== Expiring Commitments (next 30 days) ==="
nops_api GET "commitments?expiringWithinDays=30" | jq -r '
    .items[] |
    "\(.type)\t\(.service)\tExpires: \(.expirationDate[0:10])\tMonthly: $\(.monthlyAmount | . * 100 | round / 100)"
' | column -t

echo ""
echo "=== Commitment Recommendations ==="
nops_api GET "commitments/recommendations" | jq -r '
    .items[] |
    "\(.service)\tType: \(.recommendedType)\tTerm: \(.term)\tEstimated Savings: $\(.estimatedMonthlySavings | . * 100 | round / 100)/mo"
' | sort -t'$' -k4 -rn | column -t | head -10
```

### AWS Well-Architected Review

```bash
#!/bin/bash
ACCOUNT_ID="${1:-}"

echo "=== Well-Architected Review Summary ==="
ENDPOINT="well-architected/summary"
[ -n "$ACCOUNT_ID" ] && ENDPOINT="${ENDPOINT}?accountId=${ACCOUNT_ID}"
nops_api GET "$ENDPOINT" | jq '{
    costOptimization: .pillars.costOptimization,
    security: .pillars.security,
    reliability: .pillars.reliability,
    performance: .pillars.performance,
    operational: .pillars.operationalExcellence
}'

echo ""
echo "=== High Risk Items ==="
nops_api GET "well-architected/findings?risk=high" | jq -r '
    .items[] |
    "\(.pillar)\t\(.title)\tRisk: \(.risk)\tResources: \(.affectedResources)"
' | column -t | head -15
```

### Idle Resource Detection

```bash
#!/bin/bash
echo "=== Idle Resources Summary ==="
nops_api GET "idle-resources/summary" | jq '{
    totalIdleResources: .totalIdleResources,
    estimatedWaste: .estimatedMonthlyWaste,
    byService: .byService
}'

echo ""
echo "=== Top Idle Resources ==="
nops_api GET "idle-resources" | jq -r '
    .items[] |
    "\(.service)\t\(.resourceId)\t\(.region)\tWaste: $\(.estimatedMonthlyWaste | . * 100 | round / 100)/mo\tIdle Since: \(.idleSince[0:10])"
' | sort -t'$' -k4 -rn | column -t | head -20
```

### Cost Optimization Dashboard

```bash
#!/bin/bash
echo "=== Optimization Opportunities ==="
nops_api GET "recommendations" | jq -r '
    .items[] |
    "\(.category)\t\(.title)\tSavings: $\(.estimatedMonthlySavings | . * 100 | round / 100)/mo\tEffort: \(.effort)"
' | sort -t'$' -k3 -rn | column -t | head -20

echo ""
echo "=== Monthly Spend Trend ==="
nops_api GET "costs/trend?months=6" | jq -r '
    .items[] | "\(.month)\t$\(.totalCost | . * 100 | round / 100)\tSavings: $\(.savings | . * 100 | round / 100)"
' | column -t
```

## Safety Rules
- **ShareSave commitments**: Never approve new commitments without finance team review
- **Read-only by default**: nOps recommendations are advisory -- implementation requires manual action
- **Account verification**: Always confirm AWS account ID before applying recommendations
- **Commitment terms**: Review 1yr vs 3yr terms carefully -- long commitments reduce flexibility

## Output Format

Present results as a structured report:
```
Managing Nops Report
════════════════════
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
- **AWS billing lag**: Cost data may lag 24-48 hours behind actual AWS usage
- **ShareSave eligibility**: Not all instance types are eligible for ShareSave optimization
- **Multi-account payer**: Ensure payer account is connected for consolidated billing view
- **RI marketplace**: Selling unused RIs on marketplace has restrictions -- check terms
- **Savings Plan scope**: Account-scoped vs organization-scoped plans affect different workloads
- **Data freshness**: Well-architected findings refresh periodically -- not real-time
