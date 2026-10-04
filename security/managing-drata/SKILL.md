---
name: managing-drata
description: |
  Use when working with Drata — drata compliance automation platform for SOC 2,
  ISO 27001, HIPAA, PCI DSS, and GDPR compliance monitoring. Covers control
  monitoring, evidence collection, personnel management, asset tracking, and
  audit readiness. Use when reviewing compliance posture, checking control
  status, tracking evidence collection, managing personnel compliance, or
  preparing for security audits.
connection_type: drata
preload: false
---

# Drata Management Skill

Manage and analyze Drata compliance controls, evidence, personnel, and audit readiness.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $DRATA_API_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://public-api.drata.com`

### Core Helper Function

```bash
#!/bin/bash

drata_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DRATA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://public-api.drata.com${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DRATA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://public-api.drata.com${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Compliance Frameworks ==="
drata_api GET "/compliance-frameworks" \
    | jq -r '.data[] | "\(.id)\t\(.name)\tenabled:\(.enabled)"' | column -t | head -10

echo ""
echo "=== Control Summary ==="
drata_api GET "/controls?limit=1" \
    | jq '"Total controls: \(.pagination.total)"' -r

echo ""
echo "=== Personnel Count ==="
drata_api GET "/personnel?limit=1" \
    | jq '"Total personnel: \(.pagination.total)"' -r
```

## Analysis Phase

### Control Status Overview

```bash
#!/bin/bash
echo "=== Controls by Status ==="
drata_api GET "/controls?limit=200" \
    | jq -r '{
        total: (.data | length),
        passing: ([.data[] | select(.status == "PASSING")] | length),
        failing: ([.data[] | select(.status == "FAILING")] | length),
        not_tested: ([.data[] | select(.status == "NOT_TESTED")] | length)
    }'

echo ""
echo "=== Failing Controls ==="
drata_api GET "/controls?limit=200" \
    | jq -r '.data[] | select(.status == "FAILING") | "\(.status)\t\(.name[0:50])\t\(.controlId)"' \
    | column -t | head -20

echo ""
echo "=== Controls by Category ==="
drata_api GET "/controls?limit=200" \
    | jq -r '[.data[].category] | group_by(.) | map({category: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.count)\t\(.category)"' | column -t | head -10
```

### Evidence Collection

```bash
#!/bin/bash
echo "=== Evidence Status ==="
drata_api GET "/evidence?limit=200" \
    | jq '{
        total: (.data | length),
        collected: ([.data[] | select(.status == "COLLECTED")] | length),
        missing: ([.data[] | select(.status == "MISSING")] | length),
        expired: ([.data[] | select(.status == "EXPIRED")] | length)
    }'

echo ""
echo "=== Missing Evidence ==="
drata_api GET "/evidence?limit=50&status=MISSING" \
    | jq -r '.data[] | "\(.controlName[0:30])\t\(.evidenceName[0:40])\t\(.status)"' \
    | column -t | head -15
```

### Personnel Compliance

```bash
#!/bin/bash
echo "=== Personnel Compliance Status ==="
drata_api GET "/personnel?limit=200" \
    | jq '{
        total: (.data | length),
        compliant: ([.data[] | select(.complianceStatus == "COMPLIANT")] | length),
        non_compliant: ([.data[] | select(.complianceStatus == "NON_COMPLIANT")] | length)
    }'

echo ""
echo "=== Non-Compliant Personnel ==="
drata_api GET "/personnel?limit=50&complianceStatus=NON_COMPLIANT" \
    | jq -r '.data[] | "\(.name)\t\(.email[0:30])\t\(.complianceStatus)\treason:\(.nonComplianceReasons[0] // "N/A")"' \
    | column -t | head -15
```

### Asset Inventory

```bash
#!/bin/bash
echo "=== Assets by Type ==="
drata_api GET "/assets?limit=200" \
    | jq -r '[.data[].assetType] | group_by(.) | map({type: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.count)\t\(.type)"' | column -t

echo ""
echo "=== Unmanaged Assets ==="
drata_api GET "/assets?limit=50&managed=false" \
    | jq -r '.data[] | "\(.name[0:30])\t\(.assetType)\t\(.owner // "No owner")"' | column -t | head -10
```

## Output Format

Present results as a structured report:
```
Managing Drata Report
═════════════════════
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

- **Pagination**: Use `limit` and `page` parameters -- check `pagination.total` for total count
- **Rate limits**: 100 requests/minute -- check `X-RateLimit-Remaining` header
- **Control IDs**: Controls have both internal IDs and framework-specific control IDs
- **Evidence auto-collection**: Some evidence is auto-collected via integrations -- check connection status
- **Framework scoping**: Controls map to multiple frameworks -- filter by framework when needed
