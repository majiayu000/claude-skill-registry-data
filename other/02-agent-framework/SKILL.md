---
name: 02-agent-framework
description: >
  Use when building a custom agent with the OpenAI Agents SDK and MLflow
  ResponsesAgent. Covers Agent class, Runner, @function_tool, handoffs,
  streaming, ModelConfig, mlflow.models.set_model(), autolog, and manual
  tracing. Track A Step 2. Produces a customized, MLflow-compatible agent
  class ready for tools and deployment.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Agent code (OpenAI Agents SDK + MLflow ResponsesAgent) — no deployed resource of its own; deployed later by Track A 07. Authored identically on both clients. On Genie Code write the agent source under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`); see `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.1.0"
  domain: "genai-agents"
  pipeline_position: "A2"
  consumes: "mlflow_environment, running_local_agent"
  produces: "agent_class, responses_agent, customized_agent, lakebase_endpoint_uri, lakebase_cold_start_retry_policy, lakebase_pool_close_policy"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent, openai.github.io/openai-agents-python, mlflow.org/docs/latest/genai/serving/responses-agent, github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk"
fields_read:
  - agent.system_prompt
  - agent.capabilities
  - agent.model
---

# Agent Framework and ResponsesAgent

Build your agent with the **OpenAI Agents SDK** and wrap it with **MLflow ResponsesAgent**
for Databricks-compatible serving, tracing, and evaluation.

## When to Use

- You have a running local agent from Track A Step 1 and need to customize its behavior.
- You need to understand the two-layer architecture: **Agent Framework** (OpenAI Agents SDK)
  on top of **MLflow ResponsesAgent** (serving contract).
- You want to add custom instructions, swap models, configure streaming, or set up handoffs.
- You need to enable MLflow tracing for observability.

**Foundation prerequisite:** This step consumes `mlflow_environment` from
[F1](../../../foundation/01-mlflow-genai-foundation/SKILL.md) and uses the
experiment/tracing infrastructure from
[F2](../../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md).
Both must be complete.

---

## Two-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  OpenAI Agents SDK (Agent Framework)        │
│  ├─ Agent class (instructions, model, tools)│
│  ├─ Runner.run / Runner.run_streamed        │
│  ├─ @function_tool definitions              │
│  └─ Handoffs for multi-agent routing        │
├─────────────────────────────────────────────┤
│  MLflow Host Runtime (Serving Contract)     │
│  ├─ Option B (canonical): @invoke / @stream │
│  │    module-level async handlers, hosted  │
│  │    on Databricks Apps                   │
│  └─ Option A (legacy): ResponsesAgent class │
│       hosted on Databricks Model Serving   │
└─────────────────────────────────────────────┘
```

The **OpenAI Agents SDK** handles conversation management, tool orchestration, and
multi-agent routing. The **MLflow host runtime** wraps it for serving, tracing,
and evaluation. Pick the host runtime by deployment target (next section).

---

## Deployment Target Decides the Wrapping Pattern

The Track A agent runs under one of two MLflow wrapping patterns, chosen by
**where you plan to deploy**. Pick the deployment target first; the authoring
pattern and the downstream AppKit wiring skill follow automatically.

| Option | Authoring pattern | Deployment target | AppKit wiring skill |
|--------|-------------------|-------------------|---------------------|
| **B (canonical)** | Module-level `@mlflow.genai.agent_server.invoke` / `@mlflow.genai.agent_server.stream` async handlers | Databricks **Apps** (as its own App, via `databricks apps deploy`) | [`06d-appkit-agent-app-proxy`](../../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md) |
| **A (legacy)** | Class-based `mlflow.pyfunc.ResponsesAgent` wrapping the Agents SDK `Runner` | Databricks **Model Serving** endpoint (via `databricks.agents.deploy()`) | [`06-appkit-serving-wiring`](../../../../apps_lakebase/skills/06-appkit-serving-wiring/SKILL.md) |

### When to pick which

- **Pick Option B for any new use case.** Databricks recommends Apps as the
  default agent host runtime — per the 2026
  [author-agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
  and
  [migrate-agent-to-apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/migrate-agent-to-apps)
  docs. This is the canonical Track A path used by the
  [`agent-openai-agents-sdk`](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk),
  [`agent-openai-agents-sdk-multiagent`](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-multiagent),
  and
  [`agent-openai-advanced`](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced)
  templates. The canonical SkyLoyalty walkthrough uses Option B.
- **Pick Option A only when** you have a hard requirement for the legacy path
  — e.g. an existing Model Serving endpoint, a multi-agent Genie notebook
  packaged as `pyfunc`, a Knowledge Assistant wrapper that must register
  through UC Model Registry with `@champion`/`@production` aliases on the
  critical deploy path.
- **Both options** still benefit from MLflow 3 tracing, `agent-evaluate`, and
  `mlflow.openai.autolog()`. The difference is the serving contract
  (`/invocations` on an App URL vs. `/serving-endpoints/:name/invocations`)
  and the auth model (explicit `x-forwarded-access-token` forwarding vs. the
  Serving plugin's `.asUser(req)`).

---

## Option B — Module-level `@invoke` / `@stream` (canonical)

The Apps host runtime invokes module-level **async** functions decorated with
`mlflow.genai.agent_server.invoke` and `mlflow.genai.agent_server.stream`. No
class, no `mlflow.models.set_model()`, no `predict` / `predict_stream`. End-user
identity flows via `http_request` → `get_user_workspace_client(http_request)`,
so every tool call runs **on-behalf-of** the end user when the AppKit proxy
forwards `x-forwarded-access-token`.

```python
# agent.py — Option B canonical layout (mirrors agent-openai-agents-sdk template)
import os
import mlflow
from agents import Agent, Runner, function_tool
from mlflow.genai import agent_server
from mlflow.models import ModelConfig
from databricks_app.utils import get_user_workspace_client

