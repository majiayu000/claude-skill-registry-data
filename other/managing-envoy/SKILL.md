---
name: managing-envoy
description: |
  Use when working with Envoy — envoy Proxy configuration and health management.
  Covers listener configuration, cluster health checks, route table inspection,
  admin interface operations, stats monitoring, and config dump analysis. Use
  when debugging Envoy proxy configuration, inspecting upstream cluster health,
  analyzing route tables, or monitoring proxy performance.
connection_type: envoy
preload: false
---

# Envoy Proxy Management Skill

Manage Envoy Proxy listeners, clusters, routes, admin interface, and health monitoring.

## Core Helper Functions

```bash
#!/bin/bash

# Envoy admin API helper
envoy_admin() {
    local endpoint="$1"
    local admin_url="${ENVOY_ADMIN_URL:-http://localhost:9901}"
    curl -s "${admin_url}${endpoint}"
}

# Envoy admin with JSON output
envoy_admin_json() {
    local endpoint="$1"
    envoy_admin "${endpoint}?format=json"
}

# Envoy in Kubernetes (port-forward to admin)
envoy_k8s_admin() {
    local pod="$1"
    local ns="${2:-default}"
    local endpoint="$3"
    kubectl exec -n "$ns" "$pod" -- curl -s "http://localhost:9901${endpoint}" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always check Envoy server info and listener status before inspecting specific configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash
ADMIN_URL="${ENVOY_ADMIN_URL:-http://localhost:9901}"

echo "=== Envoy Server Info ==="
envoy_admin "/server_info" | jq '{
    version: .version,
    state: .state,
    uptime: .uptime_current_epoch,
    hot_restart_version: .hot_restart_version,
    command_line_options: .command_line_options.config_path
}' 2>/dev/null

echo ""
echo "=== Listeners ==="
envoy_admin "/listeners?format=json" | jq -r '
    .listener_statuses[] | "\(.name)\t\(.local_address.socket_address.address):\(.local_address.socket_address.port_value)"
' 2>/dev/null | column -t | head -15

echo ""
echo "=== Cluster Summary ==="
envoy_admin "/clusters?format=json" | jq '{
    total_clusters: (.cluster_statuses | length),
    healthy: [.cluster_statuses[] | select(.host_statuses[]?.health_status.eds_health_status == "HEALTHY")] | length,
    unhealthy: [.cluster_statuses[] | select(.host_statuses[]?.health_status.eds_health_status == "UNHEALTHY")] | length
}' 2>/dev/null

echo ""
echo "=== Admin Endpoints ==="
envoy_admin "/" 2>/dev/null | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `?format=json` with jq for structured admin API output
- Never dump full config -- use specific config_dump filters

## Common Operations

### Listener Configuration Analysis

```bash
#!/bin/bash
echo "=== Active Listeners ==="
envoy_admin "/config_dump?resource=dynamic_listeners&format=json" | jq -r '
    .configs[0].dynamic_listeners[]? | {
        name: .name,
        state: .active_state.version_info,
        address: .active_state.listener.address.socket_address.address,
        port: .active_state.listener.address.socket_address.port_value,
        filter_chains: (.active_state.listener.filter_chains | length)
    }' 2>/dev/null | head -30

echo ""
echo "=== Static Listeners ==="
envoy_admin "/config_dump?resource=static_listeners&format=json" | jq -r '
    .configs[0].static_listeners[]? | {
        name: .listener.name,
        address: .listener.address.socket_address.address,
        port: .listener.address.socket_address.port_value
    }' 2>/dev/null | head -15

echo ""
echo "=== Listener Drain Status ==="
envoy_admin "/listeners?format=json" | jq -r '
    .listener_statuses[] | "\(.name)\t\(.local_address.socket_address.port_value)\tdraining=false"
' 2>/dev/null | column -t | head -10
```

### Cluster Health Inspection

```bash
#!/bin/bash
echo "=== Cluster Health Status ==="
envoy_admin "/clusters?format=json" | jq -r '
    .cluster_statuses[] | {
        name: .name,
        hosts: [.host_statuses[]? | {
            address: "\(.address.socket_address.address):\(.address.socket_address.port_value)",
            health: .health_status.eds_health_status,
            weight: .weight,
            locality: .locality
        }]
    }' 2>/dev/null | head -40

echo ""
echo "=== Unhealthy Upstreams ==="
envoy_admin "/clusters?format=json" | jq -r '
    .cluster_statuses[] | .name as $cluster |
    .host_statuses[]? | select(.health_status.eds_health_status != "HEALTHY") |
    "\($cluster)\t\(.address.socket_address.address):\(.address.socket_address.port_value)\t\(.health_status.eds_health_status)\t\(.health_status.failed_active_health_check // false)"
