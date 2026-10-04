---
name: neatlogs-go
description: Use when adding neatlogs observability to a Go project — Google Gemini (genai), Google ADK, direct LLM/provider calls, retrieval, service boundaries, or custom code. Covers Init, WrapGenAI, the private-provider ADK integration, explicit span helpers, Trace, and Identify.
metadata:
  author: neatlogs
  language: go
  framework: genai
---

# Neatlogs Go Setup — `neatlogs-go`

The Go SDK is OpenTelemetry-based but keeps to a **private tracer provider**:
`neatlogs.Init()` configures it and **never touches process-global OTel state**
(no `otel.SetTracerProvider` / `SetTextMapPropagator`). So Neatlogs can neither
export nor parent (nor be parented by) a co-tenant tracer like Datadog — and,
symmetrically, OTel-native frameworks are **not** auto-captured. You instrument
explicitly: `WrapGenAI()` wraps a `google.golang.org/genai` client,
`contrib/adk` instruments Google ADK through injected model/tool callbacks and
a run wrapper, and a small set of span helpers cover direct provider calls,
retrieval, and boundaries.
Export is OTLP/HTTP to the managed Neatlogs cloud.

## Transport selection

Use this SDK for Go. Neatlogs also has SDKs for Python and TypeScript/Node.js. For a language without a supported Neatlogs SDK, default to the dependency-free HTTP ingest endpoint `POST /v1/trace`; if that project already emits OpenTelemetry, OTLP/gRPC is also supported. Use the `neatlogs-ingest` skill for the complete HTTP and gRPC contracts. Do not confuse `/v1/trace` nested JSON with the `/v1/traces` OTLP/HTTP protobuf route.

Module: `github.com/neatlogs/neatlogs-go` (requires Go 1.25+). The Gemini wrapper
lives in a separate module (`contrib/genai`) so its heavy dependency stays out of
apps that only need the core helpers.

```bash
go get github.com/neatlogs/neatlogs-go
go get github.com/neatlogs/neatlogs-go/contrib/genai   # only if wrapping Gemini
go get github.com/neatlogs/neatlogs-go/contrib/adk     # only if using Google ADK
```

## The small public API most integrations need

`neatlogs.Init(ctx, Config{...}) (ShutdownFunc, error)`, `neatlogs.Trace(ctx, name)`,
`neatlogs.StartSpan(ctx, name, kind, attrs...)`, `neatlogs.Identify(ctx, IdentifyOptions{...})`,
`genai.WrapGenAI(client)` (from `contrib/genai`), and the explicit span helpers
`neatlogs.StartLLMSpan`, `neatlogs.StartRetrieverSpan`, `neatlogs.StartToolSpanFromHeaders`,
`adk.InstrumentConfig` and `adk.Run` (from `contrib/adk`), plus
`neatlogs.InjectTraceContext` / `ExtractTraceContext` for cross-process boundaries.

## Core mechanism

1. **`Init` once, at startup**, and `defer` its shutdown:
   ```go
   shutdown, err := neatlogs.Init(ctx, neatlogs.Config{
       APIKey:       os.Getenv("NEATLOGS_API_KEY"), // falls back to NEATLOGS_API_KEY
       WorkflowName: "my-service",
   })
   if err != nil { log.Fatal(err) }
   defer shutdown(ctx)
   ```
2. **Gemini** — wrap the genai client (one added line); call it exactly as normal:
   ```go
   import nlgenai "github.com/neatlogs/neatlogs-go/contrib/genai"
   gc := nlgenai.WrapGenAI(client)                 // client = *genai.Client
   resp, err := gc.GenerateContent(ctx, "gemini-2.5-flash", contents, cfg)
   ```
   `WrapGenAI` owns the canonical LLM span. Do not surround calls through `gc`
   with `Trace`, `StartSpan(..., "llm")`, or `StartLLMSpan`.
3. **Google ADK** — instrument the agent config and drive each turn through the
   Neatlogs run wrapper:
   ```go
   import nladk "github.com/neatlogs/neatlogs-go/contrib/adk"

   config := nladk.InstrumentConfig(llmagent.Config{
       Name: "support_agent", Model: model, Tools: tools,
   })
   adkAgent, err := llmagent.New(config)
   // Build runner with adkAgent, then:
   for event, err := range nladk.Run(
       ctx, runner, userID, sessionID, message, agent.RunConfig{},
   ) {
       // Handle the unchanged ADK event stream.
   }
   ```
   `InstrumentConfig` owns model/tool spans. `Run` owns the workflow root,
   identity, input/output, and private trace context. Use both; do not add a
   second LLM span around the wrapped model call.
4. **Direct provider calls (OpenAI/Anthropic/…)** — open an LLM span you fill in:
   ```go
   ctx, llm := neatlogs.StartLLMSpan(ctx, neatlogs.LLMCallOptions{
       Provider: "openai", Model: "gpt-5.5",
       Messages: []neatlogs.LLMMessage{{Role: "user", Content: prompt}},
   })
   defer llm.End()
   // ... real call ...
   llm.SetOutputMessage("assistant", out)
   llm.SetUsage(promptTok, completionTok, totalTok)
   ```
