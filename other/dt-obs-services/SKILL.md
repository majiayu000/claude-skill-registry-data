---
name: dt-obs-services
description: >-
  Service performance monitoring with RED metrics (Rate, Errors, Duration) and runtime-specific
  telemetry for Java, .NET, Node.js, Python, PHP, and Go. Use when analyzing service health,
  SLA compliance, or runtime issues.
  Trigger: "service response time", "error rate", "throughput", "SLA compliance",
  "service mesh overhead", "JVM GC", "Java heap", "Node.js event loop", ".NET CLR",
  "Python threads", "PHP OPcache", "Go goroutines", "service performance",
  "p95 latency", "request failures", "database response time by name".
  Do NOT use for explaining existing queries, product documentation questions,
  infrastructure metrics (use dt-obs-hosts), log analysis (use dt-obs-logs),
  or distributed tracing workflows (use dt-obs-tracing).
license: Apache-2.0
---

# Application Services Skill

Monitor application service performance, health, and runtime-specific metrics using DQL.

---

## Core Capabilities

### 1. Service Performance (RED Metrics)

Monitor service **Rate, Errors, Duration** using metrics-based timeseries queries.

**Key Metrics:**
- `dt.service.request.response_time` - Response time (microseconds)
- `dt.service.request.count` - Request count
- `dt.service.request.failure_count` - Failed request count

**Common Use Cases:**
- Response time monitoring (avg, p50, p95, p99)
- Error rate tracking and spike detection
- Traffic analysis (throughput, peaks, growth)
- Performance degradation detection
- Multi-cluster comparison

**Quick Example:**
```dql
timeseries {
  p95 = percentile(dt.service.request.response_time, 95),
  total_requests = sum(dt.service.request.count),
  failures = sum(dt.service.request.failure_count)
}, by: {dt.service.name}
| fieldsAdd p95_ms = p95[] / 1000, error_rate_pct = (failures[] * 100.0) / total_requests[]
```

→ **For detailed queries:** See [references/service-metrics.md](references/service-metrics.md)

### 2. Advanced Service Analysis

Span-based queries for complex scenarios requiring flexible filtering and custom aggregations.

**Use Cases:**
- SLA compliance tracking with custom thresholds
- Service health scoring (multi-dimensional)
- Operation/endpoint-level performance analysis
- Custom error classification
- Failure pattern detection with error details

**Quick Example:**
```dql
fetch spans, from: now() - 1h | filter request.is_root_span == true
| fieldsAdd meets_sla = if(request.is_failed == false AND duration < 3s, 1, else: 0)
| summarize total = count(), sla_compliant = sum(meets_sla), by: {dt.service.name}
| fieldsAdd sla_compliance_pct = (sla_compliant * 100.0) / total
```

→ **For detailed queries:** See [references/service-metrics.md](references/service-metrics.md)

### 3. Service Messaging Metrics

Monitor message-based service communication (queues, topics).

**Key Metrics:**
- `dt.service.messaging.publish.count` - Messages sent to queues or topics
- `dt.service.messaging.receive.count` - Messages received from queues or topics
- `dt.service.messaging.process.count` - Messages successfully processed
- `dt.service.messaging.process.failure_count` - Messages that failed processing

**Use Cases:**
- Message throughput monitoring (publish/receive rates)
- Message processing failure tracking
- Queue/topic health analysis
- Consumer lag detection (publish vs receive rate comparison)

**Quick Example:**
```dql
timeseries {
  published = sum(dt.service.messaging.publish.count),
  received = sum(dt.service.messaging.receive.count),
  processed = sum(dt.service.messaging.process.count),
  failed = sum(dt.service.messaging.process.failure_count)
}, by: {dt.service.name}
```

→ **For detailed queries:** See [references/service-metrics.md](references/service-metrics.md)

### 4. Service Mesh Monitoring

Monitor service mesh ingress performance and overhead.

**Key Metrics:**
- `dt.service.request.service_mesh.response_time` - Mesh response time (microseconds)
- `dt.service.request.service_mesh.count` - Mesh request count
- `dt.service.request.service_mesh.failure_count` - Mesh failure count

**Use Cases:**
- Mesh vs direct performance comparison
- Mesh overhead calculation
- Mesh failure analysis
- gRPC traffic monitoring
- Multi-cluster mesh performance

