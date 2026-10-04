---
name: neatlogs-ts-pi-agent
description: Use when adding neatlogs observability to a TypeScript/Node.js project that uses maintained `@earendil-works/pi-agent-core` / `@earendil-works/pi-ai` or legacy `@mariozechner` Pi packages, including `Agent`, `AgentHarness`, functional loops, and standalone stream functions.
metadata:
  author: neatlogs
  language: typescript
  framework: pi-agent
---

# Neatlogs TypeScript Setup — Pi Agent

This project uses **Pi Agent** (maintained as `@earendil-works/pi-agent-core`). Neatlogs instruments it with **`piAgentHooks()` from `neatlogs/pi-agent`**. The wrapper also supports legacy `@mariozechner` releases through the same event interface.

## Core mechanism — `piAgentHooks(agent)`

`Agent` exposes `subscribe(listener)` and emits lifecycle events (`agent_*`, `turn_*`, `message_*`, `tool_execution_*`). Neatlogs translates them into spans. For maintained `AgentHarness`, it additionally wraps model-producing `compact()` and summarizing `navigateTree()` operations because those calls occur outside the Agent event loop. There is no import-order rule.

One `agent.prompt()` = **one trace**:

```
AGENT  pi_agent.run                  (agent_start → agent_end)
 ├─ CHAIN pi_agent.turn.1            (turn_start → turn_end)
 │   ├─ LLM  pi_agent.llm.<model>    (message_start → message_end = real provider latency)
 │   └─ TOOL pi_agent.tool.<name>    (tool_execution_start → tool_execution_end)
 └─ CHAIN pi_agent.turn.2            (the post-tool-result turn)
     └─ LLM  pi_agent.llm.<model>
```

| Span | Carries |
|------|---------|
| **AGENT** | run input (first user message), final output, `neatlogs.agent.stop_reason` + `neatlogs.error.message` on an aborted/errored run |
| **CHAIN** | `neatlogs.chain.turn_index`, the message that prompted the turn, the turn's assistant text (or the tool calls it made), `neatlogs.chain.tool_result_count` |
| **LLM** | model / `response_model` / provider / api, input messages, output + `tool_calls.*`, token counts (incl. cache read/write), **exact `cost_usd` from pi-ai's own pricing**, `metrics.ttft_ms`, `is_streaming`, `stop_reason` |
| **TOOL** | tool name, `call_id`, input args, result, `is_error`, `is_streaming` for tools that emit partial updates |

## Steps

1. [Install and check the Pi version](references/1-install.md)
2. [Add `init()` and `piAgentHooks()`](references/2-init-and-wrap.md)
3. [Set environment variables](references/3-set-env.md)
4. [Verify every Agent or harness](references/4-verify.md)
5. [Handle lifecycle and flushing](references/5-lifecycle.md)

## Rules (apply to ALL steps)

- `piAgentHooks` patches the **instance** you pass (it subscribes to it), NOT the module — so **plain static imports are fine**. There is no "init before import" rule for Pi Agent, unlike provider-SDK wrappers.
- USE the wrapped reference. `piAgentHooks` subscribes in place AND returns the agent, so `const agent = piAgentHooks(new Agent({...}))` then call `agent.prompt(...)`.
- Call it on **every** `Agent` instance you want traced. Wrapping is **idempotent** — calling it twice on the same instance is a no-op, so it never double-traces.
- NEVER pass `instrumentations: [...]`. `piAgentHooks` is the sole capture point for Pi-routed model calls; `init()` rejects provider keys.
- Pi calls the model through its `pi-ai` package, not a bare provider SDK, so do **not** also wrap the provider (`wrapOpenAI`, `wrapAnthropic`, …) for Pi-routed calls. Only wrap a provider client the app calls **directly** outside Pi.
- Cost is **not** re-derived from tokens: pi-ai prices each call against its own model registry and neatlogs carries that exact figure through as `neatlogs.llm.cost_usd`.
- Do NOT manually wrap `agent.prompt()` in `span()`/`trace()` on top of `piAgentHooks` — that double-traces. Nesting a wrapped agent INSIDE your own `span()` is fine and correct: the AGENT span parents to it.
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

- [Low-level functional API](references/low-level-api.md) — required for functional loops and standalone stream functions.
- [Full span coverage matrix](references/span-coverage.md) — Agent, AgentHarness, streaming, tools, abort, and state-only methods.
- [Sessions and end-users](references/sessions-and-end-users.md)
- [Custom spans for non-Pi code](references/decorators-and-traces.md)
