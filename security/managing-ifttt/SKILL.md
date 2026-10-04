---
name: managing-ifttt
description: |
  Use when working with Ifttt — iFTTT automation platform management covering
  applet inventory, service connection health, activity log monitoring, and
  usage tracking. Use when auditing applet configurations, investigating trigger
  or action failures, monitoring service connectivity, or reviewing automation
  activity history.
connection_type: ifttt
preload: false
---

# IFTTT Management Skill

Manage and monitor IFTTT applets, service connections, and automation activity.

## MANDATORY: Discovery-First Pattern

**Always list applets and services before querying specific resources.**

### Phase 1: Discovery

```bash
#!/bin/bash

IFTTT_API="https://connect.ifttt.com/v2"

ifttt_api() {
    curl -s -H "Authorization: Bearer $IFTTT_SERVICE_KEY" \
         -H "Content-Type: application/json" \
         "${IFTTT_API}/${1}"
}

echo "=== IFTTT Service Info ==="
ifttt_api "me" | jq '{user_id: .data.id, email: .data.email, tier: .data.tier}'

echo ""
echo "=== Active Applets ==="
ifttt_api "applets?limit=50" | jq -r '
    .data[] |
    "\(.id)\t\(.name)\t\(.status)\t\(.trigger_service // "unknown")"
' | column -t | head -30

echo ""
echo "=== Connected Services ==="
ifttt_api "connections" | jq -r '
    .data[] |
    "\(.service_id)\t\(.service_name)\t\(.status)\t\(.connected_at // "unknown")"
' | column -t | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Recent Activity Log ==="
ifttt_api "activity?limit=20" | jq -r '
    .data[] |
    "\(.timestamp)\t\(.applet_name)\t\(.status)\t\(.message // "")"
' | column -t | head -20

echo ""
echo "=== Failed Applets ==="
ifttt_api "applets?status=failed" | jq -r '
    .data[] |
    "\(.id)\t\(.name)\t\(.error_count // 0) errors\t\(.last_error // "none")"
' | column -t

echo ""
echo "=== Applet Summary ==="
ifttt_api "applets?limit=100" | jq '{
    total: (.data | length),
    active: [.data[] | select(.status == "active")] | length,
    paused: [.data[] | select(.status == "paused")] | length,
    errored: [.data[] | select(.status == "error")] | length
}'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Filter applets by status to focus on problem areas
- Never dump full applet configurations -- extract trigger and action service names

## Output Format

Present results as a structured report:
```
Managing Ifttt Report
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

- **Service disconnects**: Services require re-authentication when tokens expire
- **Polling triggers**: IFTTT polls some triggers at intervals -- not real-time for all services
- **Rate limits**: Free tier limits applet count and execution frequency
- **Filter codes**: Applets with filter code (JavaScript) can silently skip executions
- **Multi-action**: Pro+ applets with multiple actions -- one failing action does not stop others
- **Webhook security**: Webhook triggers expose URLs that anyone can call -- rotate if compromised