' 2>/dev/null | column -t | head -15

echo ""
echo "=== Cluster Circuit Breaker Status ==="
envoy_admin "/clusters" 2>/dev/null | grep -E "circuit_breaker|outlier" | head -15
```

### Route Table Inspection

```bash
#!/bin/bash
echo "=== Route Configurations ==="
envoy_admin "/config_dump?resource=dynamic_route_configs&format=json" | jq '
    .configs[0].dynamic_route_configs[]? | {
        name: .route_config.name,
        version: .version_info,
        virtual_hosts: [.route_config.virtual_hosts[]? | {
            name: .name,
            domains: .domains,
            routes: [.routes[]? | {
                match: .match,
                route: .route.cluster
            }]
        }]
    }' 2>/dev/null | head -40

echo ""
echo "=== Virtual Host Summary ==="
envoy_admin "/config_dump?resource=dynamic_route_configs&format=json" | jq -r '
    .configs[0].dynamic_route_configs[]? |
    .route_config.virtual_hosts[]? |
    "\(.name)\t\(.domains | join(",") | .[0:50])\t\(.routes | length) routes"
' 2>/dev/null | column -t | head -20
```

### Stats & Performance Monitoring

```bash
#!/bin/bash
echo "=== Key Server Stats ==="
envoy_admin "/stats?format=json&filter=server" | jq '
    .stats | map(select(.name | test("server\\."))) |
    map({(.name): .value}) | add
' 2>/dev/null | head -20

echo ""
echo "=== Connection Stats ==="
envoy_admin "/stats?format=json&filter=downstream_cx" | jq '
    .stats | map(select(.value > 0)) | map({(.name): .value}) | add
' 2>/dev/null | head -15

echo ""
echo "=== HTTP Response Code Stats ==="
envoy_admin "/stats?format=json&filter=downstream_rq" | jq '
    .stats | map(select(.name | test("downstream_rq_[1-5]"))) |
    map({(.name): .value}) | add
' 2>/dev/null | head -10

echo ""
echo "=== Upstream Health Stats ==="
envoy_admin "/stats?format=json&filter=health_check" | jq '
    .stats | map(select(.value > 0)) | map({(.name): .value}) | add
' 2>/dev/null | head -15

echo ""
echo "=== Memory Usage ==="
envoy_admin "/memory" | jq '.' 2>/dev/null
```

### Config Dump & Debugging

```bash
#!/bin/bash
echo "=== xDS Discovery Status ==="
envoy_admin "/config_dump?resource=dynamic_active_clusters&format=json" | jq '
    .configs[0].dynamic_active_clusters | length
' 2>/dev/null | xargs echo "Active dynamic clusters:"

envoy_admin "/config_dump?resource=dynamic_listeners&format=json" | jq '
    .configs[0].dynamic_listeners | length
' 2>/dev/null | xargs echo "Active dynamic listeners:"

echo ""
echo "=== Bootstrap Config ==="
envoy_admin "/config_dump?resource=bootstrap&format=json" | jq '
    .configs[0].bootstrap | {
        admin: .admin.address,
        cluster_manager: .dynamic_resources,
        static_resources_clusters: (.static_resources.clusters | length),
        static_resources_listeners: (.static_resources.listeners | length)
    }' 2>/dev/null

echo ""
echo "=== Config Versions ==="
envoy_admin "/config_dump?format=json" | jq -r '
    .configs[] | select(.dynamic_listeners != null or .dynamic_active_clusters != null) |
    (.dynamic_listeners // .dynamic_active_clusters // [])[] |
    "\(.version_info // "static")\t\(.name // "unnamed")"
' 2>/dev/null | sort -u | head -15

echo ""
echo "=== Runtime Overrides ==="
envoy_admin "/runtime?format=json" | jq '.entries | to_entries | map(select(.value.final_value != null)) | from_entries' 2>/dev/null | head -15
```

## Safety Rules
- **Read-only by default**: Use admin API GET endpoints for inspection
- **Never POST** to `/quitquitquit`, `/healthcheck/fail`, or `/drain_listeners` without confirmation
- **Admin access**: Admin interface should not be exposed externally -- use port-forwarding
- **Config dump size**: Full config dumps can be very large -- always use resource filters

## Output Format

Present results as a structured report:
```
Managing Envoy Report
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
- **Admin port**: Default is 9901 but often customized -- check Envoy bootstrap config
- **xDS vs static**: Dynamic config (xDS) overrides static config -- check both sources
- **Health check types**: EDS health vs active health vs outlier detection are independent signals
- **Hot restart**: During hot restart, two Envoy processes run simultaneously -- stats may be split
- **Filter chain matching**: Listener filter chains match by SNI, ALPN, or source IP -- order matters
