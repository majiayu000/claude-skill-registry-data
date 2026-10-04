---
name: managing-ns1
description: |
  Use when working with Ns1 — nS1 managed DNS platform covering zones, records,
  filter chains, monitoring jobs, DNSSEC, and traffic steering. Use when
  managing NS1 DNS zones, configuring intelligent traffic routing via filter
  chains, monitoring DNS health checks, analyzing query analytics, or
  troubleshooting DNS resolution.
connection_type: ns1
preload: false
---

# NS1 DNS Skill

Manage NS1 DNS zones, records, filter chains, monitoring, and traffic steering.

## Core Helper Functions

```bash
#!/bin/bash

NS1_API="https://api.nsone.net/v1"

ns1_api() {
    local endpoint="$1"
    shift
    curl -s -H "X-NSONE-Key: $NS1_API_KEY" \
         -H "Content-Type: application/json" \
         "$NS1_API/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== DNS Zones ==="
ns1_api "zones" | jq -r '
    .[] | "\(.zone)\t\(.dns_servers | length) NS\tRecords: \(.records // 0)\t\(.nx_ttl)s NX-TTL"
' | column -t | head -20

echo ""
echo "=== Monitoring Jobs ==="
ns1_api "monitoring/jobs" | jq -r '
    .[] | "\(.id[:12])\t\(.name)\t\(.job_type)\t\(.status)\t\(.regions | join(","))"
' | column -t | head -15

echo ""
echo "=== Data Sources ==="
ns1_api "data/sources" | jq -r '
    .[] | "\(.id[:12])\t\(.name)\t\(.sourcetype)\t\(.status)"
' | column -t | head -10

echo ""
echo "=== Account Usage ==="
ns1_api "account/usagewarnings" | jq '.'
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE="${1:?Zone name required}"

echo "=== Zone Details ==="
ns1_api "zones/$ZONE" | jq '{
    zone, ttl, nx_ttl, retry, refresh, expiry,
    dnssec: .dnssec, primary: .primary,
    dns_servers, networks: .networks,
    record_count: (.records | length)
}'

echo ""
echo "=== DNS Records ==="
ns1_api "zones/$ZONE" | jq -r '
    .records[] | "\(.type)\t\(.domain)\t\(.short_answers | join("; "))\t\(.ttl)s"
' | sort | column -t | head -25

echo ""
echo "=== Filter Chains ==="
ns1_api "zones/$ZONE" | jq '
    .records[] | select(.filters | length > 0) | {
        domain, type,
        filters: [.filters[] | {filter: .filter, config}]
    }' | head -20

echo ""
echo "=== Query Analytics ==="
ns1_api "stats/qps/$ZONE" | jq -r '
    .[] | "\(.timestamp)\t\(.qps) qps"
' | tail -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse NS1 API JSON responses
- Show filter chain details for intelligent routing records

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Never delete zones** without explicit confirmation
- **Filter chain changes** affect traffic routing immediately
- **Monitoring job changes** can trigger failover if misconfigured

## Output Format

Present results as a structured report:
```
Managing Ns1 Report
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
- **Filter chains are ordered**: Filters execute top-to-bottom; order matters for routing logic
- **Answer metadata**: Each answer can have metadata for filter chain decisions (e.g., geo, weight)
- **Monitoring regions**: Jobs must run from multiple regions for reliable health checks
- **API rate limits**: 500 requests per second per API key
- **DNSSEC**: Must be enabled at both NS1 and the registrar level
