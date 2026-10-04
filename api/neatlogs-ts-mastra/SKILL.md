---
name: neatlogs-ts-mastra
description: Use when adding neatlogs observability to a TypeScript/Node.js project that uses the Mastra framework (depends on `@mastra/core`, builds a Mastra agent/workflow).
metadata:
  author: neatlogs
  language: typescript
  framework: mastra
---

# Neatlogs TypeScript Setup — Mastra

This project uses **Mastra** (`@mastra/core`). Neatlogs instruments it with **`wrapMastra()` from `neatlogs/mastra`** — you wrap each Mastra entity (agent, workflow, vector store, memory) once, and neatlogs captures the full nested trace tree.

## Core mechanism — `wrapMastra(entity)`

`wrapMastra` patches the entity's own methods and emits OpenTelemetry spans, owning the capturing layer (same philosophy as `wrapAISDK` for the Vercel AI SDK). It needs **no extra packages** (`@mastra/observability` / `@neatlogs/instrumentation-mastra` are NOT required) and works on **standalone entities** created with `new Agent({...})` — no root `Mastra` instance needed.

Wrapping an entity produces a full nested span tree:

| You wrap | Parent span | Nested children |
|----------|-------------|-----------------|
| `Agent` (`.generate()` / `.stream()`) | **AGENT** | **LLM** (each model step, incl. streaming `doStream`), **TOOL** (each tool `execute`) |
| `Workflow` (`.createRun().start()`) | **WORKFLOW** | step spans |
| `MastraVector` (`.query` / `.upsert`) | **RETRIEVER** (query) / **VECTOR_STORE** (writes) | — |
| `MastraMemory` (`.recall` / `.saveMessages` …) | **CHAIN** | — |
| root `Mastra` | proxy — wraps every agent/workflow it hands out | delegates |

Plus `wrapMastraRerank(rerank)` for the `@mastra/rag` `rerank()` function → **RERANKER** spans.

## Steps

1. **Install** → `references/1-install.md`
2. **Add init() + wrapMastra** → `references/2-init-and-wrap.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Verify: wrap every entity, don't double-wrap** → `references/4-verify.md`
5. **Lifecycle (flush/shutdown)** → `references/5-lifecycle.md`

## Rules (apply to ALL steps)

- `await init(...)` MUST run BEFORE any `import` of `@mastra/core` or the LLM provider SDKs. Use **dynamic `import()`** for them AFTER init.
- `wrapMastra` captures the LLM call itself (at the agent's resolved model), so you do NOT wrap providers separately — agents using `openai/…`, `anthropic/…`, `google/…`, or `bedrock/…` models all work with just `wrapMastra(agent)`. NEVER pass `instrumentations: [...]` — `init()` **throws** for `'mastra'` and for every provider key. If the same app ALSO calls a provider SDK DIRECTLY outside Mastra (e.g. a raw `openai.chat.completions.create()` helper), wrap that client explicitly with `wrapOpenAI(new OpenAI())`; it never duplicates Mastra-routed spans.
- Call `wrapMastra()` on EACH entity you want traced (agent, workflow, vector store, memory) — or wrap the root `Mastra` instance once to cover all agents/workflows it exposes.
- USE the wrapped reference. `wrapMastra` patches in place AND returns the entity, so `const agent = wrapMastra(rawAgent)` then call `agent.generate(...)`.
- Tool definitions must use the Mastra 1.x signature `execute: async (inputData, context) => ...` — the input fields are on the FIRST argument. The old `({ context }) => ...` form is broken on `@mastra/core >= 1.0`.
- Do NOT manually wrap Mastra methods in `span()`/`trace()` on top of `wrapMastra` — that double-traces.
- All lifecycle calls are async: `await init()`, `await flush()`, `await shutdown()`.
- Never hardcode API keys — use `process.env`.
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

- **Next.js setup (init via dynamic import in instrumentation.ts)** → `references/nextjs.md` — REQUIRED if the Mastra app runs inside Next.js, else the server 500s with `Can't resolve 'crypto'` and emits no traces.
- Full span coverage matrix (entities → kinds → attributes, multi-provider, streaming) → `references/span-coverage.md`
- Custom span()/trace() (only for non-Mastra code) → `references/decorators-and-traces.md`
- Sessions & end-users (wrapper-only `identify()` per turn) → `references/sessions-and-end-users.md`
