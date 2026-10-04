---
name: managing-seq
description: |
  Use when working with Seq — seq structured log server for centralized log
  collection, querying, dashboards, alerting, and retention management. Covers
  log searching with Seq query language, signal management, alert configuration,
  API key management, and workspace administration. Use when querying Seq logs,
  investigating structured events, managing signals and alerts, or reviewing log
  retention policies.
connection_type: seq
preload: false
---

# Seq Monitoring Skill

Query, analyze, and manage Seq structured log data using the Seq HTTP API.

## API Overview

Seq uses a REST API at `https://<SEQ_HOST>/api`.

### Core Helper Function

```bash
#!/bin/bash

seq_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "${SEQ_URL}/api/${endpoint}" \
            -H "X-Seq-ApiKey: $SEQ_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${SEQ_URL}/api/${endpoint}" \
            -H "X-Seq-ApiKey: $SEQ_API_KEY"
    fi
}

seq_query() {
    local filter="$1"
    local count="${2:-30}"
    seq_api GET "events?filter=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${filter}'))")&count=${count}"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover signals, dashboards, and API keys before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Server Info ==="
seq_api GET "" | jq -r '"Version: \(.Version)\nInstance: \(.InstanceName)"'

echo ""
echo "=== Signals ==="
seq_api GET "signals" | jq -r '.[] | "\(.Id)\t\(.Title)\t\(.Filters[0].Filter // "no filter")"' | head -20

echo ""
echo "=== Dashboards ==="
seq_api GET "dashboards" | jq -r '.[] | "\(.Id)\t\(.Title)"' | head -15

echo ""
echo "=== Alert Configurations ==="
seq_api GET "alertconfigurations" | jq -r '.[] | "\(.Id)\t\(.Title)\t\(.NotificationAppInstanceId)"' | head -15

echo ""
echo "=== Retention Policies ==="
seq_api GET "retentionpolicies" | jq -r '.[] | "\(.Id)\t\(.RetentionTime)\t\(.DeletedAt // "active")"' | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Recent Error Events ==="
seq_query "@Level = 'Error'" 20 \
    | jq -r '.[] | "\(.Timestamp[0:19])\t\(.Properties["SourceContext"] // "unknown")\t\(.RenderedMessage[0:80])"' | head -20

echo ""
echo "=== Event Volume by Level ==="
seq_api GET "events/signal?signal=level" \
    | jq -r '.[] | "\(.Label)\t\(.Count)"' | head -10

echo ""
echo "=== Recent Warnings ==="
seq_query "@Level = 'Warning'" 15 \
    | jq -r '.[] | "\(.Timestamp[0:19])\t\(.RenderedMessage[0:80])"' | head -15

echo ""
echo "=== Active Alerts ==="
seq_api GET "alerts" | jq -r '.[] | "\(.Id)\t\(.State)\t\(.OwnerTitle)"' | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `count` parameter and Seq filters
- Use Seq query language for filtering (e.g., `@Level = 'Error' and SourceContext like '%Payment%'`)
- Leverage signals for pre-defined log groupings instead of ad-hoc queries

## Output Format

Present results as a structured report:
```
Managing Seq Report
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

