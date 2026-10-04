---
name: neatlogs-ts-openai
description: Use when adding neatlogs observability to a TypeScript/Node.js project that calls LLM provider SDKs directly (OpenAI, Anthropic, Google GenAI, Bedrock) and uses no agent framework.
metadata:
  author: neatlogs
  language: typescript
  framework: openai
---

# Neatlogs TypeScript Setup — Direct LLM SDK (OpenAI / Anthropic / Google / Bedrock)

This project calls an LLM provider SDK directly (no agent framework). Neatlogs instruments supported providers with an **explicit `wrap*` helper applied to the client instance**. The wrapper is the sole owner of each provider LLM span. Add `span()` only around your own multi-step orchestration; use a manual `trace({ kind: 'LLM' })` only for an unsupported/raw LLM call that has no wrapper, handler, hook, processor, or instrumentor.

> **`init({ instrumentations: [...] })` throws.** Every provider key is rejected — the underlying instrumentors drive the **global** OpenTelemetry context, which Neatlogs' private provider cannot isolate from a co-tenant tracer (Datadog, etc.). The thrown error names the helper to use instead. Older guidance offered the key as a zero-touch path — that is gone.

## Core mechanism

1. `await init({ apiKey })` once at startup — with NO `instrumentations` key.
2. Wrap each provider client at its construction site: `const client = wrapOpenAI(new OpenAI())`.
3. Call the wrapped client normally. Optionally use `span({ kind: 'WORKFLOW' }, fn)` to group a multi-step user-facing feature. Do **not** add `trace({ kind:'LLM' })` around wrapped calls.

## Provider → helper

| SDK | Helper | Import from |
|---|---|---|
| OpenAI | `wrapOpenAI(new OpenAI())` | `neatlogs/openai` |
| Azure OpenAI | `wrapAzureOpenAI(client)` | `neatlogs/azure-openai` |
| Anthropic | `wrapAnthropic(new Anthropic())` | `neatlogs/anthropic` |
| Google GenAI (Gemini / AI Studio) | `wrapGoogleGenAI(new GoogleGenAI({ apiKey }))` | `neatlogs/google-genai` |
| Google GenAI (Vertex mode) | `wrapVertexAI(client)` | `neatlogs/vertex-ai` |
| AWS Bedrock | `wrapBedrock(new BedrockRuntimeClient({}))` | `neatlogs/bedrock` |

All of these are also re-exported from the root `neatlogs` entry. Wrap once, at construction, and use the returned client everywhere — then call it exactly as normal (`gc.models.generateContent(...)`, `client.chat.completions.create(...)`). Because the helpers patch the **instance** and not the module, there is **no import-order rule**: plain static imports are correct and dynamic `import()` buys nothing.

A provider with no helper (Cohere, Groq, Mistral, Ollama, Together, raw `fetch`) is **not** traced — instrument those calls with a manual `trace({ kind: 'LLM' })` span.

## Steps

1. **Install** → `references/1-install.md`
2. **Add init() + wrap the client** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Wrap multi-step orchestration; verify provider calls are not double-wrapped** → `references/4-spans-and-traces.md`
5. **Lifecycle (flush/shutdown)** → `references/5-lifecycle.md`

## Rules (apply to ALL steps)

- `await init(...)` runs once at startup. Import order does NOT matter — the helpers patch the client instance, so static imports of the LLM SDK are fine and no dynamic `import()` is needed.
- NEVER pass `instrumentations: [...]` to `init()` — it **throws** for every provider key. Wrap the client instead.
- Every provider client the code constructs must be wrapped; an unwrapped client is silently untraced.
- All lifecycle calls are async: `await init/flush/shutdown`.
- The wrapper captures the provider LLM call (input/output, model, tokens, latency). A parentless LLM is the trace root; no blank WORKFLOW wrapper is added. It is the canonical LLM span.
- NEVER put `trace({ kind:'LLM' })`, `span()`, or another provider/framework instrumentor around a single wrapped call. That creates redundant instrumentation. A WORKFLOW/CHAIN/AGENT span may enclose several wrapped calls to represent real orchestration.
- Use manual `trace({ kind:'LLM' })` only for a provider or raw HTTP call that no supported capture layer owns. Manual spans must record their own input, output, model, usage, and errors.
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

- **Next.js setup (init via dynamic import in instrumentation.ts)** → `references/nextjs.md` — REQUIRED if the project is a Next.js app, else the server 500s with `Can't resolve 'crypto'` and emits no traces.
- Custom span()/trace() deep dive → `references/decorators-and-traces.md`
- Sessions & end-users (per-turn `identify()`) → `references/sessions-and-end-users.md`
- Troubleshooting → `references/troubleshooting.md`