mlflow.openai.autolog()

config = ModelConfig(development_config="config.yml")

@function_tool
def get_current_time() -> str:
    """Get the current ISO timestamp."""
    from datetime import datetime
    return datetime.now().isoformat()

def build_agent(ws) -> Agent:
    """Build the agent for this request, optionally per-user-scoped via ws."""
    return Agent(
        name="loyalty-assistant",
        instructions="You are a helpful loyalty program assistant.",
        model=config.get("llm_endpoint"),
        tools=[get_current_time],
    )

@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    ws = get_user_workspace_client(http_request)
    agent = build_agent(ws)
    result = await Runner.run(agent, request["input"])
    return {"output": result.final_output}

@agent_server.stream
async def handle_stream(request: dict, http_request):
    ws = get_user_workspace_client(http_request)
    agent = build_agent(ws)
    async for event in Runner.run_streamed(agent, request["input"]):
        if event.type == "raw_response_event":
            yield event.data
```

### Trace context: user, session, environment, request id

The `@invoke` / `@stream` handler is the canonical call site for
attaching trace context — user, session, environment override, and
`client_request_id` for end-user feedback correlation. Set them all on
the trace root **before** the `Runner.run` call so they're present even
if the agent fails partway:

```python
import os
import mlflow


@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    ws = get_user_workspace_client(http_request)
    user_id = ws.current_user.me().user_name
    session_id = request.get("session_id") or http_request.headers.get("x-session-id", "anon")

    mlflow.update_current_trace(
        client_request_id=request.get("client_request_id"),  # for /feedback correlation
        metadata={
            "mlflow.trace.user":    user_id,
            "mlflow.trace.session": session_id,
            "mlflow.source.type":   os.getenv("APP_ENVIRONMENT", "development"),
            "agent_version":        os.getenv("AGENT_VERSION", "unknown"),
        },
    )

    agent = build_agent(ws)
    result = await Runner.run(agent, request["input"])
    return {"output": result.final_output, "trace_id": mlflow.get_current_active_span().trace_id}
