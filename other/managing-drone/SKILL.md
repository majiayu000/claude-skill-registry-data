---
name: managing-drone
description: |
  Use when working with Drone — drone CI pipeline execution and management.
  Covers pipeline status, build logs, secret management, repository activation,
  cron scheduling, and runner monitoring. Use when checking build status,
  investigating pipeline failures, managing secrets, or configuring Drone CI
  repositories.
connection_type: drone
preload: false
---

# Drone CI Management Skill

Manage and monitor Drone CI pipelines, builds, and secrets.

## Core Helper Functions

```bash
#!/bin/bash

# Drone API helper
drone_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${DRONE_TOKEN}" \
            -H "Content-Type: application/json" \
            "${DRONE_SERVER}/api/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${DRONE_TOKEN}" \
            "${DRONE_SERVER}/api/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always list repositories and recent builds before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Current User ==="
drone_api GET "user" | jq '{login: .login, email: .email, admin: .admin, active: .active}'

echo ""
echo "=== Active Repositories ==="
drone_api GET "user/repos?latest=true" | jq -r '
    .[] | select(.active == true) |
    "\(.slug)\t\(.visibility)\tbuild=#\(.build.number // 0)\t\(.build.status // "none")"
' | column -t | head -20

echo ""
echo "=== Recent Activity ==="
drone_api GET "user/repos?latest=true" | jq -r '
    [.[] | select(.build != null)] | sort_by(-.build.finished) | .[:15][] |
    "\(.slug)\t#\(.build.number)\t\(.build.status)\t\(.build.target)\t\(.build.finished | strftime("%Y-%m-%d %H:%M"))"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Drone API returns flat JSON — use jq for formatting
- Never dump full build logs — tail relevant sections

## Common Operations

### Build Status Dashboard

```bash
#!/bin/bash
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"

echo "=== Recent Builds ==="
drone_api GET "repos/${OWNER}/${REPO}/builds?page=1&per_page=15" | jq -r '
    .[] | "\(#\(.number))\t\(.status)\t\(.event)\t\(.target)\t\(.author_login)\t\(.finished | strftime("%Y-%m-%d %H:%M"))"
' | column -t

echo ""
echo "=== Build Stats ==="
drone_api GET "repos/${OWNER}/${REPO}/builds?page=1&per_page=50" | jq '{
    total: length,
    success: [.[] | select(.status == "success")] | length,
    failure: [.[] | select(.status == "failure")] | length,
    running: [.[] | select(.status == "running")] | length,
    killed: [.[] | select(.status == "killed")] | length
}'
```

### Build Log Analysis

```bash
#!/bin/bash
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"
BUILD="${3:?Build number required}"

echo "=== Build Info ==="
drone_api GET "repos/${OWNER}/${REPO}/builds/${BUILD}" | jq '{
    number, status, event, trigger, target, started, finished,
    author: .author_login,
    stages: [.stages[] | {name: .name, status: .status, steps: [.steps[] | {name: .name, status: .status, exit_code: .exit_code}]}]
}'

echo ""
echo "=== Failed Step Logs ==="
BUILD_INFO=$(drone_api GET "repos/${OWNER}/${REPO}/builds/${BUILD}")
STAGE=$(echo "$BUILD_INFO" | jq -r '.stages[] | select(.status == "failure") | .number' | head -1)
STEP=$(echo "$BUILD_INFO" | jq -r ".stages[] | select(.number == ${STAGE:-0}) | .steps[] | select(.status == \"failure\") | .number" | head -1)
if [ -n "$STAGE" ] && [ -n "$STEP" ]; then
    drone_api GET "repos/${OWNER}/${REPO}/builds/${BUILD}/logs/${STAGE}/${STEP}" | jq -r '.[].out' | tail -50
fi
```

### Secret Management

```bash
#!/bin/bash
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"

echo "=== Repository Secrets ==="
drone_api GET "repos/${OWNER}/${REPO}/secrets" | jq -r '
    .[] | "\(.name)\tpull_request=\(.pull_request)\tupdated=\(.updated | strftime("%Y-%m-%d"))"
' | column -t

echo ""
echo "=== Organization Secrets ==="
drone_api GET "secrets/${OWNER}" | jq -r '
    .[] | "\(.name)\tpull_request=\(.pull_request)"
' | column -t 2>/dev/null || echo "No org secrets or insufficient permissions"
```

### Repository Activation

```bash
#!/bin/bash
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"
ACTION="${3:-status}"  # status, activate, deactivate

case "$ACTION" in
    "status")
        drone_api GET "repos/${OWNER}/${REPO}" | jq '{slug, active, visibility, config_path, timeout, protected, trusted}'
        ;;
    "activate")
        echo "=== Activating repository ==="
        drone_api POST "repos/${OWNER}/${REPO}" | jq '{slug, active}'
        ;;
    "deactivate")
        echo "=== Deactivating repository ==="
        drone_api DELETE "repos/${OWNER}/${REPO}" | jq .
        ;;
esac
```

### Cron Job Management

```bash
#!/bin/bash
OWNER="${1:?Owner required}"
REPO="${2:?Repo required}"

echo "=== Cron Jobs ==="
drone_api GET "repos/${OWNER}/${REPO}/cron" | jq -r '
    .[] | "\(.name)\t\(.expr)\tbranch=\(.branch)\tnext=\(.next | strftime("%Y-%m-%d %H:%M"))"
' | column -t
```

## Anti-Hallucination Rules
- NEVER guess repository owner/name — always discover from user repos first
- NEVER fabricate build numbers — query the repo builds endpoint
- NEVER assume secret values — API only returns metadata, never values
- Stage and step numbers are 1-indexed in the API

## Safety Rules
- NEVER trigger builds without explicit user confirmation
- NEVER delete secrets without user approval
- NEVER deactivate repositories without confirming
- Build logs may contain sensitive output — warn before displaying raw logs
- Secrets with `pull_request: true` are exposed to PR builds — flag as security concern

## Output Format

Present results as a structured report:
```
Managing Drone Report
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
- **Events**: `push`, `pull_request`, `tag`, `cron`, `custom` — filter builds by event type
- **Trusted repos**: Only trusted repos can use privileged containers — check `trusted` flag
- **Config path**: Default is `.drone.yml` but can be customized per repo
- **Promotion**: Drone supports build promotion (deploy events) — separate from regular builds
- **Secrets in PRs**: By default secrets are NOT available in PR builds — `pull_request: true` enables this (security risk)
- **Jsonnet/Starlark**: Drone supports multiple config formats — `.drone.yml`, `.drone.jsonnet`, `.drone.star`
