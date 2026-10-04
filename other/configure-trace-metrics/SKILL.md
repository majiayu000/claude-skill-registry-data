---
name: configure-trace-metrics
description: Recommend, create, preview, and attach Coval trace-based metrics from OpenTelemetry spans. Use when a user has Coval traces and wants custom trace metrics, trace-aware LLM judge metrics with include_traces, latency, token usage, provider failures, tool behavior, vertical-specific workflow signals, or production monitoring based on trace attributes.
---

# Configure Coval Trace Metrics

Create metrics from trace data only after at least one real trace exists for the
target agent. If a `setup-tracing` validation run is currently pending, use the
waiting time to inventory existing traces and prepare metric definitions. Create
metrics during the wait only when historical traces or the in-flight run already
prove the target span and attribute exist.

Quality bar: proof-of-ingest metrics are not the finish line. A metric that
only proves traces arrived, such as generic call duration or raw span count, is
diagnostic unless it answers a customer decision. Prefer metrics that expose a
workflow bottleneck, user-impacting failure, dependency health issue, latency
tail, cost driver, fallback, handoff, or completion signal.

This skill should usually produce two metric types when trace data supports it:
- numeric `METRIC_CUSTOM_TRACE` metrics for real span attributes
- trace-aware LLM judge metrics (`METRIC_LLM_BINARY`,
  `METRIC_CATEGORICAL`, or `METRIC_NUMERICAL_LLM_JUDGE`) with
  `include_traces: true` when traces help judge sequence, grounding, or
  recovery behavior that transcripts alone can miss

Use trace metrics only when trace spans are the right data source. Metrics like
turns per call often belong in transcript, simulation-output, or evaluation
metrics instead. Metrics like cart total, order total, provider fallback, tool
failure, or downstream latency are good trace metrics when the agent emits the
safe numeric value on a real span.

## Read First

Load:
- `../references/trace-metrics-playbook.md`
- `../references/span-schema.md`
- `../references/coval-tracing-reference.md`
- `../references/vapi-artifact-tracing.md` when the agent uses Vapi webhooks

## Phase 0: Inventory

Check auth and current resources:
```bash
coval whoami
coval agents list --format json
coval metrics list --include-builtin --format json
```

If the CLI cannot create the required metric shape, use the API after fetching the latest OpenAPI:
```bash
curl -fsS https://api.coval.dev/v1/openapi
```

Treat the live target API as authoritative. On `api.coval.dev`, custom trace
metric validation can vary by deployed environment. If create returns an
aggregation-method validation error, fall back to the accepted production set
for that environment and call out the public API/docs drift in the handoff.

Collect:
- agent ID and type
- recent run or conversation with traces, or the in-flight validation run being
  polled by `setup-tracing`
- available span names and attributes from Trace Search suggestions, the trace viewer, or a copied trace dump
- existing built-in trace metrics already attached
- existing LLM judge metrics and whether `include_traces` is already enabled
- customer use case or vertical

## Phase 1: Decide Metric Candidates

Use the playbook to propose a small set. Prefer 3-6 high-signal metrics over a large noisy bundle.

For each candidate, write the customer question it answers. Drop or label the
metric as diagnostic-only if the question is only "did tracing work?"
Also drop it if the same answer is better computed from non-trace Coval data.

Baseline recommendations:
- voice agents: LLM/TTS/STT TTFB, token usage, tool call count, STT WER when `stt` spans include `transcript`
- realtime or WebSocket agents: model/realtime latency, response TTFB, token usage, stream/error spans
- conversation monitoring: p95/p99 latency, tool/API error rate, count of critical events, production fallback rate
- custom business logic: one metric for the most important customer-specific workflow bottleneck or failure mode

High-signal first set when the trace includes tool or workflow spans:
- One vertical-specific failure-mode metric tied to the customer's domain
  workflow, such as Roadside Dispatch Latency P90, Reservation Date
  Corruption Rate, Payment Plan Blocked Rate, Identity Verification Completion
  Rate, or Escalation Triggered Rate
- Dependency Blocked Rate: required external dependency prevented completion
- Tool Failure Rate: tool/API calls returned errors or unusable responses
- Tool Latency P90: slow downstream tools before they become call failures
- Cart Total Avg or Order Total Avg: business value captured during checkout
- Workflow Completion or Fallback Rate: whether the intended customer outcome happened

