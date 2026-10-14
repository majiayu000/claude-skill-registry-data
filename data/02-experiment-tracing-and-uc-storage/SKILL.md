---
name: 02-experiment-tracing-and-uc-storage
description: >
  Use when setting up MLflow experiments, tracing, or UC OTEL trace storage for
  a GenAI agent. Covers structured experiment paths, tracing decorators, manual
  spans, tags, connection pooling, and Unity Catalog OTEL storage for SQL-queryable
  trace retention. Foundation Step 2. Consumes MLflow environment from Step 1.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Experiment + tracing + UC OTEL trace storage configured via the MLflow SDK; OTEL trace tables land in the per-user prefixed schema. No bundle resource. Identical on both clients; on Genie Code use its serverless runtime + runDatabricksCli for any CLI step. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-08-30"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.6.1"
  domain: "genai-agents"
  pipeline_position: "F2"
  consumes: "mlflow_environment"
  produces: "experiment_paths, tracing_config, connection_pool, f2_grants_complete, otel_table_prefix, mlflow_tracing_sql_warehouse_id, app_service_principal_grants"
  grounded_in: "docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog, docs.databricks.com/aws/en/mlflow3/genai, docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation, docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/automatic, docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing, docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces"
---

# Experiment tracing setup

## When to Use

Use this skill when you need to:

- Organize MLflow experiments so runs are discoverable by space, domain, and lifecycle stage
- Add tracing to GenAI agents (decorators, nested spans, inputs/outputs)
- Configure MLflow for multi-stage pipelines (development, evaluation, deployment) with consistent paths and UC prompt registry visibility
- Tune HTTP client behavior before high-throughput tracing or evaluation workloads

Prerequisite: complete **Foundation Step 1** (MLflow foundation) so tracking URI and authentication are already correct. See [MLflow GenAI Foundation (Foundation Step 1)](../01-mlflow-genai-foundation/SKILL.md).

> **TypeScript / Node agents:** this skill is the **Python** instrumentation
> reference. For the official `mlflow-tracing` + `mlflow-openai` npm path
> (Node-native `mlflow.init`, `tracedOpenAI`, `mlflow.trace`, `withSpan`,
> session grouping), see the sibling skill
> [`02b-typescript-tracing`](../02b-typescript-tracing/SKILL.md). Use OTLP
> (via custom OpenTelemetry instrumentation when the TypeScript SDK does not fit)
> only as a fallback when you need vendor-neutral spans or already run an
> OpenTelemetry collector.

> **Production deployment:** the env-var matrix for **deployed** agents
> (`ENABLE_MLFLOW_TRACING`, `MLFLOW_EXPERIMENT_ID`, SP `CAN_EDIT` on the
> experiment, the Git-folder caveat, Production Monitoring → Delta) lives in
> [`references/prod-tracing-deployment.md`](references/prod-tracing-deployment.md).
> Track A and Track C deployment skills link there.

> **User / session / environment context:** the canonical reference for
> attributing traces to a user (`mlflow.trace.user`), grouping multi-turn
> conversations (`mlflow.trace.session`), and overriding
> `mlflow.source.type` from `APP_ENVIRONMENT` lives in
> [`02c-trace-context-and-environments`](../02c-trace-context-and-environments/SKILL.md).
> The "Trace tags and metadata" section below shows the call-site shape;
> F2c is the long form (tags vs metadata, auto-populated fields, search
> examples, deployment overrides).

## Which approach: automatic vs manual vs combined

Before writing tracing code, pick the right approach. Source: [Add traces to applications (overview)](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/).

| Scenario | Recommended approach |
|---|---|
| You use **one GenAI library** (LangChain, LlamaIndex, DSPy, …) | **Automatic** tracing only — `mlflow.<library>.autolog()`. |
| You call an **LLM SDK directly** (OpenAI, Anthropic, Mistral, …) | **Automatic** for the SDK + a thin **`@mlflow.trace`** wrapper around your `run()` / orchestration function so all calls roll up into one trace. |
| You use **multiple frameworks / SDKs** in one workflow | Enable **`autolog()`** for each framework + use **`@mlflow.trace`** to combine them into a single root trace. |
| **All other** scenarios (custom logic, tool routing, complex retry/fallback, framework-less) | **Manual** with `@mlflow.trace` decorators first; drop down to `mlflow.start_span` only when you need finer-grained control. |

> **Start with automatic.** It's the fastest way to get traces working. Add
> manual tracing later if you need more control. Both approaches feed the
> same trace tree — `@mlflow.trace` parent spans naturally nest auto-traced
> child spans.

For the full **20+ supported autolog integrations** (LLM SDKs, orchestrators, agent frameworks, embedding libraries) plus the multi-framework combine pattern and the serverless-compute caveat, see [`references/autolog-integrations.md`](references/autolog-integrations.md).

## Experiment path organization

### CRITICAL: consume the experiment path from state — do not invent one

