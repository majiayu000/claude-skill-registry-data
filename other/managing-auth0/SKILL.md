---
name: managing-auth0
description: |
  Use when working with Auth0 — auth0 identity platform management for tenant
  configuration, application setup, connection analysis, rule and action review,
  user management, and log inspection. Covers universal login, social
  connections, enterprise federation, and Auth0 Actions pipelines. Read this
  skill before any Auth0 operations — it enforces discovery-first patterns and
  strict read-only safety rules.
connection_type: auth0
preload: false
---

# Auth0 Management Skill

Safely read and audit Auth0 — the identity platform for application builders.

## MANDATORY: Discovery-First Pattern

**Always discover tenant configuration, applications, and connections before performing targeted queries. Never guess client IDs or connection names.**

### Phase 1: Discovery

```bash
#!/bin/bash

auth0_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
         -H "Content-Type: application/json" \
         "https://${AUTH0_DOMAIN}/api/v2/${endpoint}"
}

echo "=== Tenant Settings ==="
auth0_api "tenants/settings" | jq '{
    friendly_name: .friendly_name,
    support_email: .support_email,
    default_directory: .default_directory,
    enabled_locales: .enabled_locales,
    flags: {
        universal_login: .flags.universal_login,
        disable_clickjack_protection: .flags.disable_clickjack_protection_headers,
        enable_pipeline2: .flags.enable_pipeline2
    }
}'

echo ""
echo "=== Applications ==="
auth0_api "clients?fields=client_id,name,app_type,callbacks&include_fields=true" | jq -r '.[] | "\(.client_id)\t\(.name)\t\(.app_type)"' | column -t

echo ""
echo "=== Connections ==="
auth0_api "connections?fields=id,name,strategy,enabled_clients" | jq -r '.[] | "\(.id)\t\(.name)\t\(.strategy)\tClients: \(.enabled_clients | length)"' | column -t

echo ""
echo "=== APIs (Resource Servers) ==="
auth0_api "resource-servers" | jq -r '.[] | "\(.id)\t\(.name)\t\(.identifier)"' | column -t
```

**Phase 1 outputs:** Tenant config, client list, connections, APIs — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess client IDs** — always list clients in Phase 1
- **NEVER assume connection names** — always list connections first
- **NEVER fabricate rule or action names** — always list before querying
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — `clients`, `connections`, `users`, `logs`, `rules`, `actions`
- **MASK sensitive data**: Redact client secrets, user passwords, and API keys in output
- **FORBIDDEN without explicit request**: POST/PUT/DELETE/PATCH to clients, connections, users; secret rotation
- **NEVER print client secrets**: Always use `*** REDACTED ***` for secret fields

## Core Helper Functions

```bash
#!/bin/bash

auth0_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
         -H "Content-Type: application/json" \
         "https://${AUTH0_DOMAIN}/api/v2/${endpoint}"
}

# Paginated fetch with Auth0's page/per_page pattern
auth0_api_paginated() {
    local endpoint="$1"
    local max_pages="${2:-5}"
    local per_page=50
    local page=0

    while [ $page -lt $max_pages ]; do
        local separator="?"
        [[ "$endpoint" == *"?"* ]] && separator="&"
        result=$(auth0_api "${endpoint}${separator}page=${page}&per_page=${per_page}&include_totals=true")
        total=$(echo "$result" | jq -r '.total // 0')
        echo "$result" | jq '.users // .logs // .[] // empty'
        [ $((($page + 1) * $per_page)) -ge $total ] && break
        page=$((page + 1))
    done
}
```

## Common Operations

### Application Configuration Review

```bash
#!/bin/bash
CLIENT_ID="${1:?Client ID required — discover via Phase 1}"

echo "=== Application Details ==="
auth0_api "clients/${CLIENT_ID}" | jq '{
    name: .name,
    app_type: .app_type,
    client_id: .client_id,
    client_secret: "*** REDACTED ***",
    callbacks: .callbacks,
    allowed_origins: .allowed_origins,
    web_origins: .web_origins,
    allowed_logout_urls: .allowed_logout_urls,
    grant_types: .grant_types,
    token_endpoint_auth_method: .token_endpoint_auth_method,
    jwt_configuration: .jwt_configuration,
    is_first_party: .is_first_party
}'

echo ""
echo "=== Enabled Connections for App ==="
auth0_api "clients/${CLIENT_ID}/connections" | jq -r '.[] | "\(.connection)\t\(.strategy)\t\(.status)"' | column -t 2>/dev/null || \
    auth0_api "connections" | jq -r --arg cid "$CLIENT_ID" '.[] | select(.enabled_clients | index($cid)) | "\(.name)\t\(.strategy)"' | column -t
```