```

The reserved metadata fields (`mlflow.trace.user` /
`mlflow.trace.session`) are **immutable** post-log and light up the
Trace UI's user / session facets. The `APP_ENVIRONMENT` env var is set
in `app.yaml` per deployment. For the full pattern (auto-populated
metadata, custom deployment metadata, search-by-metadata examples), see
[F2c — Trace context and environments](../../../foundation/02c-trace-context-and-environments/SKILL.md).
For end-user feedback correlation via `trace_id` / `client_request_id`,
see [04c — End-user feedback](../../../sdlc/04c-end-user-feedback/SKILL.md).

### `app.yaml` for Option B

The Apps host serves the module directly — no `start_server.py` is required.
Point `command` at the MLflow agent server entrypoint and the agent module:

```yaml
# app.yaml
command:
  - mlflow
  - genai
  - agent-server
  - serve
  - --module
  - agent
env:
  - name: LLM_ENDPOINT
    value: databricks-claude-sonnet-4-6
  # F2c: app code reads APP_ENVIRONMENT and overrides mlflow.source.type via metadata.
  - name: APP_ENVIRONMENT
    value: production
```

For deployment, see [`07-deploy-and-query`](../07-deploy-and-query/SKILL.md)
with `target=databricks_apps`. For wiring the AppKit frontend, see
[`06d-appkit-agent-app-proxy`](../../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md).

### Runtime model route from Tool Plan

Track A agents consume `docs/agent_tool_plan.yaml.runtime_config.llm` through `ModelConfig`, never by hardcoding model names in Python.

Minimum `config.yml` shape:

```yaml
llm_endpoint: "databricks-claude-sonnet-4-6"
llm_api_base_url: null
llm_api_mode: "databricks_openai_compatible"
```

Agent construction must read:

```python
config = ModelConfig(development_config="config.yml")

agent = Agent(
    name="loyalty-assistant",
    instructions="...",
    model=config.get("llm_endpoint"),
)
```

If `llm_api_base_url` is non-null in a future Gateway route, the client factory may pass it to the OpenAI-compatible client. The core workshop does not require that path.

### Multi-agent variant

For a triage / handoffs pattern, see the
[`agent-openai-agents-sdk-multiagent`](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-multiagent)
template and the Handoffs section below — both apply identically inside
`build_agent()` under Option B.

### Advanced variant (Lakebase memory + custom tools)

For long-term memory backed by Lakebase, see the
[`agent-openai-advanced`](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced)
template and [A5: Lakebase Memory](../05-lakebase-memory/SKILL.md). Memory
state is loaded inside `handle_invoke` / `handle_stream` per request.

### Lakebase cold-start retry policy and lazy init

The Track A agent owns the Lakebase **client policy** contract — the
endpoint URI it connects to, the retry behavior on cold-start failures
that Lakebase Autoscaling raises during the first request after idle,
and the pool-close policy on graceful shutdown. Capture these fields in
state and read them at runtime; **do not** hard-code retry counts or
error classes in the agent module.

Capture in state:

```yaml
# state://Track_A.a2_agent_framework
lakebase_endpoint_uri: "postgresql://<host>:<port>/<database>"   # resolved from databricks_app.utils.get_user_workspace_client at runtime
lakebase_cold_start_retry_policy:
  retry_on:
    - AdminShutdown                      # psycopg.errors.AdminShutdown — Lakebase autoscaler closed the prior connection
    - psycopg_pool.PoolClosed            # the pool was closed mid-request and must be re-opened
  max_attempts: 3
  initial_backoff_seconds: 5             # exponential: 5s, 10s, 20s
lakebase_pool_close_policy: "close_on_app_shutdown"
# allowed values:
#   - close_on_app_shutdown   (default; close pool in `@app.on_event("shutdown")` or equivalent)
#   - close_on_request_end    (only for short-lived dev runs — produces excessive cold starts in prod)
#   - never                   (only for diagnostic harnesses; leaks connections)
```

The retry-on classes (`psycopg.errors.AdminShutdown`,
`psycopg_pool.PoolClosed`) are the canonical first-request-after-idle
failure modes documented in the retrospective. The agent's connection
helper MUST catch exactly these classes (not a bare `Exception`) and
back off per `initial_backoff_seconds * 2 ** attempt` up to
`max_attempts`. `preflight_check_registry.lakebase_cold_start_retry_policy_present`
gates downstream prompt roles until `agent.retry_policy.lakebase_cold_start_max_retries >= 1`
is recorded in state.

#### Lazy init: Lakebase config MUST NOT execute at import time

Connecting to Lakebase from module-level code (top of `agent.py`) is a
recurring failure: imports happen during `mlflow models log` and during
`databricks apps deploy` on machines that have no path to the Lakebase
endpoint, blowing up the deploy. **All Lakebase-related setup runs
inside `handle_invoke` / `handle_stream` (or a request-scoped factory
they call), never at module import.**

```python
# agent.py — Lakebase lazy init pattern (Option B)
import os
import asyncio
import mlflow
from agents import Agent, Runner
from mlflow.genai import agent_server
from databricks_app.utils import get_user_workspace_client