High-signal trace-aware LLM judge set when the trace includes tool calls or
workflow attributes:
- Tool Output Grounding: spoken claims match successful tool outputs and do not
  ignore `tool.error` or `error.type`
- Verification Before Tool Use: sensitive identifiers or account-specific tools
  are used only after the transcript and trace show verification
- Recovery From Tool Failure: the agent re-prompts, retries, escalates, or
  refuses appropriately after a dependency failure or unusable tool response
- Read-Back Discipline: the agent confirms sensitive identifiers before using
  them in tool calls

Prefer creating new trace-aware versions of existing LLM judge metrics over
silently mutating existing production metrics, unless the customer explicitly
asked to update those metrics in place.

Do not create a custom trace metric for an attribute that is not present in
actual trace data unless you are also adding that instrumentation and have a
validation run in progress to prove it. In that case, stage the metric body and
create it only after the span/attribute appears in Coval.

Do not create latency or error-rate metrics against in-process mock or stub tool
handlers. If the tool handler is a stub that returns immediately (sub-ms
`tool.latency_ms`, `tool.error` always 0), those metrics have no signal — they
measure the stub, not the real downstream service. Metrics like P90 Tool Latency
and Tool Error Rate become meaningful only when the handlers call real external
APIs. If the agent currently uses stubs, note this and defer those metrics to
when real handlers are wired. Creating them against stubs is worse than
omitting them: they produce false confidence (latency always excellent, error
rate always zero) that masks real production behavior.
Do not create latency custom trace metrics from artifact-derived marker spans.
For Vapi-hosted agents, `stt`/`llm`/`tts` spans that carry
`trace.timing=metadata_marker` are not measured provider latency. Use real
tool/workflow metrics and trace-aware judges instead.

**Auto-pair rule.** Every new numeric attribute added during
`optimize-trace-observability` should be paired with at least one proposed
metric *in the same pass*, not in a later round. Walk the new attribute set
once:

- `metrics.ttfb` on any provider span → P90 latency metric
- `*.latency_ms` / `*.duration_s` → P90 latency metric
- `*.count` / `*_count` / `*.bytes` → average per-call metric
- `*.total` / `*.amount` / `*.value` (business numerics) → average business
  metric (e.g., `cart.total`/average/score)
- numeric `0`/`1` flags (`*.error`, `*.fallback_used`, `*.completed`,
  `*.dependency_unavailable`) → average / ratio metric
- `wait.*` / `*_to_first_*` → P90 time-to metric

If the auto-pair would create a metric that does not answer a customer
question, drop it explicitly and note why. Do not ship a trace enrichment pass
without proposing the matching metrics — the customer should not have to ask
"is that all the metrics?" twice.

First-pass floor: if real spans include the required attributes, create or
stage at least one vertical-specific metric plus Workflow Completion Rate,
Workflow Blocked/Dependency Blocked Rate, Tool Latency P90, Tool Failure Rate,
and Fallback Used Rate. A setup that only creates generic proof metrics is not
complete when the trace data already contains customer-operating signals.

## Phase 2: Validate Config Shape

Coval custom trace metric fields:
- `metric_type`: `METRIC_CUSTOM_TRACE`
- `span_name`: exact emitted span name
- `metric_attribute`: required for numeric aggregations
- `aggregation_method`: one of `average`, `median`, `p90`, `p95`, `p99`, `max`, `min`, `sum`, `count`, `error_rate`, `success_rate`
- `unit`: optional display unit such as `s`, `ms`, `count`, `percent`, `tokens`, `ratio`, or `score`

The public API/OpenAPI for the target environment is the source of truth for
accepted aggregations. Some deployed API versions only accept `average`,
`median`, `p90`, `max`, and `min` through `POST /v1/metrics`. When the API
rejects `count`, `error_rate`, `success_rate`, `p95`, `p99`, or `sum`, create a
production-safe numeric metric such as `average` or `p90` against a real
numeric attribute, then document the unsupported desired metric as a public
API/docs drift item.
Some deployed API versions also require `metric_attribute` for
`METRIC_CUSTOM_TRACE` even when a duration- or span-status-based metric would
be cleaner. In that case, emit the useful duration/status as an explicit
numeric attribute during instrumentation and create the metric against that
attribute. Example: copy the measured `insurance.workflow.dispatch_roadside`
span duration to `conversation.roadside.dispatch.latency_ms` or
`roadside.dispatch.latency_ms`, then create the P90 metric against the
attribute.

