---
name: google-adk
description: "Building agents with Google ADK (Agent Development Kit): project scaffolding and `root_agent` conventions, LlmAgent parameters, workflow agents (Sequential/Parallel/Loop) and custom BaseAgent orchestration, function tools and `ToolContext`, `McpToolset` and `OpenAPIToolset`, multi-agent collaboration modes and sub-agent delegation, sessions/state prefixes/memory/artifacts, the six lifecycle callbacks, `adk run`/`adk web`/`adk api_server`, `adk eval` metrics and evalset format, deployment via `adk deploy cloud_run`/`agent_engine`/`gke`, the A2A protocol, Live bidi streaming, and the ADK 2.0 graph-workflow migration. WHEN: \"Google ADK\", \"Agent Development Kit\", \"google-adk\", \"adk.dev\", \"adk create\", \"adk web\", \"adk run\", \"adk eval\", \"adk deploy cloud_run\", \"adk deploy agent_engine\", \"root_agent\", \"LlmAgent\", \"SequentialAgent\", \"ParallelAgent\", \"LoopAgent\", \"McpToolset\", \"OpenAPIToolset\", \"ToolContext\", \"output_key\", \"before_model_callback\", \"VertexAiSessionService\", \"GcsArtifactService\", \"Agent Runtime\", \"Agent Engine\", \"RemoteA2aAgent\", \"A2AServer\", \"run_live\", \"LiveRequestQueue\", \"ADK 2.0\", \"graph workflows\", \"com.google.adk\". NOT for: building agents with Anthropic's SDK (`ClaudeAgentOptions`, `createSdkMcpServer`) — use `claude-agent-sdk`; building agents with OpenAI's SDK (`Agent`, `Runner`, handoffs, guardrails) — use `openai-agents-sdk`; the Gemini CLI or any harness-vs-SDK-vs-API architecture choice — use `overview`; the MCP specification, transports, or writing standalone MCP servers — use `mcp`; the Claude Messages API — use `claude-api`; picking a model or tier across vendors — use `model-selection`; authoring SKILL.md Agent Skills — use `agent-skills`; general agent/LLM eval methodology beyond `adk eval` — use `evals`; prompt injection and agent threat modeling — use `ai-security`; sandbox and egress isolation architecture — use `sandboxing`. GKE/Kubernetes runtime depth beyond the ADK deploy path is the containers plugin; BigQuery/data-warehouse depth is the database plugin."
license: MIT
---

# Google ADK (Agent Development Kit)

ADK is Google's open-source framework for building, debugging, and deploying agents — described by the vendor as building "reliable AI agents at enterprise scale." This skill covers building with it: agent types, tools, multi-agent composition, sessions and state, callbacks, evaluation, and the Google Cloud deployment paths.

**Docs domain**: the canonical `https://google.github.io/adk-docs/` now **301-redirects to `https://adk.dev/`** (confirmed 2026-08-05). Send users to `adk.dev`; a stale bookmark still works but the URL in their browser will change.

Corpus fetched 2026-08-05. Where this skill says a detail is unverified, it is genuinely absent from the fetched docs — say so rather than guessing.

## Answering rules

Always establish **which language and which major line** before answering. ADK ships in five languages (Python, TypeScript, Go, Java, Kotlin) but only **Python 2.0 (GA 2026-05-19) and Go 2.0 (GA 2026-06-30)** have reached the 2.0 graph-based line; Java, Kotlin, and TypeScript are still 1.x. A 2.0 answer given to a Java user is wrong.

Always confirm the app defines a module-level **`root_agent`** before debugging "my agent doesn't load". `adk create`, `adk run`, and `adk eval` all resolve the agent through that symbol.

Never propose `adk web` as a production surface. The docs state plainly: "ADK Web is not meant for use in production deployments." Production goes to Agent Runtime, Cloud Run, GKE, or a custom container.

Never leave a `LoopAgent` without a termination mechanism. The docs are explicit that `LoopAgent` does **not** inherently decide when to stop — set `max_iterations` *and* give a sub-agent an escalation path (`tool_context.actions.escalate = True`).

Never assume `ParallelAgent` branches share state. Each sub-agent runs as an independent branch with **no automatic state sharing** and non-deterministic completion order — use distinct `output_key`s plus a downstream synthesis agent (the gather pattern).

Never ship `InMemorySessionService` or `InMemoryArtifactService` to production. Both are documented as development/testing only and lose everything on restart.

Never write a broad `try...except` around agent logic on ADK 2.0 — it masks failures from the framework's automatic retry mechanism. Let exceptions propagate.

