---
name: managing-env0
description: |
  Use when working with Env0 — env0 environment management platform. Covers
  environment lifecycle, template deployment, cost tracking, policy management,
  variable configuration, and approval workflows. Use when managing env0
  environments, tracking infrastructure costs, reviewing deployment history, or
  configuring deployment templates.
connection_type: env0
preload: false
---

# env0 Management Skill

Manage and inspect env0 environments, templates, deployments, and cost tracking.

## MANDATORY: Discovery-First Pattern

**Always list organizations and projects before managing environments.**

### Phase 1: Discovery

```bash
#!/bin/bash

env0_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $ENV0_API_TOKEN" \
        -H "Content-Type: application/json" \
        "https://api.env0.com/${endpoint}"
}

echo "=== Organizations ==="
env0_api "organizations" | jq -r '.[] | "\(.id)\t\(.name)"' | column -t

echo ""
echo "=== Projects ==="
ORG_ID=$(env0_api "organizations" | jq -r '.[0].id')
env0_api "projects?organizationId=${ORG_ID}" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.description // "")"
' | column -t | head -15

echo ""
echo "=== Environment Summary ==="
env0_api "environments?organizationId=${ORG_ID}" | jq '{
    total: length,
    by_status: (group_by(.status) | map({status: .[0].status, count: length}))
}'
```

## Core Helper Functions

```bash
#!/bin/bash

# env0 API wrapper
env0_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ENV0_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.env0.com/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ENV0_API_TOKEN" \
            "https://api.env0.com/${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use API with jq for structured output
- Filter by organization/project to limit scope
- Never dump full deployment logs -- extract summaries

## Common Operations

### Environment Management

```bash
#!/bin/bash
PROJECT_ID="${1:-}"

echo "=== Environments ==="
if [ -n "$PROJECT_ID" ]; then
    env0_api GET "environments?projectId=${PROJECT_ID}" | jq -r '
        .[] | "\(.id)\t\(.name)\t\(.status)\t\(.latestDeploymentLog.planStatus // "none")"
    ' | column -t | head -20
else
    env0_api GET "environments" | jq -r '
        .[] | "\(.id)\t\(.name)\t\(.status)\t\(.projectId)"
    ' | column -t | head -30
fi
```

### Template Deployment

```bash
#!/bin/bash
echo "=== Templates ==="
env0_api GET "blueprints" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.type // "terraform")\t\(.repository)"
' | column -t | head -20

echo ""
TEMPLATE_ID="${1:-}"
if [ -n "$TEMPLATE_ID" ]; then
    echo "=== Template Details ==="
    env0_api GET "blueprints/${TEMPLATE_ID}" | jq '{
        name: .name,
        type: .type,
        repository: .repository,
        path: .path,
        revision: .revision,
        variables: [.variables[]? | {name: .name, type: .type, sensitive: .isSensitive}]
    }'
fi
```

### Cost Tracking

```bash
#!/bin/bash
echo "=== Cost Summary ==="
env0_api GET "costs" | jq '{
    total_monthly: .totalMonthlyCost,
    by_project: [.projects[]? | {
        name: .name,
        monthly_cost: .monthlyCost,
        environment_count: .environmentCount
    }] | sort_by(-.monthly_cost) | .[0:10]
}' 2>/dev/null

echo ""
ENV_ID="${1:-}"
if [ -n "$ENV_ID" ]; then
    echo "=== Environment Cost History ==="
    env0_api GET "costs/environments/${ENV_ID}" | jq '
        .costHistory | .[-5:][] | {date: .date, cost: .totalMonthlyCost}
    ' 2>/dev/null
fi
```

### Deployment History

```bash
#!/bin/bash
ENV_ID="${1:?Environment ID required}"

echo "=== Deployment History ==="
env0_api GET "environments/${ENV_ID}/deployments" | jq '
    .[0:10][] | {
        id: .id,
        type: .type,
        status: .status,
        planStatus: .planStatus,
        startedAt: .startedAt,
        triggeredBy: .triggeredBy.name
    }
'

echo ""
echo "=== Last Deployment Details ==="
env0_api GET "environments/${ENV_ID}/deployments" | jq '
    .[0] | {
        status: .status,
        resources: .resourceCount,
        cost_estimate: .estimatedMonthlyCost,
        duration_seconds: (.finishedAt | fromdateiso8601) - (.startedAt | fromdateiso8601)
    }
' 2>/dev/null
```

### Variable and Policy Management

```bash
#!/bin/bash
echo "=== Environment Variables ==="
ENV_ID="${1:-}"
SCOPE="${2:-ENVIRONMENT}"

if [ -n "$ENV_ID" ]; then
    env0_api GET "configuration?environmentId=${ENV_ID}" | jq -r '
        .[] | "\(.name)\t\(.scope)\t\(.type)\t\(if .isSensitive then "***" else .value end)"
    ' | column -t | head -20
fi

echo ""
echo "=== Policies ==="
env0_api GET "policies" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.type)\t\(.enabled)"
' | column -t | head -15
```

## Safety Rules

- **NEVER destroy environments without explicit confirmation** -- check for dependent resources
- **Review cost estimates** before deploying new environments
- **Sensitive variables** are masked in API responses -- never log decrypted values
- **Approval workflows** should be enabled for production environments
- **Template changes affect all environments** using that template on next deployment

## Output Format

Present results as a structured report:
```
Managing Env0 Report
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

- **API token scope**: Tokens are scoped to organizations -- ensure correct organization context
- **Template versioning**: Changing templates can break existing environments if variables change
- **Cost estimation lag**: Cost data updates periodically -- recent deployments may not reflect immediately
- **TTL enforcement**: Environments with TTL auto-destroy -- ensure critical envs have TTL disabled
- **VCS webhook issues**: Missed webhooks prevent auto-deploy on push -- check VCS integration
- **Variable inheritance**: Project-level variables are inherited by environments -- overrides can be confusing
- **Concurrent deployments**: env0 queues deployments per environment -- concurrent triggers wait in queue
- **Custom flow failures**: Pre/post scripts in custom flows can fail silently -- check deployment logs
