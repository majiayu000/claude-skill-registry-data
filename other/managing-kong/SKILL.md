---
name: managing-kong
description: |
  Use when working with Kong — kong Gateway management - service and route
  configuration, plugin management, upstream health monitoring, consumer and
  credential management. Use when managing API gateway infrastructure,
  configuring rate limiting, authentication, or troubleshooting upstream
  connectivity.
connection_type: kong
preload: false
---

# Kong Gateway Management Skill

Manage Kong Gateway services, routes, plugins, upstreams, and consumers via the Admin API.

## Core Helper Functions

```bash
#!/bin/bash

# Kong Admin API base URL
KONG_ADMIN="${KONG_ADMIN_URL:-http://localhost:8001}"

# Kong Admin API wrapper
kong_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    shift 2
    curl -s -X "$method" "${KONG_ADMIN}${endpoint}" \
        -H "Content-Type: application/json" "$@" | jq '.'
}

# Paginated list helper
kong_list() {
    local endpoint="$1"
    local limit="${2:-100}"
    kong_api GET "${endpoint}?size=${limit}"
}
```

## MANDATORY: Discovery-First Pattern

**Always inspect the Kong instance and its configuration before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Kong Instance Info ==="
kong_api GET "/" | jq '{
    version: .version,
    hostname: .hostname,
    node_id: .node_id,
    database: .configuration.database,
    plugins: .plugins.available_on_server | keys
}'

echo ""
echo "=== Service Count ==="
kong_api GET "/services" | jq '{total: .data | length, services: [.data[] | {name, host, port, protocol, enabled}]}'

echo ""
echo "=== Route Count ==="
kong_api GET "/routes" | jq '{total: .data | length}'

echo ""
echo "=== Active Plugins ==="
kong_api GET "/plugins" | jq '[.data[] | {name, service: .service.id, route: .route.id, enabled}]'

echo ""
echo "=== Upstream Health ==="
kong_api GET "/upstreams" | jq '[.data[] | {name, slots, algorithm: .algorithm}]'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Always pipe through jq to extract relevant fields
- Never dump full plugin configuration -- extract key settings only

## Common Operations

### Service and Route Management

```bash
#!/bin/bash

echo "=== Services with Routes ==="
for svc in $(kong_api GET "/services" | jq -r '.data[].id'); do
    kong_api GET "/services/${svc}" | jq '{id, name, host, port, protocol, path, enabled}'
    echo "  Routes:"
    kong_api GET "/services/${svc}/routes" | jq '[.data[] | {id, name, paths, methods, hosts, protocols}]'
done

echo ""
echo "=== Routeless Services (potential orphans) ==="
for svc_id in $(kong_api GET "/services" | jq -r '.data[].id'); do
    routes=$(kong_api GET "/services/${svc_id}/routes" | jq '.data | length')
    if [ "$routes" -eq 0 ]; then
        kong_api GET "/services/${svc_id}" | jq '{name, id, host}'
    fi
done
```

### Plugin Configuration Analysis

```bash
#!/bin/bash

echo "=== Global Plugins ==="
kong_api GET "/plugins" | jq '[.data[] | select(.service == null and .route == null and .consumer == null) | {name, enabled, config_keys: (.config | keys)}]'

echo ""
echo "=== Rate Limiting Plugins ==="
kong_api GET "/plugins" | jq '[.data[] | select(.name | test("rate-limiting")) | {
    id, name, enabled,
    scope: (if .service then "service" elif .route then "route" else "global" end),
    minute: .config.minute,
    hour: .config.hour,
    policy: .config.policy
}]'

echo ""
echo "=== Auth Plugins ==="
kong_api GET "/plugins" | jq '[.data[] | select(.name | test("auth|jwt|oauth|key-auth|basic-auth")) | {name, enabled, scope: (if .service then "service" elif .route then "route" else "global" end)}]'
```

### Upstream Health Monitoring

```bash
#!/bin/bash

echo "=== Upstream Health Status ==="
for upstream in $(kong_api GET "/upstreams" | jq -r '.data[].id'); do
    name=$(kong_api GET "/upstreams/${upstream}" | jq -r '.name')
    echo "--- Upstream: $name ---"
    kong_api GET "/upstreams/${upstream}/health" | jq '{
        total_targets: (.data | length),
        healthy: [.data[] | select(.health == "HEALTHY")] | length,
        unhealthy: [.data[] | select(.health == "UNHEALTHY")] | length,
        targets: [.data[] | {target, weight, health}]
    }'
done

echo ""
echo "=== Upstream Algorithms ==="
kong_api GET "/upstreams" | jq '[.data[] | {name, algorithm, hash_on, hash_fallback, slots}]'
```

### Consumer and Credential Management

```bash
#!/bin/bash

echo "=== Consumers ==="
kong_api GET "/consumers" | jq '[.data[] | {id, username, custom_id, created_at}] | sort_by(.username)'

echo ""
echo "=== Consumer Credentials Summary ==="
for consumer in $(kong_api GET "/consumers" | jq -r '.data[].id' | head -20); do
    username=$(kong_api GET "/consumers/${consumer}" | jq -r '.username // .custom_id')
    key_auth=$(kong_api GET "/consumers/${consumer}/key-auth" | jq '.data | length')
    basic_auth=$(kong_api GET "/consumers/${consumer}/basic-auth" | jq '.data | length')
    jwt=$(kong_api GET "/consumers/${consumer}/jwt" | jq '.data | length')
    echo "${username}: key-auth=${key_auth} basic-auth=${basic_auth} jwt=${jwt}"
done

echo ""
echo "=== Consumer Groups ==="
kong_api GET "/consumer_groups" | jq '[.data[] | {name, id, created_at}]' 2>/dev/null || echo "Consumer groups not available"
```

### Certificate and SNI Management

```bash
#!/bin/bash

echo "=== Certificates ==="
kong_api GET "/certificates" | jq '[.data[] | {
    id,
    snis: .snis,
    created_at,
    tags
}]'

echo ""
echo "=== SNIs ==="
kong_api GET "/snis" | jq '[.data[] | {name, certificate: .certificate.id}]'
```

## Safety Rules
- **Read-only by default**: Only use GET requests for discovery and inspection
- **Never delete** services, routes, or plugins without explicit user confirmation
- **Never expose** API keys, JWT secrets, or basic-auth credentials in output
- **Plugin ordering matters**: Auth plugins run before rate-limiting; confirm order before changes
- **Test in non-production first**: Route or plugin changes can immediately affect live traffic

## Output Format

Present results as a structured report:
```
Managing Kong Report
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
- **Missing routes**: A service without routes receives no traffic; always verify route bindings
- **Plugin precedence**: Consumer-scoped plugins override route-scoped, which override service-scoped, which override global
- **Upstream DNS**: Kong caches DNS; TTL mismatches cause stale targets after scaling events
- **DB vs DB-less mode**: DB-less mode uses declarative config; Admin API writes are rejected
- **Health check thresholds**: Overly aggressive health checks can mark healthy targets as down during brief latency spikes