Always send a user to the local loop first — `adk run` for a terminal conversation, `adk web` for the dev UI and its interactive eval threshold sliders. That beats reasoning about the agent's behavior from source.

## Install and scaffold

**Python**:

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install google-adk
pip show google-adk                                   # verify
adk create my_agent
```

`adk create` generates `agent.py`, `.env`, and `__init__.py`. The `.env` holds `GOOGLE_API_KEY="YOUR_API_KEY"` for the API-key path.

**Java** — two artifacts: `com.google.adk:google-adk` (library) and `com.google.adk:google-adk-dev` (a Spring Boot server for running agents), both pinned at **1.6.0** in the docs as of 2026-08-05. Gradle builds must pass `-parameters` to `javac` — ADK Java relies on parameter-name reflection.

Minimal Python agent — note the module-level `root_agent`:

```python
from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

root_agent = Agent(
    model='gemini-flash-latest',
    name='root_agent',
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant...",
    tools=[get_current_time],
)
```

Run locally: `adk run my_agent` (CLI chat), `adk web --port 8000` (dev UI at `http://localhost:8000`), `adk api_server` (REST endpoints).

## Agent types

| Type | Control flow | Decided by |
|---|---|---|
| `LlmAgent` / `Agent` | Reasoning loop over tools | The model |
| `SequentialAgent` | Sub-agents in fixed order | Code (deterministic) |
| `ParallelAgent` | Sub-agents concurrently | Code (deterministic) |
| `LoopAgent` | Sub-agents in order, repeated | Code + explicit termination |
| Custom (`BaseAgent` subclass) | Arbitrary | Your code |

`LlmAgent` requires `name` and `model`; the parameters that actually shape behavior are `instruction`, `description` (used by *other* agents to route to this one), `tools`, `output_key` (writes the final response text into session state), `output_schema` / `input_schema`, `generate_content_config`, `include_contents`, `planner`, and `code_executor`.

Instructions support template variables resolved from state: `{var}`, `{artifact.var}` for artifact text, and `{var?}` for an optional variable. Only the `?` form is documented as "missing variable is ignored without error" — use it for anything not guaranteed to be set.

`SequentialAgent` passes the **same `InvocationContext`** to every sub-agent, so state (including `temp:`) flows step to step; that is what makes `output_key` → `{key}` chaining work. `ParallelAgent` does not.

Custom agents subclass `BaseAgent` and implement one async generator method — `_run_async_impl` (Python), `runAsyncImpl` (TypeScript/Java), `Run` (Go) — yielding events. Reach for one only when conditional branching on runtime results, dynamic agent selection, or external calls inside the orchestration itself rule out the built-ins. **On ADK 2.0, agents subclass `BaseNode` and overrides of legacy `_run_async_impl()` are bypassed** — see `references/versions/2.0.md` before porting a custom agent.

Read `references/agents-and-workflows.md` for the full `LlmAgent` parameter table, per-language constructor shapes for all workflow agents, worked pipeline/gather/refinement examples, and the escalation pattern.

## Tools

Any Python function in an agent's `tools` list becomes a tool. ADK derives the schema from the function's **name, docstring, type hints, and defaults** — the docstring is what the model reads, so write full `Args:`/`Returns:` sections.

```python
from google.adk.tools import ToolContext

def get_weather(city: str, unit: str, tool_context: ToolContext) -> dict:
    """
    Retrieves the weather for a city in the specified unit.

    Args:
        city (str): The city name.
        unit (str): The temperature unit, either 'Celsius' or 'Fahrenheit'.
    """
    user_id = tool_context.state.get("user_id")
    return {"status": "success", "report": f"Weather for {city} is sunny."}
```

Rules that change model behavior:

- **Required vs optional** is expressed by the *default*, not by wording — a type hint with no default is required.
- Return a **`dict`**. Non-dict returns are auto-wrapped as `{"result": value}`. Include a `"status"` key (`success`/`error`/`pending`) so the model can tell success from failure.
- A parameter annotated `ToolContext` is **auto-injected and hidden from the model** — only the annotation matters, not the parameter name. Use it for `state`, `actions` (`escalate`, `transfer_to_agent`), and `search_memory`.
- Pass data between tools inside one turn through the **`temp:`** state prefix; tools in a single agent turn share the invocation context.
- Favor few parameters and primitive types; avoid generic names like `do_stuff()`.

**MCP** — `McpToolset` discovers an MCP server's tools, converts their schemas, and proxies calls. Both directions are supported: ADK as MCP client, and exposing ADK tools through a custom MCP server.

