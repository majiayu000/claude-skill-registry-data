---
name: 02c-trace-context-and-environments
description: >
  Use when adding user, session, environment, or version context to MLflow
  traces — Python or TypeScript. Covers the reserved metadata fields
  (`mlflow.trace.user`, `mlflow.trace.session`), auto-populated environment
  metadata (`mlflow.source.*`, Git provenance, model id), the
  `APP_ENVIRONMENT` override pattern for production, custom deployment
  metadata, and how this composes with `client_request_id` and `gen_ai.*`.
  Foundation Step 2c. Sibling to F2 (Python tracing) and F2b (TS tracing).
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Trace-context metadata configuration (user/session/environment/version) — no deployed resource; identical on both clients. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-04-15"
  volatility: medium
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.0.0"
  domain: "genai-agents"
  pipeline_position: "F2c"
  consumes: "tracing_config"
  produces: "trace_context_metadata"
  grounded_in: "docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces, docs.databricks.com/aws/en/mlflow3/genai/tracing/track-environments-context, docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing"
---

# Trace context and environments — users, sessions, deployment metadata

## When to Use

Use this skill when you need to:

- Attribute traces to a **user** (`mlflow.trace.user`).
- Group traces from a multi-turn conversation under one **session**
  (`mlflow.trace.session`).
- Tag traces with the **deployment environment** (`development`,
  `staging`, `production`) and the **app version** so you can debug
  regressions and compare cohorts.
- Search traces programmatically by user, session, or environment.
- Pair trace-side user attribution with end-user feedback collection
  (see [`sdlc/04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md)).

This skill applies to **both** Python ([F2](../02-experiment-tracing-and-uc-storage/SKILL.md))
and TypeScript ([F2b](../02b-typescript-tracing/SKILL.md)) tracing. The
concepts are identical; the call sites differ.

Prerequisites:

- Foundation Step 1 (MLflow environment, tracking URI, auth).
- Foundation Step 2 or 2b (tracing already wired — `@mlflow.trace`,
  `mlflow.openai.autolog()`, or `tracedOpenAI`).
- **MLflow 3** required (`mlflow[databricks]>=3.1`). Context tracking
  is not supported on MLflow 2.x.

> **Source:** [Add context to traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces?language=Production).

## Tags vs metadata — pick the right bucket

`mlflow.update_current_trace(tags=..., metadata=...)` accepts both. The
two buckets serve different purposes and the Databricks UI treats
reserved metadata fields specially.

| Property | Tags | Metadata |
|---|---|---|
| **Mutability after log** | Mutable (you can update them later) | **Immutable** once the trace is logged |
| **UI affordances** | Filter columns | Filter columns + first-class facets for reserved keys (`mlflow.trace.user`, `mlflow.trace.session`) |
| **Best for** | Routing dimensions that may change during the trace (`feature_flag_active`, `retry_count`, `degraded_mode`) | Stable identifiers and version pins (`mlflow.trace.user`, `mlflow.trace.session`, `agent_version`, `deployment_id`) |
| **Typical examples** | `domain`, `team`, `sla_tier`, `experiment_arm` | `mlflow.trace.user`, `mlflow.trace.session`, `mlflow.source.type`, `agent_version`, `deployment_region` |

**Rule of thumb:** if the value is **the identity of something** (a user,
a session, a build), use metadata. If it's **a label you might revisit**,
use tags.

## Track users and sessions

MLflow defines two reserved metadata fields. Use these — not custom keys —
so the UI's filter / group / cohort views light up.

| Field | Purpose |
|---|---|
| `mlflow.trace.user` | Authenticated user id (email, SP id, OBO-resolved username). |
| `mlflow.trace.session` | Conversation / multi-turn session id. |

### Python (`@mlflow.trace`-wrapped handler)

```python
import mlflow


@mlflow.trace(name="answer", span_type="AGENT")
def answer(question: str, *, user_id: str, session_id: str) -> str:
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user":    user_id,
            "mlflow.trace.session": session_id,
        },
    )
    return _plan_and_execute(question)
```

Call `update_current_trace(metadata=...)` **inside** an active trace
context — typically as the first statement in your request handler,
before any LLM call. Calling it before the trace opens is a no-op.

### TypeScript (`mlflow-tracing` SDK)

```ts
import * as mlflow from "mlflow-tracing";