5. **Custom code / boundaries** — open a span you control:
   ```go
   ctx, span, end := neatlogs.Trace(ctx, "handle_request") // workflow root
   defer end()
   ```

## Steps

1. **Install** → `references/1-install.md`
2. **Add Init (+ deferred shutdown)** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Instrument Gemini, Google ADK, or direct calls** → `references/4-wrap-genai-adk.md`
5. **Trace custom code** → `references/5-trace-custom-code.md`
6. **Sessions & end-users (`Identify`)** → `references/sessions-and-end-users.md`

## Rules (apply to ALL steps)

- `neatlogs.Init()` MUST include `APIKey: os.Getenv("NEATLOGS_API_KEY")` (or set the env var) — without it, export is disabled and spans are dropped silently.
- `Init` is single-shot; call it once at startup. Always `defer shutdown(ctx)` (or call it before exit) so buffered spans flush.
- **The provider is private.** `Init` does NOT register the global OTel provider, so Google ADK is not passively auto-captured. For ADK, use `contrib/adk`'s explicit `InstrumentConfig` + `Run` integration; for other calls use `WrapGenAI` or the span helpers.
- **Google ADK needs both owners.** `InstrumentConfig` captures model/tool spans; `Run` supplies the workflow root, identity, input/output, and private trace context. Do not rely on ADK's global OTel spans, and do not add a second `WrapModel` or `StartLLMSpan` around an already instrumented ADK model.
- For remote ADK agents, use `A2AHTTPClient` and `A2AHandler` for propagation plus `A2ABeforeRequest` / `A2AAfterRequest` for client-side I/O. These helpers do not create HTTP spans.
- Gemini wrapping lives in `contrib/genai`: import `nlgenai "github.com/neatlogs/neatlogs-go/contrib/genai"` and call `nlgenai.WrapGenAI(client)` (NOT `neatlogs.WrapGenAI`).
- **Use exactly one capture owner per model call.** `WrapGenAI` owns Gemini calls made through the wrapped client. Never add `Trace`, an `llm` `StartSpan`, or `StartLLMSpan` around those calls. Use `StartLLMSpan` only for a direct or unsupported provider call that has no supported wrapper.
- Session & end-user identity is per-request — set it with `neatlogs.Identify(ctx, ...)`, NEVER on `Init`. It rides on `ctx`. See step 6.
- Pass the `ctx` from `Identify` / `Trace` / `StartLLMSpan` down into whatever runs the turn — Go propagates identity and parent-span through `context.Context`.
- Never hardcode the API key; use `os.Getenv`.
- For EU projects, set `Endpoint: "https://eu.ingest.neatlogs.com"` in `neatlogs.Config`. For other managed projects, omit `Endpoint` and `NEATLOGS_ENDPOINT`. Preserve an explicit self-hosted endpoint.
- **Multiple independent workflows in one service?** `Config.WorkflowName` is process-wide and single-shot. At each independent feature entry point, start a parentless `workflow` span with the canonical per-root override — `neatlogs.StartSpan(ctx, name, "workflow", attribute.String("neatlogs.workflow.name", name))` — so each fresh request/job becomes a distinct dashboard workflow. See the `neatlogs-multi-workflow` skill.

## `neatlogs.Init()` Config Reference

| Field | Type | Default | Description |
|---|---|---|---|
| `APIKey` | `string` | `NEATLOGS_API_KEY` env | Auth key. Empty (after env fallback) → export disabled, spans dropped |
| `Endpoint` | `string` | `NEATLOGS_ENDPOINT`, then `https://ingest.neatlogs.com` | OTLP/HTTP base URL; set to `https://eu.ingest.neatlogs.com` for EU projects. |
| `WorkflowName` | `string` | caller source path, then `neatlogs-app` | Labels this service/run |
| `Tags` | `[]string` | `nil` | Attached to every span as a resource attribute |
| `Debug` | `bool` | `false` | Verbose diagnostics on stderr |
| `DisableExport` | `bool` | `false` | Drop all spans instead of sending (useful in tests) |

> Note: `Init` has NO session / end-user field. Those are per-request — see `Identify` (step 6). Config carries no operator id either; identity is set at the trace boundary.

`neatlogs.Version` is exported (const) and stamped on every trace as the `service.version` resource attribute + the instrumentation-scope version — useful when pinning down which SDK build emitted a span.

## Verify

Run the repository's existing checks. At minimum, run `go test ./...` and
`go build ./...`; run `go mod tidy` first when dependencies changed. Restart the
real server, worker, or binary after changing startup instrumentation, then
exercise the actual instrumented path. Run with `Debug: true` and confirm export
succeeds.

Check the target Neatlogs project, not merely local debug output. For
`WrapGenAI`, confirm exactly one canonical `llm` span per call, nested under the
expected `workflow`, with input/output messages and token usage. For explicit
helpers, confirm each `StartLLMSpan` / `StartRetrieverSpan` records its I/O (an
empty retriever result is recorded as `"[]"`, not omitted).
`StartRetrieverSpan` emits the canonical `neatlogs.retriever.*` namespace;
never emit the legacy `neatlogs.retrieval.*` spelling from new code.

