---
name: managing-eppo
description: |
  Use when working with Eppo — eppo feature flag management, experiment
  assignment, statistical analysis, and metric definition. Covers flag
  configuration, experiment design, Bayesian and frequentist analysis, metric
  pipelines, and CUPED variance reduction. Use when managing feature flags,
  reviewing experiment results, configuring metrics, or analyzing treatment
  effects in Eppo.
connection_type: eppo
preload: false
---

# Eppo Management Skill

Manage and analyze feature flags, experiments, metrics, and statistical results in Eppo.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $EPPO_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.eppo.cloud/api/v1`

### Core Helper Function

```bash
#!/bin/bash

eppo_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $EPPO_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.eppo.cloud/api/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $EPPO_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.eppo.cloud/api/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Feature Flags

```bash
#!/bin/bash
echo "=== Feature Flags ==="
eppo_api GET "/feature-flags?limit=25" \
    | jq -r '.flags[] | "\(.type)\t\(.key)\t\(.enabled)\t\(.name[0:40])"' | column -t

echo ""
echo "=== Flag Summary ==="
eppo_api GET "/feature-flags?limit=100" \
    | jq '{total: (.flags | length), enabled: ([.flags[] | select(.enabled)] | length), by_type: (.flags | group_by(.type) | map({(.[0].type): length}) | add)}'
```

### List Experiments

```bash
#!/bin/bash
echo "=== Experiments ==="
eppo_api GET "/experiments?limit=20" \
    | jq -r '.experiments[] | "\(.status)\t\(.name[0:40])\t\(.variations | length) variations\t\(.start_date[0:10] // "not started")"' \
    | column -t

echo ""
echo "=== Experiment Status Summary ==="
eppo_api GET "/experiments?limit=50" \
    | jq -r '.experiments[] | .status' | sort | uniq -c | sort -rn
```

## Analysis Phase

### Experiment Results

```bash
#!/bin/bash
EXPERIMENT_KEY="${1:?Experiment key required}"

echo "=== Experiment Details ==="
eppo_api GET "/experiments/${EXPERIMENT_KEY}" \
    | jq '{name, status, hypothesis: .hypothesis[0:100], variations: [.variations[].name], primary_metric: .primary_metric, guardrail_metrics: .guardrail_metrics}'

echo ""
echo "=== Results ==="
eppo_api GET "/experiments/${EXPERIMENT_KEY}/results" \
    | jq -r '.metrics[0:10][] | "\(.metric_name[0:30])\t\(.treatment)\tlift:\(.lift // "pending")\tp:\(.p_value // "pending")\tci:\(.confidence_interval // "pending")"' \
    | column -t 2>/dev/null || echo "Results not yet available"
```

### Metrics

```bash
#!/bin/bash
echo "=== Metrics ==="
eppo_api GET "/metrics?limit=20" \
    | jq -r '.metrics[] | "\(.type)\t\(.name[0:40])\t\(.data_source)"' | column -t

echo ""
echo "=== Metric Summary ==="
eppo_api GET "/metrics?limit=50" \
    | jq '{total: (.metrics | length), by_type: (.metrics | group_by(.type) | map({(.[0].type): length}) | add)}'

echo ""
echo "=== Assignments ==="
eppo_api GET "/assignments/summary" \
    | jq -r '.[] | "\(.experiment_key)\t\(.total_assignments)\t\(.variation_counts | to_entries | map("\(.key):\(.value)") | join(", "))"' \
    | column -t | head -10 2>/dev/null
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Statistical rigor**: Eppo emphasizes proper statistics -- CUPED variance reduction is applied by default
- **Sequential testing**: Experiments use sequential testing -- results are valid at any point during the experiment
- **Metric types**: `conversion`, `revenue`, `ratio`, `funnel` -- type affects analysis method
- **Guardrail metrics**: Monitored for regressions but not optimized for
- **Warehouse-native**: Eppo reads data directly from your data warehouse -- check data source configuration
- **Rate limits**: Respect API rate limiting headers
- **Pagination**: Use `limit` and `offset` parameters