Production-safe rate pattern: emit numeric `0`/`1` attributes and aggregate with
`average` when span-level rate aggregations are not accepted. Examples:
- `llm_tool_call` / `tool.error` / `average` / `ratio`
- `llm_tool_call` / `tool.dependency_unavailable` / `average` / `ratio`
- `conversation` / `workflow.dependency_blocked` / `average` / `ratio`
- `conversation` / `workflow.completed` / `average` / `ratio`

For `count`, `error_rate`, and `success_rate`, omit `metric_attribute` when the
target API allows it. If a deployed API still requires an attribute, use a
known-present span attribute only when that preserves the metric's meaning;
otherwise do not create the metric from API automation.

Example API body:
```json
{
  "metric_name": "P95 LLM TTFB",
  "description": "95th percentile time to first token from llm spans.",
  "metric_type": "METRIC_CUSTOM_TRACE",
  "span_name": "llm",
  "metric_attribute": "metrics.ttfb",
  "aggregation_method": "p95",
  "unit": "s"
}
```

Trace-aware LLM judge metric fields:
- `metric_type`: `METRIC_LLM_BINARY`, `METRIC_CATEGORICAL`, or
  `METRIC_NUMERICAL_LLM_JUDGE`
- `prompt`: explicitly tell the judge to use both transcript and OTel trace
  context
- `include_traces`: `true`

Create these when the current Metrics OpenAPI confirms `include_traces` support
for the selected LLM judge type. Good prompts reference concrete trace evidence
such as `llm_tool_call`, `function.name`, `function.arguments`, `tool.error`,
`error.type`, and workflow root attributes.

Example trace-aware judge body:
```json
{
  "metric_name": "Trace-Aware Tool Output Grounding",
  "description": "Uses transcript plus OTel tool-call traces to verify agent claims are grounded in successful tool outputs.",
  "metric_type": "METRIC_LLM_BINARY",
  "prompt": "Use BOTH the transcript and OTel trace context. Score YES only if the agent's customer-facing claims are supported by successful llm_tool_call outputs. Score NO if the agent asserts outcomes not supported by successful tool outputs, or if it ignores a tool.error or error.type result and presents the workflow as completed.",
  "include_traces": true
}
```

Create only after confirming the span/attribute exists in real traces. If the
initial validation is still running, keep polling with the Coval CLI/API while
you prepare the metric request bodies, then create the metrics as soon as Trace
Search or the run trace output confirms the data.

## Phase 3: Attach And Verify

After creating metrics:
1. Attach them to the target agent, run template, or run configuration using the CLI/API path that matches the current OpenAPI. If the agent has no default metrics but the customer uses run templates, patch the run template rather than assuming agent defaults are used.
2. Launch or rerun one small evaluation through the Coval CLI/API, unless the
   in-flight validation run already includes the newly attached metric.
3. Poll the run through the CLI/API until it finishes. While waiting, inspect
   trace quality or prepare the handoff instead of blocking.
4. Confirm each newly attached trace metric reaches a terminal status on the
   validation simulation (`COMPLETED` or `FAILED`). Do not stop while outputs
   are still `IN QUEUE` or `IN PROGRESS`.
5. Confirm the metric computes and does not error with "No spans named..." or "metric_attribute is required".
6. Confirm trace-aware LLM judges run with trace context by launching a
   validation run that includes those metrics after traces are exported.
7. Confirm the computed value is interpretable for the customer question. If it
   computes but is only a tracing proof, mark it diagnostic and replace it with
   a higher-signal metric before handoff.
8. If a metric errors because data is missing, fix the instrumentation rather than changing the metric to measure a less useful signal.
9. If prior runs show metric failures, verify against the first run launched
   after your metric/instrumentation updates before declaring the metric broken.
10. If the creation API rejects a valid-in-code aggregation, keep the validated fallback metric small and explicit, and include the rejected response in the validation notes.

## Phase 4: Handoff

Report:
- created metric IDs and names
- span/attribute/aggregation/unit for each
- LLM judge type and `include_traces` state for trace-aware judge metrics
- customer question and operational interpretation for each
- evidence that each span/attribute existed before creation
- run or conversation used to validate computation
- direct Coval URLs for runs list, run detail, run result, and trace viewer
- any proof-only metrics that were intentionally not created or replaced
- any recommended follow-up instrumentation