mlflow.update_current_trace({
  session_id: req.headers["x-session-id"] as string,
  user_id: resolvedUserId,
});
```

The TS SDK's `session_id` / `user_id` shorthand keys map to the same
reserved metadata fields (`mlflow.trace.session` / `mlflow.trace.user`).
See [F2b § Sessions and users](../02b-typescript-tracing/SKILL.md#sessions-and-users)
for the full handler shape.

> **Why metadata, not tags?** The doc explicitly recommends metadata
> because: (a) these IDs are immutable identifiers — they should not
> change after the trace is logged; and (b) MLflow treats them as
> first-class facets only when stored as metadata under the reserved
> keys. Older code that placed them under tags works for read but
> loses the UI affordances.

## Track environments and versions

### Auto-populated metadata

MLflow auto-fills several metadata fields from your runtime. You don't
have to set these — but you should know what's there so you don't
double-write.

| Field | Set automatically from |
|---|---|
| `mlflow.source.name` | Script filename, notebook name. |
| `mlflow.source.git.commit` | Current Git commit hash, if running in a Git repo. |
| `mlflow.source.git.branch` | Current Git branch. |
| `mlflow.source.git.repoURL` | Git remote URL. |
| `mlflow.source.type` | `NOTEBOOK` (Jupyter / Databricks notebook), `LOCAL` (Python script), or `UNKNOWN`. **Override this in deployed apps.** |
| `mlflow.sourceRun` | The MLflow run id, if the trace was created inside `mlflow.start_run()`. |
| `metadata.mlflow.modelId` | The active `LoggedModel` id (from `MLFLOW_ACTIVE_MODEL_ID` or `mlflow.set_active_model()`). |

### Override `mlflow.source.type` from `APP_ENVIRONMENT`

In production, `mlflow.source.type` defaults to `LOCAL` or `UNKNOWN`,
which is misleading. Override it from an environment variable that the
deployment sets:

```python
import os
import mlflow


def trace_environment_metadata() -> dict[str, str]:
    return {
        "mlflow.source.type": os.getenv("APP_ENVIRONMENT", "development"),
    }


@mlflow.trace(name="answer", span_type="AGENT")
def answer(question: str, *, user_id: str, session_id: str) -> str:
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user":    user_id,
            "mlflow.trace.session": session_id,
            **trace_environment_metadata(),
        },
    )
    return _plan_and_execute(question)
```

Set `APP_ENVIRONMENT` per deployment via `databricks.yml` (Model Serving)
or `app.yaml` (Databricks Apps) — see
[`references/prod-tracing-deployment.md`](../02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md)
for the full env-var matrix.

```yaml
# app.yaml fragment
env:
  - name: APP_ENVIRONMENT
    value: "production"
```

> **Don't hard-code environment names** in the application source.
> Pulling from an env var means the same image runs in dev / staging /
> prod with different `mlflow.source.type` values.

## Custom deployment metadata

Add app-specific metadata for routing, version pinning, and audit. Pull
values from env vars, not literals, so the same code works across
deployments.

```python
import os
import mlflow


def deployment_metadata() -> dict[str, str]:
    return {
        "mlflow.source.type":   os.getenv("APP_ENVIRONMENT", "development"),
        "agent_version":        os.getenv("AGENT_VERSION", "unknown"),
        "deployment_id":        os.getenv("DEPLOYMENT_ID", "unknown"),
        "deployment_region":    os.getenv("DEPLOYMENT_REGION", "unknown"),
        "feature_flags":        os.getenv("FEATURE_FLAGS", ""),
    }


