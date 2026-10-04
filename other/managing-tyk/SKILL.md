---
name: managing-tyk
description: |
  Use when working with Tyk — tyk API gateway management - API definitions,
  policy configuration, analytics and usage data, key management, and dashboard
  operations. Use when managing Tyk-based API infrastructure, configuring access
  policies, analyzing API usage, or managing developer keys.
connection_type: tyk
preload: false
---

# Tyk API Management Skill

Manage Tyk API definitions, policies, keys, and analytics via the Gateway and Dashboard APIs.

## Core Helper Functions

```bash
#!/bin/bash

# Tyk Gateway and Dashboard URLs
TYK_GATEWAY="${TYK_GATEWAY_URL:-http://localhost:8080}"
TYK_DASHBOARD="${TYK_DASHBOARD_URL:-http://localhost:3000}"
TYK_GW_SECRET="${TYK_GW_SECRET:-}"
TYK_DASH_KEY="${TYK_DASHBOARD_KEY:-}"

# Gateway API wrapper
tyk_gw() {
    local method="${1:-GET}"
    local endpoint="$2"
    shift 2
    curl -s -X "$method" "${TYK_GATEWAY}/tyk${endpoint}" \
        -H "x-tyk-authorization: ${TYK_GW_SECRET}" \
        -H "Content-Type: application/json" "$@" | jq '.'
}

# Dashboard API wrapper
tyk_dash() {
    local method="${1:-GET}"
    local endpoint="$2"
    shift 2
    curl -s -X "$method" "${TYK_DASHBOARD}/api${endpoint}" \
        -H "Authorization: ${TYK_DASH_KEY}" \
        -H "Content-Type: application/json" "$@" | jq '.'
}
```

## MANDATORY: Discovery-First Pattern

**Always inspect the Tyk instance before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Gateway Status ==="
tyk_gw GET "/hello" | jq '{status: .status, description: .description}'

echo ""
echo "=== API Definitions ==="
tyk_dash GET "/apis" | jq '{
    total: (.apis | length),
    apis: [.apis[] | {name: .api_definition.name, id: .api_definition.api_id, active: .api_definition.active, auth_type: .api_definition.auth.auth_header_name}]
}'

echo ""
echo "=== Policies ==="
tyk_dash GET "/portal/policies" | jq '{total: (.Data | length), policies: [.Data[] | {name, id, rate, per, quota_max}]}'

echo ""
echo "=== Hot Reload Status ==="
tyk_gw GET "/reload" | jq '.'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Always use jq to extract relevant fields from responses
- Never dump full API definitions -- extract key configuration fields

## Common Operations

### API Definition Management

```bash
#!/bin/bash

echo "=== API Definitions Overview ==="
tyk_dash GET "/apis" | jq '[.apis[] | .api_definition | {
    name,
    api_id,
    active,
    listen_path: .proxy.listen_path,
    target_url: .proxy.target_url,
    strip_listen_path: .proxy.strip_listen_path,
    auth_type: (if .use_keyless then "keyless" elif .use_basic_auth then "basic" elif .enable_jwt then "jwt" else "token" end),
    rate_limit: {rate: .global_rate_limit.rate, per: .global_rate_limit.per},
    version_data: (.version_data.versions | keys)
}]'

echo ""
echo "=== Inactive APIs ==="
tyk_dash GET "/apis" | jq '[.apis[] | .api_definition | select(.active == false) | {name, api_id}]'
```

### Policy Configuration

```bash
#!/bin/bash

echo "=== Access Policies ==="
tyk_dash GET "/portal/policies" | jq '[.Data[] | {
    name,
    id: ._id,
    rate,
    per,
    quota_max,
    quota_renewal_rate,
    access_rights_count: (.access_rights | length),
    apis: [.access_rights | to_entries[] | .value.api_name],
    active: .active,
    tags
}]'

echo ""
echo "=== Policies Without APIs ==="
tyk_dash GET "/portal/policies" | jq '[.Data[] | select((.access_rights | length) == 0) | {name, id: ._id}]'
```

### Analytics and Usage Data

```bash
#!/bin/bash

echo "=== API Usage (Today) ==="
tyk_dash GET "/usage" | jq '{
    total_hits: .total,
    by_api: [.data[] | {api_name: .id, hits: .hits, errors: .errors, success_rate: (if .hits > 0 then ((.hits - .errors) / .hits * 100 | floor) else 0 end)}] | sort_by(-.hits)
}'

echo ""
echo "=== Error Breakdown ==="
tyk_dash GET "/errors" | jq '[.data[] | {api_name: .id, error_code: .code, count: .count}] | sort_by(-.count) | .[0:20]'

echo ""
echo "=== Latency Overview ==="
tyk_dash GET "/latency" | jq '[.data[] | {api_name: .id, avg_latency_ms: .average, max_latency_ms: .max}] | sort_by(-.avg_latency_ms)'
```

### Key Management

```bash
#!/bin/bash

echo "=== Active Keys Summary ==="
tyk_gw GET "/keys" | jq '{total: (.keys | length), keys: [.keys[:20]]}'

echo ""
echo "=== Key Details ==="
KEY_ID="${1:?Key ID required}"
tyk_gw GET "/keys/${KEY_ID}" | jq '{
    alias: .alias,
    expires: .expires,
    quota_max: .quota_max,
    quota_remaining: .quota_remaining,
    rate: .rate,
    per: .per,
    access_rights: [.access_rights | to_entries[] | {api: .value.api_name, versions: .value.versions}],
    is_inactive: .is_inactive
}'

echo ""
echo "=== Expired Keys ==="
tyk_gw GET "/keys" | jq --arg now "$(date +%s)" '[.keys[] | select(.expires > 0 and .expires < ($now | tonumber))]'
```

### Dashboard and Organization

```bash
#!/bin/bash

echo "=== Organization Info ==="
tyk_dash GET "/org" | jq '{id: .id, owner_name: .owner_name, cname: .cname}'

echo ""
echo "=== Dashboard Users ==="
tyk_dash GET "/users" | jq '[.users[] | {email: .email_address, role: .user_permissions, active: .active}]'

echo ""
echo "=== Portal Configuration ==="
tyk_dash GET "/portal/configuration" | jq '{enabled: .config.enable_portal, signup_enabled: .config.signup_enabled}'
```

## Safety Rules
- **Read-only by default**: Only use GET requests for discovery and inspection
- **Never delete** API definitions or policies without explicit user confirmation
- **Never expose** API keys, secrets, or auth tokens in output
- **Hot reload awareness**: Changes to API definitions require a gateway hot reload to take effect
- **Policy cascading**: Changing a policy affects all keys referencing that policy

## Output Format

Present results as a structured report:
```
Managing Tyk Report
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
- **Hot reload required**: After API changes, call `/tyk/reload/group` or the gateway won't pick up updates
- **Key hash mode**: When key hashing is enabled, raw keys cannot be retrieved; only hashed lookups work
- **Rate limit scope**: Rate limits can be set at API, policy, and key levels; the most restrictive wins
- **Dashboard vs Gateway API**: Some endpoints differ between the Dashboard API and the Gateway API; use the correct one
- **Quota reset timing**: Quotas reset based on `quota_renewal_rate` seconds, not calendar boundaries
