---
name: managing-modal
description: |
  Use when working with Modal — modal serverless compute management covering app
  inventory, function deployments, container status, volume mounts, secret
  management, scheduled job analysis, GPU utilization, and usage metrics. Use
  for comprehensive Modal workspace assessment and compute optimization.
connection_type: modal
preload: false
---

# Modal Management

Analyze Modal apps, functions, containers, volumes, and GPU compute usage.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${MODAL_TOKEN_ID}:${MODAL_TOKEN_SECRET}"
BASE="https://api.modal.com/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Apps Inventory ==="
curl -s "${BASE}/apps" "${AUTH[@]}" \
  | jq -r '.apps[] | "\(.app_id)\t\(.name)\t\(.state)\t\(.created_at[0:19])"' \
  | column -t | head -20

echo ""
echo "=== Functions ==="
for APP in $(curl -s "${BASE}/apps" "${AUTH[@]}" | jq -r '.apps[].app_id'); do
  APP_NAME=$(curl -s "${BASE}/apps/${APP}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/apps/${APP}/functions" "${AUTH[@]}" \
    | jq -r ".functions[]? | \"${APP_NAME}\t\(.name)\t\(.gpu // \"cpu\")\t\(.memory_mb // \"default\")MB\t\(.timeout_secs // 300)s\"" 2>/dev/null
done | column -t | head -30

echo ""
echo "=== Volumes ==="
curl -s "${BASE}/volumes" "${AUTH[@]}" \
  | jq -r '.volumes[] | "\(.name)\t\(.volume_id)\t\(.created_at[0:10])"' \
  | column -t | head -15

echo ""
echo "=== Secrets (names only) ==="
curl -s "${BASE}/secrets" "${AUTH[@]}" \
  | jq -r '.secrets[] | "\(.name)\t\(.created_at[0:10])"' \
  | column -t | head -15
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${MODAL_TOKEN_ID}:${MODAL_TOKEN_SECRET}"
BASE="https://api.modal.com/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Active Containers ==="
for APP in $(curl -s "${BASE}/apps" "${AUTH[@]}" | jq -r '.apps[].app_id'); do
  APP_NAME=$(curl -s "${BASE}/apps/${APP}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/apps/${APP}/containers" "${AUTH[@]}" \
    | jq -r ".containers[]? | \"${APP_NAME}\t\(.container_id[0:12])\t\(.state)\t\(.gpu // \"cpu\")\t\(.region)\"" 2>/dev/null
done | column -t | head -20

echo ""
echo "=== Scheduled Functions ==="
for APP in $(curl -s "${BASE}/apps" "${AUTH[@]}" | jq -r '.apps[].app_id'); do
  APP_NAME=$(curl -s "${BASE}/apps/${APP}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/apps/${APP}/schedules" "${AUTH[@]}" \
    | jq -r ".schedules[]? | \"${APP_NAME}\t\(.function_name)\t\(.cron)\t\(.last_run // \"never\")\t\(.next_run)\"" 2>/dev/null
done | column -t | head -15

echo ""
echo "=== GPU Usage Summary ==="
for APP in $(curl -s "${BASE}/apps" "${AUTH[@]}" | jq -r '.apps[].app_id'); do
  APP_NAME=$(curl -s "${BASE}/apps/${APP}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/apps/${APP}/functions" "${AUTH[@]}" \
    | jq -r ".functions[]? | select(.gpu != null) | \"${APP_NAME}\t\(.name)\t\(.gpu)\t\(.concurrency_limit // \"default\")\"" 2>/dev/null
done | column -t | head -15

echo ""
echo "=== Recent Invocations ==="
curl -s "${BASE}/task-logs?limit=10" "${AUTH[@]}" \
  | jq -r '.logs[]? | "\(.app_name)\t\(.function_name)\t\(.status)\t\(.duration_ms)ms\t\(.created_at[0:19])"' \
  | column -t | head -15

echo ""
echo "=== Resource Summary ==="
echo "Apps: $(curl -s "${BASE}/apps" "${AUTH[@]}" | jq '.apps | length')"
echo "Volumes: $(curl -s "${BASE}/volumes" "${AUTH[@]}" | jq '.volumes | length')"
echo "Secrets: $(curl -s "${BASE}/secrets" "${AUTH[@]}" | jq '.secrets | length')"
```

## Output Format

```
MODAL ANALYSIS
================
App              Functions  GPU        Containers  Volumes  Schedules
──────────────────────────────────────────────────────────────────────
ml-pipeline      5          A100x2     3 active    2        2 cron
api-server       3          cpu        1 active    0        0
batch-process    4          T4x1       0 idle      1        1 cron

GPU Usage: A100(2) T4(1) | Functions: 12 total
Active Containers: 4 | Volumes: 3 | Secrets: 8
Schedules: 3 cron jobs (all healthy)
```

## Safety Rules

- **Read-only**: Only use GET/list API endpoints
- **Never deploy, stop, or delete** apps or functions without confirmation
- **Secrets**: Never output secret values, only list names
- **Token security**: Never expose Modal token ID or secret in output

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

