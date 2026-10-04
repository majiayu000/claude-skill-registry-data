---
name: neatlogs-py-setup
description: Use when adding neatlogs observability to a Python LLM/agent project and no framework-specific neatlogs skill matches the stack — i.e. the generic fallback for instrumenting Python apps that call LLMs or run agents.
metadata:
  author: neatlogs
  language: python
---

# Neatlogs Python Setup — Wizard Procedure (generic fallback)

Follow these steps in exact order. Do not skip steps. Each step has a verification check — confirm it passes before moving to the next.

## Prefer a framework-specific skill when one applies

This is the GENERIC procedure. If the project uses a known framework/SDK, use its dedicated skill instead — those teach the exact instrumentation entry point:

| Stack | Skill | Entry point |
|---|---|---|
| Direct OpenAI / Anthropic / Google GenAI | `neatlogs-py-openai` | `neatlogs.wrap(client)` |
| CrewAI | `neatlogs-py-crewai` | `neatlogs.wrap(crew)` |
| Pydantic AI | `neatlogs-py-pydantic-ai` | `neatlogs.wrap(agent)` |
| DSPy | `neatlogs-py-dspy` | `neatlogs.wrap(module)` |
| Agno | `neatlogs-py-agno` | `neatlogs.wrap(agent)` |
| Google ADK | `neatlogs-py-google-adk` | `neatlogs.wrap(runner)` |
| Strands | `neatlogs-py-strands` | native (init only) |
| LangChain / LangGraph | `neatlogs-py-langchain` | `neatlogs.langchain_handler()` |
| OpenAI Agents SDK | `neatlogs-py-openai-agents` | `neatlogs.openai_agents_processor()` |

## Instrumentation model (read first)

Neatlogs instruments LLM/agent calls by **wrapping the client/agent** — not by a global `instrumentations=[...]` list:

- **`neatlogs.wrap(x)`** — auto-detects and patches OpenAI/Anthropic/Google-GenAI clients, CrewAI Crew, Pydantic AI Agent, DSPy module, Agno agent, Google ADK runner. One call per instance. Extra keyword args are stamped on the root WORKFLOW span as `neatlogs.workflow.<key>` (searchable metadata), e.g. `neatlogs.wrap(OpenAI(), route="/api/chat", surface="copilot")` — but session/end-user identity goes through `identify()`, not `wrap()` kwargs.
- **`neatlogs.langchain_handler()`** — LangChain callback handler, passed via `config={"callbacks": [handler]}`.
- **`neatlogs.openai_agents_processor()`** — OpenAI Agents SDK trace processor, registered via `add_trace_processor(...)`.
- **Strands** — self-instruments via native OTel; `init()` alone captures it.
- **`instrumentations=[...]`** — only for providers `wrap()` doesn't cover (Groq, Cohere, Bedrock, Mistral, Together, LiteLLM).

Layer `@neatlogs.span` / `neatlogs.log` only on your own orchestration and custom operations. Never add a manual LLM span on top of a wrapper, callback handler, hook, processor, native framework telemetry, or provider instrumentor.

## Steps

0. **Understand the agentic system first** (read-only; do this before any edits) → `references/understand-first.md`
1. **Install SDK** → `references/1-install-sdk.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Identify and decorate orchestration functions** → `references/4-decorate-functions.md`
5. **Verify exactly one capture owner per LLM call** → `references/5-wrap-llm-calls.md`
6. **Decorate tool functions** → `references/6-decorate-tools.md`
7. **Add flush/shutdown** → `references/7-flush-shutdown.md`

## Rules (apply to ALL steps)

- Import `neatlogs` at module top level, never inside functions.
- `neatlogs.init()` MUST execute BEFORE any LLM library imports and BEFORE the client/agent is constructed/wrapped.
- If `load_dotenv()` exists, it MUST run BEFORE `neatlogs.init()`.
- Never hardcode API keys in source. Use `os.getenv()`.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.
- `@neatlogs.span()` goes BELOW framework decorators (`@retry`, `@app.route`, `@tool`) — closest to `def`.
- Minimal edits only. Add wrap()/handler/decorators + imports. Do not reformat, add comments, or refactor.

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

## Reference (for decision-making during steps 4-6)

- Build the component inventory BEFORE instrumenting → `references/understand-first.md`
- Sessions & end-users (group multi-turn conversations, per-customer analytics) → `references/sessions-and-end-users.md`
- Span kinds and when to use each → `references/span-kinds.md`
- What the wrapper/handler/processor already covers → `references/auto-instrumented.md`
- LLM call patterns across all libraries → `references/llm-call-patterns.md`
- Raw HTTP LLM calls (httpx/requests — wrap() is BLIND, needs manual spans):
  - Per-provider request/response field paths → `references/raw-http-llm-formats.md`
  - Streaming manual-span lifecycle → `references/raw-http-streaming-span.md`
