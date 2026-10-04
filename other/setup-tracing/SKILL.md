---
name: setup-tracing
description: Configure an AI agent to send OpenTelemetry traces to Coval. Use when a user wants to add Coval tracing, instrument an agent for simulations or conversation monitoring, make traces show up in Coval, handle SIP/PSTN/WebSocket trace correlation, or replace the one-command wizard with a security-reviewable manual setup.
---

# Setup Coval Tracing

Set up tracing in the customer's agent with the smallest additive change that produces a real Coval trace, then verify that trace against the agent's actual Coval connection path.

Operate from the customer's agent side. Do not assume access to Coval internal
backend, frontend, docs, wizard, research, or example source repositories, and
do not ask the customer for them. Use only the customer's repo, public Coval
docs, public SDK examples, the Coval CLI/API, and fetched public OpenAPI specs.
Code edits belong in the customer's agent/service repo. Coval-side changes must
be limited to documented configuration through the Coval CLI, public API, or
dashboard, and should be explained before mutation.

## Preflight

1. Confirm the agent repo or service scope. In a monorepo, do not instrument every service unless the user explicitly asks.
2. Check Coval authentication without reading secret files:
   ```bash
   coval whoami
   coval agents list --format json
   ```
   If the CLI is unavailable, use `COVAL_API_KEY` from the user's shell environment and direct API calls. Never print or store the raw key. When listing agents through the API, redact `metadata` before showing output because some provider integrations store model API keys there.
3. Fetch current API shape before writing API integrations:
   ```bash
   curl -fsS https://api.coval.dev/v1/openapi
   ```
   For broader docs discovery, fetch `https://docs.coval.dev/llms.txt` and then
   the specific public docs page needed for the task.
4. Stay inside the customer-owned code surface. Do not reference or require
   `coval-ai/backend`, `coval-ai/frontend`, `coval-ai/docs`,
   `coval-ai/wizard`, internal engineering docs, or private Coval repos as
   local source code. Public docs, public SDK examples, and installed skill
   reference files are the support material available to the customer-side
   agent.
5. Read the shared references before editing:
   - `../references/coval-tracing-reference.md`
   - `../references/agent-type-routing.md`
   - `../references/span-schema.md`
   - if the agent is Vapi-based, `../references/vapi-artifact-tracing.md`

## Phase 1: Read-Only Analysis

Do not edit files until this phase is complete.

Identify:
- language and package manager
- app start command and one representative local invocation
- agent framework or provider stack: Pipecat, LiveKit, Vapi, Twilio, WebSocket, direct OpenAI/Anthropic, custom loop, etc.
- nearby same-stack agent implementations (if available in the same workspace)
  that already emit richer traces; use them as additive instrumentation
  references instead of reinventing span structure
- Coval agent type and connection path: SIP inbound, PSTN inbound, outbound voice, WebSocket voice/chat, or conversation monitoring
- where a per-call Coval ID can enter the agent process
- existing telemetry owner: OpenTelemetry, Sentry, Datadog, Honeycomb, Langfuse, Arize, LangSmith, Traceloop, or custom OTLP exporter
- short-lived process behavior and shutdown/flush path
- customer-owned files that need edits, and any Coval configuration changes
  that must be done through CLI/API/dashboard rather than code changes

Return a concise analysis summary. If the target service or repo scope is
ambiguous, ask before editing. Do not ask the customer to choose a correlation
route from a menu. Customers usually cannot know whether SIP headers, pre-call
webhooks, or trigger payloads are supported from the outside; infer the best
route from the discovered agent configuration and the decision rules below.

## Phase 2: Pick The Correlation Path

Use exactly one target header per export:
- simulations: `X-Simulation-Id` with the simulation output ID
- conversation monitoring: `X-Conversation-Id` with the `conversation_id` returned by `POST /v1/conversations:submit`

Pick the route yourself when the repo and Coval agent configuration make one
route clearly safer. Do not present an open-ended "which route should I use?"
question. Use this decision order:

1. If the current connection path already delivers a Coval ID into the process,
   use that path. Examples: SIP participant attributes, outbound trigger
   payload, WebSocket initialization payload, or a monitoring
   `conversation_id`.
2. If the current Coval agent record or fetched OpenAPI confirms an existing
   pre-call/registration webhook field and the service already exposes a
   suitable endpoint, configure or reuse that webhook.
3. For inbound PSTN phone agents with no verified SIP headers and no confirmed
   Coval pre-call webhook wiring, default to a self-contained registration
   endpoint plus a smoke launcher that registers `simulation_output_id` right
   before the call. This is the safest first validation because it does not
   guess at Coval agent metadata shape or mutate customer agent config. After it
   works, state the production upgrade: wire the same endpoint into the verified
   Coval pre-call webhook field when available, or provision SIP if the customer
   needs Coval-managed per-call injection.