**Quick Example:**
```dql
timeseries {
  direct_p95 = percentile(dt.service.request.response_time, 95),
  mesh_p95 = percentile(dt.service.request.service_mesh.response_time, 95)
}, by: {dt.service.name}
| fieldsAdd mesh_overhead_ms = (mesh_p95[] - direct_p95[]) / 1000
```

→ **For detailed queries:** See [references/service-metrics.md](references/service-metrics.md)

### 5. Runtime-Specific Monitoring

Technology-specific runtime performance and resource usage metrics.

**Java/JVM** - [references/java.md](references/java.md)
- Memory: heap, pools, metaspace
- GC: impact, suspension, frequency, pause time
- Threads: count monitoring, leak detection
- Classes: loading, unloading, growth

**Node.js** - [references/nodejs.md](references/nodejs.md)
- Event loop: utilization, active handles
- V8 heap: memory used, total
- GC: collection time, suspension
- Process: RSS memory

**.NET CLR** - [references/dotnet.md](references/dotnet.md)
- Memory: consumption by generation
- GC: collection count, suspension time
- Thread pool: threads, queued work
- JIT: compilation time

**Python** - [references/python.md](references/python.md)
- Threads: active thread count
- Heap: allocated blocks
- GC: collection by generation, pause time
- Objects: collected, uncollectable

**PHP** - [references/php.md](references/php.md)
- OPcache: hit ratio, memory, restarts
- GC: effectiveness, duration
- JIT: buffer usage
- Interned strings: usage, buffer

**Go** - [references/go.md](references/go.md)
- Goroutines: count, leak detection
- GC: suspension, collection time
- Memory: heap by state, committed
- Scheduler: worker threads, queue size
- CGo: call frequency

---

## When to Use This Skill

✅ **Use for:**
- Monitoring service performance (response time, errors, traffic)
- Calculating SLA compliance
- Analyzing service mesh performance
- Monitoring messaging throughput and processing failures
- Troubleshooting runtime-specific issues (GC, memory, threads)
- Multi-cluster service comparison
- Operation/endpoint-level analysis

❌ **Don't use for:**
- Infrastructure metrics (use infrastructure skills)
- Log analysis (use logs skills)
- Distributed tracing workflows (use traces/spans skills)
- Database performance (use database skills)
- Product documentation or how-to configuration questions → use `ask-dynatrace-docs`

---

## Agent Instructions

### Act First, Refine Later

When a user asks for analysis — threshold checks, anomaly detection, performance
comparisons — **proceed immediately** with sensible defaults. Do not ask the user
for parameter values you can reasonably assume.

Why this matters: analysis tools (e.g., `static-threshold-analyzer`) require specific
inputs like threshold values and service scope. The user expects results, not a
parameter interview. Pick reasonable defaults, state them clearly in the response,
and let the user refine.

