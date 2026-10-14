---
name: 04c-end-user-feedback
description: >
  Use when wiring **end-user feedback** (thumbs up/down, ratings, free-form
  comments) from a deployed app back into MLflow as Assessments on the
  originating trace. Covers the canonical `mlflow.log_feedback(...)` pattern,
  trace-id vs `client_request_id` correlation, the streaming case (SSE/WebSocket
  delivery of `trace_id` after the stream ends), multi-dimensional feedback
  (rating-per-aspect), update/delete of existing assessments, and analysis
  queries over collected feedback. Triggers on "collect user feedback",
  "end user feedback", "thumbs up production", "log_feedback", "trace_id
  feedback", "feedback API", "feedback route", "user rating production",
  "feedback assessment". SDLC Step 4c.
license: Apache-2.0
compatibility: "Requires MLflow 3.1+ (`mlflow[databricks]>=3.1.0` or `mlflow-tracing` for production), tracing already enabled on the agent (Track A 02-agent-framework). Works with both Databricks Apps (canonical) and Model Serving (alternate)."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "End-user feedback logged as MLflow Assessments on the originating trace via `mlflow.log_feedback(...)`; no bundle resource. The wiring lives in the deployed app (Apps or Model Serving). Identical SDK pattern on both clients. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.2.0"
  domain: "genai-agents"
  pipeline_position: "S4c"
  consumes: "deployed_agent, trace_id"
  produces: "feedback_assessments, feedback_volume_metric, feedback_eval_dataset"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/tracing/collect-user-feedback/, https://docs.databricks.com/aws/en/mlflow3/genai/getting-started/human-feedback, https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/dev-annotations, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
fields_read:
  - agent.feedback.dimensions
  - agent.feedback.user_id_source
---

# End-user feedback collection (production)

Canonical reference for **collecting end-user feedback in production** and writing it back as **MLflow Assessments** on the originating trace. Pair with [Track A 02-agent-framework](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) (which owns the tracing setup that produces the `trace_id`) and [04-evaluation-runs](../04-evaluation-runs/SKILL.md) (which owns *expert / labeling-session* feedback).

## Upstream Lineage

This skill references Databricks Agent Skills' `databricks-mlflow-evaluation` skill for feedback-to-dataset, production trace analysis, and evaluation-loop guidance. If collected feedback needs to become labeled eval data or monitoring signal, consult the upstream skill first, then apply this skill's production feedback correlation and assessment write-path contracts.

This skill is the **production user-feedback** counterpart to [04-evaluation-runs](../04-evaluation-runs/SKILL.md):

| Concern | Owner skill |
|---|---|
| End-user thumbs/rating from a live app → `log_feedback` on the trace | **This skill (04c)** |
| Expert labeling sessions, label schemas, Review App, `session.sync()` | [04-evaluation-runs](../04-evaluation-runs/SKILL.md) (Human feedback section) |
| Stakeholder business sign-off gate before deploy | [04b-stakeholder-signoff](../04b-stakeholder-signoff/SKILL.md) |
| Periodic resampling of production traces into labeling sessions | [07-production-monitoring](../07-production-monitoring/SKILL.md) |
| AppKit-side UI, Vote table, REST POST plumbing | [`apps_lakebase/skills/08-appkit-feedback`](../../../apps_lakebase/skills/08-appkit-feedback/SKILL.md) |

> **Canonical write-path (always):** `mlflow.log_feedback(trace_id=..., name="user_feedback", value=..., source=AssessmentSource(HUMAN, source_id=user_id), rationale=...)`. Whether that runs in your Track A Agent App's `@invoke` handler, a sidecar FastAPI route, or the AppKit `08-appkit-feedback` REST proxy, the **API surface is the same** and the assessments land on the same trace.

---

## When to Use

