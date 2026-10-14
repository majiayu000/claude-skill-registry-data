---
name: 02b-typescript-tracing
description: >
  Use when adding MLflow tracing to a Node/TypeScript GenAI agent. Covers the
  official `mlflow-tracing` and `mlflow-openai` npm packages: `mlflow.init()`,
  `tracedOpenAI`, manual `mlflow.trace`/`@mlflow.trace`/`mlflow.withSpan`,
  nested spans, sessions/users, and when to choose a custom OTLP fallback.
  Foundation Step 2b.
  Sibling to the Python tracing skill (Foundation Step 2). Consumes the MLflow
  environment from Step 1.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Node/TypeScript tracing via the `mlflow-tracing`/`mlflow-openai` npm packages — no deployed resource; identical on both clients. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.0.0"
  domain: "genai-agents"
  pipeline_position: "F2b"
  consumes: "mlflow_environment"
  produces: "ts_tracing_config"
  grounded_in: "docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/typescript-sdk, docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation, docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing"
---

# TypeScript / Node tracing with `mlflow-tracing`

## When to Use

Use this skill when:

- Your agent runs in **Node.js / TypeScript** (Databricks Apps with an
  AppKit/Express/Hono backend, AppKit-integrated agents, custom Node services).
- You want **first-class MLflow trace shapes** matching the Python SDK
  (same span types, same `gen_ai.*` attributes, same UI affordances).
- You want **automatic** tracing for OpenAI-compatible clients (Foundation
  Models, Azure OpenAI, etc.) the same way `mlflow.openai.autolog()` works
  in Python.

**Pick a custom OTLP path instead only when**:

- You already operate an OpenTelemetry collector and want vendor-neutral spans.
- You instrument multiple services and prefer one OTel exporter pipeline.
- The `mlflow-tracing` npm package does not yet cover a hook you need.

In every other Node case, **prefer this skill**. It is the canonical
Node tracing path and matches the [Databricks TypeScript SDK guide](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/typescript-sdk).

Prerequisites:

- Foundation Step 1 (MLflow environment, tracking URI, auth) — applies
  to Node too. See [`01-mlflow-genai-foundation`](../01-mlflow-genai-foundation/SKILL.md).
- An MLflow experiment id (Python or REST). The Node SDK does **not**
  create experiments — it only writes traces into an existing one.

## Install

```bash
npm install mlflow-tracing
# Add the OpenAI autolog wrapper if you call OpenAI / Foundation Models / Azure OpenAI directly
npm install mlflow-openai
```

The `mlflow-tracing` package is the core SDK (`mlflow.init`,
`mlflow.trace`, `mlflow.withSpan`, `mlflow.startSpan`,
`mlflow.update_current_trace`). The `mlflow-openai` package adds the
`tracedOpenAI` helper that wraps an `OpenAI` client so every
`chat.completions.create(...)` call becomes an auto-traced span.

> **Pin the version.** Like the Python SDK, the npm packages evolve with
> each MLflow minor release. Pin `mlflow-tracing` and `mlflow-openai` in
> `package.json` and review release notes when bumping.

## Initialize

Call `mlflow.init` **once at process startup**, before any LLM call:

```ts
import * as mlflow from "mlflow-tracing";

mlflow.init({
  trackingUri: "databricks",
  experimentId: process.env.MLFLOW_EXPERIMENT_ID!,
});
```

The SDK reads Databricks credentials from environment variables (same as
the Python SDK):

| Variable | Purpose |
|---|---|
| `DATABRICKS_HOST` | Workspace URL (e.g. `https://my-workspace.cloud.databricks.com`) |
| `DATABRICKS_TOKEN` | PAT for the calling identity (user PAT in dev, SP PAT or OAuth in prod) |
| `MLFLOW_EXPERIMENT_ID` | Experiment id where traces should land |

For **Databricks Apps**, the host is auto-injected; pass the SP token
(or use the OBO `x-forwarded-access-token` for per-user attribution if
the SDK supports it in your version). Set `MLFLOW_EXPERIMENT_ID` in
`app.yaml`. See [`references/prod-tracing-deployment.md`](../02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md)
for the full env-var matrix.

For **AppKit** projects, the standard pattern is to lift Databricks env
vars from the AppKit runtime and pass them through to your Node server —
the same way you already do for the model client.

## Automatic tracing — `tracedOpenAI`

The Node equivalent of `mlflow.openai.autolog()`:

```ts
import OpenAI from "openai";
import { tracedOpenAI } from "mlflow-openai";

const client = tracedOpenAI(
  new OpenAI({
    apiKey: process.env.DATABRICKS_TOKEN, // or per-user OBO token
    baseURL: `${process.env.DATABRICKS_HOST}/serving-endpoints`,
  }),
);

const resp = await client.chat.completions.create({
  model: "databricks-claude-sonnet-4-6",
  messages: [{ role: "user", content: "Hello" }],
});
```

Every `chat.completions.create(...)` (and `responses.create(...)`,
embeddings, etc.) call now produces an LLM span with token counts,
latency, model id, and request/response messages — no manual
instrumentation.

