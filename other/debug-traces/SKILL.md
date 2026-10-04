---
name: debug-traces
description: Troubleshoot Coval OpenTelemetry trace ingestion, missing trace UI, sparse traces, bad simulation or conversation correlation, auth/org errors, oversized payloads, duplicate spans, and production debugging with Trace Search.
---

# Debug Coval Traces

Use this skill when a customer expected traces in Coval and they are missing, wrong, sparse, duplicated, or not useful for production debugging.

## Read First

Load:
- `../references/debugging-matrix.md`
- `../references/coval-tracing-reference.md`
- `../references/agent-type-routing.md`
- `../references/span-schema.md` when trace quality is the problem
- `../references/vapi-artifact-tracing.md` when debugging Vapi webhook traces

## Phase 1: Identify The Failure Boundary

Separate the problem into one of these boundaries:
- agent never exported spans
- export returned an HTTP error
- export succeeded but targeted the wrong simulation/conversation/org
- spans are stored but the UI route is not where the user looked
- spans exist but are sparse or not useful
- custom trace metrics cannot find spans or attributes

Collect:
- endpoint used
- response status/body from `/v1/traces`
- whether the export used `X-Simulation-Id` or `X-Conversation-Id`
- simulation output ID or conversation ID, not the run ID unless this is a monitoring conversation
- Coval agent type and connection path
- recent trace viewer URL, Trace Search URL, or copied trace dump
- whether spans were sent as OTLP JSON or protobuf

Do not ask for raw API keys. Ask the user to run commands locally with env vars. Redact Coval agent `metadata` before sharing API responses; provider keys may be stored there.

## Phase 2: Run Minimal Checks

Check Coval auth:
```bash
coval whoami
```

Run a standalone connectivity check when useful:
```bash
python skills/traces/setup-tracing/scripts/send-test-span.py \
  --api-key "$COVAL_API_KEY" \
  --simulation-id "$SIMULATION_OUTPUT_ID"
```

Interpretation:
- 200 means Coval accepted and stored the test span for that target.
- 404 for `coval-tracing-test` or another known-fake ID means auth/connectivity worked but the target ID is not real. Use `--allow-not-found` for intentional fake-ID checks.
- 404 for a real target usually means wrong ID, wrong org key, or using a run ID instead of a simulation output ID.

For conversation monitoring, use:
```bash
python skills/traces/setup-tracing/scripts/send-test-span.py \
  --api-key "$COVAL_API_KEY" \
  --conversation-id "$CONVERSATION_ID"
```

## Phase 3: Apply The Troubleshooting Matrix

Use `../references/debugging-matrix.md` to map symptom to cause and fix.

High-probability causes:
- no target header, or both target headers sent
- `X-Simulation-Id` contains a run ID instead of a simulation output ID
- `X-Conversation-Id` used for a non-monitoring run
- PSTN phone path expected SIP headers that cannot arrive
- WebSocket initialization payload did not include the simulation output ID
- wrong organization's API key
- payload over roughly 3-4 MB
- retry resent already accepted spans
- only auto-instrumented provider spans exist, so the trace lacks STT/TTS/tool context
- Vapi-hosted PSTN trace uses artifact-derived STT/LLM/TTS marker spans but
  reports them as measured provider latency
- tracing helper files or OpenTelemetry dependencies were added locally but not copied into the deployed image/bundle
- WebSocket smoke tests sent less audio than the agent's response threshold, or the agent streamed a long canned response after Coval closed the socket
- run progress reached `completed_test_cases == total_test_cases`, but run
  status is still non-terminal and metric outputs are still queueing
- older runs reflect stale metric definitions and are being treated as proof of
  current instrumentation state

For Vapi-hosted PSTN agents, inspect the source of each span before calling it
real provider observability. `tool-calls` webhooks are real tool execution.
`end-of-call-report.artifact.messages` are real transcript/turn evidence.
Provider-internal STT/LLM/TTS timing is not real unless the span has measured
provider timing or explicit provider fields rather than
`trace.timing=metadata_marker`.

For Vapi-hosted PSTN agents, inspect the source of each span before calling it
real provider observability. `tool-calls` webhooks are real tool execution.
`end-of-call-report.artifact.messages` are real transcript/turn evidence.
Provider-internal STT/LLM/TTS timing is not real unless the span has measured
provider timing or explicit provider fields rather than
`trace.timing=metadata_marker`.

## Phase 4: Verify In Coval UI

Use the right surface:
- simulation result: run result page, OTel Traces card, trace viewer
- cross-call investigation: Trace Search under Observability
- run-level flow failures: Transition Hotspots tab
- conversation monitoring: conversation result/trace search, not simulation-only routes

Trace Search filters that usually isolate issues:
- span name: `llm`, `stt`, `tts`, `llm_tool_call`
- status: `ERROR`
- duration greater than expected thresholds
- attribute exists: `metrics.ttfb`, `stt.providerName`, `function.name`, `llm.finish_reason`
- agent/test set scope

For metric debugging, use the simulation metrics API/CLI output in addition to
the run summary:
- run may still show `IN PROGRESS` while metrics are computing
- each metric output should become terminal (`COMPLETED` or `FAILED`)
- treat `IN QUEUE` / `IN PROGRESS` metric outputs as pending, not failed

## Phase 5: Fix Or Escalate

Fix implementation issues directly when the repo is available and the change is additive. Escalate with exact evidence when:
- the target ID belongs to another org and the user must provide the correct key
- the customer needs SIP provisioning or Coval agent config changes outside the repo
- the Coval API returns repeated 500/503 after valid retries
- the trace exists in storage but the UI cannot load it

End with a short incident-style summary: observed status, root cause, fix applied or required, and the exact command or Coval UI check that proves the current state.