4. Ask a customer question only when every viable route requires a policy or
   deployment decision you cannot infer, such as whether you may expose a new
   public webhook, update the Coval agent configuration, or provision a SIP
   route. In that case, give one recommendation first, explain why, and ask for
   the smallest approval needed.

Coval-side config changes that are **purely additive** to a documented field
that is currently empty (e.g., setting `initialization_json` from `"{}"` to the
documented `{"simulation_id":"{{simulation_id}}"}` placeholder, or filling an
empty `pre_call_webhook_url`) do not need a consent prompt — the customer's
"get traces working" intent implies it, and the change is trivially reversible
via the same PATCH. Show the before/after value in the handoff but proceed
without asking. Always ask before changes that delete config, downgrade auth,
overwrite a non-empty field, or modify shared resources like phone numbers,
SIP routes, test sets, or webhook secrets.

Choose the route from `../references/agent-type-routing.md`:
- SIP inbound voice: extract `X-Coval-Simulation-Id` from SIP headers or framework participant attributes.
- PSTN inbound phone: do not expect SIP headers. Add or configure `pre_call_webhook_url` / registration-webhook correlation, or guide the customer to provision a SIP address.
- Outbound voice: carry `simulation_output_id` in the trigger payload and read it in the trigger handler.
- WebSocket voice/chat: carry the simulation output ID in the initial setup payload or initialization JSON.
- Conversation monitoring: buffer spans during the call, submit the conversation at call end, then export buffered spans with `X-Conversation-Id`.

For direct WebSocket agents, prefer configuring Coval metadata with an explicit initialization payload such as:

```json
{"simulation_id": "{{simulation_id}}"}
```

Then treat the first non-audio frame as setup metadata, extract `simulation_id` or
`simulation_output_id`, and only export with `X-Simulation-Id` after that ID is
present. Current production examples use `{{simulation_id}}`; if docs mention
`{{simulation_output_id}}`, verify current agent metadata behavior before
hardcoding either name.

## Phase 3: Implement Additive Instrumentation

Prefer an existing telemetry owner. If the app already has a `TracerProvider`,
add a Coval exporter/processor to it instead of replacing the provider. If
there is no telemetry setup, create one central module such as
`coval_tracing.py`, `covalTracing.ts`, or `coval_tracing.go` and keep the agent
entry point focused on business/webhook routing. Do not leave the final
implementation as a large inline tracing block inside `server.py`, `app.ts`, or
the main webhook handler unless the repo is a tiny single-file prototype.

Implementation requirements:
- Endpoint: `https://api.coval.dev/v1/traces`
- Auth header: `x-api-key` or `X-API-Key` from an environment variable, never a literal secret
- Timeout: 30 seconds
- Resource: set `service.name` to the agent or service name. Also add stable
  customer-visible resource attributes when known: `service.namespace`,
  `agent.name`, `agent.provider`, `coval.agent_type`, and
  `coval.correlation.method`.
- Export one target header only: `X-Simulation-Id` or `X-Conversation-Id`
- Buffer spans only when the Coval ID is not yet available; bound the buffer
- Use the standard OpenTelemetry SDK where available. For call flows where the
  Coval target ID arrives after spans start, use an SDK-backed buffer such as
  `InMemorySpanExporter`, then export the finished spans with an
  `OTLPSpanExporter` after the ID is known. Avoid hand-rolled OTLP JSON
  exporters unless the language/runtime has no usable SDK.
- Use `BatchSpanProcessor` or equivalent for high-volume agents and keep batches comfortably below 3-4 MB
- Flush/shutdown tracing before short-lived processes exit
- Retry only failed batches; Coval stores spans append-only and does not deduplicate successful retries
- Update deployment packaging. Dockerfiles, serverless bundles, Pipecat Cloud
  packages, and Fly/Render/Heroku deploys must include any new tracing helper
  module and dependency files.
- Emit the canonical span names from `../references/span-schema.md` first:
  `llm`, `tts`, `stt`, `stt.provider.<name>`, `vad`, `llm_tool_call`,
  `turn`, `conversation`, `pipeline`, and `transport`. These names drive
  semantic UI labels, colors, and built-in trace metrics.
- When adding tool or workflow spans, include metric-ready numeric attributes
  from the first implementation: `tool.latency_ms`, numeric `tool.error`,
  numeric `tool.dependency_unavailable`, `tool.call.count`,
  `tool.failure.count`, numeric `workflow.completed`, numeric
  `workflow.dependency_blocked`, and numeric `workflow.fallback_used` when
  available. These keep `configure-trace-metrics` from having to settle for
  proof-only metrics.