- You have a **deployed agent** (Track A on Databricks Apps, or Model Serving) that already emits MLflow traces.
- You want **end users** of a frontend (AppKit dashboard, template chat UI, Slack bot, etc.) to be able to give feedback (👍/👎, 1–5 stars, free-form comment) that lands on the originating trace.
- You need to **return `trace_id`** to the frontend so the user can later attach feedback to the same trace.
- You need **streaming** support — the trace id is only available **after** the SSE stream finishes; the UI must wait.
- You want to **update or delete** an assessment (user changed their mind, accidental thumb).
- You want to **analyze** collected feedback (positive rate, dimensional ratings, traces with feedback) for monitoring or to seed an evaluation dataset.

Skip if you only need **expert / SME labeling** — that is `04-evaluation-runs` → Human feedback. Skip if you have **no live users** yet — instrument tracing first ([Track A 02](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md)) and come back.

---

## Architecture

```
End user clicks 👍 / 👎 / star rating / writes comment
        │
        ▼
Frontend calls POST /feedback
  body: { trace_id, value, rationale?, dimension? }
  auth: x-forwarded-access-token (OBO) — see Track A 04-authentication
        │
        ▼
Backend route (Track A Agent App or AppKit server)
  resolves user_id from x-app-user-email / x-forwarded-email first,
  then falls back to OBO current_user.me() only when the inbound Bearer is
  the user's own OBO token.
        │
        ▼
mlflow.log_feedback(
    trace_id=...,
    name="user_feedback",
    value=value,
    rationale=rationale,
    source=AssessmentSource(HUMAN, source_id=user_id),
)
        │
        ▼
Assessment attached to the trace in Unity Catalog (OTeL trace location)
        │
        ▼
Visible in:
  - MLflow Trace UI → Assessments panel
  - SQL over UC trace tables (analytics)
  - mlflow.search_traces() (dataset construction)
  - Production monitoring dashboards (Step 07)
```

The two **correlation IDs** you can use:

| ID | Source | When to pick |
|---|---|---|
| `trace_id` | `_resolve_active_trace_id()` — wraps `mlflow.get_current_active_span()` with `mlflow.tracing.fluent.get_last_active_trace_id()` fallback | **Default.** Simplest; no extra plumbing. Works for non-streaming responses. |
| `client_request_id` | Frontend-generated UUID, passed in the request, attached to the trace via `mlflow.update_current_trace(client_request_id=...)` | Pick when you can't return `trace_id` synchronously (deeply async pipelines, WebSockets where the UI generates IDs first). |

Both end up on the same trace; you choose which one the **feedback POST** carries.

---

## Trace ID Contract: Two Forms

A `trace_id` you read off the wire and a `trace_id` you pass to the MLflow Assessments backend are **not always the same string**. Skills that confuse the two will quietly drop assessments. Document and exchange both forms explicitly.

### Form 1 — Client / UI form (UC v4)

What the agent returns to the frontend (in the JSON body or the SSE `done` event) is the **Unity Catalog v4 trace URI**:

```
trace:/<catalog>.<schema>.<prefix>/<bare_id>
```

Example: `trace:/main.skyloyalty_ops.agent_traces/0a1b2c3d4e5f...`. This is the canonical, fully qualified handle the UI stores per assistant message and replays into `POST /feedback`. Storing the bare id alone is fragile because the same bare id can collide across catalogs / schemas. Always round-trip the full `trace:/...` URI.

### Form 2 — Assessments backend form

The MLflow Assessments API (`mlflow.log_feedback`, `mlflow.override_feedback`, `mlflow.delete_assessment`) accepts whatever the **target runtime** requires. Concretely:

- On Databricks workspaces running MLflow 3.1+, the backend accepts the UC v4 URI directly.
- On older runtimes or self-hosted MLflow, the backend wants the bare id (`<bare_id>`) and resolves the trace from the configured experiment.

The feedback route MUST normalize the inbound id once, at the edge, before calling `log_feedback`. Centralize the conversion so the agent code never branches on runtime version inline:

```python
def to_assessments_id(trace_uri_or_id: str) -> str:
    """Convert UC v4 client form to whatever the Assessments backend expects."""
    if trace_uri_or_id.startswith("trace:/"):
        # Modern Databricks runtimes accept the URI as-is.
        # If your runtime requires a bare id, strip to the segment after the last '/'.
        return trace_uri_or_id
    return trace_uri_or_id  # already bare
```

