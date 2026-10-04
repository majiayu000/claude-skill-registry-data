---
name: managing-ray
description: |
  Use when working with Ray — ray distributed computing platform management.
  Covers cluster management, job submission, Ray Serve deployment, dashboard
  monitoring, actor management, and resource utilization. Use when managing
  distributed ML workloads, deploying model serving, investigating job failures,
  or monitoring Ray cluster health.
connection_type: ray
preload: false
---

# Ray Management Skill

Manage and monitor Ray clusters, jobs, serve deployments, and distributed workloads.

## MANDATORY: Discovery-First Pattern

**Always check cluster status and existing resources before submitting jobs or deploying services.**

### Phase 1: Discovery

```bash
#!/bin/bash

RAY_ADDRESS="${RAY_ADDRESS:-http://localhost:8265}"

ray_api() {
    local endpoint="$1"
    curl -s "${RAY_ADDRESS}/api/v0/${endpoint}"
}

echo "=== Ray Cluster Status ==="
ray_api "cluster_status" | jq '{
    alive_nodes: .data.clusterStatus.loadMetricsReport.numNodesAlive,
    total_resources: .data.clusterStatus.loadMetricsReport.usage | to_entries | map("\(.key): \(.value[0])/\(.value[1])") | join(", ")
}' 2>/dev/null || ray status 2>/dev/null | head -20

echo ""
echo "=== Running Jobs ==="
ray_api "jobs/" | jq -r '
    .[] | select(.status == "RUNNING" or .status == "PENDING") |
    "\(.job_id // .submission_id)\t\(.status)\t\(.start_time // 0 | . / 1000 | strftime("%Y-%m-%d %H:%M"))"
' | column -t | head -15

echo ""
echo "=== Serve Deployments ==="
curl -s "${RAY_ADDRESS}/api/serve/deployments/" 2>/dev/null | jq -r '
    .deployments | to_entries[]? | "\(.key)\t\(.value.status)\t\(.value.num_replicas // "N/A") replicas"
' | column -t

echo ""
echo "=== Nodes ==="
ray_api "nodes" | jq -r '
    .data.summary[]? | "\(.raylet.nodeId[0:12])\t\(.raylet.state)\t\(.raylet.nodeManagerAddress)\tCPU=\(.raylet.resourcesTotal.CPU // 0)"
' | column -t
```

## Core Helper Functions

```bash
#!/bin/bash

RAY_ADDRESS="${RAY_ADDRESS:-http://localhost:8265}"

# Ray Dashboard API helper
ray_api() {
    local endpoint="$1"
    curl -s "${RAY_ADDRESS}/api/v0/${endpoint}"
}

# Ray Jobs API helper
ray_jobs_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"
    if [ -n "$data" ]; then
        curl -s -X "$method" -H "Content-Type: application/json" \
            "${RAY_ADDRESS}/api/jobs/${endpoint}" -d "$data"
    else
        curl -s -X "$method" "${RAY_ADDRESS}/api/jobs/${endpoint}"
    fi
}

# Ray CLI wrapper
ray_cmd() {
    ray "$@" 2>/dev/null
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Target ≤50 lines per output
- Use Dashboard API with jq for structured queries
- Never dump full job logs -- use `tail` for recent entries
- Truncate node IDs to first 12 characters for readability

## Common Operations

### Cluster Health and Resources

```bash
#!/bin/bash
echo "=== Cluster Resources ==="
ray_api "cluster_status" | jq '{
    nodes_alive: .data.clusterStatus.loadMetricsReport.numNodesAlive,
    resource_usage: (.data.clusterStatus.loadMetricsReport.usage | to_entries | map({
        resource: .key,
        used: .value[0],
        total: .value[1],
        utilization: (if .value[1] > 0 then (.value[0] / .value[1] * 100 | round) else 0 end | tostring) + "%"
    }))
}'

echo ""
echo "=== Node Details ==="
ray_api "nodes" | jq -r '
    .data.summary[]? | "\(.raylet.nodeId[0:12])\t\(.raylet.state)\tCPU=\(.raylet.resourcesTotal.CPU // 0)\tGPU=\(.raylet.resourcesTotal.GPU // 0)\tMem=\(.raylet.objectStoreAvailableMemory // 0 | . / 1073741824 | floor)GB"
' | column -t
```

### Job Submission and Monitoring

```bash
#!/bin/bash
echo "=== All Jobs ==="
ray_api "jobs/" | jq -r '
    sort_by(.start_time) | reverse | .[:15][] |
    "\(.job_id // .submission_id)\t\(.status)\t\(.driver_info.pid // "N/A")\t\(.start_time // 0 | . / 1000 | strftime("%Y-%m-%d %H:%M"))"
' | column -t

