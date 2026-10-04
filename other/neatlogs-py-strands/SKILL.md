---
name: neatlogs-py-strands
description: Use when adding neatlogs observability to a Python project that uses Strands Agents (imports `strands`, builds a Strands `Agent`).
metadata:
  author: neatlogs
  language: python
  framework: strands
---

# Neatlogs Python Setup — Strands Agents

This project uses **Strands Agents** (`strands.Agent`). Strands **self-instruments** via native OpenTelemetry, and `neatlogs.strands_hooks(agent)` enriches those native spans with input/output so they render fully.

## Core mechanism — init() + strands_hooks(agent)

1. `neatlogs.init()` registers the global tracer provider, so Strands' own OTel spans (invoke_agent, execute_tool, model `chat` calls) flow into neatlogs and the attribute mapper classifies them as AGENT / TOOL / LLM (with token usage).
2. **`neatlogs.strands_hooks(agent)` is REQUIRED** to capture prompt/response **content**. Strands records I/O as OTel span *events* (`gen_ai.user.message`, `gen_ai.choice`, …), which neatlogs doesn't render from events. `strands_hooks()` installs a hook on Strands' telemetry that copies that content onto the span as `input.value`/`output.value` — so LLM/TOOL spans show their actual input/output, not just tokens. Without it you get spans + tokens but **empty I/O**.

```python
import neatlogs
neatlogs.init(api_key=os.getenv("NEATLOGS_API_KEY"), workflow_name="my-app")

from strands import Agent
agent = neatlogs.strands_hooks(Agent(model=model, tools=[...]))   # enables I/O capture
agent("Hello")
```

`strands_hooks()` does NOT create its own spans (Strands' native tracing stays the source of truth) and is idempotent — the hook installs once globally. Combine with `@neatlogs.span` / `neatlogs.trace` / `neatlogs.log` for your own orchestration — the native Strands spans nest under your manual spans.

## Steps

1. **Install** → `references/1-install.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Wrap the agent with strands_hooks() + run it** → `references/4-run-agent.md`
5. **Add @span / trace / log to orchestration** → `references/5-spans-trace-log.md`
6. **Lifecycle (flush/shutdown)** → `references/6-flush-shutdown.md`

## Rules (apply to ALL steps)

- `neatlogs.init()` MUST run BEFORE importing `strands` so the tracer provider is registered before Strands reads it. `load_dotenv()` runs before `init()`.
- Do NOT add `instrumentations=[...]` for Strands — init() + Strands' native OTel is the capture path.
- Wrap EVERY agent with `agent = neatlogs.strands_hooks(agent)` — REQUIRED for input/output content (not just tokens). It installs the I/O hook once (idempotent) and returns the same agent; it does NOT create extra spans.
- Strands native telemetry owns AGENT/LLM/TOOL spans and `strands_hooks()` only enriches them. Do NOT add manual LLM/tool decorators, provider wrappers, or spans around a single `agent(...)` call. Use manual spans only for meaningful surrounding orchestration.
- Strands ships `BedrockModel`; ensure AWS creds + region are set.
- Never hardcode keys/credentials. `import neatlogs` at module top level.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.

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
- Combining with @span/trace/log → `references/5-spans-trace-log.md`
- Span kinds reference → `references/span-kinds.md`
- Sessions & end-users → `references/sessions-and-end-users.md`
