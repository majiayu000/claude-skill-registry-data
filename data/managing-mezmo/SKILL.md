---
name: managing-mezmo
description: |
  Use when working with Mezmo — mezmo (formerly LogDNA) observability pipeline
  and log management platform for log ingestion, routing, processing, and
  analysis. Covers log querying, pipeline management, view configuration,
  alerting, and usage analytics. Use when searching Mezmo logs, managing log
  pipelines, configuring alert rules, or analyzing ingestion patterns.
connection_type: mezmo
preload: false
---

# Mezmo Monitoring Skill

Query, analyze, and manage Mezmo log data and pipelines using the Mezmo API.

## API Overview

Mezmo uses REST APIs at `https://api.mezmo.com` for log management and `https://pipeline.mezmo.com` for pipeline operations.

### Core Helper Function

```bash
#!/bin/bash

mezmo_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" "https://api.mezmo.com/v2/${endpoint}" \
            -H "Authorization: Bearer $MEZMO_SERVICE_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "https://api.mezmo.com/v2/${endpoint}" \
            -H "Authorization: Bearer $MEZMO_SERVICE_KEY"
    fi
}

mezmo_pipeline() {
    local method="$1"
    local endpoint="$2"
    curl -s -X "$method" "https://pipeline.mezmo.com/v1/${endpoint}" \
        -H "Authorization: Bearer $MEZMO_PIPELINE_KEY" \
        -H "Content-Type: application/json"
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available sources, apps, and pipelines before querying.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Usage by App ==="
mezmo_api GET "usage/app" | jq -r '.[] | "\(.name)\t\(.lines) lines"' | sort -t$'\t' -k2 -rn | head -20

echo ""
echo "=== Usage by Host ==="
mezmo_api GET "usage/host" | jq -r '.[] | "\(.name)\t\(.lines) lines"' | sort -t$'\t' -k2 -rn | head -20

echo ""
echo "=== Views ==="
mezmo_api GET "config/view" | jq -r '.[] | "\(.name)\t\(.query // "no filter")"' | head -15

echo ""
echo "=== Pipelines ==="
mezmo_pipeline GET "pipelines" | jq -r '.data[] | "\(.id)\t\(.title)\t\(.status)"' | head -15

echo ""
echo "=== Alerts ==="
mezmo_api GET "config/alert" | jq -r '.[] | "\(.name)\t\(.active)"' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Recent Error Logs ==="
mezmo_api GET "export?query=level%3Aerror&size=30" \
    | jq -r '.lines[] | "\(._ts[0:19])\t\(._app)\t\(._line[0:80])"' | head -20

echo ""
echo "=== Log Volume by Level ==="
mezmo_api GET "usage/level" | jq -r '.[] | "\(.name)\t\(.lines)"' | sort -t$'\t' -k2 -rn | head -10

echo ""
echo "=== Pipeline Health ==="
mezmo_pipeline GET "pipelines" \
    | jq -r '.data[] | "\(.title)\tstatus:\(.status)\tnodes:\(.nodes | length)"' | head -15

echo ""
echo "=== Top Ingestion Sources ==="
mezmo_api GET "usage/tag" | jq -r '.[] | "\(.name)\t\(.lines) lines"' | sort -t$'\t' -k2 -rn | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines — use `size` parameter and `head` in output
- Use usage endpoints for aggregated volume data
- Filter at query level before post-processing with jq

## Output Format

Present results as a structured report:
```
Managing Mezmo Report
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

