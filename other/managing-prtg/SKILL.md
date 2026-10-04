---
name: managing-prtg
description: |
  Use when working with Prtg — pRTG Network Monitor platform for network
  devices, bandwidth, servers, applications, and cloud services monitoring.
  Covers sensor status, device tree management, alert review, historic data
  analysis, and notification management. Use when monitoring PRTG sensors,
  investigating device issues, reviewing alarms, or analyzing bandwidth and
  performance data.
connection_type: prtg
preload: false
---

# PRTG Monitoring Skill

Query, analyze, and manage PRTG monitoring data using the PRTG HTTP API.

## API Overview

PRTG uses an HTTP API at `https://<PRTG_HOST>/api`.

### Core Helper Function

```bash
#!/bin/bash

prtg_api() {
    local endpoint="$1"
    local params="${2:-}"
    curl -s "${PRTG_URL}/api/${endpoint}?username=${PRTG_USER}&passhash=${PRTG_PASSHASH}&${params}&output=json"
}

prtg_table() {
    local content="$1"
    local columns="${2:-objid,name,status}"
    local count="${3:-50}"
    local filter="${4:-}"
    prtg_api "table.json" "content=${content}&columns=${columns}&count=${count}&${filter}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover groups, devices, and sensors before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Server Status ==="
prtg_api "status.json" | jq -r '"Version: \(.Version)\nSensors: \(.Sensors)\nAlarms: \(.Alarms)\nUp: \(.UpSens) Down: \(.DownSens) Warning: \(.WarnSens)"'

echo ""
echo "=== Groups ==="
prtg_table "groups" "objid,name,active,totalsens" 20 \
    | jq -r '.groups[] | "\(.objid)\t\(.name)\tsensors:\(.totalsens)\t\(.active)"' | head -20

echo ""
echo "=== Devices ==="
prtg_table "devices" "objid,device,host,active,status" 25 \
    | jq -r '.devices[] | "\(.objid)\t\(.device)\t\(.host)\t\(.status)"' | head -25

echo ""
echo "=== Sensor Types ==="
prtg_table "sensors" "objid,name,sensor,status" 50 \
    | jq -r '[.sensors[].sensor] | group_by(.) | map({type: .[0], count: length}) | sort_by(-.count)[] | "\(.type)\t\(.count)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Down Sensors ==="
prtg_table "sensors" "objid,name,device,status,message" 30 "filter_status=5" \
    | jq -r '.sensors[] | "\(.device)\t\(.name)\t\(.message[0:50])"' | head -15

echo ""
echo "=== Warning Sensors ==="
prtg_table "sensors" "objid,name,device,status,lastvalue" 20 "filter_status=4" \
    | jq -r '.sensors[] | "\(.device)\t\(.name)\t\(.lastvalue)"' | head -15

echo ""
echo "=== Alarms ==="
prtg_table "sensors" "objid,name,device,status,message,lastdown" 20 "filter_status=5&filter_status=4" \
    | jq -r '.sensors[] | "\(.status)\t\(.device)/\(.name)\t\(.message[0:50])"' | head -15

echo ""
echo "=== Top Bandwidth Sensors ==="
prtg_table "sensors" "objid,name,device,lastvalue" 15 "filter_type=snmptraffic" \
    | jq -r '.sensors[] | "\(.device)\t\(.name)\t\(.lastvalue)"' | head -15

echo ""
echo "=== System Health ==="
prtg_api "status.json" | jq -r '"Acknowledged: \(.AckAlarms)\nPartial Down: \(.PartialDownSens)\nPaused: \(.PausedSens)\nUnusual: \(.UnusualSens)"'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `count` and `filter_status` parameters
- Sensor status codes: 1=Unknown, 2=Scanning, 3=Up, 4=Warning, 5=Down, 7=NotUp, 8=Paused
- Use `filter_status` for server-side filtering of sensor states
- Use `columns` parameter to limit returned fields

## Output Format

Present results as a structured report:
```
Managing Prtg Report
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