mlflow.openai.autolog()

# DO NOT instantiate the Lakebase pool here — that runs at import time
# and breaks `mlflow models log` and `databricks apps deploy`.
_LAKEBASE_POOL = None
_LAKEBASE_LOCK = asyncio.Lock()


async def _get_lakebase_pool(ws):
    """Build the pool the first time a request needs it; cache for the lifetime of the process."""
    global _LAKEBASE_POOL
    if _LAKEBASE_POOL is not None:
        return _LAKEBASE_POOL
    async with _LAKEBASE_LOCK:
        if _LAKEBASE_POOL is None:
            from psycopg_pool import AsyncConnectionPool
            uri = os.environ["LAKEBASE_ENDPOINT_URI"]   # from state://lakebase_endpoint_uri
            _LAKEBASE_POOL = AsyncConnectionPool(uri, open=False)
            await _LAKEBASE_POOL.open()
    return _LAKEBASE_POOL


async def _with_cold_start_retry(coro_factory):
    """Wrap a coroutine factory with the policy from state://lakebase_cold_start_retry_policy."""
    import psycopg.errors
    import psycopg_pool

    max_attempts = 3
    backoff = 5
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return await coro_factory()
        except (psycopg.errors.AdminShutdown, psycopg_pool.PoolClosed) as exc:
            last_exc = exc
            if attempt + 1 == max_attempts:
                raise
            await asyncio.sleep(backoff * (2 ** attempt))
    raise last_exc  # unreachable


@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    ws = get_user_workspace_client(http_request)
    pool = await _get_lakebase_pool(ws)                      # lazy: first call only

    async def _do_work():
        async with pool.connection() as conn:
            # ... read/write memory using conn ...
            agent = Agent(name="my-agent", instructions="...", tools=[])
            return await Runner.run(agent, request["input"])

    result = await _with_cold_start_retry(_do_work)
    return {"output": result.final_output}


@agent_server.stream
async def handle_stream(request: dict, http_request):
    # Same lazy-init + retry pattern as handle_invoke. Do NOT touch _LAKEBASE_POOL at module level.
    ...
```

For graceful pool close at app shutdown (per `lakebase_pool_close_policy:
close_on_app_shutdown`), register a shutdown hook **inside** the agent
server's lifecycle — not at module import. Track A 05 (Lakebase Memory)
covers the AppKit / FastAPI lifecycle hook patterns.

#### DO / DON'T (Lakebase init)

**DO** — Build the pool inside the request handler the first time it's needed:

```python
async def handle_invoke(request, http_request):
    pool = await _get_lakebase_pool(ws)   # OK — first call builds; later calls cached
    ...
```

**DON'T** — Open the pool at module top level:

```python
# WRONG: this runs during `mlflow models log` and `databricks apps deploy`
from psycopg_pool import AsyncConnectionPool
pool = AsyncConnectionPool(os.environ["LAKEBASE_ENDPOINT_URI"], open=True)
```

**DON'T** — Catch a bare `Exception` for cold-start retries:

```python
# WRONG: hides legitimate errors (auth, schema, etc.)
try:
    return await pool.connection()
except Exception:
    await asyncio.sleep(5)
    ...
```

**DO** — Catch only the canonical cold-start classes and use the captured policy:

```python
import psycopg.errors, psycopg_pool
try:
    return await pool.connection()
except (psycopg.errors.AdminShutdown, psycopg_pool.PoolClosed):
    ...
