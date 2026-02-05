---
name: observability
description: Use when diagnosing operation failures, stuck or slow operations, querying Jaeger traces, working with Grafana dashboards, debugging distributed system issues, or investigating worker selection and service communication problems.
---

# Observability & Debugging

Load this skill when:
- Diagnosing operation failures, stuck operations, or slow operations
- Working with Jaeger traces or Grafana dashboards
- Debugging distributed system issues
- Investigating worker selection or service communication problems

---

## First Rule: Check Observability Before Logs

When users report issues with operations, use Jaeger first — not logs. KTRDR has comprehensive OpenTelemetry instrumentation that provides complete visibility into distributed operations.

This enables **first-response diagnosis** instead of iterative detective work.

---

## When to Query Jaeger

Query Jaeger when user reports:

| Symptom | What Jaeger Shows |
|---------|-------------------|
| "Operation stuck" | Which phase is stuck and why |
| "Operation failed" | Exact error with full context |
| "Operation slow" | Bottleneck span immediately |
| "No workers selected" | Worker selection decision |
| "Missing data" | Data flow from IB to cache |
| "Service not responding" | HTTP call attempt and result |

---

## Quick Start Workflow

### Step 1: Get operation ID
From CLI output or API response (e.g., `op_training_20251113_123456_abc123`)

### Step 2: Query Jaeger API

```bash
OPERATION_ID="op_training_20251113_123456_abc123"
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID&limit=1" | jq
```

### Step 3: Analyze trace structure

```bash
# Get span summary with durations
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID" | jq '
  .data[0].spans[] |
  {
    span: .operationName,
    service: .process.serviceName,
    duration_ms: (.duration / 1000),
    error: ([.tags[] | select(.key == "error" and .value == "true")] | length > 0)
  }' | jq -s 'sort_by(.duration_ms) | reverse'
```

### Step 4: Extract relevant attributes

```bash
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OPERATION_ID" | jq '
  .data[0].spans[] |
  {
    span: .operationName,
    attributes: (.tags | map({key: .key, value: .value}) | from_entries)
  }'
```

---

## Common Diagnostic Patterns

### Pattern 1: Operation Stuck

```bash
# Check for worker selection and dispatch
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.operationName == "worker_registry.select_worker") |
  .tags[] |
  select(.key | startswith("worker_registry.")) |
  {key: .key, value: .value}'
```

Look for:
- `worker_registry.total_workers: 0` → No workers started
- `worker_registry.capable_workers: 0` → No capable workers
- `worker_registry.selection_status: NO_WORKERS_AVAILABLE` → All busy

### Pattern 2: Operation Failed

```bash
# Extract error details
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.tags[] | select(.key == "error" and .value == "true")) |
  {
    span: .operationName,
    service: .process.serviceName,
    exception_type: (.tags[] | select(.key == "exception.type") | .value),
    exception_message: (.tags[] | select(.key == "exception.message") | .value)
  }'
```

Common errors:
- `ConnectionRefusedError` → Service not running (check `http.url`)
- `ValueError` → Invalid input parameters
- `DataNotFoundError` → Data not loaded (check `data.symbol`, `data.timeframe`)

### Pattern 3: Operation Slow

```bash
# Find bottleneck span (longest duration)
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  {
    span: .operationName,
    duration_ms: (.duration / 1000)
  }' | jq -s 'sort_by(.duration_ms) | reverse | .[0]'
```

Common bottlenecks:
- `training.training_loop` → Check `training.device` (GPU vs CPU)
- `data.fetch` → Check `ib.latency_ms`
- `ib.fetch_historical` → Check `data.bars_requested`

### Pattern 4: Service Communication Failure

```bash
# Check HTTP calls between services
curl -s "http://localhost:16686/api/traces?tag=operation.id:$OP_ID" | jq '
  .data[0].spans[] |
  select(.operationName | startswith("POST") or startswith("GET")) |
  {
    http_call: .operationName,
    url: (.tags[] | select(.key == "http.url") | .value),
    status: (.tags[] | select(.key == "http.status_code") | .value),
    error: (.tags[] | select(.key == "error.type") | .value)
  }'
```

Look for:
- `http.status_code: null` → Connection failed
- `error.type: ConnectionRefusedError` → Target service not running
- `http.url` → Shows which service was being called

---

## Key Span Attributes Reference

### Operation Attributes
- `operation.id` — Operation identifier
- `operation.type` — TRAINING, BACKTESTING, DATA_DOWNLOAD
- `operation.status` — PENDING, RUNNING, COMPLETED, FAILED

### Worker Selection
- `worker_registry.total_workers` — Total registered workers
- `worker_registry.available_workers` — Available workers
- `worker_registry.capable_workers` — Capable workers for this operation
- `worker_registry.selected_worker_id` — Which worker was chosen
- `worker_registry.selection_status` — SUCCESS, NO_WORKERS_AVAILABLE, NO_CAPABLE_WORKERS

### Progress Tracking
- `progress.percentage` — Current progress (0-100)
- `progress.phase` — Current execution phase
- `operations_service.instance_id` — OperationsService instance (check for mismatches)

### Error Context
- `exception.type` — Python exception class
- `exception.message` — Error message
- `exception.stacktrace` — Full stack trace
- `error.symbol`, `error.strategy` — Business context

### Performance
- `http.status_code` — HTTP response status
- `http.url` — Target URL for HTTP calls
- `ib.latency_ms` — IB Gateway latency
- `training.device` — cuda:0 or cpu
- `gpu.utilization_percent` — GPU usage

---

## Response Template

When diagnosing with observability, use this structure:

```
🔍 **Trace Analysis for operation_id: {operation_id}**

**Trace Summary**:
- Trace ID: {trace_id}
- Total Duration: {duration_ms}ms
- Services: {list of services}
- Status: {OK/ERROR}

**Execution Flow**:
1. {span_name} ({service}) - {duration_ms}ms
2. {span_name} ({service}) - {duration_ms}ms
...

**Diagnosis**:
{identified_issue_with_evidence_from_spans}

**Root Cause**:
{root_cause_explanation_with_span_attributes}

**Solution**:
{recommended_fix_with_commands}
```

---

## Grafana Dashboards

Check Grafana for quick diagnostics before diving into traces.

**URL**: http://localhost:3000

| Dashboard | Path | Use Case |
|-----------|------|----------|
| System Overview | `/d/ktrdr-system-overview` | Service health, error rates, latency |
| Worker Status | `/d/ktrdr-worker-status` | Worker capacity, resource usage |
| Operations | `/d/ktrdr-operations` | Operation counts, success rates |

### Quick Workflows

- **"Is it working?"** → System Overview: Healthy Services count
- **"Why is it slow?"** → System Overview: P95 Latency panel
- **"Workers missing?"** → Worker Status: Healthy Workers and Health Matrix
- **"Operations failing?"** → Operations: Success Rate and Status Distribution

---

## Benefits of Observability-First Debugging

- **Diagnosis in FIRST response** (not 10+ messages later)
- **Complete context** (all services, all phases, all attributes)
- **Objective evidence** (no guessing or assumptions)
- **Distributed visibility** (Backend → Worker → Host Service)
- **Performance insights** (identify bottlenecks immediately)
- **Root cause analysis** (trace error from source to root)

---

## Full Documentation

For comprehensive workflows and scenarios:
[docs/debugging/observability-debugging-workflows.md](docs/debugging/observability-debugging-workflows.md)