**Default values when not specified:**

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| Response time threshold | 1000 ms (= 1,000,000 µs in the metric's base unit) | Common SLA boundary |
| Service scope | All services | Show the most relevant violations |
| Timeframe | From the request, or last 30 min for threshold checks, 2h for general analysis | Matches typical operational windows |

**Example: threshold violation request**
1. Use `create-dql` to build a timeseries query for `avg(dt.service.request.response_time)` grouped by `dt.smartscape.service`
2. Pass the query to `static-threshold-analyzer` with threshold = 1000000 (µs), alertCondition = ABOVE
3. Resolve entity IDs to names using `get-entity-name`
4. Present violations with service names, timestamps, values, and duration

**Reading user phrasing:** Phrases like "the fixed threshold", "a threshold", or "the limit"
name the *type of analysis* — static threshold check — not a specific number the user expects
you to already know. "Fixed" distinguishes a static cutoff from a dynamic or seasonal baseline.
When you see these phrases, apply the 1000 ms default from the table above and present
results — the user can then refine if the default doesn't match their intent.

### Scope Boundary

This skill covers **service performance metrics and runtime monitoring only**. If the
user asks a product documentation or configuration question (e.g., "How do I add custom
sensors?", "How do I configure service detection?"), use `ask-dynatrace-docs` instead —
this skill does not contain configuration how-tos.

### Understanding User Intent

**Map user questions to capabilities:**

| User Request | Use Capability | Key Files |
|--------------|----------------|-----------|
| "service performance", "response time", "error rate" | Service Performance (RED) | service-metrics.md |
| "SLA tracking", "health scoring" | Advanced Service Analysis | service-metrics.md |
| "service mesh", "Istio", "Linkerd", "mesh overhead" | Service Mesh Monitoring | service-metrics.md |
| "messaging", "queue", "topic", "publish", "consumer" | Service Messaging Metrics | service-metrics.md |
| "JVM GC", "Java memory", "heap" | Runtime-Specific (Java) | java.md |
| "Node.js event loop", "V8 heap" | Runtime-Specific (Node.js) | nodejs.md |
| ".NET CLR", "GC generation" | Runtime-Specific (.NET) | dotnet.md |
| "Python GC", "thread count" | Runtime-Specific (Python) | python.md |
| "OPcache", "PHP GC" | Runtime-Specific (PHP) | php.md |
| "goroutines", "Go GC", "scheduler" | Runtime-Specific (Go) | go.md |

### Query Construction Patterns

**1. Metrics-based (timeseries)**
- **Use for:** Standard monitoring, dashboards, alerting
- **Pattern:** `timeseries <metric> = <aggregation>(<metric_name>), by: {dimensions}`
- **Files:** service-metrics.md, all runtime-specific files

**2. Span-based (fetch spans)**
- **Use for:** Complex filtering, custom logic, detailed analysis
- **Pattern:** `fetch spans | filter request.is_root_span == true | fieldsAdd ... | summarize ...`
- **Files:** service-metrics.md (Advanced Service Analysis section)

**3. Comparison queries**
- Use `append` for baseline comparison
- Use `shift: -15m` for time-shifted baselines
- **Example:** Performance degradation detection

### Response Construction Guidelines

**Always include:**
1. **Metric name(s)** - Clear metric identifiers
2. **Aggregation** - How data is aggregated (avg, sum, percentile)
3. **Grouping** - Dimensions used (`dt.service.name`, `k8s.workload.name`, etc.)
4. **Unit conversion** - Convert microseconds to milliseconds where appropriate
5. **Filtering** - Relevant thresholds or conditions

**When referencing runtime-specific content:**
- **Check** user's technology stack first
- **Provide** only relevant runtime queries (don't overwhelm with all 6 runtimes)
- **Explain** runtime-specific metrics (e.g., "OPcache hit ratio" measures PHP opcode cache efficiency)

---

## Common Workflows

### Workflow: Service Health Check
```
1. Check response time (RED metrics)
2. Check error rate (RED metrics)
3. Check traffic patterns (RED metrics)
4. If runtime-specific issues suspected → Load runtime-specific reference
```

### Workflow: SLA Monitoring
```
1. Define SLA criteria (e.g., < 3s response time AND < 1% error rate)
2. Use span-based query for custom SLA logic
3. Calculate compliance percentage
4. Filter non-compliant services
```

### Workflow: Service Mesh Analysis
```
1. Check mesh response time
2. Compare mesh vs direct performance
3. Calculate mesh overhead
4. Analyze mesh failure rates
```

### Workflow: Runtime Troubleshooting
1. Identify technology stack → Load runtime-specific reference
2. Check memory/GC metrics → threads/goroutines → runtime features

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Response time values look too large | Metric is in microseconds | Divide by 1000 to convert to milliseconds |
| No data for service mesh metrics | Service mesh not configured | Verify mesh sidecar injection is enabled |
| Runtime metrics missing | Wrong technology or no OneAgent | Confirm the runtime is supported and OneAgent is active |
| `dt.smartscape.service` returns SmartscapeId, not name | Need entity name resolution | Use `getNodeName(dt.smartscape.service)` |
| Error rate always zero | Using wrong failure metric | Use `dt.service.request.failure_count`, not custom fields |

---

## References

**Core Service Monitoring:**
- [references/service-metrics.md](references/service-metrics.md) - Complete RED metrics, SLA tracking, service mesh queries

**Runtime-Specific Monitoring:**
- [references/java.md](references/java.md) - Java/JVM monitoring
- [references/nodejs.md](references/nodejs.md) - Node.js monitoring  
- [references/dotnet.md](references/dotnet.md) - .NET CLR monitoring
- [references/python.md](references/python.md) - Python monitoring
- [references/php.md](references/php.md) - PHP monitoring
- [references/go.md](references/go.md) - Go runtime monitoring