Use the same `client` everywhere in your codebase. `tracedOpenAI` is a
transparent proxy; it has the same TypeScript types as the underlying
`OpenAI` instance.

## Manual tracing

### `mlflow.trace(fn, options)` — wrap a function

The function-wrapping form is the closest equivalent to Python's
`@mlflow.trace`:

```ts
import * as mlflow from "mlflow-tracing";

async function classifyIntent(query: string) {
  const resp = await client.chat.completions.create({
    model: "databricks-claude-sonnet-4-6",
    messages: [{ role: "user", content: query }],
  });
  return resp.choices[0].message.content;
}

const tracedClassifyIntent = mlflow.trace(classifyIntent, {
  name: "classify_intent",
  spanType: "AGENT",
});

// use tracedClassifyIntent everywhere instead of classifyIntent
```

### `@mlflow.trace` decorator (TS 5.0+)

If your project enables TypeScript 5.0 stage-3 decorators, you can
decorate class methods directly:

```ts
import * as mlflow from "mlflow-tracing";

class SkyloyaltyAgent {
  @mlflow.trace({ name: "answer", spanType: "AGENT" })
  async answer(question: string) {
    return this._planAndExecute(question);
  }

  @mlflow.trace({ name: "plan_and_execute", spanType: "CHAIN" })
  private async _planAndExecute(q: string) {
    /* ... */
  }
}
```

Enable stage-3 decorators in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "experimentalDecorators": false
  }
}
```

### `mlflow.withSpan(...)` — block scope

For inline blocks where wrapping or decorating doesn't fit:

```ts
import * as mlflow from "mlflow-tracing";

await mlflow.withSpan(
  { name: "retrieve_context", spanType: "RETRIEVER" },
  async (span) => {
    span.setInputs({ query });
    const docs = await vector.search(query);
    span.setOutputs({ docCount: docs.length });
    return docs;
  },
);
```

`withSpan` opens a child of the current trace, runs the callback, and
closes the span on return or throw. Inputs/outputs/attributes can be
set via the `span` argument.

### Explicit `startSpan` / `span.end`

For long-running spans that don't fit a single async callback (e.g. a
streaming SSE response that finishes incrementally):

```ts
const span = mlflow.startSpan({ name: "stream_response", spanType: "LLM" });
span.setInputs({ prompt });

try {
  for await (const chunk of stream) {
    /* push to client */
  }
  span.setOutputs({ status: "ok" });
} catch (err) {
  span.setOutputs({ status: "error", error: String(err) });
  throw err;
} finally {
  span.end();
}
```

Match every `startSpan` with a `span.end()` (typically in `finally`) or
the trace will hang open in the UI.

## Nested spans

Nested spans work the same as Python: any span opened inside another
becomes a child:

```ts
const computeArea = mlflow.trace(
  async (radius: number) => {
    return mlflow.withSpan({ name: "square", spanType: "FUNCTION" }, () => {
      return Math.PI * radius * radius;
    });
  },
  { name: "compute_area", spanType: "FUNCTION" },
);

await computeArea(2);
// Trace tree:
//   compute_area  (FUNCTION)
//     └─ square   (FUNCTION)
```

This is the canonical way to compose your agent: one `@mlflow.trace`
parent per logical step, with auto-traced LLM/tool calls as children.

## Sessions and users

Group conversational turns under one **session** and attribute each turn
to a **user** by tagging the current trace:

```ts
import * as mlflow from "mlflow-tracing";

mlflow.update_current_trace({
  session_id: req.headers["x-session-id"] as string,
  user_id: resolvedUserId,
});
```

In the MLflow UI, traces grouped by `session.id` show as a single
conversation; `user.id` enables per-user filtering and feedback
attribution. The TS SDK's `session_id` / `user_id` shorthand keys map
to the same reserved MLflow **metadata** fields (`mlflow.trace.session`
/ `mlflow.trace.user`) that Python writes via
`mlflow.update_current_trace(metadata=...)`.

Call this **inside** an active trace (typically in your `/chat` route
handler, after you've opened the request span). The same pattern, plus
the auto-populated environment metadata (`mlflow.source.type` override
from `APP_ENVIRONMENT`, `agent_version`, `deployment_id`, etc.), is
documented language-agnostically in
[F2c — Trace context and environments](../02c-trace-context-and-environments/SKILL.md).

## Pairing with end-user feedback

End-user thumbs-up/down lives in [`sdlc/04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md).
The Node side returns the **trace id** to the frontend so feedback can
attach to the right trace:

```ts
import * as mlflow from "mlflow-tracing";

app.post("/chat", async (req, res) => {
  const result = await tracedAnswer(req.body.question);

  // Read the trace id of the just-finished root span
  const traceId = mlflow.getCurrentTraceId();

  res.json({ answer: result, traceId });
});
```

