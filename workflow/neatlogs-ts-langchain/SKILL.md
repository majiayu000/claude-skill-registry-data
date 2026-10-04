---
name: neatlogs-ts-langchain
description: Use when adding neatlogs observability to a TypeScript/Node.js project that uses LangChain or LangGraph (depends on `@langchain/*` / `@langchain/langgraph`).
metadata:
  author: neatlogs
  language: typescript
  framework: langchain
---

# Neatlogs TypeScript Setup — LangChain / LangGraph

This project uses LangChain (`@langchain/*`) or LangGraph (`@langchain/langgraph`). Neatlogs instruments it with **`langchainHandler()`** — a LangChain callback handler you attach via `{ callbacks: [handler] }`. This is the **only** supported path.

> **`init({ instrumentations: ['langchain'] })` throws.** The OpenInference LangChain instrumentor creates and activates spans on the **global** OpenTelemetry context, which Neatlogs' private provider cannot isolate from a co-tenant tracer (Datadog, etc.), so `init()` rejects the key outright with a message pointing at `langchainHandler()`. Older guidance offered it as a zero-touch alternative — that is gone.

## Core mechanism — `langchainHandler()`

Create ONE handler and pass it via `{ callbacks: [handler] }` on the calls you want traced:

```typescript
import { init, langchainHandler, span, flush, shutdown } from 'neatlogs';
import { ChatOpenAI } from '@langchain/openai';

await init({ apiKey: process.env.NEATLOGS_API_KEY, workflowName: 'langchain-app' });

const llm = new ChatOpenAI({ model: 'gpt-4o' });

const handler = langchainHandler();
const res = await llm.invoke('Hello', { callbacks: [handler] });
```

The handler is bound to Neatlogs' private provider, so import order doesn't matter — a static `import` of `@langchain/*` above `init()` is fine.

### LangGraph: attach at the GRAPH invocation — NOT the per-node model call

For LangGraph, attach the handler at the **graph invocation** (`app.invoke(...)` / `stream` / etc.), not on the per-node `llm.invoke()`. LangGraph fires the per-node `on_chain_start` only on the **graph-level callback manager**, so a handler passed to a single node's model call never sees the node boundaries — you get no node spans and the LLM span orphans to the workflow root (flat, no node hierarchy). Attach once at the graph invocation and each node gets its own span with the LLM nested under it.

```typescript
async function analystNode(state) {
  const response = await llm.invoke(messages);                   // no per-node handler
  return { messages: [response] };
}
// ✅ attach at the graph invocation — nodes + nested LLMs all get spans
await app.invoke(state, { callbacks: [handler] });               // graph level ✅
// NOT: await llm.invoke(messages, { callbacks: [handler] });    // per-node ❌ (no node spans, LLM orphans)
```

(Plain LangChain — LCEL chains / bare `llm.invoke()` — is the opposite: attach per model/chain call as in the example above. The graph-level rule is LangGraph-specific.)

## What the handler captures (DO NOT manually wrap)

- Chat-model / LLM calls → LLM span (model, tokens, latency)
- Chain / node execution → CHAIN span
- LangChain tools → TOOL span
- Retrievers → RETRIEVER span

## Steps

1. **Install** → `references/1-install.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Attach the handler; optionally add an app-owned WORKFLOW** → `references/4-add-workflow.md`
5. **Lifecycle (flush/shutdown)** → `references/5-lifecycle.md`

## Rules (apply to ALL steps)

- `await init(...)` runs once at startup. Import order does NOT matter — the handler binds to Neatlogs' private provider per call, so a static `import` of `@langchain/*` is fine (no dynamic `import()` needed).
- NEVER pass `instrumentations: ['langchain']` to `init()` — it **throws**. The callback handler is the only path.
- Create ONE `langchainHandler()` and pass it via `{ callbacks: [handler] }`. For plain LangChain (LCEL chains / bare model calls) attach per model/chain call. For LangGraph attach at the graph invocation (`app.invoke(..., { callbacks: [handler] })`), NOT the per-node `llm.invoke()`.
- The handler self-roots a parentless supported run. Add at most one app-owned `span({ kind:'WORKFLOW' })` only when the user-facing entry performs meaningful pre/post work or coordinates multiple runs.
- NEVER wrap individual chains, graph nodes, LangChain tools, or `llm.invoke()` with `span()`/`trace()` — they are auto-traced by the handler; manual wrapping duplicates.
- All lifecycle calls are async. Never hardcode API keys — use `process.env`.
- For EU projects, set `endpoint: 'https://eu.ingest.neatlogs.com'` in `init()`; for other managed projects, omit `endpoint`, `baseUrl`, and `NEATLOGS_ENDPOINT`.

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

## Reference

- **Next.js setup (init via dynamic import in instrumentation.ts)** → `references/nextjs.md` — REQUIRED if the project is a Next.js app.
- Custom span()/trace() (rare here) → `references/decorators-and-traces.md`
- Sessions & end-users (per-turn `identify()` wrapper-only) → `references/sessions-and-end-users.md`
- Troubleshooting → `references/troubleshooting.md`