mlflow.update_current_trace(metadata=deployment_metadata())
```

Recommended custom-metadata keys:

| Key | Purpose |
|---|---|
| `agent_version` | Semantic version of the agent code (build tag). |
| `deployment_id` | Unique id per deploy (CI run id, asset bundle deployment id). |
| `deployment_region` | AWS region / Azure region where the workload runs. |
| `feature_flags` | Comma-separated active feature flags. Use tags instead if these change mid-trace. |

## Production package choice

| Environment | Install | Why |
|---|---|---|
| **Production** (Model Serving, Databricks Apps, batch jobs) | `pip install --upgrade mlflow-tracing` | Tracing-only, smaller dependency footprint, faster cold start, fewer transitive risks. |
| **Development** (notebooks, local CLI, eval runs that also need full MLflow features) | `pip install --upgrade "mlflow[databricks]>=3.1"` | Full SDK: experiments, runs, models, evaluation, registry. |

`mlflow-tracing` is API-compatible with `mlflow[databricks]` for the
tracing surface (`mlflow.trace`, `mlflow.update_current_trace`,
`mlflow.start_span`, `mlflow.search_traces` for tracing-only usage).
Use it on the deployed side; use `mlflow[databricks]` everywhere
else.

> MLflow 3 is required for context tracking. MLflow 2.x is **not
> supported** for `mlflow.trace.user` / `mlflow.trace.session` due to
> performance limitations and missing trace-info fields.

## Coexistence with `client_request_id` and `gen_ai.*`

Trace context is **layered** — these are not alternatives, they are
different scopes:

| Layer | Field | Where it lives | What it answers |
|---|---|---|---|
| Request correlation | `client_request_id` | `TraceInfo` (set via `mlflow.update_current_trace(client_request_id=...)`) | Which HTTP request produced this trace? |
| User attribution | `mlflow.trace.user` (metadata) | Trace root | Who triggered this trace? |
| Session grouping | `mlflow.trace.session` (metadata) | Trace root | Which conversation does this trace belong to? |
| Environment | `mlflow.source.type`, `agent_version`, `deployment_id` (metadata) | Trace root | Where / what version produced this trace? |
| Per-call OTeL | `gen_ai.operation.name`, `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.*` (span attributes) | Each LLM / tool span | What did this specific LLM call do? |

Set them all on the **same** trace. Reserved metadata + auto-populated
metadata + `client_request_id` go on the trace root (one
`update_current_trace` call). `gen_ai.*` go on the spans
(`span.set_attributes(...)` inside each LLM/tool call).

The composed call site looks like:

```python
import mlflow
import os


@mlflow.trace(name="answer", span_type="AGENT")
def answer(
    question: str,
    *,
    user_id: str,
    session_id: str,
    client_request_id: str,
) -> str:
    mlflow.update_current_trace(
        client_request_id=client_request_id,
        metadata={
            "mlflow.trace.user":    user_id,
            "mlflow.trace.session": session_id,
            "mlflow.source.type":   os.getenv("APP_ENVIRONMENT", "development"),
            "agent_version":        os.getenv("AGENT_VERSION", "unknown"),
        },
        tags={
            "domain":     "billing",
            "sla_tier":   "gold",
        },
    )
    return _plan_and_execute(question)
