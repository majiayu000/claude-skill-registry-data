---
name: neatlogs-py-langchain
description: Use when adding neatlogs observability to a Python project that uses LangChain or LangGraph (imports `langchain*` / `langgraph`, builds chains, runnables, or a graph).
metadata:
  author: neatlogs
  language: python
  framework: langchain
---

# Neatlogs Python Setup — LangChain / LangGraph

This project uses LangChain or LangGraph. Neatlogs offers **two ways** to instrument it:

1. **`neatlogs.langchain_handler()`** — a LangChain callback handler you attach per call via `config={"callbacks": [handler]}`. This is the **recommended, first-class** path (LangChain's own callback system; explicit control over exactly which calls are traced). This skill uses it throughout.
2. **`instrumentations=["langchain"]`** on `init()` — zero-touch auto-instrumentation (OpenInference) that traces LangChain/LangGraph globally without editing call sites. Use this when you can't (or don't want to) thread a handler through your code.

Pick ONE — don't combine them (that double-traces). The rest of this skill shows the handler approach.

## Core mechanism — `neatlogs.langchain_handler()`

Create ONE handler and pass it via `config={"callbacks": [handler]}` on the calls you want traced. The handler emits the span tree from LangChain's callback events:

```
CHAIN  chain / graph execution
  ↳ LLM        chat-model / llm call
  ↳ TOOL       @tool invocation (via ToolNode)
  ↳ RETRIEVER  retriever call
```

```python
import neatlogs
from langchain_openai import ChatOpenAI

handler = neatlogs.langchain_handler()
model = ChatOpenAI(model="gpt-4o")
result = model.invoke("Hello", config={"callbacks": [handler]})
```

### LangGraph: attach at the GRAPH invocation — NOT the per-node model call

For LangGraph, attach the handler at the **graph invocation** (`app.invoke(...)` / `ainvoke` / `stream` / `astream`), not on the per-node `llm.invoke()`. LangGraph fires the per-node `on_chain_start` only on the **graph-level callback manager**, so a handler passed to a single node's model call never sees the node boundaries — you get no node spans and the LLM span orphans to the workflow root (flat, no node hierarchy). Attach once at the graph invocation and each node gets its own span with the LLM nested under it. Do not add manual spans inside nodes.

```python
def analyst_node(state):
    response = llm.invoke(messages)                                    # no per-node handler
    return {"messages": [response]}

# ✅ attach at the graph invocation — nodes + nested LLMs all get spans
app.invoke(state, config={"callbacks": [handler]})                     # graph level ✅
# NOT: llm.invoke(messages, config={"callbacks": [handler]})           # per-node ❌ (no node spans, LLM orphans)
```

The same boundary rule applies asynchronously. An `async def` node should await
`llm.ainvoke(...)` without a per-node callback; attach the handler once to
`await app.ainvoke(..., config={"callbacks": [handler]})` or
`app.astream(..., config={"callbacks": [handler]})`. Do not call synchronous
`invoke()` from an async node, and do not `await app.astream(...)` itself—iterate
it with `async for`.

(Plain LangChain — LCEL chains / bare `model.invoke()` — is the opposite: attach per model/chain call as in the example above. The graph-level rule is LangGraph-specific.)

### Deep Agents (`deepagents`) — prebuilt harness, attach on the top-level invoke

Deep Agents (`from deepagents import create_deep_agent`) is a LangGraph harness — you do NOT write the nodes, so there's no per-node model call to attach to. Pass the handler on the agent's top-level `invoke` / `ainvoke` / `stream`:

```python
handler = neatlogs.langchain_handler()
agent = create_deep_agent(model="openai:gpt-4o-mini", tools=[...], system_prompt="...")
result = agent.invoke(
    {"messages": [{"role": "user", "content": "..."}]},
    config={"callbacks": [handler]},
)
```

For hand-written LangGraph (your own nodes) as well as prebuilt harnesses (Deep Agents), the top-level / graph invocation is the attach point — use it. (Consistent with the graph-level rule above.)

Use a WORKFLOW span and `neatlogs.log` only for your own surrounding orchestration; the handler-owned spans nest underneath. Never add manual LLM, node, chain, tool, or retriever spans for operations the handler captures.

## What the handler captures (DO NOT manually decorate)

- Chat-model / LLM calls → LLM span (model, tokens, latency)
- `@tool` invocations via ToolNode → TOOL span
- Retriever calls → RETRIEVER span
- Chain / node execution → CHAIN span

Token usage is read from both LangChain's standard `usage_metadata` and provider `llm_output.token_usage`, normalized to `neatlogs.llm.token_count.*` across providers — including Gemini (`prompt_token_count` / `candidates_token_count`), cache tokens, and reasoning tokens. Async callbacks (`ainvoke` / `astream`) are supported, and LangGraph node spans use the bare node name (e.g. `researcher`). Nothing to configure.

## Steps

1. **Install SDK** → `references/1-install-sdk.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Create + attach the callback handler** → `references/4-attach-handler.md`
5. **Optionally add an app-owned WORKFLOW for real surrounding orchestration** → `references/5-add-workflow.md`
6. **Verify handler-owned LLM calls are not manually wrapped** → `references/6-wrap-llm-calls.md`
7. **Verify tool functions are untouched** → `references/7-verify-tools.md`
7.5. **Embeddings: decorate ONLY custom ones** → `references/7.5-embeddings.md`
8. **Add flush/shutdown** → `references/8-flush-shutdown.md`

## Rules (apply to ALL steps)

- `neatlogs.init()` MUST execute BEFORE any LangChain library imports.
- If `load_dotenv()` exists, it MUST run BEFORE `neatlogs.init()`.
- This skill uses the **callback handler**; if you go that route, do NOT ALSO pass `instrumentations=["langchain"]` to `init()` — running both double-traces. (`instrumentations=["langchain"]` is a valid standalone alternative — see the intro — just don't combine the two. Provider instrumentors for embeddings are a separate concern — see step 7.5.)
- Create ONE `neatlogs.langchain_handler()` and pass it via `config={"callbacks": [handler]}`. For plain LangChain (LCEL chains / bare model calls) attach per model/chain call. For LangGraph attach at the graph invocation (`app.invoke(..., config={"callbacks": [handler]})`), NOT the per-node `llm.invoke()`.
- Never hardcode API keys in source. Use `os.getenv()`.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.
- Add imports ONLY for what a file actually uses:
  - File calls `neatlogs.langchain_handler(...)` / `neatlogs.span(...)` / `neatlogs.log(...)` → add `import neatlogs`.
- When present, `import neatlogs` goes at module top level, never inside functions.
- `@neatlogs.span()` goes BELOW framework decorators, closest to `def`.
- Minimal edits only. Add the handler + decorators + imports. Do not reformat or refactor.
- NEVER add `@neatlogs.span()` to `@tool` functions or LangGraph node functions.
- The handler self-roots a parentless supported call. Add at most one app-owned `@span(kind="WORKFLOW")` on a user-facing entry only when it performs meaningful pre/post work or coordinates multiple calls. `@span(kind="EMBEDDING")` is added only for a custom embedder (step 7.5).
- NEVER put `neatlogs.trace(kind="LLM")`, `@neatlogs.span`, or another provider instrumentor around `invoke`/`stream`, graph nodes, tools, or retrievers captured by the handler.

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
- Sessions & end-users (per-turn `identify()` for customer analytics) → `references/sessions-and-end-users.md`