For Google ADK, confirm one `workflow` root with the expected `llm` and `tool`
children, that root and LLM input/output are populated, and that token usage is
present when ADK returns it. For A2A, also confirm the semantic `agent` span.
Confirm no transport-only HTTP span was introduced.

## Safety gate

Before any edit, confirm this service is Go. Identify the Go package manager
and toolchain from `go.mod`, `go.work`, and `go.sum`. Resolve the installed
SDK module version without changing dependencies:

```bash
go list -m -f '{{.Version}}' github.com/neatlogs/neatlogs-go
```

A Go module dependency does not install its CLI. If the `neatlogs` binary is
missing, check the canonical module tags for the latest published stable
release. If the project uses an older release that lacks Doctor v2, show the
exact module-upgrade command and obtain explicit user approval before running
it. Accept newer compatible releases and never downgrade one. After resolving
the project module version, replace `<resolved-module-version>` below with that
exact value. Show the command and obtain separate explicit user approval:

```bash
go install github.com/neatlogs/neatlogs-go/cmd/neatlogs@<resolved-module-version>
```

Do not substitute `go run`, `@latest`, `npx`, a Wizard command, or an
unversioned download. The approved `go install` command must use the same
version as the project module. Then run the installed Doctor binary:

```bash
neatlogs doctor --local --json
```

Local mode must be read-only and network-free. It requires no credential and
must not change source or configuration. Require `format_version:
"neatlogs.doctor/v2"`, `runtime.language: "go"`, and
`runtime.schema_version: "2"`. Require that the binary and project module
versions match. Treat `runtime.sdk_version` as identity evidence, not as an
exact-version allowlist.

If the command is missing or its result has the wrong format, language, schema,
or module identity, fail closed. If the installed release is already the latest
published stable release but lacks Doctor v2, stop and give safe manual/support
remediation. Rerun local Doctor after an approved upgrade or CLI installation.
Do not edit while this gate is unresolved.

A local `pass` proves only that the installed SDK produced and validated its
controlled in-process envelope. It does not prove that the application is
instrumented, that anything was exported, or that a hosted trace is visible.
Preserve every `reason_code` and `remediation_code` exactly. Treat a warning,
failure, or unknown future code as manual/support remediation unless the code is
explicitly safe/fixable here. The only source fixes allowed by this gate are:

- `INSTRUMENTOR_INACTIVE`: apply only this skill's documented initialization or
  wrapper/helper step.
- `ROOT_MISSING`: add only the already-requested, documented workflow boundary
  at a confirmed entry point.
- `ROOT_NOT_ENDED`: add only this skill's documented lifecycle hook.

Do not edit for credential, authentication, transport, backend, ambiguous
ownership, or unknown codes. Never reproduce backend PII, routing, mapping, or
finalization implementation. Before any build, test, or user-workflow command,
show the exact command and obtain explicit user approval. Make reruns idempotent:
reread the target first and never duplicate initialization, wrappers, roots, or
shutdown hooks. Keep a pre-edit diff. If an approved check fails, use the
rollback plan to revert only the edits from this run when they can be isolated
safely. Otherwise, stop and give manual recovery instructions that preserve
unrelated user work.

After instrumentation, obtain approval for the project checks and one
representative real workflow. Obtain separate approval for the authenticated
probe. Use only a credential already supplied through the process environment.
Never print it, place it in command arguments or files, copy it into output, or
put it in agent context.

```bash
neatlogs doctor --probe --json
```

Probe mode sends one controlled four-span trace through `POST /v1/traces` with
`x-neatlogs-doctor: v1`, then reads that exact trace through
`GET /api/traces/v3/{trace_id}` with the same project credential. Accept a
probe `pass` only when capture and readback trace IDs match, the trace is
finalized, exactly four spans contain one meaningful WORKFLOW root with
AGENT→LLM and root→TOOL relationships, there are no duplicates, required
semantics and I/O are present, and token values remain numeric. Never infer
success from installation, local logs, exporter flush, HTTP 2xx, or any
uncorrelated trace. Probe success proves the controlled path only. Verify the
real user workflow separately through the completion gate below.

## Completion gate

After local Doctor passes and the requested instrumentation is in place:

1. Show the exact project build, test, and real-workflow commands and obtain
   explicit user approval before running them.
2. Run only the approved checks. Restart a long-running process so it loads the
   new initialization and wrappers; keep reruns idempotent.
3. Exercise one representative real user workflow. End every opened span and
   use the documented flush/shutdown lifecycle for that process type.
4. Through the target project's normal product trace view or supported public
   read path, verify that exact run is finalized, has one meaningful root and
   the expected semantic hierarchy, and contains no duplicate operation spans.

Keep project credentials in the process environment or client secret storage;
never put them in commands, output, files, or agent context. Do not use a
legacy marker-discovery protocol. Installation, local logs, exporter flush,
HTTP 2xx, a local Doctor pass, and a separate probe pass are not proof that the
application's real workflow is correct. If the exact user trace cannot be
inspected, report the missing access or observation as a blocker and provide
rollback/manual recovery instructions without claiming completion.