```python
McpToolset(connection_params=StdioConnectionParams(server_params=StdioServerParameters(
    command='npx', args=['-y', '@modelcontextprotocol/server-filesystem', '/path/to/folder'])))

McpToolset(connection_params=StreamableHTTPConnectionParams(
    url="https://mapstools.googleapis.com/mcp", headers={'X-Goog-Api-Key': api_key}))
```

Filter with `tool_filter`, bound with `timeout`, stream progress with `progress_callback`. **For Cloud Run and GKE, define the toolset synchronously in `agent.py`** — an async definition is a documented deployment failure mode.

**OpenAPI** — `OpenAPIToolset(spec_str=..., spec_str_type="json")` or `spec_dict=...` parses an OpenAPI v3.x spec and emits one `RestApiTool` per operation; `auth_scheme` + `auth_credential` on the toolset apply to all of them.

**Built-in tools (Google Search, code execution, RAG) are a documented gap here.** The `/tools-custom/` and `/grounding/` pages name them and defer implementation detail to the separate `/integrations/` catalog, which is not in this corpus. State the capability exists — Google Search grounding, grounding with Vertex AI Search, agentic RAG — and send the user to `https://adk.dev/` integrations rather than inventing import paths.

For the MCP protocol itself (spec, transports, OAuth, writing servers) use the `mcp` sibling skill.

Read `references/tools-and-mcp.md` for the full function-tool signature rules, nullable parameters, the complete MCP connection options, and the OpenAPI toolset details.

## Multi-agent composition

Two distinct mechanisms — do not conflate them:

1. **Sub-agent delegation** (in-process). A coordinator `LlmAgent` lists specialists in `sub_agents`; ADK auto-generates a delegation tool and control returns automatically on completion. This is distinct from a manual `transfer_to_agent` call.
2. **A2A** (across the network). Expose an agent as an `A2AServer`, consume a remote one with `RemoteA2aAgent`.

Delegation behavior is governed by the sub-agent's **mode**:

| Mode | User interaction | Return to parent | Notes |
|---|---|---|---|
| `chat` (default) | Full | Manual | Not recommended for structured workflows |
| `task` | Clarifications only | Automatic on `finish_task` | Cannot itself have sub-agents; **disabled in graph workflows** on Python 2.0.0 |
| `single_turn` | None | Automatic on completion | Supports parallel execution of multiple sub-agents |

```python
weather_agent = Agent(name="weather_checker", mode="single_turn",
                      tools=[get_weather, user_info, geocode_address])
coordinator  = Agent(name="travel_planner", sub_agents=[weather_agent, flight_agent])
```

Task-mode and single-turn agents each run in their own **session branch** — parallel agents cannot observe each other's context and the parent receives aggregated results only. Design for that: anything a sibling needs must come back through the parent.

Reach for A2A when integrating standalone services owned by different teams, crossing language/framework boundaries, building microservices, or enforcing a formal contract. Avoid it for internal code organization, high-frequency low-latency calls needing shared memory, or simple helpers — those are local components. ADK's A2A implementation preserves reasoning traces, tracks long-running tools to prevent timeouts, and transfers artifacts.

A **managed agent** is a third thing: an agent whose reasoning, tools, and execution environment are hosted and operated by Google, consumed as a component rather than orchestrated locally.

*Gap*: the dedicated `/agents/routing/` page (LLM-driven transfer, `AgentTool`, `transfer_to_agent` mechanics) is not in this corpus. Answer transfer questions from the mode system above and flag the rest as unverified.

Read `references/agents-and-workflows.md` for collaboration-mode constraints and `references/deployment-and-a2a.md` for the A2A surface and per-language quickstart URLs.

## Sessions, state, memory, artifacts

A `Session` is one ongoing user↔agent interaction: `id`, `user_id`, `state` (mutable dict), `events` (chronological history). Created via a `SessionService` and passed into `runner.run_async()`.

**State prefixes decide lifetime** — this is the single most useful thing to teach:

| Prefix | Scope |
|---|---|
| `temp:` | Current invocation/turn only |
| `user:` | Across all of one user's sessions (needs a persistent `SessionService`) |
| `app:` | Application-wide, all users |
| *(none)* | This session |

`SessionService` implementations: `InMemoryService` (dev/testing), `DatabaseSessionService` (production, database-backed), `VertexAiSessionService` (cloud-managed). Writes like `context.state["key"] = value` are auto-tracked into `EventActions.state_delta` and applied by the service when persisting the event — which is what preserves the audit trail and scope hierarchy. Never mutate persisted state out of band.

`MemoryService` searches historical context and external knowledge, reached from a tool: `tool_context.search_memory("query about topic")`.

