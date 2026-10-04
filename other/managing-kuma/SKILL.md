---
name: managing-kuma
description: |
  Use when working with Kuma — kuma service mesh management covering meshes,
  dataplanes, traffic policies, mesh gateways, fault injection, rate limiting,
  and observability configuration. Supports both Kubernetes and Universal (VM)
  mode. Use when managing Kuma mesh, configuring traffic policies, debugging
  dataplane proxies, or setting up multi-zone mesh deployment.
connection_type: kuma
preload: false
---

# Kuma Service Mesh Skill

Manage Kuma service mesh, dataplanes, traffic policies, and multi-zone configuration.

## Core Helper Functions

```bash
#!/bin/bash

KUMA_API="${KUMA_API_URL:-http://localhost:5681}"

kuma_api() {
    local endpoint="$1"
    shift
    curl -s "$KUMA_API/$endpoint" "$@"
}

# Kubernetes mode helper
kuma_k8s() {
    local resource="$1" ns="${2:---all-namespaces}"
    if [ "$ns" = "--all-namespaces" ]; then
        kubectl get "$resource" -A -o json 2>/dev/null
    else
        kubectl get "$resource" -n "$ns" -o json 2>/dev/null
    fi
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Kuma Version & Mode ==="
kuma_api "" | jq '{version, hostname, tagline, environment}'

echo ""
echo "=== Meshes ==="
kuma_api "meshes" | jq -r '
    .items[] | "\(.name)\tBackend: \(.mtls.backends[0].name // "none")\tmTLS: \(.mtls.enabledBackend // "disabled")"
' | column -t | head -10

echo ""
echo "=== Dataplanes ==="
kuma_api "dataplanes" | jq -r '
    .items[] | "\(.name)\t\(.mesh)\t\(.networking.address // "n/a")\t\(.networking.inbound[0].tags["kuma.io/service"] // "n/a")"
' | column -t | head -20

echo ""
echo "=== Dataplane Health ==="
kuma_api "mesh-insights" | jq -r '
    .items[] | "\(.name)\tOnline: \(.dataplanesByType.standard.online // 0)\tOffline: \(.dataplanesByType.standard.offline // 0)\tTotal: \(.dataplanesByType.standard.total // 0)"
' | column -t | head -10

echo ""
echo "=== Zones (Multi-Zone) ==="
kuma_api "zones" | jq -r '
    .items[]? | "\(.name)\t\(.enabled)"
' | column -t 2>/dev/null | head -10

echo ""
echo "=== Policy Summary ==="
for policy in trafficpermissions trafficlogs traffictraces trafficroutes timeouts circuitbreakers healthchecks faultinjections retries ratelimits; do
    COUNT=$(kuma_api "$policy" 2>/dev/null | jq '.total // 0')
    [ "$COUNT" -gt 0 ] && echo "$policy: $COUNT"
done
```

### Phase 2: Analysis

```bash
#!/bin/bash
MESH="${1:-default}"

echo "=== Mesh Configuration ==="
kuma_api "meshes/$MESH" | jq '{
    name, mtls, tracing, logging, metrics, routing
}'

echo ""
echo "=== Traffic Permissions ==="
kuma_api "meshes/$MESH/trafficpermissions" | jq -r '
    .items[] | "\(.name)\tSources: \(.sources[0].match["kuma.io/service"] // "*")\tDest: \(.destinations[0].match["kuma.io/service"] // "*")"
' | column -t | head -15

echo ""
echo "=== Traffic Routes ==="
kuma_api "meshes/$MESH/trafficroutes" | jq '
    .items[] | {name, sources: .sources, destinations: .destinations, conf: .conf}
' | head -20

echo ""
echo "=== Circuit Breakers ==="
kuma_api "meshes/$MESH/circuitbreakers" | jq '
    .items[]? | {name, sources: .sources[0].match, destinations: .destinations[0].match, conf: .conf}
' | head -15

echo ""
echo "=== Health Checks ==="
kuma_api "meshes/$MESH/healthchecks" | jq -r '
    .items[]? | "\(.name)\tInterval: \(.conf.interval)\tThreshold: \(.conf.unhealthyThreshold)"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Kuma HTTP API responses
- Specify mesh context for all policy queries

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Traffic permission changes** affect service communication immediately
- **mTLS mode changes** can break all mesh traffic if backends are misconfigured
- **Multi-zone policy changes** propagate to all zones

## Output Format

Present results as a structured report:
```
Managing Kuma Report
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
- **Universal vs Kubernetes**: API and resource formats differ between modes
- **Default mesh**: Resources without explicit mesh belong to the `default` mesh
- **Traffic permission deny-by-default**: Without permissions, services cannot communicate
- **Zone sync**: Multi-zone deployments sync policies from global to zone control planes
- **Dataplane tokens**: Universal mode requires tokens for dataplane authentication