### Connection Analysis

```bash
#!/bin/bash
echo "=== All Connections with Details ==="
auth0_api "connections" | jq -r '.[] | {
    id: .id,
    name: .name,
    strategy: .strategy,
    enabled_clients_count: (.enabled_clients | length),
    realms: .realms,
    is_domain_connection: .is_domain_connection
}'

echo ""
echo "=== Social Connections ==="
auth0_api "connections?strategy=google-oauth2,github,facebook,apple,linkedin,microsoft" | jq -r '.[] | "\(.name)\t\(.strategy)\tClients: \(.enabled_clients | length)"' | column -t

echo ""
echo "=== Enterprise Connections ==="
auth0_api "connections" | jq -r '.[] | select(.strategy | test("samlp|oidc|waad|adfs|ad|google-apps")) | "\(.name)\t\(.strategy)\tClients: \(.enabled_clients | length)"' | column -t
```

### Rule & Action Review

```bash
#!/bin/bash
echo "=== Rules (Legacy) ==="
auth0_api "rules" | jq -r '.[] | "\(.id)\t\(.name)\t\(.stage)\t\(.enabled)\tOrder: \(.order)"' | column -t

echo ""
echo "=== Actions ==="
auth0_api "actions/actions?deployed=true" | jq -r '.actions[] | "\(.id)\t\(.name)\t\(.status)\tTrigger: \(.supported_triggers[0].id)"' | column -t

echo ""
echo "=== Action Flows (Triggers) ==="
for trigger in post-login credentials-exchange pre-user-registration post-user-registration post-change-password send-phone-message; do
    bindings=$(auth0_api "actions/triggers/${trigger}/bindings" | jq '.bindings | length')
    [ "$bindings" -gt 0 ] 2>/dev/null && echo "${trigger}: ${bindings} action(s) bound"
done
```

### User Management & Search

```bash
#!/bin/bash
SEARCH="${1:?Search term required (email or name)}"

echo "=== User Search: $SEARCH ==="
auth0_api "users?q=email%3A*${SEARCH}*&search_engine=v3&fields=user_id,email,name,logins_count,last_login,created_at,blocked,identities" | jq -r '.[] | {
    user_id: .user_id,
    email: .email,
    name: .name,
    logins_count: .logins_count,
    last_login: .last_login,
    created_at: .created_at,
    blocked: .blocked,
    providers: [.identities[].provider]
}'
```

### Log & Event Analysis

```bash
#!/bin/bash
echo "=== Recent Logs (last 50 events) ==="
auth0_api "logs?sort=date:-1&per_page=50" | jq -r '.[] | {
    date: .date,
    type: .type,
    description: .description,
    client_name: .client_name,
    user_name: .user_name,
    ip: .ip,
    location: "\(.location_info.city_name // "N/A"), \(.location_info.country_name // "N/A")"
}'

echo ""
echo "=== Failed Login Events ==="
auth0_api "logs?q=type%3Af*&sort=date:-1&per_page=20" | jq -r '.[] | "\(.date)\t\(.type)\t\(.user_name // "unknown")\t\(.ip)\t\(.description)"' | column -t

echo ""
echo "=== Event Type Summary ==="
auth0_api "logs?sort=date:-1&per_page=100" | jq -r '[.[] | .type] | group_by(.) | map({type: .[0], count: length}) | sort_by(-.count) | .[:10][] | "\(.type)\t\(.count)"' | column -t
```

## Output Format

Present results as a structured report:
```
Managing Auth0 Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Management API token expiry**: Tokens are short-lived (24h default) — regenerate via client credentials grant to `/oauth/token`
- **Rate limits**: Management API has strict rate limits (varies by endpoint) — check `X-RateLimit-Remaining` header
- **Search engine v3**: User search requires `search_engine=v3` parameter — v2 is deprecated and returns different results
- **Rules vs Actions**: Rules are legacy (single pipeline); Actions are the modern replacement — check both during audits
- **Log event types**: Auth0 uses short codes (`s`, `f`, `fp`, `fu`) — reference the Log Event Type Codes documentation
- **Connection strategy names**: `waad` = Azure AD, `google-apps` = Google Workspace, `ad` = Active Directory — names differ from marketing names
- **Client secrets**: Machine-to-machine apps need secrets; SPAs should use PKCE — mismatched auth methods cause silent failures
- **Tenant log retention**: Depends on plan tier (2-30 days) — export to external storage for long-term analysis