**Artifacts** are named, versioned binary data (`google.genai.types.Part` with `inline_data` + `mime_type`), session-scoped by plain filename or cross-session with a `user:` prefix:

```python
version   = await context.save_artifact(filename="report.pdf", artifact=pdf_part)
artifact  = await context.load_artifact(filename="report.pdf")            # latest
artifact  = await context.load_artifact(filename="report.pdf", version=0) # pinned
filenames = await context.list_artifacts()
```

`InMemoryArtifactService` for dev; `GcsArtifactService` for production, with user-level namespacing.

Read `references/sessions-state-artifacts.md` for the service comparison, delta-tracking behavior, artifact versioning/namespacing rules, and use cases.

## Callbacks

Six hook points, each with a documented return contract that is the whole reason to use them:

| Callback | Returning `None` | Returning a value |
|---|---|---|
| `before_agent_callback` | Normal execution | `Content` → skips agent logic, becomes the final response |
| `after_agent_callback` | — | `Content` replaces the agent's output |
| `before_model_callback` | Proceeds with the LLM call | `LlmResponse` → **bypasses the LLM entirely** |
| `after_model_callback` | — | modified `LlmResponse` |
| `before_tool_callback` | Executes the tool | `Dict` → **skips the tool**, used as its result |
| `after_tool_callback` | — | modified tool result `Dict` |

Register them as `LlmAgent` constructor kwargs. Use them for guardrails (validate inputs/outputs, enforce safety rules), caching (`before_model_callback` returning a cached `LlmResponse`), observation/logging, and state management — the documented use cases.

Prefer a callback over prompt wording whenever the user wants a guarantee. `before_tool_callback` returning a dict is an enforced block; an instruction asking the model not to call the tool is not.

Read `references/callbacks-and-runtime.md` for exact signatures, the runtime execution surfaces, and what the runtime sub-pages do and do not cover here.

## Evaluation

```bash
adk eval <AGENT_MODULE_FILE_PATH> <EVAL_SET_FILE_PATH> \
  --config_file_path=test_config.json --print_detailed_results
```

`AGENT_MODULE_FILE_PATH` points at the `__init__.py` containing `root_agent`. Multiple evalset files are allowed, and `file.json:eval_1,eval_2` filters to specific cases.

An evalset holds eval cases, each a distinct session: `eval_id`, `conversation` (multi-turn user content + expected `final_response`), `session_input` (`app_name`, `user_id`, `state`), and `intermediate_data` (expected tool trajectories and sub-agent responses).

**Default metrics when none are specified**: `tool_trajectory_avg_score` at **1.0** — 100% tool-trajectory match, which is strict and the usual cause of surprise failures — and `response_match_score` at **0.8**. Override in `test_config.json`. LLM-judged criteria also available: `final_response_match_v2`, `hallucinations_v1`, `safety_v1`, with multi-turn variants.

In CI, wrap it with pytest:

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.mark.asyncio
async def test_agent():
    await AgentEvaluator.evaluate(agent_module="agent_name",
                                  eval_dataset_file_path_or_dir="tests/eval_file.test.json")
```

For eval *methodology* across vendors — designing suites, judge design, regression strategy — use the `evals` sibling skill; this section is the ADK harness only.

Read `references/evaluation.md` for the full `.test.json` schema and threshold configuration.

## Deployment

| Target | Command | When |
|---|---|---|
| Agent Runtime (Agent Platform) | `adk deploy agent_engine` | Fully managed, auto-scaling; least infra to own |
| Cloud Run | `adk deploy cloud_run` | Container-based managed compute |
| GKE | `adk deploy gke` (Python) or manual | More control, or running open models |
| Custom container | your own image | Any container-compatible infra, disconnected systems |

"Agent Runtime on Agent Platform" is ADK's current name for what the docs previously called Agent Engine / Vertex AI Agent Engine — expect both names in the wild.

```bash
adk deploy cloud_run --project=$GOOGLE_CLOUD_PROJECT --region=$GOOGLE_CLOUD_LOCATION \
  --service_name=$SERVICE_NAME --app_name=capital_agent --with_ui $AGENT_PATH
```

`--project` and `--region` are required; `--with_ui` ships the web interface; `--session_service_uri` (e.g. `sqlite://`, `agentengine://`) and `--artifact_service_uri` wire persistence. Raw `gcloud` flags pass through after `--`.

`adk deploy agent_engine` packages the code, builds a container, and deploys to the managed service. **Language support is Python and Go v1.2.0+ only** as of 2026-08-05 — and the Python package deliberately **excludes the ADK API server and web UI libraries** while Go includes the dedicated API server. A user expecting `adk web` on a Python Agent Runtime deployment will not find it.