The workshop pins MLflow experiment paths to the **same user-and-use-case identity** that backs `APP_NAME` (e.g. `jane-d-stayfinder`) so concurrent attendees on a shared workspace cannot collide on a single experiment, and so the leaf in the MLflow UI is never a generic word like `Tracing`, `traces`, `Default`, or `my-agent`.

The canonical derivation lives in [`vibecoding-state` `migrate_canonical`](../../vibecoding-state/SKILL.md#operation-migrate_canonical) and is captured in state at the prompt that first resolves `$APP_NAME` / `$AGENT_NAME`:

| State field | Derivation | Example |
|---|---|---|
| `mlflow_experiment_path` | `/Users/<user_email>/mlflow/<APP_NAME or AGENT_NAME>-agent` | `/Users/jane.doe@example.com/mlflow/jane-d-stayfinder-agent` |
| `mlflow_feedback_experiment_path` | `/Users/<user_email>/mlflow/<APP_NAME>-feedback` | `/Users/jane.doe@example.com/mlflow/jane-d-stayfinder-feedback` |

This skill **consumes** those values from `state://Resources.mlflow_experiment_path` rather than constructing its own. If state shows `<pending>` for the path, halt and route back to `vibecoding-state` `migrate_canonical` — do not paper over it with a hand-rolled `/Shared/...` default.

### Path template (for projects that do not run on top of `vibecoding-state`)

If your project does not use the `vibecoding-state` skill, define a template that still pins identity onto the leaf:

```text
EXPERIMENT_PATH_TEMPLATE = "/Users/{{ user_email }}/mlflow/{{ app_name }}-{{ stage }}"
```

Where `app_name` is the user-prefixed, use-case-suffixed identity (e.g. `jane-d-stayfinder`) and `stage` ∈ {`agent`, `eval`, `feedback`, `deploy`}.

### Three-experiment lifecycle pattern

For multi-stage pipelines, use **separate experiments** (one leaf per stage under the same `app_name`):

| Stage | Leaf | Purpose |
| --- | --- | --- |
| **agent / dev** | `<app_name>-agent` | Interactive debugging, short runs, permissive logging — the default tracing destination |
| **eval** | `<app_name>-eval` | Benchmarks, `mlflow.genai.evaluate`, regression gates |
| **feedback** | `<app_name>-feedback` | End-user thumbs / human assessments persisted from the AppKit feedback skill |
| **deploy** | `<app_name>-deploy` | Production or promotion runs, stricter tags and retention |

The leaf must always carry `<app_name>` so that browsing MLflow experiments lists `jane-d-stayfinder-agent`, `jane-d-stayfinder-eval`, etc. — never a bare `agent` / `eval` / `Tracing`.

### Setting the experiment

When running inside the workshop, read the path from state:

```python
import mlflow

# state://Resources.mlflow_experiment_path is already pinned to
# /Users/<user_email>/mlflow/<APP_NAME>-agent by vibecoding-state.migrate_canonical.
experiment_path = state["Resources"]["mlflow_experiment_path"]
mlflow.set_experiment(experiment_path)
```

Stand-alone projects build the path from the same identity inputs:

```python
import mlflow

user_email = "jane.doe@example.com"
app_name = "jane-d-stayfinder"  # ${FIRSTNAME}-${LASTINITIAL}-${use_case_slug}
experiment_path = f"/Users/{user_email}/mlflow/{app_name}-agent"
mlflow.set_experiment(experiment_path)
```

Set the experiment early in your entrypoint — before enabling autolog and making any LLM calls. **Never** use a literal leaf like `traces`, `Tracing`, or `my-agent`; the leaf is the only thing surfacing in the MLflow UI search column and a generic value defeats per-attendee isolation.

For complete experiment organization patterns including `ExperimentManager`, search, cleanup, and decision tables, see: [`references/experiment-organization.md`](references/experiment-organization.md).

## CRITICAL: Prompt registry linkage

Prompts registered in Unity Catalog must be linked to the experiment or they **will not** surface correctly in the Experiment UI for prompt-aware workflows.

After `set_experiment`, set the experiment tag:

```python
mlflow.set_experiment_tags({
    "mlflow.promptRegistryLocation": f"{catalog}.{schema}",
})
```

Use your UC catalog and schema where prompts are registered. Without `mlflow.promptRegistryLocation`, UC-registered prompts may not appear as expected in the UI.

## Tracing with decorators

Use `@mlflow.trace` for automatic span creation around functions. Pick a **name** and **span_type** that match how you want traces grouped in the UI.

```python
import mlflow


@mlflow.trace(name="classify_intent", span_type="AGENT")
def classify_intent(query: str) -> dict:
    ...


@mlflow.trace(name="call_llm", span_type="LLM")
def call_llm(prompt: str) -> str:
    ...


@mlflow.trace(name="evaluate_response", span_type="JUDGE")
def evaluate_response(response: str) -> float:
    ...
```

Common **span_type** values: `AGENT`, `TOOL`, `LLM`, `RETRIEVER`, `JUDGE`, `EMBEDDING`. Align names with your team's conventions so traces stay searchable across services.

For complete decorator and async tracing examples, see: [`references/tracing-patterns.md`](references/tracing-patterns.md).

For the **20+ `mlflow.<library>.autolog()` integrations** (OpenAI, Anthropic, Mistral, LangChain, LangGraph, LlamaIndex, DSPy, LiteLLM, etc.), the **multi-framework combine** snippet, and the **serverless-compute caveat** (autolog is not auto-enabled), see [`references/autolog-integrations.md`](references/autolog-integrations.md).

## Manual span creation

For fine-grained control (nested work units, partial inputs/outputs, retries), use `mlflow.start_span`. This pattern matches how the optimizer wraps LLM calls.

For complex tracing, open a span with `span_type=SpanType.CHAIN`, set inputs before the call, record token usage, and set outputs on success or failure — including retry events via `SpanEvent`.

Illustrative nested pattern (same structural idea: parent span, child LLM span, explicit inputs/outputs):

```python
import mlflow


def run_optimization_step(query, context):
    with mlflow.start_span(name="optimization_step") as span:
        span.set_inputs({"query": query})

        with mlflow.start_span(name="strategist_call", span_type="LLM") as llm_span:
            llm_span.set_inputs({"prompt": formatted_prompt})
            result = call_llm(formatted_prompt)
            llm_span.set_outputs({"response": result})

        span.set_outputs({"result": result})
        return result
```

In production code you may prefer `from mlflow.entities import SpanType` and types such as `SpanType.CHAIN` for LLM orchestration spans, consistent with `_traced_llm_call`.

For the full `_traced_llm_call` implementation, error handling, token logging, and a multi-step agent example with nested AGENT/LLM/TOOL/JUDGE spans, see: [`references/tracing-patterns.md`](references/tracing-patterns.md).

## Trace tags and metadata

Enrich the **current trace** with session, user, and deployment context so
runs are filterable and attributable. Reserved identity fields belong
under `metadata=` (immutable, MLflow-recognized for UI filter / group);
mutable routing dimensions belong under `tags=`.

```python
import os

mlflow.update_current_trace(
    metadata={
        "mlflow.trace.user":    user_id,
        "mlflow.trace.session": session_id,
        "mlflow.source.type":   os.getenv("APP_ENVIRONMENT", "development"),
        "agent_version":        "1.2.0",
        "space_id":             space_id,
    },
    tags={
        "domain":   domain,
        "sla_tier": "gold",
    },
)
```

Call this from code that runs inside an active trace (for example after `mlflow.start_run` / autolog / `@mlflow.trace` has established trace context). Setting `mlflow.trace.user` / `mlflow.trace.session` under `tags=` still works for read-back but loses the immutability guarantee and the UI's first-class user / session facets — prefer metadata.

For the full tag taxonomy, metadata patterns, trace search queries, and monitoring dashboard integration, see: [`references/trace-context-patterns.md`](references/trace-context-patterns.md). For the canonical reference on user / session / environment context (auto-populated metadata, `APP_ENVIRONMENT` override, search by metadata), see [`02c-trace-context-and-environments`](../02c-trace-context-and-environments/SKILL.md).

## Connection pool configuration

Reduce flaky failures under load by setting MLflow HTTP client defaults **before** heavy tracing or evaluation traffic:

```python
import os

os.environ.setdefault("MLFLOW_HTTP_REQUEST_MAX_RETRIES", "5")
os.environ.setdefault("MLFLOW_HTTP_REQUEST_TIMEOUT", "120")
```

Set these as early as possible in the job or app entrypoint (alongside other MLflow env vars from Foundation Step 1). Adjust retries and timeout for your workspace network and batch sizes.

For connection pool tuning in high-throughput serving scenarios and async tracing performance tips, see: [`references/tracing-patterns.md` § 8](references/tracing-patterns.md#8-performance-tips-for-high-throughput-tracing).

## DO / DON'T examples

### Experiment organization

**DO** — Pin the experiment leaf to the user-and-use-case identity, and prefer reading from `vibecoding-state`:

```python
# In a workshop-managed project, read the pre-derived path from state.
experiment_path = state["Resources"]["mlflow_experiment_path"]
# e.g. "/Users/jane.doe@example.com/mlflow/jane-d-stayfinder-agent"
mlflow.set_experiment(experiment_path)
```

```python
# Stand-alone project — build the path from the same identity inputs.
user_email = "jane.doe@example.com"
app_name = "jane-d-stayfinder"  # ${FIRSTNAME}-${LASTINITIAL}-${use_case_slug}
experiment_path = f"/Users/{user_email}/mlflow/{app_name}-agent"
mlflow.set_experiment(experiment_path)
```

**DON'T** — Use a generic leaf, a hand-rolled `/Shared/...` default, or a hard-coded workspace path. The leaf is what shows up in the MLflow UI experiment list, and `traces` / `Tracing` / `my-agent` give every attendee on a shared workspace the same name:

```python
# WRONG: generic leaf — collides across attendees, useless in the UI
mlflow.set_experiment("/Shared/my-agent/traces")

# WRONG: hard-coded workspace path that won't work across workspaces
mlflow.set_experiment("/Shared/my-specific-workspace-path/eval")
```

### Tracing inputs and outputs

**DO** — Set inputs before the work and outputs after, including on failure:

```python
with mlflow.start_span(name="llm_call", span_type=SpanType.CHAIN) as span:
    span.set_inputs({"prompt_chars": len(prompt), "model": model_name})
    try:
        result = call_llm(prompt)
        span.set_outputs({"response_chars": len(result), "status": "ok"})
    except Exception as exc:
        span.set_outputs({"error": str(exc)[:500], "status": "error"})
        raise
```

**DON'T** — Skip inputs/outputs or only record on success:

```python
# WRONG: no inputs recorded, no outputs on failure path
with mlflow.start_span(name="llm_call") as span:
    result = call_llm(prompt)
    span.set_outputs({"result": result})  # never reached if call_llm raises
```

### Trace context tags

**DO** — Put reserved identity fields (`mlflow.trace.user` / `mlflow.trace.session`) under metadata, mutable routing dimensions under tags:

```python
mlflow.update_current_trace(
    metadata={
        "mlflow.trace.user":    user_id,
        "mlflow.trace.session": session_id,
        "space_id":             space_id,
        "agent_version":        "1.2.0",
    },
    tags={
        "domain":     domain,
        "sla_tier":   "gold",
    },
)
```

**DON'T** — Put `mlflow.trace.user` / `mlflow.trace.session` under tags, or skip context entirely:

```python
# WRONG: reserved identity fields under tags — loses immutability + UI facets
mlflow.update_current_trace(
    tags={"mlflow.trace.user": user_id, "mlflow.trace.session": session_id},
)

# WRONG: no context at all — traces become impossible to attribute or group
# (just calling the function without update_current_trace)
```

### Connection pool timing

**DO** — Set HTTP env vars at the top of your entrypoint, before any MLflow call:

```python
import os
os.environ.setdefault("MLFLOW_HTTP_REQUEST_MAX_RETRIES", "5")
os.environ.setdefault("MLFLOW_HTTP_REQUEST_TIMEOUT", "120")

import mlflow  # env vars are read at import time
```

**DON'T** — Set env vars after MLflow is imported or mid-pipeline:

```python
import mlflow  # already imported — env vars may be cached

# WRONG: setting after import may not take effect
os.environ["MLFLOW_HTTP_REQUEST_MAX_RETRIES"] = "5"
```

## Unity Catalog OTEL trace storage (MLflow 3.11+)

Store MLflow traces in Unity Catalog Delta tables using an OpenTelemetry-compatible format. This enables SQL-queryable, long-term trace retention with UC access control, unlike the default experiment-scoped storage which is limited in retention and query flexibility.

### When to use UC OTEL storage

| Scenario | Default Experiment Storage | UC OTEL Storage |
|----------|---------------------------|-----------------|
| Development debugging | ✓ Sufficient | Optional |
| Production monitoring | Limited retention | ✓ Recommended |
| Compliance / audit trails | Not durable | ✓ Required |
| Cross-experiment analysis | Difficult | ✓ SQL joins across tables |
| Dashboard SQL queries | Not supported | ✓ Native SQL access |
| Role-based access control | Experiment-level only | ✓ UC table-level ACLs |

### Enable UC OTEL trace storage

Bind an experiment to a Unity Catalog location so traces flow into Delta tables:

```python
import os
import mlflow
from mlflow.entities.trace_location import UnityCatalog

mlflow.set_tracking_uri("databricks")

# Required: SQL warehouse for writing traces to Delta tables
os.environ["MLFLOW_TRACING_SQL_WAREHOUSE_ID"] = "<SQL_WAREHOUSE_ID>"

experiment = mlflow.set_experiment(
    # Read from state — pinned to /Users/<user_email>/mlflow/<APP_NAME>-agent.
    experiment_name=state["Resources"]["mlflow_experiment_path"],
    trace_location=UnityCatalog(
        catalog_name="main",
        schema_name="agent_traces",
        # The prefix MUST mirror APP_NAME (underscored for table-name safety),
        # e.g. "jane_d_stayfinder" — never a generic "my_agent".
        table_prefix="my_agent",
    ),
)
```

This creates **four Delta tables** in the specified UC schema (with `<table_prefix>` bound to the underscored `APP_NAME`):

| Table | Content |
|-------|---------|
| `my_agent_otel_annotations` | Trace-level annotations, tags, and feedback |
| `my_agent_otel_logs` | Structured log events within spans |
| `my_agent_otel_metrics` | Numeric metrics (token usage, latency, scores) |
| `my_agent_otel_spans` | Span hierarchy with inputs, outputs, timing, status |

### CRITICAL: Table permissions

UC OTEL tables require **explicit** `MODIFY` + `SELECT` grants (not `ALL_PRIVILEGES`) on each table for the service principal and any readers:

```sql
-- Grant write access to the app's service principal
GRANT MODIFY, SELECT ON TABLE main.agent_traces.my_agent_otel_annotations TO `<app-sp>`;
GRANT MODIFY, SELECT ON TABLE main.agent_traces.my_agent_otel_logs TO `<app-sp>`;
GRANT MODIFY, SELECT ON TABLE main.agent_traces.my_agent_otel_metrics TO `<app-sp>`;
GRANT MODIFY, SELECT ON TABLE main.agent_traces.my_agent_otel_spans TO `<app-sp>`;

-- Grant read access to analysts / dashboards
GRANT SELECT ON TABLE main.agent_traces.my_agent_otel_spans TO `analysts`;
GRANT SELECT ON TABLE main.agent_traces.my_agent_otel_metrics TO `analysts`;
```

### Enable monitoring with UC OTEL

For production monitoring scorers to write results back to UC OTEL tables, bind the SQL warehouse ID:

```python
from mlflow.tracing import set_databricks_monitoring_sql_warehouse_id

set_databricks_monitoring_sql_warehouse_id(
    sql_warehouse_id="<SQL_WAREHOUSE_ID>",
    experiment_id=experiment.experiment_id,
)
```

Call this at application startup, alongside `set_experiment`. Without it, registered scorers (SDLC Step 7) cannot persist results to UC OTEL tables.

### Query UC OTEL traces with SQL

Once traces flow into UC Delta tables, query them directly:

```sql
-- Recent traces with latency
SELECT
    trace_id,
    span_name,
    start_time,
    end_time,
    TIMESTAMPDIFF(MILLISECOND, start_time, end_time) AS duration_ms,
    status_code
FROM main.agent_traces.my_agent_otel_spans
WHERE start_time > DATEADD(HOUR, -24, CURRENT_TIMESTAMP())
ORDER BY start_time DESC
LIMIT 100;

-- Token usage by model
SELECT
    JSON_EXTRACT_SCALAR(attributes, '$.llm.model') AS model,
    SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.llm.token_count.prompt') AS INT)) AS prompt_tokens,
    SUM(CAST(JSON_EXTRACT_SCALAR(attributes, '$.llm.token_count.completion') AS INT)) AS completion_tokens
FROM main.agent_traces.my_agent_otel_spans
WHERE span_kind = 'LLM'
  AND start_time > DATEADD(DAY, -7, CURRENT_TIMESTAMP())
GROUP BY 1;
```

### DO — Set warehouse ID before creating the experiment

```python
import os
os.environ["MLFLOW_TRACING_SQL_WAREHOUSE_ID"] = "<WAREHOUSE_ID>"

import mlflow
from mlflow.entities.trace_location import UnityCatalog

experiment = mlflow.set_experiment(
    # /Users/<user_email>/mlflow/<APP_NAME>-agent — read from state.
    experiment_name=state["Resources"]["mlflow_experiment_path"],
    trace_location=UnityCatalog(
        catalog_name="main",
        schema_name="agent_traces",
        table_prefix="my_agent",  # MUST mirror underscored APP_NAME in production
    ),
)
```

### DON'T — Create the experiment without the warehouse env var

```python
import mlflow
from mlflow.entities.trace_location import UnityCatalog

# WRONG: MLFLOW_TRACING_SQL_WAREHOUSE_ID not set — tables can't be written
experiment = mlflow.set_experiment(
    experiment_name=state["Resources"]["mlflow_experiment_path"],
    trace_location=UnityCatalog(
        catalog_name="main",
        schema_name="agent_traces",
        table_prefix="my_agent",
    ),
)
```

### DON'T — Use ALL_PRIVILEGES instead of explicit grants

```sql
-- WRONG: ALL_PRIVILEGES does not always include MODIFY for OTEL writes
GRANT ALL_PRIVILEGES ON TABLE main.agent_traces.my_agent_otel_spans TO `<sp>`;

-- DO: Explicit MODIFY + SELECT
GRANT MODIFY, SELECT ON TABLE main.agent_traces.my_agent_otel_spans TO `<sp>`;
```

### F2 owns OTel grants and warehouse env (state capture)

F2 is the **single owner** of the OTel infrastructure contract — the Delta
table prefix, the SQL warehouse env var, and the explicit per-table grants
applied to the app service principal. Downstream skills (Track A 07 deploy,
SDLC 06 deployment, SDLC 07 monitoring) **do not** re-derive any of these;
they read them from state. The `f2_grants_complete` flag is the single
gate read by `preflight_check_registry.f2_grants_complete` and by
`deferred_actions[]` to unblock downstream prompts.

Capture these fields in state once F2 finishes provisioning:

```yaml
# state://Foundation.f2_tracing
f2_grants_complete: true               # bool — set true only after every grant in app_service_principal_grants[] succeeds
otel_table_prefix: "my_agent"          # string — value passed to UnityCatalog(table_prefix=...); MUST match the literal string used; do NOT add a trailing underscore (MLflow appends `_otel_*`)
mlflow_tracing_sql_warehouse_id: "<warehouse-id>"  # canonical env var MLFLOW_TRACING_SQL_WAREHOUSE_ID; preflight_check_registry.mlflow_tracing_sql_warehouse_id_present reads this
app_service_principal_grants:          # one entry per (principal, object) tuple actually applied
  - principal: "<app-sp-application-id>"   # Databricks Apps SP application id (UUID), not display name
    object: "main.agent_traces.my_agent_otel_annotations"
    privileges: [MODIFY, SELECT]
  - principal: "<app-sp-application-id>"
    object: "main.agent_traces.my_agent_otel_logs"
    privileges: [MODIFY, SELECT]
  - principal: "<app-sp-application-id>"
    object: "main.agent_traces.my_agent_otel_metrics"
    privileges: [MODIFY, SELECT]
  - principal: "<app-sp-application-id>"
    object: "main.agent_traces.my_agent_otel_spans"
    privileges: [MODIFY, SELECT]
```

**Rules:**

- `otel_table_prefix` is the literal string passed to
  `UnityCatalog(table_prefix=...)` — **no trailing underscore**. MLflow
  appends `_otel_annotations` / `_otel_logs` / `_otel_metrics` /
  `_otel_spans`. Passing `my_agent_` produces `my_agent__otel_*` (double
  underscore) and breaks downstream queries; this is a recurring
  retrospective failure. The Track A and SDLC deploy skills read this
  field rather than re-deriving the prefix from the experiment name.
- `mlflow_tracing_sql_warehouse_id` is the canonical name from
  `canonical_names.env_vars`. `preflight_check_registry.mlflow_tracing_sql_warehouse_id_present`
  fails closed if it is missing or empty — apps deployed without it
  silently drop UC OTel writes.
- `app_service_principal_grants[]` enumerates **explicit** `MODIFY,
  SELECT` grants on each of the four `*_otel_*` tables (annotations,
  logs, metrics, spans) for the agent's deployment SP. `ALL_PRIVILEGES`
  is **not equivalent** for OTel writes — capture the literal grant
  applied. Track A 07 / SDLC 06 inspect this list at deploy time.
- `f2_grants_complete: true` is the single gate. Set it only after every
  entry in `app_service_principal_grants[]` has been verified
  (`SHOW GRANTS ON TABLE ... TO `<sp>`` returns the recorded
  privileges). Until it is `true`, every prompt role listed under
  `preflight_check_registry.f2_grants_complete.blocks_prompt_roles[]`
  halts on `enter`.

## OTeL GenAI Semantic-Convention Attributes

MLflow's trace UI and search indexing recognize a specific set of OpenTelemetry GenAI semantic-convention attributes (`gen_ai.*`, `session.id`, `user.id`). Spans that set these attributes render richer in the UI (clean prompt/response panes, token counts, session grouping) and become searchable via the MLflow API. Spans that skip them still work but show up as plain generic spans.

This matters most when you write **custom spans** (manual `mlflow.start_span`) or when you wire a **3rd-party OTeL SDK** (e.g. a home-grown agent framework) into MLflow tracing.

### Core attributes

| Attribute | Meaning | Where to set |
|-----------|---------|--------------|
| `gen_ai.operation.name` | `chat`, `completion`, `embedding`, `tool_call` | Every LLM/tool span |
| `gen_ai.system` | `anthropic`, `openai`, `databricks` | LLM spans |
| `gen_ai.request.model` | Model id (e.g. `databricks-claude-sonnet-4-6`) | LLM spans |
| `gen_ai.input.messages` | JSON array of messages sent to the model | LLM spans |
| `gen_ai.output.messages` | JSON array of messages returned | LLM spans |
| `gen_ai.usage.input_tokens` | Prompt tokens | LLM spans |
| `gen_ai.usage.output_tokens` | Completion tokens | LLM spans |
| `gen_ai.tool.name` | Tool invoked | Tool spans |
| `gen_ai.tool.arguments` | Tool arguments (JSON) | Tool spans |
| `session.id` | Conversation / session correlation id | Root span of every turn |
| `user.id` | Authenticated user id | Root span of every turn |

### Setting attributes in manual spans

```python
import mlflow, json

with mlflow.start_span(name="call_llm", span_type="LLM") as span:
    span.set_attributes({
        "gen_ai.operation.name":      "chat",
        "gen_ai.system":              "databricks",
        "gen_ai.request.model":       "databricks-claude-sonnet-4-6",
        "gen_ai.input.messages":      json.dumps(messages),
    })

    resp = client.chat.completions.create(...)

    span.set_attributes({
        "gen_ai.output.messages":     json.dumps([resp.choices[0].message.model_dump()]),
        "gen_ai.usage.input_tokens":  resp.usage.prompt_tokens,
        "gen_ai.usage.output_tokens": resp.usage.completion_tokens,
    })
```

For MLflow-native filter / group / cohort views, prefer the reserved
**metadata** keys `mlflow.trace.user` / `mlflow.trace.session` over the
OTeL dotted-attribute form:

```python
mlflow.update_current_trace(metadata={
    "mlflow.trace.user":    user_id,
    "mlflow.trace.session": session_id,
})
```

The OTeL `session.id` / `user.id` form is the **span-attribute**
equivalent for third-party OTeL integrations (set on individual spans
via `span.set_attributes(...)`). The MLflow form (metadata on the trace
root) is preferred for first-party MLflow tracing because it's
immutable post-log and lights up the Trace UI's user / session
facets. See [`02c-trace-context-and-environments`](../02c-trace-context-and-environments/SKILL.md)
for the full pattern.

### Searching traces by gen_ai attributes

```python
import mlflow

traces = mlflow.search_traces(
    experiment_names=["/Shared/skyloyalty/agent"],
    filter_string="span_attributes['gen_ai.request.model'] = 'databricks-claude-sonnet-4-6'"
                  " AND tags['session.id'] = 'abc-123'",
    max_results=100,
)
```

Without these attributes, the best you can do is filter by trace name or timestamp — much coarser.

### Third-party OTeL integration

If your agent uses a non-MLflow OTeL SDK (e.g. OpenTelemetry Python directly, or a framework's built-in tracer), configure the OTeL exporter to target MLflow's tracing endpoint and ensure your spans follow the `gen_ai.*` naming. The Databricks docs have the full list and any MLflow-specific extensions.

See [Databricks: OTeL span attributes for 3rd-party integrations](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/third-party/otel-span-attributes) for the complete attribute reference.

### Do / Don't

| DO | DON'T |
|----|-------|
| Set `gen_ai.operation.name` on every LLM/tool span. | Leave span attributes empty and expect rich UI rendering. |
| Store messages as JSON in `gen_ai.input.messages` / `gen_ai.output.messages`. | Store them as Python dicts — JSON-encode first. |
| Set `mlflow.trace.user` / `mlflow.trace.session` (metadata) on the trace root, not each span. | Repeat them on every span, or store them under tags — wastes storage and loses UI facets. |
| Use `span_attributes['gen_ai.*']` in `search_traces` filters. | Parse trace JSON by hand to filter offline. |
| Include `gen_ai.usage.*_tokens` when available. | Let cost dashboards estimate tokens from request length. |

---

## Validation checklist

- [ ] Experiment path follows the template convention (`EXPERIMENT_PATH_TEMPLATE` + `format_mlflow_template`)
- [ ] `mlflow.promptRegistryLocation` tag set on the experiment (UC catalog.schema)
- [ ] `@mlflow.trace` on main agent-facing functions where automatic spans are enough
- [ ] Span types assigned consistently (`AGENT`, `LLM`, `TOOL`, `JUDGE`, etc.)
- [ ] Trace metadata includes `mlflow.trace.user`, `mlflow.trace.session`, and `mlflow.source.type` (overridden from `APP_ENVIRONMENT`); see [F2c](../02c-trace-context-and-environments/SKILL.md)
- [ ] Connection pool / HTTP retry and timeout env vars set for production-scale workloads
- [ ] (UC OTEL) `MLFLOW_TRACING_SQL_WAREHOUSE_ID` env var set before `set_experiment`
- [ ] (UC OTEL) `trace_location=UnityCatalog(...)` configured with correct catalog, schema, table prefix
- [ ] (UC OTEL) `otel_table_prefix` captured in state with **no trailing underscore** (matches the literal string passed to `UnityCatalog(table_prefix=...)`)
- [ ] (UC OTEL) All four `*_otel_*` tables have explicit `MODIFY` + `SELECT` grants for the app SP (not `ALL_PRIVILEGES`); each grant captured under `app_service_principal_grants[]`
- [ ] (UC OTEL) `mlflow_tracing_sql_warehouse_id` captured in state (canonical env-var name) so `preflight_check_registry.mlflow_tracing_sql_warehouse_id_present` passes for all downstream prompt roles
- [ ] (UC OTEL) `f2_grants_complete: true` written to state **only after** every grant in `app_service_principal_grants[]` is verified — this gate unblocks every prompt role listed in `preflight_check_registry.f2_grants_complete.blocks_prompt_roles[]`
- [ ] (UC OTEL) `set_databricks_monitoring_sql_warehouse_id()` called for production monitoring integration
- [ ] (gen_ai attrs) Manual spans set `gen_ai.operation.name` and relevant `gen_ai.*` fields per OTeL GenAI semantic conventions
- [ ] (gen_ai attrs) Trace root sets `mlflow.trace.user` / `mlflow.trace.session` (metadata) — preferred over the OTeL `session.id` / `user.id` span-attribute form for first-party MLflow tracing

## References

### Official documentation

- [MLflow tracing overview](https://mlflow.org/docs/latest/genai/tracing/index.html)
- [Databricks: MLflow 3 and GenAI](https://docs.databricks.com/en/mlflow/index.html) (tracing, evaluation, and workspace-specific behavior)
- [Trace tags and metadata](https://mlflow.org/docs/latest/genai/tracing/tracing-schema.html) (tag keys, `update_current_trace`)
- [Store MLflow traces in Unity Catalog](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog) (UC OTEL trace storage, table schema, permissions)
- [Enable production monitoring with UC traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog#enable-production-monitoring) (monitoring SQL warehouse binding)
- [Third-party OTeL span attributes for GenAI](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/third-party/otel-span-attributes) (gen_ai.* semantic-convention reference)
- [Add traces to applications: automatic and manual tracing](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/) (decision matrix for auto / manual / combined)
- [Automatic tracing](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/automatic) (20+ supported libraries)
- [Trace agents deployed on Databricks](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing) (production env vars, Production Monitoring → Delta)
- [Instrument Node.js applications with MLflow Tracing](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/app-instrumentation/typescript-sdk) (companion sibling skill: [`02b-typescript-tracing`](../02b-typescript-tracing/SKILL.md))
- [Add context to traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces?language=Production) (canonical reference for `mlflow.trace.user` / `mlflow.trace.session` / environment metadata — sibling skill: [`02c-trace-context-and-environments`](../02c-trace-context-and-environments/SKILL.md))

### Related skills

- [Foundation Step 1: MLflow GenAI Foundation](../01-mlflow-genai-foundation/SKILL.md) — tracking URI, auth, environment detection
- [Foundation Step 2b: TypeScript tracing](../02b-typescript-tracing/SKILL.md) — Node sibling using the official `mlflow-tracing` npm SDK
- [Foundation Step 2c: Trace context and environments](../02c-trace-context-and-environments/SKILL.md) — canonical user / session / environment metadata + `APP_ENVIRONMENT` override

The patterns in this skill are demonstrated in the
[Genie Space Optimizer](../../README.md) reference implementation. In your
own project, apply them to your module structure.

### Local reference files

| Reference | Lines | Content |
| --- | --- | --- |
| [`references/experiment-organization.md`](references/experiment-organization.md) | ~300 | `ExperimentManager` class, path templates, tagging strategies, search & cleanup |
| [`references/tracing-patterns.md`](references/tracing-patterns.md) | ~350 | All span types, decorator/manual tracing, nested agents, error handling, perf tips |
| [`references/trace-context-patterns.md`](references/trace-context-patterns.md) | ~200 | Tag taxonomy, metadata patterns, trace search, dashboard integration |
| [`references/autolog-integrations.md`](references/autolog-integrations.md) | ~250 | 20+ `mlflow.<library>.autolog()` integrations, multi-framework combine, serverless caveat |
| [`references/prod-tracing-deployment.md`](references/prod-tracing-deployment.md) | ~250 | Production deployment env-var matrix: Agent Framework auto-tracing, custom CPU serving (`ENABLE_MLFLOW_TRACING`, `MLFLOW_EXPERIMENT_ID`, SP `CAN_EDIT`), Git-folder caveat, Production Monitoring → Delta, AI Gateway alternative |

## Version history

| Version | Date | Changes |
| --- | --- | --- |
| 3.6.0 | 2026-04-26 | F2 now owns the OTel grants + warehouse env contract. Added "F2 owns OTel grants and warehouse env (state capture)" subsection capturing `f2_grants_complete`, `otel_table_prefix`, `mlflow_tracing_sql_warehouse_id`, and `app_service_principal_grants[]` so downstream skills (Track A 07, SDLC 06/07) read them from state instead of re-deriving. Documents the `gw`-style "no trailing underscore" trap (passing `my_agent_` produces `my_agent__otel_*`). Validation checklist gates the four fields. Closes the rollup "`UCSchemaLocation` vs `UnityCatalog(table_prefix=...)`" row. |
| 3.5.0 | 2026-04-24 | Modernized "Trace tags and metadata" + DO/DON'T examples to put `mlflow.trace.user` / `mlflow.trace.session` under `metadata=` (immutable, MLflow-recognized) instead of `tags=`. Updated OTeL section to prefer the metadata form over the `session.id` / `user.id` span-attribute form. Added F2c sibling-skill callout. Updated validation checklist + grounded_in metadata. |
| 3.4.0 | 2026-04-24 | Added auto-vs-manual-vs-combined decision matrix (sourced from app-instrumentation overview). Added TypeScript / Node sibling-skill callout (F2b). Added production-deployment callout pointing at `references/prod-tracing-deployment.md`. New references: `autolog-integrations.md` (20+ libraries), `prod-tracing-deployment.md` (env-var matrix). Updated grounded_in metadata. |
| 3.3.0 | 2026-04-19 | Added OTeL GenAI semantic-convention attributes section: `gen_ai.*` attributes, `session.id` / `user.id`, search filters, 3rd-party OTeL integration link. Extended validation checklist. |
| 3.2.0 | 2026-04-10 | Added Unity Catalog OTEL trace storage section (MLflow 3.11+): `trace_location=UnityCatalog(...)`, 4-table schema, MODIFY+SELECT grants, monitoring warehouse binding, SQL query examples, DO/DON'T pairs. Updated validation checklist and references. |
| 3.1.0 | 2026-03-26 | Added reference files, DO/DON'T examples, version history, connection pool reference pointer |
| 3.0.0 | 2026-03-25 | Initial structured skill with experiment organization, tracing, trace context, and connection pool |