Document at the top of the feedback route which form your runtime accepts. Cross-reference [Track A 02-agent-framework](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) for the producer side that emits the URI.

---

## Trace assessment round-trip gate

Before declaring feedback wired-up, exercise the full assessment lifecycle against a **single trace** and verify the result reads back from the SQL warehouse. Run the gate against a known trace from a real `/chat` round trip:

```bash
python genai-agents/sdlc/04c-end-user-feedback/scripts/feedback_round_trip.py \
    --trace-id "$KNOWN_GOOD_TRACE_ID" \
    --user-id "$EXPECTED_USER_EMAIL" \
    --assessments-table "$MLFLOW_TRACING_TABLE_PREFIX"_assessments \
    --warehouse-id "$MLFLOW_TRACING_SQL_WAREHOUSE_ID"
```

The script exercises `log_feedback → override_feedback → delete_assessment → re-log` and verifies via the SQL warehouse that:

1. `log_feedback` returns a non-empty `assessment_id`.
2. `override_feedback` preserves `assessment_id`.
3. `delete_assessment` succeeds.
4. The re-log mints a fresh `assessment_id` distinct from the deleted one.
5. The latest warehouse row matches the re-log id and the deleted id does not leak back.

Wire this into the same CI step that runs the dataset / scorer smoke tests. Required env for the warehouse verify: `MLFLOW_TRACING_SQL_WAREHOUSE_ID`, `MLFLOW_TRACING_TABLE_PREFIX`, `DATABRICKS_HOST`, `DATABRICKS_TOKEN`. Missing warehouse inputs fail by default. Use `--api-only` only for a local smoke test that intentionally does not claim end-to-end verification.

If any step fails — `log_feedback` rejects the id, `delete_assessment` 404s, the re-log mints the same id, or the SQL warehouse omits or duplicates rows — the deployment is blocked. The two most common failures this gate catches:

1. The frontend stored the bare id instead of the UC v4 URI, so the backend can't resolve the trace.
2. The runtime accepts `log_feedback` but the warehouse lag means the row isn't queryable yet — the script's `--warehouse-wait-seconds` flag (default 10s) absorbs replication lag instead of debugging it post-launch.

---

## Step 1 — Return `trace_id` from the agent response

The trace id must reach the frontend *somehow*. Pick **one** of three patterns based on your transport.

### Defensive `trace_id` capture

Both `mlflow.get_current_active_span()` and `mlflow.tracing.fluent.get_last_active_trace_id()` are valid sources, but each can return `None` depending on **when** in the request lifecycle you call it. Use this helper everywhere instead of either bare call:

```python
import mlflow

def _resolve_active_trace_id() -> str | None:
    """Return the current trace id, defensively.

    Tries the active span first (works inside a traced handler before the
    span closes). Falls back to the most recently completed trace on this
    thread (works after the function returns and the span auto-closes).
    Returns None only when there is genuinely no trace on this thread —
    in which case feedback should be disabled in the UI for this turn.
    """
    span = mlflow.get_current_active_span()
    if span is not None:
        return span.trace_id
    try:
        from mlflow.tracing.fluent import get_last_active_trace_id
        return get_last_active_trace_id()
    except Exception:
        return None
```

### Pattern A — Non-streaming `@invoke` (canonical, easiest)

Track A Agent App handlers built with `@mlflow.genai.agent_server.invoke`:

```python
import mlflow
from mlflow.genai import agent_server

@agent_server.invoke
async def invoke(request, context):
    response_text = await run_agent(request)
    trace_id = _resolve_active_trace_id()
    if trace_id is None:
        raise RuntimeError("no active or recent trace; tracing not enabled")
    return {
        "output_text": response_text,
        "trace_id": trace_id,
    }
```

The frontend reads `data.trace_id` from the JSON response and stores it alongside the assistant message.

### Pattern B — Streaming `@stream` (SSE)