```

For `client_request_id` request-correlation patterns and the
frontend-handshake details, see
[`sdlc/04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md).
For the `gen_ai.*` semantic-convention attributes, see
[F2 § OTeL GenAI Semantic-Convention Attributes](../02-experiment-tracing-and-uc-storage/SKILL.md#otel-genai-semantic-convention-attributes).

## Search traces by metadata

Once metadata is on the trace, search by it with `mlflow.search_traces`.
The result is a pandas DataFrame; metadata appears in the `metadata`
column.

```python
import mlflow


# All traces from a specific user in production
df = mlflow.search_traces(
    experiment_names=["/Shared/skyloyalty/agent"],
    filter_string=(
        "metadata.`mlflow.trace.user` = 'alice@example.com' "
        "AND metadata.`mlflow.source.type` = 'production'"
    ),
    max_results=200,
)

# All traces in one conversation, ordered chronologically
df = mlflow.search_traces(
    experiment_names=["/Shared/skyloyalty/agent"],
    filter_string="metadata.`mlflow.trace.session` = 'sess-2026-04-24-abc'",
    order_by=["timestamp ASC"],
)

# Per-trace access from Trace objects
trace = mlflow.get_trace(trace_id)
print(trace.info.trace_metadata["mlflow.trace.user"])
print(trace.info.tags.get("domain"))
```

The DataFrame columns expose `metadata` (immutable, includes the
reserved keys) and `tags` (mutable). Filter by metadata for stable
identifiers; filter by tags for routing dimensions.

## DO / DON'T

| DO | DON'T |
|---|---|
| Put `mlflow.trace.user` / `mlflow.trace.session` under **metadata**. | Put them under tags — you lose the immutability guarantee and the UI's first-class filter/group affordances. |
| Override `mlflow.source.type` from `APP_ENVIRONMENT` in deployed code. | Hard-code `"production"` in the source. The same image should produce different traces in dev / staging / prod. |
| Pull `agent_version` / `deployment_id` from env vars set at deploy time. | Pin them as Python constants — they go stale at the next release. |
| Install `mlflow-tracing` in production images. | Install full `mlflow[databricks]` everywhere — slower cold start, larger image, more transitive deps. |
| Set metadata once at the top of the request handler, before any LLM call. | Sprinkle `update_current_trace` calls across child spans — wastes work and can race. |
| Use **metadata** for stable IDs and version pins; **tags** for routing dimensions that may change. | Mix the two — `mlflow.trace.user` belongs to metadata, `feature_flag_active` belongs to tags. |
| Compose user/session/environment metadata with `client_request_id` and `gen_ai.*` (they're layered, not alternatives). | Treat them as competing — they answer different questions. |

## Validation checklist

- [ ] `mlflow.trace.user` and `mlflow.trace.session` set under **metadata** (not tags) on the trace root, once per request.
- [ ] Set as the **first** call inside the traced request handler, before any LLM/tool call.
- [ ] `mlflow.source.type` overridden from `APP_ENVIRONMENT` env var in deployed code.
- [ ] `APP_ENVIRONMENT` set in `databricks.yml` (Model Serving) or `app.yaml` (Apps) per deployment.
- [ ] `agent_version` and (optional) `deployment_id` / `deployment_region` populated from env vars.
- [ ] Production image installs `mlflow-tracing` (not full `mlflow[databricks]`) for footprint.
- [ ] MLflow runtime version is **3.1+**.
- [ ] If the agent collects end-user feedback, `mlflow.trace.user` is set at request time (not just `AssessmentSource.source_id` at feedback time). See [04c](../../sdlc/04c-end-user-feedback/SKILL.md).
- [ ] `client_request_id` set on the same trace root via `mlflow.update_current_trace(client_request_id=...)` for request correlation.
- [ ] `gen_ai.*` attributes set on individual LLM / tool **spans** (not on trace metadata).
- [ ] `mlflow.search_traces(filter_string="metadata.`mlflow.trace.user` = ...")` returns expected traces in dev before deploy.

## References

### Official documentation

- [Add context to traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces?language=Production) — primary source for this skill.
- [Track environments and context](https://mlflow.org/docs/latest/genai/tracing/track-environments-context/) — auto-populated metadata, reserved tags, override patterns.
- [Tutorial: Trace and analyze users and environments](https://mlflow.org/docs/latest/genai/tracing/track-environments-context/) — end-to-end example.
- [`mlflow.search_traces` API](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.search_traces) — filter syntax for metadata and tags.
- [Trace agents deployed on Databricks](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing) — production env-var matrix.

### Related skills

- [Foundation Step 2: Python tracing](../02-experiment-tracing-and-uc-storage/SKILL.md) — `@mlflow.trace`, `update_current_trace`, manual spans, UC OTEL storage.
- [Foundation Step 2b: TypeScript tracing](../02b-typescript-tracing/SKILL.md) — Node sibling, `mlflow.update_current_trace({ session_id, user_id })`.
- [Production tracing deployment reference](../02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md) — `ENABLE_MLFLOW_TRACING`, `MLFLOW_EXPERIMENT_ID`, `APP_ENVIRONMENT`, SP `CAN_EDIT`.
- [Trace context patterns reference](../02-experiment-tracing-and-uc-storage/references/trace-context-patterns.md) — full tag taxonomy, search examples, dashboard SQL.
- [Autolog integrations](../02-experiment-tracing-and-uc-storage/references/autolog-integrations.md) — auto-instrument 20+ libraries (token counts, span tree).
- [`sdlc/04c-end-user-feedback`](../../sdlc/04c-end-user-feedback/SKILL.md) — companion: tag the trace with the user **and** attach feedback to the same user.
- [`sdlc/06-deployment-and-automation`](../../sdlc/06-deployment-and-automation/SKILL.md) — `databricks.yml` / `app.yaml` env wiring including `APP_ENVIRONMENT`.

## Version history

| Version | Date | Changes |
| --- | --- | --- |
| 1.0.0 | 2026-04-24 | Initial skill: tags-vs-metadata decision matrix, reserved metadata fields (`mlflow.trace.user` / `mlflow.trace.session`), auto-populated environment metadata table, `APP_ENVIRONMENT` override pattern, custom deployment metadata (`agent_version`, `deployment_id`, `deployment_region`), `mlflow-tracing` vs `mlflow[databricks]` package choice, coexistence layering with `client_request_id` and `gen_ai.*`, search-by-metadata examples, validation checklist, DO/DON'T table. Sourced from [Add context to traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/add-context-to-traces?language=Production). |