```

---

## Option A — Class-based `ResponsesAgent` (legacy, Model Serving)

> **Use only if you have a hard Model-Serving requirement.** New work should
> use Option B. The pattern below is preserved for migrations and for users
> on the legacy [`06-appkit-serving-wiring`](../../../../apps_lakebase/skills/06-appkit-serving-wiring/SKILL.md)
> AppKit path.

---

## OpenAI Agents SDK Core Concepts

### Agent Class

The `Agent` is the core building block. It combines instructions, a model, and tools:

```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

agent = Agent(
    name="my-assistant",
    instructions="You are a helpful data analyst. Always cite your sources.",
    model="databricks-claude-sonnet-4-6",
    tools=[get_weather],
)
```

**Key parameters:**

| Parameter | Purpose |
|-----------|---------|
| `name` | Agent identity (appears in traces and logs) |
| `instructions` | System prompt — controls agent behavior |
| `model` | LLM endpoint name (Databricks serving endpoint) |
| `tools` | List of `@function_tool` callables or MCP servers |
| `handoffs` | List of other `Agent` instances for multi-agent routing |

### Runner: Executing the Agent

`Runner` executes the agent loop (LLM call → tool calls → LLM call → ...) until completion:

```python
from agents import Runner

# Synchronous (blocking)
result = Runner.run_sync(agent, "What's the weather in Seattle?")
print(result.final_output)

# Async
result = await Runner.run(agent, "What's the weather in Seattle?")
print(result.final_output)
```

### Streaming

For real-time response delivery (critical for chat UIs):

```python
from agents import Runner

async for event in Runner.run_streamed(agent, "Analyze my data"):
    if event.type == "raw_response_event":
        # Token-by-token output
        print(event.data, end="", flush=True)
```

The Databricks App template's `start_server.py` wires this into the built-in chat UI
automatically via MLflow AgentServer.

### Handoffs (Multi-Agent Routing)

Route conversations to specialized agents based on intent:

```python
from agents import Agent

billing_agent = Agent(
    name="billing-expert",
    instructions="You answer billing and cost questions.",
    model="databricks-claude-sonnet-4-6",
)

usage_agent = Agent(
    name="usage-expert",
    instructions="You answer usage and consumption questions.",
    model="databricks-claude-sonnet-4-6",
)

triage_agent = Agent(
    name="triage",
    instructions="""Route the user's question to the right expert.
    - Billing/cost questions → billing-expert
    - Usage/consumption questions → usage-expert""",
    model="databricks-claude-sonnet-4-6",
    handoffs=[billing_agent, usage_agent],
)
```

---

## MLflow ResponsesAgent Wrapping (Option A only)

> Skip this section entirely if you are on the canonical Option B path.

ResponsesAgent is **mandatory for Option A** (Model Serving target). It provides:

- Automatic model signature inference (compatible with AI Playground)
- `predict()` and `predict_stream()` methods for the serving contract
- Built-in MLflow tracing integration
- Structured request/response format

### The Wrapping Pattern

In your `agent.py`, the agent is created with the OpenAI Agents SDK and then
registered with `mlflow.models.set_model()`:

```python
import mlflow
from agents import Agent, function_tool

@function_tool
def search_docs(query: str) -> str:
    """Search internal documentation."""
    return "Found: relevant document content..."

agent = Agent(
    name="my-agent",
    instructions="You are a helpful assistant with access to internal docs.",
    model="databricks-claude-sonnet-4-6",
    tools=[search_docs],
)

# CRITICAL: This line makes the agent discoverable by MLflow
mlflow.models.set_model(agent)
```

`mlflow.models.set_model()` tells MLflow where to find the agent when
`start_server.py` or `log_model()` references this file. **Without it,
serving and logging fail silently.**

### ModelConfig for Parametrization

Externalize settings so you can change models, endpoints, or feature flags
without editing code:

```yaml
# config.yml
llm_endpoint: "databricks-claude-sonnet-4-6"
warehouse_id: "${WAREHOUSE_ID}"
temperature: 0.7
max_tokens: 4096
```

```python
from mlflow.models import ModelConfig

config = ModelConfig(development_config="config.yml")