The trace id is only complete **after** the stream finishes. Send it as the **last** SSE event, with a distinct event `type`:

```python
import json
import mlflow
from mlflow.genai import agent_server

@agent_server.stream
async def stream(request, context):
    with mlflow.start_span(name="agent_turn") as span:
        async for token in run_agent_streaming(request):
            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        trace_id = span.trace_id or _resolve_active_trace_id()
        yield f"data: {json.dumps({'type': 'done', 'trace_id': trace_id})}\n\n"
```

Frontend handling (sketch):

```javascript
for (const line of lines) {
  if (!line.startsWith("data: ")) continue;
  const event = JSON.parse(line.slice(6));
  if (event.type === "token") appendToken(event.content);
  else if (event.type === "done") setTraceId(event.trace_id);  // enables 👍/👎 buttons
  else if (event.type === "error") showError(event.error);
}
```

The feedback buttons stay disabled until `trace_id` arrives. See [trace-context-patterns.md](../../tracks/A-custom-agent-apps/02-agent-framework/references/trace-context-patterns.md) for the full streaming pattern.

### Pattern C — `client_request_id` correlation

Frontend generates a UUID per request, sends it on **both** `/chat` and `/feedback`. Backend tags the trace:

```python
import uuid, mlflow

@agent_server.invoke
async def invoke(request, context):
    client_request_id = request.get("client_request_id") or str(uuid.uuid4())
    mlflow.update_current_trace(client_request_id=client_request_id)
    response_text = await run_agent(request)
    return {"output_text": response_text, "client_request_id": client_request_id}
```

On the feedback side, look up the trace by `client_request_id` first:

```python
traces = mlflow.search_traces(
    filter_string=f"attributes.client_request_id = '{client_request_id}'",
    max_results=1,
)
trace_id = traces[0].info.trace_id
```

Use this pattern when the frontend has its own request-id discipline (typed analytics, Sentry breadcrumbs, etc.) that should be the system of record.

---

## Step 2 — Backend feedback route (Python)

This is the **canonical write-path**. Same code regardless of where it runs (Track A Agent App, AppKit Python sidecar, FastAPI on Model Serving sidecar):

```python
from typing import Optional
from fastapi import APIRouter, Header, Query, Request
from pydantic import BaseModel
import mlflow
from mlflow.entities import AssessmentSource

router = APIRouter()

class FeedbackBody(BaseModel):
    is_positive: bool                  # True = thumbs up
    rationale: Optional[str] = None    # free-form comment

@router.post("/feedback")
def submit_feedback(
    body: FeedbackBody,
    trace_id: str = Query(..., description="Trace id returned by /chat"),
    request: Request,
):
    user_id = _resolve_user_id(dict(request.headers))
    mlflow.log_feedback(
        trace_id=trace_id,
        name="user_feedback",
        value=body.is_positive,
        rationale=body.rationale,
        source=AssessmentSource(
            source_type="HUMAN",
            source_id=user_id,
        ),
    )
    return {"status": "ok", "trace_id": trace_id}
```

`_resolve_user_id` resolves the originating end-user identity from inbound headers, with a clear priority order so 2-Apps Pathway-C deployments do not attribute feedback to the AppKit service principal:

```python
from databricks.sdk import WorkspaceClient
from databricks_app.utils import get_user_workspace_client

def _resolve_user_id(headers: dict[str, str]) -> str:
    """Resolve the originating end-user's identity.

    Priority order (high → low):

      1. x-app-user-email          — set by an AppKit Pathway-C proxy (skill 06d)
                                     when the inbound Bearer is the AppKit SP.
      2. x-forwarded-email         — set by the Apps platform on direct
                                     end-user requests (1-App pathway).
      3. x-forwarded-preferred-username — fallback when email is missing.
      4. OBO -> current_user.me()  — works only when the inbound Bearer is
                                     the user's own OBO token, NOT an SP.
      5. "anonymous"               — last resort, breaks per-user dashboards.
    """
    for key in ("x-app-user-email", "x-forwarded-email", "x-forwarded-preferred-username"):
        v = headers.get(key) or headers.get(key.title())
        if v:
            return v
    obo = headers.get("x-forwarded-access-token")
    if obo:
        try:
            w: WorkspaceClient = get_user_workspace_client(obo)
            return w.current_user.me().user_name
        except Exception:
            pass
    return "anonymous"
```