- Add one vertical-specific workflow span or root attribute for the customer's
  most important failure mode during the first pass. Examples:
  `roadside.dispatch.latency_ms`, `reservation.date.changed`,
  `identity.verification.completed`, `payment_plan.blocked`, or
  `handoff.required`. Generic tool metrics are not enough when the repo clearly
  exposes a business-critical path.
- Emit OTel span events on the conversation root for moment-in-time business
  milestones such as `simulation_id_received`, `dispatch_called`,
  `delay_acknowledged`, `callback_offered`, `fnol_started`, `fnol_completed`,
  `booking_attempted`, or `escalation_triggered`. Use events for timeline dots;
  use spans for work with duration.
- For webhook-style voice agents, do not rely only on a final end-of-call event
  if tool-call or turn webhooks already have the Coval target ID. Export the
  per-event spans when the target ID is known, or buffer them until it is known,
  then flush once. Avoid replaying spans after a successful export because Coval
  trace ingest is append-only.
- For Vapi-hosted PSTN agents, parse `end-of-call-report.artifact.messages`
  after basic tool-call tracing works. Use Vapi message windows for `turn`
  spans, but do not fabricate provider latency. If you emit `stt`, `llm`, or
  `tts` spans from artifact messages, mark them as metadata markers with
  `trace.source=vapi_artifact`, `trace.timing=metadata_marker`, and a
  `trace.duration_note`; alternatively use marker-suffixed span names. Do not
  create LLM/STT/TTS latency metrics from these marker spans.

For Python voice agents, an existing generated `coval_tracing.py` helper in the
customer repo is an acceptable baseline, but improve it for the discovered
connection path and existing telemetry.

## Phase 4: Minimum Span Coverage

The first working trace should contain:
- a root `conversation` or equivalent session span when the framework gives a call boundary
- at least one `stt`, `llm`, `tts`, or `llm_tool_call` span that matches the actual agent path
- correct parent/child relationships where the framework exposes them
- `service.name` resource metadata
- Coval-compatible target ID routing

If the app cannot expose STT/TTS/LLM internals yet, ship the minimum useful trace first, then use `optimize-trace-observability` for enrichment.

**Anti-pattern: per-chunk or per-frame transport spans.** Voice/realtime agents
stream audio in many small chunks (often 20-100 ms). Emitting one OTel span per
chunk produces hundreds of micro-spans that visually drown the trace viewer and
collapse the real `turn`/`tts`/`llm` spans into invisible slivers — the trace
will *look* empty even when it is not. Aggregate per-chunk activity into
counter attributes on the parent stream span instead:

- `audio.chunks_sent` (count) and `audio.chunk_target_ms` (configured cadence)
  on the `tts` span
- `audio.chunks_received` on the `turn` or `stt` span
- `audio.payload_bytes`, `audio.duration_s` already capture the totals

The same rule applies to per-frame `transport.recv_audio`, per-event WebSocket
pings, and per-token streaming spans. One span per high-level operation; per-
chunk detail goes into numeric attributes.

## Phase 5: Verification

Run local checks first:
```bash
python -m compileall .
npm test
npm run typecheck
go test ./...
```
Use the checks that match the repo; do not invent package-manager commands.

Then start the Coval validation through CLI/API and do useful work while it
runs. Coval simulations and monitoring conversations are asynchronous; do not
sit idle after launching one.

1. Use the discovered Coval CLI/API path to launch one real test through the
   same Coval agent type the customer uses. Prefer CLI commands when available;
   otherwise use the public API after fetching OpenAPI. Capture the run ID,
   simulation output ID, conversation ID, dashboard URL, or polling endpoint
   returned by the launch.
2. Start a bounded poll loop through the CLI/API. Record the command or endpoint
   used, poll interval, and timeout. Do not print API keys or raw provider
   metadata from Coval agent responses.
   For simulations, do not wait only for `GET /v1/runs/{run_id}` to expose
   `results.output_ids`; that can lag until completion, which is too late for
   PSTN/webhook registration. Also poll:
   `GET /v1/simulations?filter=run_id%3D%22<RUN_ID>%22`, register the first
   returned `simulation_id` / simulation output ID immediately, then continue
   watching the run.
