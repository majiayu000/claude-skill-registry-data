---
name: managing-dbt
description: |
  Use when working with Dbt — dbt (data build tool) project management and
  monitoring. Covers model runs, test results, source freshness, documentation
  generation, manifest analysis, and dbt Cloud API integration. Use when
  checking dbt run status, investigating test failures, analyzing model lineage,
  or managing dbt Cloud jobs.
connection_type: dbt
preload: false
---

# dbt Management Skill

Manage and monitor dbt projects, model runs, and test results via dbt CLI and dbt Cloud API.

## MANDATORY: Discovery-First Pattern

**Always discover project structure and recent run status before querying specific models or tests.**

### Phase 1: Discovery

```bash
#!/bin/bash

# dbt Cloud API helper
dbt_cloud_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://cloud.getdbt.com/api/v2/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}" \
            "https://cloud.getdbt.com/api/v2/${endpoint}"
    fi
}

echo "=== dbt Cloud Account Info ==="
dbt_cloud_api GET "accounts/${DBT_CLOUD_ACCOUNT_ID}/" | jq '{
    name: .data.name,
    plan: .data.plan,
    run_slots: .data.run_slots
}'

echo ""
echo "=== Projects ==="
dbt_cloud_api GET "accounts/${DBT_CLOUD_ACCOUNT_ID}/projects/" | jq -r '
    .data[] | "\(.id)\t\(.name)\t\(.connection.type // "N/A")\t\(.repository.remote_url // "N/A")"
' | column -t

echo ""
echo "=== Recent Runs ==="
dbt_cloud_api GET "accounts/${DBT_CLOUD_ACCOUNT_ID}/runs/?limit=15&order_by=-finished_at" | jq -r '
    .data[] | "\(.id)\t\(.status_humanized)\t\(.job.name // .job_id)\t\(.finished_at[0:16] // "running")"
' | column -t
```

## Core Helper Functions

```bash
#!/bin/bash

dbt_cloud_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://cloud.getdbt.com/api/v2/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}" \
            "https://cloud.getdbt.com/api/v2/${endpoint}"
    fi
}

# dbt Cloud Administrative API (v3)
dbt_admin_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    curl -s -X "$method" \
        -H "Authorization: Token ${DBT_CLOUD_API_TOKEN}" \
        "https://cloud.getdbt.com/api/v3/accounts/${DBT_CLOUD_ACCOUNT_ID}/${endpoint}"
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use jq to extract only needed fields from API responses
- Never dump full manifest.json — extract specific nodes
- Filter runs by status at the API level

## Common Operations

### Job Run Dashboard

```bash
#!/bin/bash
ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID}"

echo "=== Job Run Summary ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/?limit=50&order_by=-finished_at" | jq '
    .data | group_by(.status_humanized) | map({status: .[0].status_humanized, count: length}) |
    .[] | "\(.status): \(.count)"
' -r

echo ""
echo "=== Failed Runs (recent) ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/?limit=10&order_by=-finished_at&status=20" | jq -r '
    .data[] | "\(.id)\t\(.job.name // .job_id)\t\(.finished_at[0:16])\t\(.duration_humanized)"
' | column -t

echo ""
echo "=== Currently Running ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/?limit=10&status=3" | jq -r '
    .data[] | "\(.id)\t\(.job.name // .job_id)\t\(.created_at[0:16])\t\(.duration_humanized)"
' | column -t
```

### Run Details and Model Results

```bash
#!/bin/bash
ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID}"
RUN_ID="${1:?Run ID required}"

echo "=== Run Details ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/" | jq '{
    id: .data.id,
    status: .data.status_humanized,
    job_name: .data.job.name,
    duration: .data.duration_humanized,
    started: .data.started_at,
    finished: .data.finished_at,
    git_sha: .data.git_sha
}'

echo ""
echo "=== Run Artifacts (model results) ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/run_results.json" | jq -r '
    .results[] |
    select(.status == "error" or .status == "fail") |
    "\(.unique_id)\t\(.status)\t\(.execution_time | floor)s\t\(.message[0:80] // "")"