> **2-Apps Pathway-C note.** When the agent sits behind an AppKit proxy (skill [`06d-appkit-agent-app-proxy`](../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md)), the inbound `Authorization: Bearer` token is the AppKit service principal — `current_user.me()` would attribute every assessment to the SP UUID. The proxy stamps the originating user's email as `x-app-user-email`; the resolver above checks that header first. The four-probe verification script in 06d (`feedback_source_id` probe) asserts this end-to-end.

> **Canonical name:** use `name="user_feedback"` for the binary thumbs assessment. Downstream dashboards, the `04-evaluation-runs` analysis snippet, and the AppKit feedback skill all assume this name. If you must rename, update **all three** places in lockstep.

> **Auth:** the feedback route requires the same OBO context as the agent itself. See [Track A 04-authentication](../../tracks/A-custom-agent-apps/04-authentication/SKILL.md) for `user_api_scopes` and the `x-forwarded-access-token` flow. Don't read `process.env.DATABRICKS_TOKEN`.

> **Tag the trace with the user too — at request time, not just feedback time.**
> The `user_id` resolved here is "who gave the feedback" (the
> `AssessmentSource.source_id`). For "who triggered the trace", call
> `mlflow.update_current_trace(metadata={"mlflow.trace.user": user_id, "mlflow.trace.session": session_id})`
> in your `/chat` (or `@invoke`) handler at request time. That way every
> trace — even ones the user never gives feedback on — is searchable
> and groupable by user/session in the MLflow UI. The reserved metadata
> fields and the `APP_ENVIRONMENT` override pattern live in
> [F2c — Trace context and environments](../../foundation/02c-trace-context-and-environments/SKILL.md).

---

## Step 3 — Update or delete an existing assessment

Users change their minds. Three operations:

```python
import mlflow
from mlflow.entities import AssessmentSource

source = AssessmentSource(source_type="HUMAN", source_id=user_id)

# 1. Create — first thumb / first comment for this user-message
created = mlflow.log_feedback(
    trace_id=trace_id,
    name="user_feedback",
    value=True,
    rationale="Helpful",
    source=source,
)
assessment_id = created.assessment_id  # store this alongside the trace_id

# 2. Update in place — preferred when you already have assessment_id
#    Preserves assessment_id and produces a single audit row per user-message.
mlflow.override_feedback(
    trace_id=trace_id,
    assessment_id=assessment_id,
    value=False,
    rationale="Actually missed the policy citation",
)

# 3. Delete — accidental click or thumbs withdrawn
mlflow.delete_assessment(trace_id=trace_id, assessment_id=assessment_id)
```

> **When to use which.** If the frontend stores `assessment_id` per assistant message (recommended — it is returned by `log_feedback`), prefer `mlflow.override_feedback` for thumbs-toggle. Use bare `mlflow.log_feedback` again only when the frontend has lost the `assessment_id` (cold reload, no chat history) — that path mints a fresh row and the latest-by-`create_time_ms` wins for downstream queries.

> **API surface note:** `mlflow.delete_assessment(...)` is the top-level callable. Earlier MLflow snippets called `MlflowClient().delete_assessment(...)`; on current Databricks-bundled MLflow that attribute does not exist and the call fails with `AttributeError: 'MlflowClient' object has no attribute 'delete_assessment'`. Always use the top-level function.

The MLflow Trace UI shows the latest value as primary; older versions remain in the assessment history.

---

## Step 4 — Multi-dimensional feedback (ratings)

When you need richer signal than 👍/👎, log **one assessment per dimension** so each can be aggregated independently:

```python
class DetailedFeedbackBody(BaseModel):
    accuracy: int     # 1..5
    helpfulness: int  # 1..5
    relevance: int    # 1..5
    rationale: Optional[str] = None

@router.post("/feedback/detailed")
def submit_detailed_feedback(
    body: DetailedFeedbackBody,
    trace_id: str = Query(...),
    request: Request,
):
    user_id = _resolve_user_id(dict(request.headers))
    source = AssessmentSource(source_type="HUMAN", source_id=user_id)
    for dimension, score in {
        "user_accuracy": body.accuracy,
        "user_helpfulness": body.helpfulness,
        "user_relevance": body.relevance,
    }.items():
        mlflow.log_feedback(
            trace_id=trace_id,
            name=dimension,
            value=score / 5.0,                      # normalize to 0..1
            rationale=body.rationale if dimension == "user_accuracy" else None,
            source=source,
        )
    return {"status": "ok"}
```

Naming convention: prefix every user-facing rating with `user_` so the analysis snippets in Step 6 (and `07-production-monitoring`) can pick them out generically.

---

## Step 5 — End-user vs developer / expert assessments

Three assessment **sources** land on the same trace; downstream analytics partition them by `source.source_type`:

| `source_type` | Who | How they get there |
|---|---|---|
| `HUMAN` (end user) | Real product user | This skill — `/feedback` route. |
| `HUMAN` (developer / SME) | Engineer or domain expert during dev | MLflow UI → trace → **Assessments** → **Add new assessment**, *or* a labeling session ([04-evaluation-runs](../04-evaluation-runs/SKILL.md) → Human feedback). |
| `LLM_JUDGE` | Automated scorer | [03-scorers-and-judges](../03-scorers-and-judges/SKILL.md) + [07-production-monitoring](../07-production-monitoring/SKILL.md) registered scorers. |

When you build evaluation datasets from production (Step 7 below), filter on `source_type = HUMAN` AND `source_id != <bot_user>` to keep only genuine end-user signal.

---

## Step 6 — Analyze feedback

### Positive rate over the last 24 hours

```python
from datetime import datetime, timedelta
from mlflow.client import MlflowClient

client = MlflowClient()
cutoff_ms = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)

traces = client.search_traces(
    experiment_names=["/Users/you@company.com/skyloyalty-agent"],
    filter_string=f"trace.timestamp_ms > {cutoff_ms}",
)

total = len(traces)
with_feedback = positive = negative = 0
for t in traces:
    detail = client.get_trace(t.info.trace_id)
    user_assessments = [
        a for a in (detail.data.assessments or [])
        if a.name == "user_feedback" and a.source.source_type == "HUMAN"
    ]
    if not user_assessments:
        continue
    with_feedback += 1
    latest = user_assessments[-1]
    if latest.value:
        positive += 1
    else:
        negative += 1

feedback_rate = (with_feedback / total) * 100 if total else 0
positive_rate = (positive / with_feedback) * 100 if with_feedback else 0
print(f"feedback_rate={feedback_rate:.1f}%  positive_rate={positive_rate:.1f}%")
```

### Multi-dimensional rating averages

```python
def average_user_ratings(traces):
    by_dim = {}
    for t in traces:
        detail = client.get_trace(t.info.trace_id)
        for a in (detail.data.assessments or []):
            if (
                a.source.source_type == "HUMAN"
                and a.name.startswith("user_")
                and a.name != "user_feedback"
            ):
                by_dim.setdefault(a.name.removeprefix("user_"), []).append(a.value)
    return {k: sum(v) / len(v) for k, v in by_dim.items() if v}
```

Persist these aggregates in a SQL dashboard alongside the registered-scorer outputs from [07-production-monitoring](../07-production-monitoring/SKILL.md).

---

## Step 7 — Promote feedback into an evaluation dataset

Negative end-user feedback is the highest-signal raw material for regression tests:

```python
import mlflow

# Pull traces with negative user feedback from the last 7 days
negative_trace_ids = [
    t.info.trace_id for t in traces
    if any(
        a.name == "user_feedback"
        and a.source.source_type == "HUMAN"
        and a.value is False
        for a in (client.get_trace(t.info.trace_id).data.assessments or [])
    )
]

# Build / append to an evaluation dataset
dataset = mlflow.genai.datasets.create_dataset(
    uc_table_name="main.skyloyalty.user_feedback_regression",
)
dataset.merge_records(trace_ids=negative_trace_ids)
```

Then send those traces to a **labeling session** ([04-evaluation-runs](../04-evaluation-runs/SKILL.md) → Human feedback) so a domain expert can produce the **`expected_response`** ground truth, and re-run `mlflow.genai.evaluate(..., scorers=[Correctness()])` to quantify the gap.

This closes the production → eval → fix loop:

```
end user 👎  →  log_feedback (this skill)
            →  search_traces filter on negative HUMAN feedback
            →  merge into eval dataset (02-evaluation-datasets)
            →  expert labeling session (04-evaluation-runs)
            →  Correctness eval against expert expected_response (04-evaluation-runs)
            →  prompt / scorer fixes (08-prompt-optimization, 03-scorers-and-judges)
            →  redeploy (06-deployment-and-automation)
            →  monitor positive_rate trending up (07-production-monitoring)
```

---

## Streaming gotcha checklist

When the frontend uses SSE / WebSockets:

- [ ] Final SSE event has `type: "done"` and includes `trace_id`.
- [ ] Frontend disables 👍/👎 buttons until `trace_id` arrives.
- [ ] Stream sets `X-Accel-Buffering: no` (and any equivalent for your reverse proxy / Apps frontdoor).
- [ ] Frontend resets `traceId` on every new turn (don't accidentally attach feedback to the **previous** turn).
- [ ] `mlflow.start_span(name=...)` wraps the whole turn so the id you yield is the **trace** root, not a sub-span.
- [ ] If you use `client_request_id` instead, attach it via `mlflow.update_current_trace(client_request_id=...)` **before** any tool calls so it's present even if the LLM call fails partway.

---

## Do's and Don'ts

|  | Do | Don't |
|---|---|---|
| Naming | `name="user_feedback"` for binary thumbs; `name="user_<dimension>"` for ratings. | Pick a different name in each frontend (AppKit vs template UI vs Slack) — analysis breaks. |
| Source | `AssessmentSource(source_type="HUMAN", source_id=<email-from-OBO>)`. | Use `"anonymous"` when you have an OBO token; you'll lose per-user dashboards. |
| Source | Resolve end-user identity from `x-app-user-email`, then `x-forwarded-email`, then OBO `current_user.me()` when the Bearer is user-scoped. | Infer the user from the app-to-app `Authorization` Bearer; in 2-Apps deployments that token belongs to the AppKit SP. |
| Trace id | Return from `@invoke` body; yield as `done` event from `@stream`. | Try to reconstruct it on the client; it doesn't exist until the server span closes. |
| Update | `mlflow.log_feedback(...)` again with same name to overwrite. | Manually `PATCH` the assessment unless you specifically need to keep `assessment_id` stable. |
| Streaming | Final event carries `trace_id`. | Send the trace id as the **first** event — it's wrong (the trace hasn't closed yet). |
| Dataset loop | Pull negative HUMAN feedback into eval datasets weekly. | Ignore negative feedback because "the scorer says we're fine." End users see what scorers miss. |

---

## Validation Checklist

