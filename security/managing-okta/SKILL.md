---
name: managing-okta
description: |
  Use when working with Okta — okta identity and access management for user
  lifecycle management, application assignments, MFA status review, group and
  policy administration, and system log analysis. Covers user provisioning, SSO
  app management, authentication policy review, and security event
  investigation. Read this skill before any Okta operations — it enforces
  discovery-first patterns and strict read-only safety rules.
connection_type: okta
preload: false
---

# Okta Management Skill

Safely read and audit Okta — the identity and access management platform.

## MANDATORY: Discovery-First Pattern

**Always discover the Okta org configuration and available resources before performing targeted queries. Never guess user IDs or app IDs.**

### Phase 1: Discovery

```bash
#!/bin/bash

okta_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: SSWS $OKTA_API_TOKEN" \
         -H "Content-Type: application/json" \
         "${OKTA_ORG_URL}/api/v1/${endpoint}"
}

echo "=== Okta Org Info ==="
okta_api "org" | jq '{
    id: .id,
    company_name: .companyName,
    subdomain: .subdomain,
    status: .status,
    created: .created
}'

echo ""
echo "=== User Count ==="
okta_api "users?limit=1" -I 2>/dev/null | grep -i x-rate-limit || \
    okta_api "users?limit=1&filter=status+eq+%22ACTIVE%22" | jq '. | length | "Sample returned: \(.)"' -r

echo ""
echo "=== Applications (first 20) ==="
okta_api "apps?limit=20" | jq -r '.[] | "\(.id)\t\(.label)\t\(.status)\t\(.signOnMode)"' | column -t

echo ""
echo "=== Authentication Policies ==="
okta_api "policies?type=ACCESS_POLICY" | jq -r '.[] | "\(.id)\t\(.name)\t\(.status)"' | column -t
```

**Phase 1 outputs:** Org details, app inventory, policy list — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess user login or ID** — always search via `users?search=` or `users?filter=`
- **NEVER assume app labels** — always list apps in Phase 1
- **NEVER fabricate group names** — always list via `groups?q=`
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — `users`, `apps`, `groups`, `logs`, `policies`
- **MASK sensitive data**: When displaying user profiles, redact SSN, passwords, recovery questions
- **FORBIDDEN without explicit request**: POST/PUT/DELETE to users, apps, groups; password resets; MFA factor enrollment
- **NEVER print API tokens**: Always redact token values in output

## Core Helper Functions

```bash
#!/bin/bash

okta_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: SSWS $OKTA_API_TOKEN" \
         -H "Content-Type: application/json" \
         "${OKTA_ORG_URL}/api/v1/${endpoint}"
}

# Paginated fetch — follows Okta's Link header pagination
okta_api_paginated() {
    local endpoint="$1"
    local max_pages="${2:-5}"
    local url="${OKTA_ORG_URL}/api/v1/${endpoint}"
    local page=0

    while [ -n "$url" ] && [ $page -lt $max_pages ]; do
        response=$(curl -s -D /tmp/okta_headers \
            -H "Authorization: SSWS $OKTA_API_TOKEN" \
            -H "Content-Type: application/json" \
            "$url")
        echo "$response"
        url=$(grep -i '^link:' /tmp/okta_headers | grep 'rel="next"' | sed 's/.*<\(.*\)>.*/\1/' | tr -d '\r')
        page=$((page + 1))
    done
}

# Search users safely
search_users() {
    local query="$1"
    okta_api "users?search=profile.email+sw+%22${query}%22&limit=10"
}
```

## Common Operations

### User Lookup & Status

```bash
#!/bin/bash
SEARCH="${1:?Search term required (email, login, or name)}"

echo "=== User Search: $SEARCH ==="
okta_api "users?search=profile.login+sw+%22${SEARCH}%22+or+profile.email+sw+%22${SEARCH}%22&limit=10" | jq -r '.[] | {
    id: .id,
    login: .profile.login,
    email: .profile.email,
    name: "\(.profile.firstName) \(.profile.lastName)",
    status: .status,
    created: .created,
    last_login: .lastLogin,
    password_changed: .passwordChanged
}'
```

### MFA Factor Status

