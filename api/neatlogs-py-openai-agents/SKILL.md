---
name: neatlogs-py-openai-agents
description: Use when adding neatlogs observability to a Python project that uses the OpenAI Agents SDK (imports `agents` / `openai-agents`, defines `Agent`s and calls `Runner.run`).
metadata:
  author: neatlogs
  language: python
  framework: openai-agents
---

# Neatlogs Python Setup — OpenAI Agents SDK

This project uses the OpenAI Agents SDK (`from agents import Agent, Runner, function_tool, handoff, ...`). Neatlogs instruments it with a **trace processor** — `neatlogs.openai_agents_processor()` registered via `add_trace_processor()`. This is the first-class OpenAI Agents path (the SDK's own tracing-processor protocol).

## Core mechanism — `add_trace_processor(neatlogs.openai_agents_processor())`

The OpenAI Agents SDK emits its own trace/span events. Registering the neatlogs processor maps them to neatlogs spans:

```
WORKFLOW   trace
  ↳ AGENT       agent span (instructions = prompt)
  ↳ LLM         generation / response span
  ↳ TOOL        @function_tool span
  ↳ AGENT       handoff span
  ↳ GUARDRAIL   guardrail span
```

```python
import neatlogs
from agents import add_trace_processor

add_trace_processor(neatlogs.openai_agents_processor())   # register once, before Runner.run()
```

Register the processor ONCE at startup, after `init()` and after importing `agents`. Everything the SDK runs afterward is traced — agents, tools, handoffs, guardrails, and LLM calls — with nothing to wire up per-agent.

Combine with `@neatlogs.span` / `neatlogs.trace` / `neatlogs.log` for your own orchestration; the SDK spans nest under your manual spans.

## What the processor captures (DO NOT manually decorate)

- `Runner.run()` / `Runner.run_sync()` / `Runner.run_streamed()` → the agent run
- Each `Agent` turn (instructions as the system prompt) → AGENT span
- ALL `@function_tool` functions → TOOL span
- Handoffs between agents → AGENT span
- Input/output guardrails → GUARDRAIL span
- Underlying LLM calls → LLM span (model, tokens, prompt)

## Steps

1. **Install SDK** → `references/1-install-sdk.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Register the trace processor** → `references/4-register-processor.md`
5. **Optionally add an app-owned WORKFLOW for real surrounding orchestration** → `references/5-add-workflow.md`
6. **Verify agents/tools/guardrails are untouched** → `references/7-verify-tools.md`
7. **Add flush/shutdown** → `references/8-flush-shutdown.md`

## Rules (apply to ALL steps)

- `neatlogs.init()` MUST execute BEFORE any `agents` / openai imports.
- If `load_dotenv()` exists, it MUST run BEFORE `neatlogs.init()`.
- Do NOT pass `instrumentations=["openai_agents"]` to `init()` — the trace processor is the instrumentation path. Listing it would double-fire spans.
- Register the processor ONCE with `add_trace_processor(neatlogs.openai_agents_processor())` at startup, before the first `Runner.run()`.
- Never hardcode API keys in source. Use `os.getenv()`.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.
- Add imports ONLY for what a file uses: a file that calls `neatlogs.openai_agents_processor(...)` / `neatlogs.span(...)` needs `import neatlogs`; files that only define Agents/tools need NOTHING added.
- `@neatlogs.span()` goes BELOW framework decorators, closest to `def`.
- Minimal edits only. Add the processor registration and imports; add an outer decorator only when the app owns meaningful surrounding orchestration. Do not reformat or refactor.
- NEVER add `@neatlogs.span()` / `@neatlogs.trace()` to:
  - `@function_tool` functions (traced as TOOL)
  - `Agent(...)` definitions or agent factory functions (traced as AGENT)
  - guardrail functions (`@input_guardrail`/`@output_guardrail` or `*_guardrail_fn`) (traced as GUARDRAIL)
  - handoff functions
- The processor owns the underlying LLM spans too. Do NOT wrap the Agents SDK's
  provider client or add a manual `trace(kind="LLM")` around `Runner` calls.
- The processor already creates the canonical `WORKFLOW` root for a standalone `Runner` trace. Add at most one app-owned `@span(kind="WORKFLOW")` on the user-facing `Runner.run()` caller only when that function has meaningful pre/post work or coordinates multiple runs; never add it merely to make a trace render.

## Safety gate

Before any edit, confirm this service is Python. Identify the active interpreter
and package manager from its manifests and lockfiles, then read the declared and
installed SDK version. Do not install or change dependencies during this
inspection. Run Doctor through the active interpreter so it can use only the
installed SDK:

```bash
python -m neatlogs doctor --local --json
```

Do not substitute `npx`, `uvx`, `pipx run`, a Wizard command, or another
downloaded Doctor. Local mode must be read-only and network-free. It requires no
credential and must not change source or configuration. Require
`format_version: "neatlogs.doctor/v2"`, `runtime.language: "python"`, and
`runtime.schema_version: "2"`. Treat `runtime.sdk_version` as evidence of the
installed package, not as an exact-version allowlist.

If the command is missing or its result has the wrong format, language, or
schema, fail closed. Check the canonical package registry for the latest
published stable release. If the project uses an older release, show the exact
upgrade command for the detected package manager and obtain explicit user
approval before running it. Accept newer compatible releases and never
downgrade one. If the installed release is already current but lacks Doctor v2,
stop and give safe manual/support remediation. Rerun local Doctor after any
approved upgrade. Do not edit while this gate is unresolved.

A local `pass` proves only that the installed SDK produced and validated its
controlled in-process envelope. It does not prove that the application is
instrumented, that anything was exported, or that a hosted trace is visible.
Preserve every `reason_code` and `remediation_code` exactly. Treat a warning,
failure, or unknown future code as manual/support remediation unless the code is
explicitly safe/fixable here. The only source fixes allowed by this gate are:

- `INSTRUMENTOR_INACTIVE`: apply only this skill's documented initialization or
  wrapper step.
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

```bash
python -m neatlogs doctor --probe --json
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

- Span kinds → `references/span-kinds.md`
- Sessions & end-users (group turns into conversations, tag your customers' end-users via `neatlogs.identify()`) → `references/sessions-and-end-users.md`