JOB_ID="${1:-}"
if [ -n "$JOB_ID" ]; then
    echo ""
    echo "=== Job Details: $JOB_ID ==="
    ray_api "jobs/${JOB_ID}" | jq '{
        job_id: .job_id,
        status: .status,
        entrypoint: .entrypoint,
        runtime_env: .runtime_env,
        start_time: (.start_time // 0 | . / 1000 | strftime("%Y-%m-%d %H:%M:%S")),
        end_time: (.end_time // 0 | if . > 0 then . / 1000 | strftime("%Y-%m-%d %H:%M:%S") else "running" end),
        error_type: .error_type,
        message: .message
    }'

    echo ""
    echo "=== Job Logs (last 30 lines) ==="
    ray_api "jobs/${JOB_ID}/logs" | tail -30
fi
```

### Serve Deployment Management

```bash
#!/bin/bash
echo "=== Serve Applications ==="
curl -s "${RAY_ADDRESS}/api/serve/applications/" 2>/dev/null | jq -r '
    .applications | to_entries[]? | "\(.key)\t\(.value.status)\t\(.value.deployed_app_status.deployment_timestamp // "unknown")"
' | column -t

echo ""
echo "=== Deployment Replicas ==="
curl -s "${RAY_ADDRESS}/api/serve/deployments/" 2>/dev/null | jq -r '
    .deployments | to_entries[]? | "\(.key)\t\(.value.status)\treplicas=\(.value.num_replicas // 0)\trunning=\(.value.running_replicas // 0)"
' | column -t

DEPLOYMENT="${1:-}"
if [ -n "$DEPLOYMENT" ]; then
    echo ""
    echo "=== Deployment Detail: $DEPLOYMENT ==="
    curl -s "${RAY_ADDRESS}/api/serve/deployments/${DEPLOYMENT}" 2>/dev/null | jq '{
        name: .name,
        status: .status,
        num_replicas: .num_replicas,
        route_prefix: .route_prefix,
        ray_actor_options: .ray_actor_options,
        health_check_period_s: .health_check_period_s
    }'
fi
```

### Actor and Task Monitoring

```bash
#!/bin/bash
echo "=== Active Actors ==="
ray_api "actors" | jq -r '
    .data.summary | to_entries[]? | "\(.key)\tstate=\(.value.stateValue)\tpid=\(.value.pid // "N/A")\tnode=\(.value.address.rayletId[0:12] // "N/A")"
' | column -t | head -20

echo ""
echo "=== Task Summary ==="
ray_api "tasks" | jq '{
    total_tasks: (.data.summary | length),
    by_state: (.data.summary | group_by(.stateValue) | map({state: .[0].stateValue, count: length}))
}' 2>/dev/null | head -20
```

### Dashboard Monitoring

```bash
#!/bin/bash
echo "=== Memory Usage ==="
ray_api "memory/memory_table" | jq '{
    total_local_ref_count: .data.summary.totalLocalRefCount,
    total_pinned_in_memory: .data.summary.totalPinnedInMemory,
    total_object_size: .data.summary.totalObjectSize
}' 2>/dev/null

echo ""
echo "=== Placement Groups ==="
ray_api "placement_groups" | jq -r '
    .data.summary[]? | "\(.placementGroupId[0:12])\t\(.state)\t\(.bundles | length) bundles"
' | column -t | head -10
```

## Safety Rules

- **NEVER stop running jobs** without explicit confirmation -- distributed tasks will be lost
- **NEVER scale down Serve deployments to zero** in production without traffic drain
- **Always check actor dependencies** before killing actors -- downstream actors may hang
- **Autoscaler caution**: Changing autoscaler config affects the entire cluster -- verify settings before applying
- **Object store**: Do not force-evict objects from the object store -- dependent tasks will fail

## Output Format

Present results as a structured report:
```
Managing Ray Report
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

- **Address format**: `RAY_ADDRESS` for the dashboard API uses HTTP (port 8265), not the Ray client address (port 10001)
- **Job runtime environments**: Runtime env packaging can be slow -- large dependencies should use pre-built container images
- **Serve autoscaling**: Serve autoscaling and Ray autoscaling are separate -- configure both for elastic deployments
- **Memory pressure**: Object store spilling to disk degrades performance -- monitor with the memory dashboard
- **Head node bottleneck**: GCS on the head node is a single point of failure -- enable GCS fault tolerance for production
- **GPU scheduling**: Ray schedules GPUs as resources -- requesting fractional GPUs allows co-location but risks OOM
- **Detached actors**: Detached actors persist across jobs -- they must be explicitly killed or they leak resources
- **Network timeouts**: Large cluster deployments may hit gRPC timeouts -- increase `RAY_grpc_keepalive_timeout_ms`
