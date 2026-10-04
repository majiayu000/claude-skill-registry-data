---
name: neatlogs-py-crewai
description: Use when adding neatlogs observability to a Python project that uses CrewAI (imports `crewai`, builds a Crew/Flow with agents and tasks).
metadata:
  author: neatlogs
  language: python
  framework: crewai
---

# Neatlogs Python Setup — CrewAI

This project uses CrewAI. Neatlogs instruments it with **`neatlogs.wrap(crew)`** — wrap the Crew (or Flow, or standalone Agent) instance once and the full span hierarchy is auto-traced.

## Core mechanism — `neatlogs.wrap(crew)`

`neatlogs.wrap()` detects the CrewAI Crew/Flow/Agent and patches every run entrypoint, the crew's agents and tasks, plus installs class-level hooks on the tool dispatch paths (`BaseTool.run` AND `CrewStructuredTool.invoke`) and `LLM.call`. Span tree:

```
WORKFLOW  crew.kickoff()
  ↳ AGENT   each agent's task execution
  ↳ TOOL    each tool call (BaseTool.run OR CrewStructuredTool.invoke)
  ↳ LLM     LLM.call (the underlying model request)
```

Covered entrypoints: `kickoff` / `kickoff_async` / `akickoff` / `kickoff_for_each` / `kickoff_for_each_async` / `akickoff_for_each`, plus `train` / `test` / `replay`. Flows: `flow.kickoff` / `kickoff_async` / `akickoff`.

**No provider pairing.** Older guidance paired `"crewai"` with a provider instrumentor (`"openai"`, `"anthropic"`, …) to get LLM spans. Neatlogs patches `LLM.call` directly, so LLM spans are captured regardless of the model backend — never match a provider key to the model string.

**`wrap()` vs `instrumentations=["crewai"]`.** Both install the SAME class-level hooks (`Crew.kickoff`, `Task`, `Agent`, `BaseTool.run`, `LLM.call`), so either one gives a bare crew a full tree. Prefer `wrap(crew)` — it additionally binds workflow metadata and is required for **Flows** and **standalone Agents**, which are routed per instance and NOT covered by the key alone. Passing the key is not an error.

`wrap()` also auto-suppresses CrewAI's own built-in telemetry (the no-I/O `Crew Created` / `Task Created` / `Flow Creation` lifecycle spans), so those don't pollute your traces.

Combine with `@neatlogs.span` / `neatlogs.trace` / `neatlogs.log` for your own orchestration; the crew spans nest under them.

## Standalone Agents (no Crew)

`wrap()` also handles a standalone agent run — `agent.kickoff(messages=...)` with no Crew. Wrap the agent before kicking it off:

```python
agent = neatlogs.wrap(Agent(role="...", goal="...", backstory="...", tools=[...]))
result = agent.kickoff(messages="What is 2+2?")
```

Emits an `AGENT` span (`crewai.agent.<role>`) capturing the `messages` input, with tool/LLM calls nested under it.

## Tools are auto-traced — do NOT add manual tool spans

`wrap()` traces tool calls on BOTH dispatch paths — `BaseTool.run` (for `BaseTool` subclasses) and `CrewStructuredTool.invoke` (for `@tool` function tools) — on every supported crewai version (0.130.x through 1.15.x). This is NOT version-dependent. Leave plain action tools undecorated: adding `@neatlogs.span` or a manual `trace(kind="TOOL")` inside a plain tool produces a DUPLICATE span. A tool body may contain a distinct custom operation the wrapper does not capture—for example, a `RETRIEVER` child for custom search or an `EMBEDDING` child for a custom embedder. Step 7 covers this.

## What you MUST do

1. `crew = neatlogs.wrap(crew)` on the Crew/Flow/Agent instance before its run entrypoint (`kickoff` / `train` / `agent.kickoff` / …).
2. (Recommended) Add `@neatlogs.span(kind="WORKFLOW")` on YOUR user-facing function that builds + kicks off the crew, so your orchestration code is the trace root and the crew nests under it.

## Steps

1. **Install SDK** → `references/1-install-sdk.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Wrap the Crew with neatlogs.wrap()** → `references/4-wrap-crew.md`
5. **Add a WORKFLOW span on your entry point** → `references/5-add-workflow.md`
6. **Tools — auto-traced; what NOT to add** → `references/7-verify-tools.md`
7. **Add flush/shutdown** → `references/8-flush-shutdown.md`

## Rules (apply to ALL steps)

- `neatlogs.init()` MUST execute BEFORE any crewai / LLM library imports.
- If `load_dotenv()` exists, it MUST run BEFORE `neatlogs.init()`.
- Instrument via `wrap(crew)`, not `instrumentations=[...]` — it captures agents/tasks/tools/LLM AND binds workflow metadata, and it is the only path that covers Flows / standalone Agents. (`instrumentations=["crewai"]` is a valid key that installs the same class hooks; if a project already has it, leave it — just add the `wrap()`.)
- Wrap the Crew/Flow instance: `crew = neatlogs.wrap(crew)`. Returns the same instance.
- Never hardcode API keys in source. Use `os.getenv()`.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.
- Add imports ONLY for what a file uses:
  - File calls `neatlogs.wrap(...)`/`neatlogs.span(...)`/`neatlogs.trace(...)` → add `import neatlogs`.
- `@neatlogs.span()` goes BELOW framework decorators, closest to `def`.
- Minimal edits only. Add wrap()/decorators + imports. Do not reformat or refactor.
- NEVER add `@neatlogs.span()` to `@tool` functions, Agent definitions, or Task definitions — `wrap()` traces them.
- NEVER add a manual `with neatlogs.trace(kind="TOOL")` inside a plain tool body — `wrap()` already emits a TOOL span, so this DUPLICATES it. Add a child semantic span only for a distinct unsupported/custom operation (`RETRIEVER` for search, `EMBEDDING` for embedding), never as another record of the tool itself (Step 7).

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
- Sessions & end-users → `references/sessions-and-end-users.md`