agent = Agent(
    name="my-agent",
    instructions="You are a helpful assistant.",
    model=config.get("llm_endpoint"),
)
```

`ModelConfig` reads from the YAML file during development and from logged
artifacts during serving. This is the prescribed way to parametrize agents.

### Agent Spec Model Endpoint

In the Agents Accelerator flow, the selected model endpoint comes from
`docs/agent_spec.yaml.agent.model`.

Implementation contract:

1. Copy `agent.model` into `config.yml` as `llm_endpoint`.
2. Load it with `ModelConfig(development_config="config.yml")`.
3. Build the OpenAI Agents SDK agent with `model=config.get("llm_endpoint")`.
4. Do not hardcode `databricks-claude-sonnet-4-6` in Python agent construction unless that exact value came from `agent.model`.

```yaml
# config.yml
llm_endpoint: "databricks-claude-sonnet-4-6"
```

```python
from mlflow.models import ModelConfig

config = ModelConfig(development_config="config.yml")

agent = Agent(
    name=agent_name,
    instructions=agent_instructions,
    model=config.get("llm_endpoint"),
    tools=tools,
)
```

### predict and predict_stream

When served via MLflow AgentServer, the agent exposes these endpoints:

```python
# Synchronous prediction (POST /invocations)
response = agent.predict({"input": [{"role": "user", "content": "Hello"}]})

# Streaming prediction (POST /invocations with Accept: text/event-stream)
for chunk in agent.predict_stream({"input": [{"role": "user", "content": "Hello"}]}):
    print(chunk)
```

ResponsesAgent handles the translation between the OpenAI Agents SDK's
`Runner.run()` / `Runner.run_streamed()` and the MLflow serving contract.

---

## MLflow Tracing

### Enable Autolog

At the top of `agent.py` (or your entrypoint), enable autolog to capture all
LLM calls automatically:

```python
import mlflow

mlflow.openai.autolog()
```

This captures:
- Every LLM API call (input, output, tokens, latency)
- Tool invocations
- Agent reasoning steps

### Manual Tracing with @mlflow.trace

For custom spans around your own functions:

```python
import mlflow

@mlflow.trace(name="process_query", span_type="AGENT")
def process_query(query: str) -> dict:
    classified = classify_intent(query)
    result = route_to_agent(classified)
    return result

@mlflow.trace(name="classify_intent", span_type="LLM")
def classify_intent(query: str) -> str:
    # LLM call for classification
    ...
```

Common span types: `AGENT`, `LLM`, `TOOL`, `RETRIEVER`, `JUDGE`, `EMBEDDING`.

### Viewing Traces

After running the agent locally with `uv run start-app`, traces appear in the
MLflow Experiment UI. Navigate to your experiment and click the "Traces" tab.

---

## Customization Patterns

### Modifying Instructions

Edit the `instructions` parameter to change agent behavior:

```python
agent = Agent(
    name="data-analyst",
    instructions="""You are a senior data analyst at Acme Corp.

Rules:
- Always query the data warehouse before answering data questions
- Format numbers with appropriate units (K, M, B)
- When uncertain, say so rather than guessing
- Cite the specific table and column used in your answer""",
    model="databricks-claude-sonnet-4-6",
    tools=[query_warehouse],
)
```

### Swapping Models

Change the `model` parameter to use a different serving endpoint:

```python
# For development (faster, cheaper)
agent = Agent(name="dev-agent", model="databricks-meta-llama-3-3-70b-instruct", ...)

# For production (more capable)
agent = Agent(name="prod-agent", model="databricks-claude-sonnet-4-6", ...)
```

Use `ModelConfig` to make this configurable without code changes.

---

## DO / DON'T

### DO (Option A only) — Call `mlflow.models.set_model()` at module level

```python
# agent.py — Option A
import mlflow
from agents import Agent

agent = Agent(name="my-agent", ...)
mlflow.models.set_model(agent)
```

### DON'T (Option A only) — Forget `set_model()` or call it inside a function

Under Option A, missing `set_model` causes `log_model` and `start_server` to
fail. Under Option B, `set_model` is **not required** — the
`@agent_server.invoke` / `@agent_server.stream` decorators are the discovery
mechanism; never combine them with `set_model`.

### DO — Use ModelConfig for all configurable values

```python
config = ModelConfig(development_config="config.yml")
agent = Agent(model=config.get("llm_endpoint"), ...)
```

### DON'T — Hardcode endpoint names in agent definitions

```python
agent = Agent(model="databricks-claude-sonnet-4-6", ...)
# Breaks when endpoint name changes or differs across environments
```

### DO — Enable autolog at module level

```python
import mlflow
mlflow.openai.autolog()
```

### DON'T — Enable autolog inside request handlers

```python
def handle_request(query):
    mlflow.openai.autolog()  # Called per-request — wasteful
    ...