' | column -t | head -20
```

### Test Results Analysis

```bash
#!/bin/bash
ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID}"
RUN_ID="${1:?Run ID required}"

echo "=== Test Results Summary ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/run_results.json" | jq '
    [.results[] | select(.unique_id | startswith("test."))] |
    group_by(.status) | map({status: .[0].status, count: length}) |
    .[] | "\(.status): \(.count)"
' -r

echo ""
echo "=== Failed Tests ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/run_results.json" | jq -r '
    .results[] |
    select(.unique_id | startswith("test.")) |
    select(.status == "fail" or .status == "error") |
    "\(.unique_id | split(".") | .[-1])\t\(.status)\t\(.failures) failures\t\(.message[0:80] // "")"
' | column -t | head -15

echo ""
echo "=== Slowest Tests ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/run_results.json" | jq -r '
    [.results[] | select(.unique_id | startswith("test."))] |
    sort_by(-.execution_time) | .[:10][] |
    "\(.unique_id | split(".") | .[-1])\t\(.execution_time | floor)s\t\(.status)"
' | column -t
```

### Source Freshness

```bash
#!/bin/bash
ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID}"
RUN_ID="${1:?Run ID required}"

echo "=== Source Freshness Results ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/sources.json" | jq -r '
    .results[] |
    "\(.unique_id)\t\(.status)\t\(.max_loaded_at[0:16] // "unknown")\t\(.criteria.warn_after.count // "?") \(.criteria.warn_after.period // "")"
' | column -t | head -20

echo ""
echo "=== Stale Sources ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/sources.json" | jq -r '
    .results[] |
    select(.status == "warn" or .status == "error") |
    "\(.unique_id)\t\(.status)\t\(.max_loaded_at[0:16] // "unknown")\t\(.snapshotted_at[0:16])"
' | column -t
```

### Manifest and Lineage Analysis

```bash
#!/bin/bash
ACCOUNT_ID="${DBT_CLOUD_ACCOUNT_ID}"
RUN_ID="${1:?Run ID required}"

echo "=== Model Count by Materialization ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/manifest.json" | jq -r '
    [.nodes[] | select(.resource_type == "model") | .config.materialized] |
    group_by(.) | map({type: .[0], count: length}) |
    sort_by(-.count) | .[] | "\(.type)\t\(.count)"
' | column -t

echo ""
echo "=== Models Without Tests ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/manifest.json" | jq -r '
    .nodes | to_entries |
    map(select(.value.resource_type == "model")) |
    map(select(
        [.key as $k | .value.depends_on.nodes[]? | select(startswith("test."))] | length == 0
    )) |
    .[:10][] | .value.unique_id
'

echo ""
echo "=== Models Without Descriptions ==="
dbt_cloud_api GET "accounts/${ACCOUNT_ID}/runs/${RUN_ID}/artifacts/manifest.json" | jq -r '
    [.nodes[] | select(.resource_type == "model") | select(.description == "" or .description == null)] |
    .[:10][] | .unique_id
'
```

## Output Format

Present results as a structured report:
```
Managing Dbt Report
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

- **Run status codes**: `10=success, 20=error, 30=cancelled, 3=running` — use `status_humanized` for readability
- **Artifact availability**: Artifacts (manifest, run_results, sources) only available after run completes
- **API rate limits**: dbt Cloud API has rate limits — avoid rapid sequential calls, use specific endpoints
- **Manifest size**: `manifest.json` can be very large — always filter with jq, never dump entirely
- **Test naming**: Tests are prefixed with `test.` in `unique_id` — schema tests auto-generate names from column/model
- **Source freshness**: Only available if the job includes `dbt source freshness` step — not all jobs run it
- **dbt Core vs Cloud**: CLI commands (`dbt run`, `dbt test`) work locally; API endpoints are dbt Cloud only
- **Job vs Run**: A Job is the definition (schedule, commands), a Run is a specific execution of that Job
- **Environment branches**: dbt Cloud environments may target different git branches — check environment config before comparing runs