Read `references/deployment-and-a2a.md` for the manual `gcloud`/`Dockerfile`/`main.py` path, the TypeScript/Go/Java commands, GKE cluster + Workload Identity setup, deployed-agent smoke tests, the A2A surface, and Live/bidi streaming (`run_live()`, `LiveRequestQueue`, `RunConfig` streaming mode).

## ADK 2.0 and version gating

ADK 2.0 replaces the hierarchical agent executor with a **graph-based execution engine** where agents, tools, and functions are nodes. Four things break on upgrade: event schema gains `node_info` and `output` (custom DB schemas must accommodate them), agents subclass `BaseNode` so legacy `_run_async_impl()` overrides are bypassed, broad `try...except` masks the automatic retry mechanism, and the Go import path moves to `google.golang.org/adk/v2`.

The **1.x line is still maintained in parallel** (v1.37.0 shipped 2026-07-30, same day as v2.6.0) — a team not ready for graph workflows can stay on 1.x rather than being forced forward.

Read `references/versions/2.0.md` first whenever a user reports a behavior that "used to work", names a version, or is on Java/Kotlin/TypeScript.

## Reference files

- `references/agents-and-workflows.md` — `LlmAgent` parameters, Sequential/Parallel/Loop semantics and per-language constructors, custom agents, collaboration modes
- `references/tools-and-mcp.md` — function-tool schema rules, `ToolContext`, `McpToolset` connections, `OpenAPIToolset`, grounding and the built-in-tools gap
- `references/sessions-state-artifacts.md` — session objects, state prefixes, `SessionService` implementations, memory, artifact versioning
- `references/callbacks-and-runtime.md` — six callback signatures and return contracts, runtime execution surfaces
- `references/evaluation.md` — `adk eval` CLI, evalset/`.test.json` schema, metrics and thresholds, pytest integration
- `references/deployment-and-a2a.md` — Cloud Run/Agent Runtime/GKE/custom container, A2A, Live streaming
- `references/versions/2.0.md` — ADK 2.0 graph engine, migration breakages, per-language GA status, recent release history

## Diagnostic script

- `scripts/adk-preflight.py` — read-only environment check: Python version, installed `google-adk` version, `adk` CLI presence, whether a target agent directory actually defines `root_agent`, and which ADK-relevant environment variables are set (names only, values masked). Run `python scripts/adk-preflight.py [agent_dir]` before debugging load or deploy failures.

## Known gaps in this skill's sources

State these rather than filling them from memory:

- Built-in tool import paths and code samples (Google Search, code execution, Vertex AI Search) — deferred by the docs to the `/integrations/` catalog, not fetched.
- Exact `Runner.run_async()` signature and the full `RunConfig` field list — the `/runtime/` sub-pages were not fetched individually.
- `/agents/routing/` — LLM-driven transfer, `AgentTool`, and `transfer_to_agent` mechanics.
- The "Agents CLI" accelerated deployment path with CI/CD and infrastructure-as-code.
- Java parity for workflow agents, callbacks, and tools beyond the install/deploy snippets — the fetched pages default to Python samples.

## Sources

- https://adk.dev/
- https://adk.dev/sitemap.xml
- https://adk.dev/get-started/installation/
- https://adk.dev/get-started/python/
- https://adk.dev/agents/llm-agents/
- https://adk.dev/agents/workflow-agents/sequential-agents/
- https://adk.dev/agents/workflow-agents/parallel-agents/
- https://adk.dev/agents/workflow-agents/loop-agents/
- https://adk.dev/agents/custom-agents/
- https://adk.dev/agents/managed-agents/
- https://adk.dev/workflows/patterns/
- https://adk.dev/workflows/collaboration/
- https://adk.dev/tools-custom/
- https://adk.dev/tools-custom/function-tools/
- https://adk.dev/tools-custom/mcp-tools/
- https://adk.dev/tools-custom/openapi-tools/
- https://adk.dev/grounding/
- https://adk.dev/context/
- https://adk.dev/sessions/
- https://adk.dev/artifacts/
- https://adk.dev/callbacks/
- https://adk.dev/runtime/
- https://adk.dev/evaluate/
- https://adk.dev/deploy/
- https://adk.dev/deploy/cloud-run/
- https://adk.dev/deploy/gke/
- https://adk.dev/deploy/agent-runtime/deploy/
- https://adk.dev/a2a/intro/
- https://adk.dev/live/
- https://adk.dev/2.0/
- https://github.com/google/adk-python/releases

Fetched: 2026-08-05