```

### DO — Let ResponsesAgent infer the model signature

```python
mlflow.pyfunc.log_model(
    python_model=agent,
    artifact_path="agent",
    input_example={"input": [{"role": "user", "content": "Hello"}]},
)
```

### DON'T — Pass `signature=` to `log_model()` for ResponsesAgent

```python
# Manual signatures break auto-inference and cause Playground/eval mismatches
mlflow.pyfunc.log_model(
    python_model=agent,
    signature=my_custom_signature,  # WRONG
)
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `set_model` not found | Ensure `mlflow[databricks]>=3.10.1` installed |
| Agent doesn't stream | Use `Runner.run_streamed()` and verify `predict_stream` is wired in `start_server.py` |
| Traces missing in MLflow UI | Call `mlflow.openai.autolog()` before any LLM calls |
| `ModelConfig` not finding values | Check that `config.yml` exists and keys match `config.get("key")` calls |
| Handoff agent not invoked | Verify the triage agent's instructions clearly describe when to handoff |
| Agent returns empty response | Check that `Runner.run()` result has `final_output` — tool-only responses may need explicit formatting |

---

## Validation Gate

All must pass before proceeding:

- [ ] Agent instructions customized for your use case
- [ ] **Option B:** `@mlflow.genai.agent_server.invoke` and `@mlflow.genai.agent_server.stream` handlers defined at module level; **no** `mlflow.models.set_model()` present
- [ ] **Option A only:** `mlflow.models.set_model(agent)` called at module level in `agent.py`
- [ ] `mlflow.openai.autolog()` enabled — traces visible in MLflow UI
- [ ] Agent responds correctly to test queries via chat UI
- [ ] `ModelConfig` externalizes at least the LLM endpoint name
- [ ] Streaming works in the built-in chat UI (tokens appear incrementally)
- [ ] Deployment target recorded (`databricks_apps` for Option B, `model_serving` for Option A) — passed forward to A7
- [ ] **Lakebase (if used):** `lakebase_endpoint_uri`, `lakebase_cold_start_retry_policy` (with `retry_on: [AdminShutdown, psycopg_pool.PoolClosed]`, `max_attempts: 3`, `initial_backoff_seconds: 5`), and `lakebase_pool_close_policy` captured in state
- [ ] **Lakebase (if used):** No Lakebase pool, connection, or env-var read happens at module import time — all Lakebase initialization is inside `handle_invoke` / `handle_stream` (verified by grep: no `AsyncConnectionPool(...)` or `pool.open()` at module top level)
- [ ] **Lakebase (if used):** Cold-start retry catches **only** `psycopg.errors.AdminShutdown` and `psycopg_pool.PoolClosed` (not bare `Exception`) and uses the captured `initial_backoff_seconds` exponential backoff

## Next Step

After passing this gate, **load and execute**
`tracks/A-custom-agent-apps/03-tools-and-mcp/SKILL.md` (A3: Tools and MCP).

## Notes to Carry Forward