```bash
#!/bin/bash
USER_ID="${1:?User ID required — discover via user search first}"

echo "=== MFA Factors for $USER_ID ==="
okta_api "users/${USER_ID}/factors" | jq -r '.[] | {
    id: .id,
    type: .factorType,
    provider: .provider,
    status: .status,
    created: .created,
    last_verified: .lastVerifiedAt
}'

echo ""
echo "=== Available (Not Enrolled) Factors ==="
okta_api "users/${USER_ID}/factors/catalog" | jq -r '.[] | "\(.factorType)\t\(.provider)\t\(.status)"' | column -t
```

### Application Assignments

```bash
#!/bin/bash
USER_ID="${1:?User ID required}"

echo "=== Apps Assigned to User $USER_ID ==="
okta_api "users/${USER_ID}/appLinks" | jq -r '.[] | "\(.appName)\t\(.label)\t\(.linkUrl)"' | column -t

echo ""
echo "=== App User Count (top 10 apps) ==="
okta_api "apps?limit=10" | jq -r '.[] | .id' | while read app_id; do
    label=$(okta_api "apps/$app_id" | jq -r '.label')
    count=$(okta_api "apps/${app_id}/users?limit=1" | jq '. | length')
    echo "$label\t$count users (sampled)"
done | column -t
```

### System Log Analysis

```bash
#!/bin/bash
SINCE="${1:-$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)}"

echo "=== System Log Events (since $SINCE) ==="
okta_api "logs?since=${SINCE}&limit=20&sortOrder=DESCENDING" | jq -r '.[] | {
    time: .published,
    event: .eventType,
    severity: .severity,
    actor: .actor.displayName,
    outcome: .outcome.result,
    target: (.target[0].displayName // "N/A"),
    client_ip: .client.ipAddress
}'

echo ""
echo "=== Failed Login Attempts ==="
okta_api "logs?since=${SINCE}&filter=eventType+eq+%22user.session.start%22+and+outcome.result+eq+%22FAILURE%22&limit=20" | jq -r '.[] | "\(.published)\t\(.actor.displayName)\t\(.client.ipAddress)\t\(.outcome.reason)"' | column -t
```

### Group & Policy Review

```bash
#!/bin/bash
echo "=== Groups (first 20) ==="
okta_api "groups?limit=20" | jq -r '.[] | "\(.id)\t\(.profile.name)\t\(.type)\tMembers: \(.profile.memberCount // "N/A")"' | column -t

echo ""
echo "=== Sign-On Policies ==="
okta_api "policies?type=OKTA_SIGN_ON" | jq -r '.[] | {
    id: .id,
    name: .name,
    status: .status,
    description: .description,
    priority: .priority
}'

echo ""
echo "=== Password Policies ==="
okta_api "policies?type=PASSWORD" | jq -r '.[] | {
    id: .id,
    name: .name,
    min_length: .settings.password.complexity.minLength,
    require_lowercase: .settings.password.complexity.minLowerCase,
    require_uppercase: .settings.password.complexity.minUpperCase,
    require_number: .settings.password.complexity.minNumber,
    max_age_days: .settings.password.age.maxAgeDays
}'
```

## Output Format

Present results as a structured report:
```
Managing Okta Report
════════════════════
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

- **Rate limits**: Okta enforces per-endpoint rate limits (typically 600/min for `/api/v1/users`) — check `X-Rate-Limit-Remaining` header
- **Pagination**: List endpoints return max 200 items — always follow `Link: rel="next"` headers for complete data
- **User status lifecycle**: STAGED -> PROVISIONED -> ACTIVE -> SUSPENDED/DEPROVISIONED — status transitions are one-directional in some cases
- **Search vs filter**: `search` uses Okta's search engine (eventual consistency); `filter` is exact match (strong consistency) — use filter for precise lookups
- **System log retention**: Default 90 days; compressed logs may take longer to query — always specify `since` parameter
- **API token scope**: Token inherits permissions of the admin who created it — insufficient permissions return 403, not empty results
- **Group types**: OKTA_GROUP (manually managed) vs APP_GROUP (synced from app) vs BUILT_IN — behavior differs by type
- **Deprovisioned users**: Still exist in Okta but cannot authenticate — include `status eq "DEPROVISIONED"` in filter to find them