The frontend echoes `traceId` back on the `/feedback` POST. The Python
contract in [`04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md)
calls `mlflow.log_feedback(trace_id=...)` to attach the assessment.

You can also use **`client_request_id`** for correlation if you need the
frontend to issue a stable id before the backend opens the trace — see
[04c](../../sdlc/04c-end-user-feedback/SKILL.md) for that pattern.

## Relation to the OTLP fallback path

| Aspect | `mlflow-tracing` SDK (this skill, **default**) | Custom OTLP fallback |
|---|---|---|
| Span shape | First-class MLflow (matches Python) | Generic OpenTelemetry spans |
| Auto LLM tracing | `tracedOpenAI` covers OpenAI-compatible clients | Manual or third-party instrumentation |
| Trace UI affordances | Full (gen_ai panes, session grouping, token panes) | Partial (you supply `gen_ai.*` attrs yourself) |
| Setup | One npm package + `mlflow.init` | Multiple `@opentelemetry/*` packages + collector wiring |
| Best for | Node-native Databricks Apps and AppKit agents | Polyglot platforms with an existing OTel collector |

Treat OTLP as an **escape hatch** for environments where the npm SDK isn't an
option. For greenfield Node agents, start here (F2b).

## Validation Checklist

- [ ] `mlflow-tracing` npm package installed and pinned in `package.json`.
- [ ] `mlflow-openai` installed if the agent calls any OpenAI-compatible client (Foundation Models / Azure OpenAI).
- [ ] `mlflow.init({ trackingUri: "databricks", experimentId })` called **once**, at process startup, before the first LLM call.
- [ ] `DATABRICKS_HOST`, `DATABRICKS_TOKEN`, `MLFLOW_EXPERIMENT_ID` set via `app.yaml` / AppKit env wiring.
- [ ] OpenAI client wrapped with `tracedOpenAI(...)` (autolog equivalent).
- [ ] One **`@mlflow.trace`** / `mlflow.trace(...)` parent per request handler so nested LLM/tool spans roll up.
- [ ] `mlflow.update_current_trace({ session_id, user_id })` called per turn for session grouping and user attribution.
- [ ] `traceId` returned to the frontend (`/chat` response) for end-user feedback correlation. See [04c](../../sdlc/04c-end-user-feedback/SKILL.md).
- [ ] Production deployment uses the env-var matrix in [`prod-tracing-deployment.md`](../02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md): `ENABLE_MLFLOW_TRACING`, SP `CAN_EDIT` on the experiment, Git-folder caveat understood.

## Do / Don't

| DO | DON'T |
|---|---|
| Use `tracedOpenAI` for every OpenAI/Foundation Models client. | Hand-instrument every `chat.completions.create` call. |
| Wrap each request handler in **one** `mlflow.trace(...)` parent. | Open a span per request without a parent — traces become orphaned. |
| Set `session_id` and `user_id` once via `update_current_trace`. | Set them as attributes on every child span — wastes storage. |
| Pin `mlflow-tracing` / `mlflow-openai` versions in `package.json`. | Use `latest` — span schema can shift between releases. |
| Return `traceId` to the frontend for feedback correlation. | Force the frontend to guess the trace id from logs. |
| Use the OTLP path only when the `mlflow-tracing` SDK genuinely doesn't fit. | Default to OTLP because it's "more standard" — you lose the MLflow UI affordances. |

## References

### Official documentation

- [Instrument Node.js applications with MLflow Tracing (TypeScript SDK)](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/typescript-sdk) — install, init, `tracedOpenAI`, manual API, sessions.
- [Add traces to applications (overview + decision matrix)](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/) — auto vs manual vs combined.
- [Trace agents deployed on Databricks](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing) — production env vars, Production Monitoring → Delta.
- [`mlflow-tracing` on npm](https://www.npmjs.com/package/mlflow-tracing) — release notes and API surface.
- [`mlflow-openai` on npm](https://www.npmjs.com/package/mlflow-openai) — autolog wrapper.

### Related skills

- [Foundation Step 1: MLflow GenAI Foundation](../01-mlflow-genai-foundation/SKILL.md) — auth and environment detection (applies to Node too).
- [Foundation Step 2: Python tracing](../02-experiment-tracing-and-uc-storage/SKILL.md) — Python sibling, decision matrix, UC OTEL storage.
- [Foundation Step 2c: Trace context and environments](../02c-trace-context-and-environments/SKILL.md) — canonical user / session / environment metadata + `APP_ENVIRONMENT` override (applies to Node and Python).
- [Autolog integrations reference](../02-experiment-tracing-and-uc-storage/references/autolog-integrations.md) — Python autolog equivalents.
- [Production tracing deployment reference](../02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md) — env vars, SP `CAN_EDIT`, Git-folder caveat.
- [`sdlc/04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md) — companion skill for thumbs-up/down logging via `mlflow.log_feedback`.

## Version history

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2026-04-24 | Initial skill: install, `mlflow.init`, `tracedOpenAI`, manual API (`mlflow.trace`, `@mlflow.trace`, `withSpan`, `startSpan`), nested spans, sessions/users, end-user feedback pairing, OTLP-fallback comparison table. |