3. While the run is pending, continue with non-blocking trace improvement:
   - add safe span enrichment visible from the code path, such as stable
     `conversation`, `turn`, `stt`, `llm`, `tts`, `llm_tool_call`,
     `transport`, or provider spans
   - add bounded high-value attributes such as `metrics.ttfb`, token counts,
     finish reasons, tool names, safe tool argument summaries, status, and
     errors
   - add customer-signal numeric attributes that can become metrics, such as
     `tool.error`, `tool.latency_ms`, `tool.call.count`,
     `workflow.dependency_blocked`, `workflow.completed`, and
     `workflow.fallback_used`
   - improve flush/shutdown, buffering, batch size, retry, or deployment
     packaging issues found during implementation
   - prepare custom trace metric candidates from expected spans and any
     historical Coval traces already available; treat generic duration or
     span-count metrics as diagnostic proof unless they answer a customer
     operating question
   - prepare trace-aware LLM judge metric candidates with `include_traces=true`
     when trace context is needed to grade ordering, tool-output grounding,
     verification before tool use, or recovery from tool errors
4. Create custom trace metrics during the wait only when real trace data already
   proves the span name and metric attribute exist, either from historical
   traced runs or from the in-flight validation once spans appear in Trace
   Search. If this validation is the first trace for the agent, stage the metric
   definitions while waiting and create them immediately after the run produces
   confirmed spans.
   Create trace-aware LLM judge metrics before the follow-up validation run when
   the Metrics OpenAPI supports `include_traces` and their prompts depend on
   trace context that the first trace already proved exists.
5. When the run finishes, confirm the agent export returned 200 or that the
   exporter logged a successful accepted batch. A 404 from the standalone test
   script only proves auth/connectivity, not lifecycle wiring.
6. Open the Coval run or conversation result and verify the OTel Traces card or
   Trace Search result appears.
7. Inspect the trace for expected spans and attributes. If it is missing, sparse,
   duplicated, or attached to the wrong result, stop further metric creation and
   apply `debug-traces` before continuing.
8. **Trace density self-check.** Before declaring success, count spans by name.
   If a single span name is more than ~70% of total spans and those spans are
   each shorter than ~50 ms, that name is almost certainly per-chunk/per-frame
   noise. Collapse it into a counter attribute on the parent span and redeploy
   *before* opening the result for the customer — the trace viewer will look
   empty otherwise. Do not rely on the customer to flag visual noise.
9. **Verify correlation activation from the exporter, not from pre-existing
   agent counters.** Pre-existing counters like a `non_audio_messages` or
   `non_setup_frames` tally on the agent often increment *after* the
   setup/init branch returns, so they read `0` even when correlation worked.
   The authoritative signal that the simulation ID reached the exporter is
   the OTel logger line (`activated OTLP export simulation_id=<id>`) or the
   batch processor's accepted-batch log. Check those first; only chase
   counters if the exporter never activated.
10. After the initial trace is confirmed, finish any prepared metric creation
    and run one follow-up calculation/preview/attached-run check through the
    CLI/API when the public API supports it.
11. If you changed metric definitions or attached new metrics, run a post-change
    validation and poll until the run status is terminal (`COMPLETED`, `FAILED`,
    or `CANCELLED`) and each newly attached trace metric has a terminal output
    on the simulation (`COMPLETED` or `FAILED`). Do not stop while outputs are
    still `IN QUEUE` / `IN PROGRESS`, even when `progress.completed_test_cases`
    already equals `total_test_cases`.
12. When prior runs show `FAILED` trace metrics, verify against the first run
    launched after your instrumentation and metric changes instead of treating
    older runs as current-state proof. Metric failures on older runs may reflect
    stale definitions that no longer match the latest instrumentation.

For WebSocket agents, make the smoke interaction long enough to trigger the
agent's response threshold. A client that sends too little audio, or an agent
that waits for more silence/audio than Coval sends, can make tracing look broken
even when the exporter is wired correctly. If a `tts` span is marked `ERROR`
with a WebSocket disconnect after partial audio, shorten the canned response or
stop streaming when the client closes.

Optional connectivity-only check:
```bash
python skills/traces/setup-tracing/scripts/send-test-span.py \
  --api-key "$COVAL_API_KEY" \
  --simulation-id coval-tracing-test
```
A 404 with `Simulation output not found` means the key reached Coval and auth worked, but it is not proof that the agent call lifecycle is wired.

## Handoff

End with:
- files changed and why
- exact correlation path used
- how the customer sets required env vars
- commands run, including the Coval launch and polling commands/API endpoints
- Coval trace URL or simulation/conversation ID used for proof
- direct Coval URLs for:
  - runs list (`https://app.coval.dev/<org-slug>/runs?sort=createdAt%3Adescending`)
  - run details (`https://app.coval.dev/<org-slug>/runs/<run-id>`)
  - run result (`https://app.coval.dev/<org-slug>/runs/<run-id>/results/<simulation-output-id>`)
  - trace viewer (`https://app.coval.dev/<org-slug>/runs/<run-id>/results/<simulation-output-id>/traces`)
- custom trace metrics created, staged, or deferred and why
- any remaining gaps to handle with `optimize-trace-observability`, `configure-trace-metrics`, or `debug-traces`
