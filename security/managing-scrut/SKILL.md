---
name: managing-scrut
description: |
  Use when working with Scrut — scrut Automation compliance platform for SOC 2,
  ISO 27001, HIPAA, GDPR, and other security frameworks. Covers risk management,
  control monitoring, evidence automation, vendor risk assessment, and
  continuous compliance. Use when reviewing compliance posture, tracking control
  effectiveness, managing risk registers, monitoring vendor security, or
  preparing for compliance audits.
connection_type: scrut
preload: false
---

# Scrut Automation Management Skill

Manage and analyze Scrut controls, risks, evidence, vendors, and compliance posture.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $SCRUT_API_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://api.scrut.io/v1`

### Core Helper Function

```bash
#!/bin/bash

scrut_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $SCRUT_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.scrut.io/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $SCRUT_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.scrut.io/v1${endpoint}"
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
echo "=== Frameworks ==="
scrut_api GET "/frameworks" \
    | jq -r '.data[] | "\(.id)\t\(.name)\t\(.complianceScore // "N/A")%"' | column -t | head -10

echo ""
echo "=== Controls Summary ==="
scrut_api GET "/controls?limit=1" \
    | jq '"Total controls: \(.meta.total // "N/A")"' -r

echo ""
echo "=== Integrations ==="
scrut_api GET "/integrations" \
    | jq -r '.data[] | "\(.name)\t\(.status)\t\(.category)"' | column -t | head -10
```

## Analysis Phase

### Control Health

```bash
#!/bin/bash
echo "=== Controls by Status ==="
CONTROLS=$(scrut_api GET "/controls?limit=200")
echo "$CONTROLS" | jq '{
    total: (.data | length),
    passing: ([.data[] | select(.status == "passing")] | length),
    failing: ([.data[] | select(.status == "failing")] | length),
    warning: ([.data[] | select(.status == "warning")] | length),
    not_applicable: ([.data[] | select(.status == "not_applicable")] | length)
}'

echo ""
echo "=== Failing Controls ==="
echo "$CONTROLS" | jq -r '.data[] | select(.status == "failing") | "\(.status)\t\(.name[0:45])\t\(.framework[0:15])\towner:\(.owner[0:20] // "Unassigned")"' \
    | column -t | head -15

echo ""
echo "=== Compliance Score by Framework ==="
scrut_api GET "/frameworks" \
    | jq -r '.data[] | "\(.name[0:25])\tscore:\(.complianceScore // 0)%\tcontrols:\(.controlCount // "N/A")"' | column -t
```

### Risk Management

```bash
#!/bin/bash
echo "=== Risk Register ==="
scrut_api GET "/risks?limit=100" \
    | jq '{
        total: (.data | length),
        by_level: ([.data[].riskLevel] | group_by(.) | map({level: .[0], count: length}))
    }'

echo ""
echo "=== High/Critical Risks ==="
scrut_api GET "/risks?limit=50&riskLevel=high,critical" \
    | jq -r '.data[] | "\(.riskLevel)\t\(.name[0:40])\tstatus:\(.treatmentStatus)\timpact:\(.impactScore // "N/A")"' \
    | column -t | head -15

echo ""
echo "=== Risks Requiring Treatment ==="
scrut_api GET "/risks?limit=50&treatmentStatus=untreated" \
    | jq -r '.data[] | "\(.riskLevel)\t\(.name[0:45])\towner:\(.owner[0:20] // "Unassigned")"' | column -t | head -10
```

### Evidence Automation

```bash
#!/bin/bash
echo "=== Evidence Collection Status ==="
scrut_api GET "/evidence?limit=200" \
    | jq '{
        total: (.data | length),
        automated: ([.data[] | select(.collectionType == "automated")] | length),
        manual: ([.data[] | select(.collectionType == "manual")] | length),
        current: ([.data[] | select(.status == "current")] | length),
        overdue: ([.data[] | select(.status == "overdue")] | length)
    }'

echo ""
echo "=== Overdue Evidence ==="
scrut_api GET "/evidence?limit=50&status=overdue" \
    | jq -r '.data[] | "\(.controlName[0:30])\t\(.name[0:30])\tdue:\(.dueDate[0:10] // "N/A")\ttype:\(.collectionType)"' \
    | column -t | head -15
```

### Vendor Assessment

```bash
#!/bin/bash
echo "=== Vendor Risk Overview ==="
scrut_api GET "/vendors?limit=100" \
    | jq -r '[.data[].riskLevel] | group_by(.) | map({risk: .[0], count: length}) | sort_by(.count) | reverse | .[] | "\(.risk): \(.count)"'

echo ""
echo "=== Vendors Requiring Review ==="
scrut_api GET "/vendors?limit=50&reviewStatus=pending" \
    | jq -r '.data[] | "\(.name[0:25])\t\(.riskLevel)\t\(.category[0:20])\tlastAssessed:\(.lastAssessmentDate[0:10] // "Never")"' \
    | column -t | head -10
```

## Output Format

Present results as a structured report:
```
Managing Scrut Report
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

- **Continuous monitoring**: Controls update in real-time via integrations -- check integration health
- **Multi-framework**: Single control can satisfy multiple framework requirements
- **Pagination**: Use `limit` and `offset` -- check `meta.total` for total count
- **Rate limits**: Check `X-RateLimit-Remaining` response header
- **Risk scoring**: Risk scores combine likelihood and impact -- both are configurable