- [ ] `mlflow[databricks]>=3.1.0` (dev) or `mlflow-tracing` (prod) installed in the Agent App image.
- [ ] Tracing already enabled on the agent ([Track A 02-agent-framework](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md), MLflow `set_experiment` with `trace_location=UnityCatalog(...)`).
- [ ] `/feedback` route added to the Agent App (or AppKit sidecar) and protected by the same OBO check as `/chat`.
- [ ] Frontend stores `trace_id` per assistant message and clears it on new turns.
- [ ] Frontend stores the **UC v4 client form** (`trace:/<catalog>.<schema>.<prefix>/<bare_id>`) per assistant message; the feedback route normalizes it to whatever the Assessments backend requires before calling `log_feedback`.
- [ ] Round-trip gate runs: `log_feedback + override_feedback + delete_assessment + re-log` against a known trace, verifying `override_feedback` preserves `assessment_id` and the deleted id does not leak back via the SQL warehouse (`MLFLOW_TRACING_SQL_WAREHOUSE_ID`).
- [ ] One curl-test that POSTs feedback with a real `trace_id` succeeds and the assessment shows up in the MLflow Trace UI within ~10s.
- [ ] Positive rate query (Step 6) runs cleanly on the experiment after at least one round of test feedback.
- [ ] Weekly cron / job that materializes negative-feedback traces into a UC eval dataset.
- [ ] Dashboard tile in [07-production-monitoring](../07-production-monitoring/SKILL.md) shows `feedback_rate` and `positive_rate` alongside scorer metrics.

---

## Integration With Other Skills

- **Producer of `trace_id`:** [Track A 02-agent-framework](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) — sets up `mlflow.update_current_trace`, `client_request_id`, and the `@invoke` / `@stream` shape.
- **Auth:** [Track A 04-authentication](../../tracks/A-custom-agent-apps/04-authentication/SKILL.md) — OBO + `user_api_scopes`.
- **AppKit-side wire-up:** [`apps_lakebase/skills/08-appkit-feedback`](../../../apps_lakebase/skills/08-appkit-feedback/SKILL.md) — Vote table, REST proxy, UI buttons. **This skill (04c) is the Python contract that AppKit feedback ultimately calls.**
- **Expert / labeling sessions:** [04-evaluation-runs](../04-evaluation-runs/SKILL.md) → Human feedback section.
- **Production monitoring:** [07-production-monitoring](../07-production-monitoring/SKILL.md) — sample production traces (including those with user feedback) into periodic labeling sessions; surface `feedback_rate`, `positive_rate` on dashboards.
- **Eval datasets:** [02-evaluation-datasets](../02-evaluation-datasets/SKILL.md) — turn negative-feedback traces into versioned eval datasets.
- **Stakeholder signoff:** [04b-stakeholder-signoff](../04b-stakeholder-signoff/SKILL.md) — the business-metrics report should cite the latest `positive_rate` from this skill's analytics.

---

## References

### Official documentation

- [Collect user feedback (production tracing)](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/collect-user-feedback/) — primary source for this skill
- [10-minute demo: Collect human feedback](https://docs.databricks.com/aws/en/mlflow3/genai/getting-started/human-feedback) — end-to-end walk including labeling sessions
- [Feedback / Assessment data model (dev annotations)](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/dev-annotations)
- [Build evaluation datasets](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset)
- [Deploy agents with tracing](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/prod-tracing)

### Related skills

[F2c — Trace context and environments](../../foundation/02c-trace-context-and-environments/SKILL.md) · [02-evaluation-datasets](../02-evaluation-datasets/SKILL.md) · [03-scorers-and-judges](../03-scorers-and-judges/SKILL.md) · [04-evaluation-runs](../04-evaluation-runs/SKILL.md) · [04b-stakeholder-signoff](../04b-stakeholder-signoff/SKILL.md) · [07-production-monitoring](../07-production-monitoring/SKILL.md) · [Track A 02-agent-framework](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) · [Track A 04-authentication](../../tracks/A-custom-agent-apps/04-authentication/SKILL.md) · [`apps_lakebase/skills/08-appkit-feedback`](../../../apps_lakebase/skills/08-appkit-feedback/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-26 | Added Trace ID Contract: Two Forms (UC v4 client form vs Assessments backend form) and the `log_feedback + delete_assessment + re-log` round-trip gate verified via `MLFLOW_TRACING_SQL_WAREHOUSE_ID`. |
| 1.0.0 | 2026-04-24 | Initial skill: production `mlflow.log_feedback` write-path, trace-id vs client-request-id correlation, streaming pattern, multi-dimensional feedback, update/delete, analysis snippets, dataset promotion loop. |