| Key | Value |
|-----|-------|
| `agent_framework` | OpenAI Agents SDK |
| `agent_file` | `agent.py` (or your agent module path) |
| `wrapping_pattern` | `option_b_invoke_stream` (canonical) or `option_a_responses_agent` (legacy) |
| `deployment_target` | `databricks_apps` (Option B) or `model_serving` (Option A) |
| `model_endpoint` | LLM serving endpoint name from `config.yml` |
| `config_file` | `config.yml` (ModelConfig source) |
| `autolog_type` | `mlflow.openai.autolog()` |
| `tools_defined` | List of `@function_tool` names (if any added here) |
| `lakebase_endpoint_uri` | (if Lakebase memory) PostgreSQL URI for Lakebase, resolved per-request |
| `lakebase_cold_start_retry_policy` | (if Lakebase memory) `{retry_on: [AdminShutdown, psycopg_pool.PoolClosed], max_attempts: 3, initial_backoff_seconds: 5}` |
| `lakebase_pool_close_policy` | (if Lakebase memory) one of `close_on_app_shutdown` / `close_on_request_end` / `never` |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [F1: MLflow Foundation](../../../foundation/01-mlflow-genai-foundation/SKILL.md) | Produces `mlflow_environment` consumed here |
| [F2: Tracing & UC OTEL](../../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md) | Experiment and tracing infrastructure used by autolog |
| [A1: Clone and Run](../01-clone-and-run/SKILL.md) | Previous step — produces `running_local_agent` |
| [A3: Tools and MCP](../03-tools-and-mcp/SKILL.md) | Next step |

## References

- [Author an AI agent and deploy it on Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [OpenAI Agents SDK documentation](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK — Tools](https://openai.github.io/openai-agents-python/tools/)
- [OpenAI Agents SDK — Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [MLflow ResponsesAgent](https://mlflow.org/docs/latest/genai/serving/responses-agent/)
- [MLflow AgentServer](https://mlflow.org/docs/latest/genai/serving/agent-server/)
- [MLflow ModelConfig](https://mlflow.org/docs/latest/python_api/mlflow.models.html#mlflow.models.ModelConfig)
- [Databricks app-templates — agent-openai-agents-sdk](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk)
- [Databricks app-templates — agent-openai-agents-sdk-multiagent](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-multiagent)
- [Databricks app-templates — agent-openai-advanced](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced)
- [Migrate an agent to Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/migrate-agent-to-apps)

### Reference files (this skill)

| File | Content |
|------|---------|
| [`references/streaming-patterns.md`](references/streaming-patterns.md) | `predict_stream`, `create_text_delta`, SSE patterns, error propagation |
| [`references/custom-inputs-outputs.md`](references/custom-inputs-outputs.md) | `custom_inputs` / `custom_outputs`, Playground UI, Review App caveats |
| [`references/wrapping-existing-agents.md`](references/wrapping-existing-agents.md) | Wrapping non-OpenAI-SDK agents with ResponsesAgent |
| [`references/common-mistakes.md`](references/common-mistakes.md) | Signature drift, missing set_model, autolog placement errors |
| [`references/trace-context-patterns.md`](references/trace-context-patterns.md) | Span types, trace tags, nested agent traces |
| [`assets/templates/agent-class-template.py`](assets/templates/agent-class-template.py) | Starter agent.py with OpenAI Agents SDK + ResponsesAgent |
| [`assets/templates/agent-config-template.yml`](assets/templates/agent-config-template.yml) | Starter config.yml for ModelConfig |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.1.0 | 2026-04-26 | A2 now owns the Lakebase **client policy** contract: added "Lakebase cold-start retry policy and lazy init" section capturing `lakebase_endpoint_uri`, `lakebase_cold_start_retry_policy` (`retry_on: [AdminShutdown, psycopg_pool.PoolClosed]`, `max_attempts: 3`, `initial_backoff_seconds: 5`), and `lakebase_pool_close_policy`. Documents the lazy-init requirement (Lakebase config MUST NOT execute at import time — recurring deploy failure mode in `mlflow models log` / `databricks apps deploy`) with a worked Option B example. New DO/DON'T pairs for module-level pool init and bare-`Exception` retry. Validation gate gates the three captures, the no-import-time check, and the canonical retry-class allowlist. |
| 3.0.0 | 2026-04-22 | Reordered to lead with Option B (`@invoke` / `@stream` on Apps) as canonical; demoted Option A (`ResponsesAgent` on Model Serving) to legacy. Added full Option B authoring example, `app.yaml`, multi-agent + advanced template references. Validation gate now branches by wrapping pattern. |
| 2.0.0 | 2026-04-10 | Merged from fast-02 and 02-responses-agent-patterns. Single prescribed framework (OpenAI Agents SDK). Covers Agent, Runner, streaming, handoffs, ResponsesAgent wrapping, ModelConfig, autolog, manual tracing. |
