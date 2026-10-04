---
name: neatlogs-ts
description: >
  NeatLogs is an AI agent debugging and observability platform. Use this skill when
  instrumenting TypeScript/Node.js LLM applications with neatlogs for tracing, monitoring,
  debugging, observability, spans, or instrumentation of
  LLM providers and agent frameworks.
---

# NeatLogs TypeScript SDK — Agent Skill

NeatLogs auto-instruments LLM calls, agent frameworks, and custom code with these core exports:
`init()`, `flush()`, `shutdown()`, `span()`, `Span()`, `trace()`, `identify()`, and `log()`.

---

## Installation

Always install the latest published version (don't pin an older one):

```bash
npm install neatlogs@latest
# pnpm add neatlogs@latest · yarn add neatlogs@latest · bun add neatlogs@latest
```

Requires Node.js >= 18.

---

## Core Principles

1. **Import order does NOT matter**: instrumentation is per-instance via a `wrap*` helper (`wrapOpenAI(new OpenAI())`), so static top-of-file imports are fine. No dynamic `import()` gymnastics.
2. **Scripts**: end with `await flush()` then `await shutdown()`. **Servers**: call `init()` once at startup; do NOT call `flush()` or `shutdown()` on every request.
3. **One capture owner per operation**: a provider/framework wrapper, handler, hook, or processor owns the spans for calls it captures. Use `span()` for your own orchestration. Use `trace()` for custom attributes or a manual LLM span only when no supported capture layer owns that operation.
4. **Region endpoint**: for EU projects, set `endpoint: 'https://eu.ingest.neatlogs.com'` in `init()`. For other managed projects, omit `endpoint`, `baseUrl`, and `NEATLOGS_ENDPOINT`. Preserve an explicit self-hosted endpoint.
4. **NEVER pass `instrumentations: [...]`.** The public option and registry are removed. TypeScript rejects the property, and the JavaScript compatibility guard throws a typed configuration error before telemetry starts. Use the explicit helper from the [Supported Instrumentations](#supported-instrumentations) table.
5. **Init is single-shot**: `init()` configures a **private** telemetry provider (never registered globally — see [OTel Isolation](#otel-isolation)). Calling it again is a no-op (with a warning). Call `shutdown()` first to reinitialize (rare).
6. **All lifecycle functions are async**: `init()`, `flush()`, and `shutdown()` return Promises and must be awaited.
7. **Named imports**: Always use named imports from `'neatlogs'`.

### Transport selection

Use this SDK for TypeScript/Node.js. Neatlogs also has SDKs for Python and Go. For a language without a supported Neatlogs SDK, default to the dependency-free HTTP ingest endpoint `POST /v1/trace`; if that project already emits OpenTelemetry, OTLP/gRPC is also supported. Use the `neatlogs-ingest` skill for the complete HTTP and gRPC contracts. Do not confuse `/v1/trace` nested JSON with the `/v1/traces` OTLP/HTTP protobuf route.

---

## Quick Start

Complete minimal working example:

```typescript
import { init, wrapOpenAI, span, flush, shutdown } from 'neatlogs';
import { OpenAI } from 'openai';

await init({
  apiKey: process.env.NEATLOGS_API_KEY ?? '',
  workflowName: 'my-app',
});

// wrapOpenAI patches THIS instance — import order is irrelevant.
const client = wrapOpenAI(new OpenAI());

const myWorkflow = span({ kind: 'WORKFLOW' }, async (query: string) => {
  const response = await client.chat.completions.create({
    model: 'gpt-4o',
    messages: [{ role: 'user', content: query }],
  });
  return response.choices[0].message.content;
});

await myWorkflow('Hello!');
await flush();
await shutdown();
```

---

## Instrumentation Workflow

1. **Assess**: Detect what LLM providers/frameworks the project uses.
2. **Instrument**: Choose the correct approach:
   - Providers/frameworks → the matching `wrap*` helper / handler / processor (see [Supported Instrumentations](#supported-instrumentations))
   - `span()` wrappers for custom orchestration code
   - `trace()` for custom span attributes and unsupported/raw operations only—never around a call already owned by a wrapper, handler, hook, processor, or instrumentor
3. **Init**: Add `await init()` once at startup, with **no** `instrumentations` key.
4. **Verify**: build/typecheck the changed project, restart any server/startup process, exercise the real instrumented path, and confirm a new NeatLogs trace with one canonical span per operation.

For a generic Next.js retrieval-and-generation example, see [Retrieval-and-generation workflow verification](references/retrieval-generation-workflow.md).

## Safety gate

Before any edit, confirm this service is TypeScript/Node.js. Identify its
package manager from the manifest and lockfile, then read the declared and
installed SDK version. Do not install or change dependencies during this
inspection. Run exactly one project-local command for the detected package
manager:

```text
npm:  npm exec --offline --no -- neatlogs doctor --local --json
pnpm: pnpm exec neatlogs doctor --local --json
Yarn: yarn run neatlogs doctor --local --json
Bun:  bun --no-install run neatlogs doctor --local --json
```

These commands let the package manager select the platform-specific local
executable, including the Windows shim. Do not substitute `npx`, `pnpm dlx`,
`yarn dlx`, `bunx`, a Wizard command, or another downloaded Doctor. Local
mode must be read-only and network-free. It requires no credential and must not
change source or configuration. Require `format_version:
"neatlogs.doctor/v2"`, `runtime.language: "typescript"`, and
`runtime.schema_version: "2"`. Compare `runtime.sdk_version` with the
installed project package to prove that the runner did not select another copy.
Do not compare it with one hardcoded patch version.

If the command is missing or its result has the wrong format, language, schema,
or installed-package identity, fail closed. Check the canonical package
registry for the latest published stable release. If the project uses an older
release, show the exact upgrade command for the detected package manager and
obtain explicit user approval before running it. Accept newer compatible
releases and never downgrade one. If the installed release is already current
but lacks Doctor v2, stop and give safe manual/support remediation. Rerun local
Doctor after any approved upgrade. Do not edit while this gate is unresolved.

A local `pass` proves only that the installed SDK produced and validated its
controlled in-process envelope. It does not prove that the application is
instrumented, that anything was exported, or that a hosted trace is visible.
Preserve every `reason_code` and `remediation_code` exactly. Treat a warning,
failure, or unknown future code as manual/support remediation unless the code is
explicitly safe/fixable here. The only source fixes allowed by this gate are:

- `INSTRUMENTOR_INACTIVE`: apply only this skill's documented initialization or
  wrapper/hook step.
- `ROOT_MISSING`: add only the already-requested, documented WORKFLOW boundary
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

Run the matching project-local command:

```text
npm:  npm exec --offline --no -- neatlogs doctor --probe --json
pnpm: pnpm exec neatlogs doctor --probe --json
Yarn: yarn run neatlogs doctor --probe --json
Bun:  bun --no-install run neatlogs doctor --probe --json
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

## `init()` Reference

```typescript
import { init } from 'neatlogs';
await init(options);
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `apiKey` | `string` | `undefined` | API key (or set `NEATLOGS_API_KEY` env var). If neither is set, spans are created locally but **silently not exported** |
| `workflowName` | `string` | derived from `process.argv[1]` | Name for this workflow/application |
| `tags` | `string[]` | `undefined` | Tags for filtering in dashboard |
| `userId` | `string` | `undefined` | The **operator** running the SDK (developer / service account), NOT your app's end-user. For end-user & session identity, see [Sessions & End-Users](#sessions--end-users) |
| `sampleRate` | `number` | `1.0` | Sampling rate (0.0 to 1.0) |
| `flushInterval` | `number` | `5` | Seconds between batch flushes |
| `batchSize` | `number` | `100` | Max spans per batch |
| `debug` | `boolean` | `false` | Enable verbose logging |
| `disableExport` | `boolean` | `false` | Disable span export to backend |
| `captureLogs` | `boolean` | `false` | Capture `log()` calls as LOG spans |
| `pii` | `'redact' \| 'hash' \| false` | `undefined` | PII detection setting |
| `piiEnabled` | `boolean` | `undefined` | Override team-level server-side PII redaction |
| `piiSpanTypes` | `string[]` | `undefined` | Override which span types have PII redaction |
| `mask` | `MaskFunction` | `undefined` | Client-side mask function |
| `metadata` | `Record<string, any>` | `undefined` | Custom metadata to attach to all spans |
| `tracerProvider` | `BasicTracerProvider` | `undefined` | Caller-owned private provider. Neatlogs adds its processors + flushes it, but never registers it globally or shuts it down |
| `registerShutdownHandlers` | `boolean` | `true` when Neatlogs owns the provider, else `false` | Register `beforeExit`/`SIGTERM`/`SIGINT` flush + shutdown handlers |

---

## OTel Isolation

Neatlogs runs on a **private `TracerProvider` and a private active-context store** — it never registers globally, and never adopts or shuts down a foreign global provider. A co-tenant tracer's active span (Datadog, Braintrust, another OTel SDK) can't become a Neatlogs parent, and vice-versa; `trace()`, auto-roots, `log()`, and `isRootSpan()` all resolve the active span from the private store.

- **`tracerProvider`** (init option): pass your own `BasicTracerProvider` — the SDK adds processors + flushes but never registers it globally or shuts it down.
- **`registerShutdownHandlers`** (init option): `beforeExit`/`SIGTERM`/`SIGINT` flush + shutdown; defaults `true` when Neatlogs owns the provider (so scripts drain spans), `false` when you pass `tracerProvider`.
- **`injectTraceContext(carrier)`**: caller-side W3C propagation. Returns `false` if no valid Neatlogs span is active.
- **`extractTraceContext(carrier, fn)`**: callee-side continuation. Runs `fn` under the inbound remote parent in Neatlogs' private context and returns its sync value or Promise. Invalid/missing headers are a fail-open passthrough.

```typescript
import { extractTraceContext, injectTraceContext, trace } from 'neatlogs';
const headers: Record<string, string> = {};
if (injectTraceContext(headers)) await fetch(url, { headers });

await extractTraceContext(request.headers, () =>
  trace({ name: 'remote_work' }, async () => { /* joins caller's trace */ }),
);
```

---

## Trace Output

`setTraceOutput(value)` stamps `neatlogs.trace.output` on the active trace's ROOT span, so the dashboard shows a meaningful output instead of a raw status object (e.g. an agent that suspends awaiting input). No-op outside a trace; never throws.

```typescript
import { trace, setTraceOutput } from 'neatlogs';
await trace({ name: 'turn', sessionId }, async () => {
  const plan = await proposePlan();
  setTraceOutput(plan.title); // show the plan, not the raw status object
});
```

---

## Sessions & End-Users

Track **your app's end-users** and group a conversation's turns so you can analyze usage/cost/errors per customer & segment, view multi-turn timelines, and do per-customer replay.

Model: **one turn = one trace**; a **session** groups the turns of a conversation (pass the same `sessionId` on every turn). The end-user is per session. Identity is stamped on the **trace ROOT only** — the backend rolls it up; child spans ignore these fields. `init()` does **not** accept any session/end-user param.

Three ways to declare identity (per-request):

```typescript
// 1. On a trace() root
await trace({ name: 'turn', sessionId: 'conv_123', endUserId: 'u_456', endUserMetadata: { plan: 'pro' } }, async () => { /* ... */ });

// 2. On a span() root
span({ kind: 'WORKFLOW', sessionId: 'conv_123', endUserId: 'u_456', endUserMetadata: { plan: 'pro' } }, fn);

// 3. Wrapper-only code (no root of your own — you only call neatlogs.wrap(...))
await identify({ sessionId: 'conv_123', endUserId: 'u_456', endUserMetadata: { plan: 'pro' } }, async () => {
  await client.chat.completions.create(/* ... */); // the LLM root inherits the identity
});
```

Lineage uses `parentSessionId`; application-defined fields use one arbitrary `sessionCustomFields` object:

```typescript
await identify({
  sessionId: 'child_123',
  parentSessionId: 'parent_456',
  sessionCustomFields: { feature_name: 'chat', entry_point: 'slack', tenant: 'acme' },
}, runTurn);
```

Never hardcode a custom key as a new SDK option. Custom fields are encoded under `neatlogs.session.custom_fields`.

For retrieval spans, always emit the canonical `neatlogs.retriever.*`
namespace. `neatlogs.retrieval.*` is an ingestion-only legacy alias.

> **Browser SDK** (`neatlogs/browser`) uses the same field names — `endUserId`, `endUserMetadata`, `sessionId` — as client-constructor defaults or per-call on `trace()` / `trackAI()`.

---

## Supported Instrumentations

**There is no `instrumentations: [...]` path in the TypeScript SDK.** Each library gets an explicit helper you attach to the object yourself. This is the ONLY supported mechanism.

| Library | Helper | Import from |
|---|---|---|
| `openai` | `wrapOpenAI(client)` | `neatlogs` or `neatlogs/openai` |
| `@anthropic-ai/sdk` | `wrapAnthropic(client)` | `neatlogs` or `neatlogs/anthropic` |
| Azure OpenAI | `wrapAzureOpenAI(client)` | `neatlogs/azure-openai` |
| `@aws-sdk/client-bedrock-runtime` | `wrapBedrock(client)` | `neatlogs/bedrock` |
| `@google/genai` (Gemini / AI Studio, `provider=google`) | `wrapGoogleGenAI(client)`, `wrapGoogleGenAIChat(chat)` | `neatlogs/google-genai` |
| `@google/genai` in Vertex mode (`provider=vertex_ai`) | `wrapVertexAI(client)`, `wrapVertexAIChat(chat)` | `neatlogs/vertex-ai` |
| OpenRouter | `wrapOpenRouterAgent(client)`, `wrapCallModel(fn)` | `neatlogs/openrouter-agent` |
| Vercel AI SDK (`ai`) | `wrapAISDK(ai)` | `neatlogs/ai` |
| Mastra | `wrapMastra(entity)`, `wrapMastraRerank(fn)` | `neatlogs/mastra` |
| `@anthropic-ai/claude-agent-sdk` | `wrapClaudeAgentSDK(sdk)` | `neatlogs/claude-agent-sdk` |
| `@langchain/core` (covers LangGraph) | `langchainHandler()` → `config.callbacks` | `neatlogs` or `neatlogs/langchain` |
| OpenAI Agents SDK | `openaiAgentsProcessor()` → `addTraceProcessor()` | `neatlogs` |
| Strands / Pi agents | `strandsHooks(agent)` / `piAgentHooks(agent)` | `neatlogs` |
| OpenCode | `NeatlogsOpencodePlugin` | `neatlogs/opencode` |

The direct provider wrappers (`wrapOpenAI`, `wrapAnthropic`, `wrapAzureOpenAI`, `wrapBedrock`, `wrapGoogleGenAI`, `wrapVertexAI`, `wrapOpenRouterAgent`) keep a parentless `LLM` as the trace root. A standalone non-root provider or manual operation receives one automatic `WORKFLOW` parent. Framework helpers root themselves.

### Why the instrumentations key was removed

Global OpenInference/OTel-contrib instrumentors create and activate spans on process-global context, which a private Neatlogs provider cannot isolate in either direction. The TypeScript SDK therefore has no public `instrumentations` option or runtime registry. A compatibility guard rejects the removed property before initialization and points to explicit per-instance helpers:

```
The "openai" auto-instrumentation uses the global OpenTelemetry context and cannot
guarantee isolation from other tracing SDKs (Datadog, etc.).

Use wrapOpenAI() from 'neatlogs/openai' for isolated tracing. Neatlogs does not
support shared global-context instrumentation.
```

No provider/framework key is accepted, including formerly advertised no-op keys. Python retains a limited fallback `instrumentations=[...]` path for uncovered providers; do not port that list into TypeScript.

> **HTTP auto-instrumentation** (fetch/undici) is always enabled by `init()` for trace context propagation — nothing to configure.

---

## Reference Docs

For deep dives, see the companion reference files:

- **Custom instrumentation** with `span()`, `Span()`, and `trace()` → [`references/decorators-and-traces.md`](references/decorators-and-traces.md)
- **Raw HTTP LLM calls** (fetch/undici/axios — wrappers are BLIND, need manual spans; streaming lifecycle + per-provider field paths) → [`references/raw-http-llm.md`](references/raw-http-llm.md)
- **Framework-specific** integration patterns → [`references/framework-integrations.md`](references/framework-integrations.md)
- **Troubleshooting** and common mistakes → [`references/troubleshooting.md`](references/troubleshooting.md)
- **Multiple independent workflows in one codebase** (a copilot + a summarizer + a background job, each a distinct dashboard workflow) → use the `neatlogs-multi-workflow` skill. `workflowName` on `init()` is process-wide/single-shot; give each feature its own `WORKFLOW` root via `trace({ name, kind: 'WORKFLOW', attributes: { 'neatlogs.workflow.name': ... } }, …)`.

---

## Environment Variables

| Variable | Description |
|---|---|
| `NEATLOGS_API_KEY` | API key (alternative to `apiKey` param) |
| `NEATLOGS_DISABLE_EXPORT` | Set to `"true"` to disable span export |

---

## Data Masking and PII

NeatLogs supports both client-side and server-side PII redaction.

### Client-Side Masking

Provide a `mask` callback to `init()` to redact sensitive data before spans leave the process. You can also pass `mask` per-span via `span({ mask: fn })` or `trace({ mask: fn })`.

```typescript
import { init } from 'neatlogs';
import type { MaskFunction } from 'neatlogs';

const redactPii: MaskFunction = (spanData) => {
  for (const key of Object.keys(spanData)) {
    if (key.includes('email') || key.includes('password')) {
      spanData[key] = '[REDACTED]';
    }
  }
  return spanData;
};

await init({ mask: redactPii });
```

### Server-Side PII Redaction

Enable automatic server-side redaction:

```typescript
await init({
  piiEnabled: true,
});
```

---

## Documentation

Full documentation: [https://docs.neatlogs.com/](https://docs.neatlogs.com/)
