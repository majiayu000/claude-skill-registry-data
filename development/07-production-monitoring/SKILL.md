---
name: 07-production-monitoring
description: >
  Use when setting up live quality monitoring for a deployed agent. Covers
  registered scorers with sampling, trace archival to Delta, metric
  backfill, and periodic human review — even if you just want "monitor
  my agent's safety score in production." Also use when adding
  conversation-level judges, tuning sampling rates, or building
  monitoring dashboards from UC trace data. SDLC Step 7.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: jobs
deploy_verb: bundle_deploy
deploy_note: "Live monitoring = MLflow registered scorers (SDK) + periodic trace-archival/backfill jobs deployed via the `bundle deploy --target dev` spine; archived traces land in the per-user prefixed schema. On Genie Code run job deploy/run through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-08-30"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.0.1"
  domain: "genai-agents"
  pipeline_position: "S7"
  consumes: "databricks_app, serving_endpoint"
  produces: "production_scorers, trace_archival_table, monitoring_dashboards"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations, https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
fields_read:
  - governance.scorer_suite.production_scorers
  - governance.monitoring.required_alerts
---

# Production Monitoring (MLflow 3.10+)

Continuous monitoring for GenAI agents after deployment: **define → register → start** scorers with sampling, optional **stop** / **delete**, trace archival to Unity Catalog, historical backfill, SQL dashboards, and periodic human labeling on production traces. Assumes the app logs traces (SDLC Step 6).

## Upstream Lineage

This skill extends Databricks Agent Skills' `databricks-mlflow-evaluation` skill for UC trace ingestion, production monitoring, registered scorers, backfill, and trace analysis patterns. If monitoring APIs, UC trace table behavior, or scorer lifecycle semantics drift, consult the upstream skill first, then apply this skill's live-traffic sampling and dashboard conventions.

## When to Use

- Enable live quality monitoring on production traffic (built-in or custom scorers).
- Persist traces to UC Delta for compliance, debugging, and trend SQL.
- Backfill scorers after policy or scorer code changes.
- Run multi-turn judges when sessions are tagged; calibrate automated scorers with expert labels.

For offline evaluation on fixed datasets before release, use the dev evaluation skill (Step 2). This skill is **live** traffic.

---

## Trace Destination (Unity Catalog)

Bind the experiment to a UC OTEL location (MLflow **3.11+** on Databricks per [Store MLflow traces in Unity Catalog](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog)). Prefer this supported SDK pattern instead of custom helpers such as `_configure_uc_trace_destination()` or a non-standard `set_trace_destination` shim:

```python
import os
import mlflow
from mlflow.entities.trace_location import UnityCatalog

mlflow.set_tracking_uri("databricks")
os.environ["MLFLOW_TRACING_SQL_WAREHOUSE_ID"] = "<SQL_WAREHOUSE_ID>"

mlflow.set_experiment(
    experiment_name="/Users/you@example.com/my-genai-experiment",
    trace_location=UnityCatalog(
        catalog_name="my_catalog",
        schema_name="my_schema",
        table_prefix="my_prefix",  # optional; defaults if omitted
    ),
)
```

On older MLflow (for example 3.10), use `mlflow.tracing.set_experiment_trace_location` with `UCSchemaLocation` from `mlflow.entities.trace_location` instead—see MLflow release notes for your workspace. Grant the app identity **USE** on catalog/schema and **SELECT**/**MODIFY** on the `*_otel_*` tables.

---

## Registered Scorer Lifecycle

Scorers are **immutable**: every `.register()`, `.start()`, `.update()`, `.stop()` returns a **new** handle—always reassign.

| Phase | What happens | API |
|--------|----------------|-----|
| Define | Unregistered function or built-in instance | `@scorer` / `Safety()`, etc. |
| Register | Name bound to active experiment | `.register(name="...", ...)` |
| Active | Sampling &gt; 0 | `.start(sampling_config=ScorerSamplingConfig(sample_rate=...))` |
| Stopped | Registered, sample_rate = 0 | `.stop()` |
| Deleted | Removed from server | `delete_scorer(name=...)` |

```python
from mlflow.genai.scorers import Safety, ScorerSamplingConfig, delete_scorer, get_scorer

safety = Safety().register(name="prod_safety_check")
safety = safety.start(sampling_config=ScorerSamplingConfig(sample_rate=1.0))
# ... monitor ...
safety = safety.stop()
delete_scorer(name="prod_safety_check")
```

**DO — reassign**

```python
s = Safety().register(name="prod_safety")
s = s.start(sampling_config=ScorerSamplingConfig(sample_rate=1.0))
```

**DON'T — discard return value**

```python
s = Safety().register(name="prod_safety")
s.start(sampling_config=ScorerSamplingConfig(sample_rate=1.0))  # s still pre-start; .stop() unreliable
```

Tune sampling with `.update(sampling_config=ScorerSamplingConfig(sample_rate=0.8))` (also returns a new instance).

---

## Sampling Strategy (Best Practices)

Use `ScorerSamplingConfig(sample_rate=...)` (0.0–1.0). Official guidance: **1.0** for safety-critical; **0.05–0.2** for expensive LLM judges; moderate rates during iteration.

| Phase / volume | Sample rate | Rationale |
|----------------|-------------|-----------|
| Launch / low volume | 1.0 | Max signal while traffic is small; easier debugging. |
| Steady high volume | 0.1 (or 0.05–0.2 for judges) | LLM-judge scorers bill per scored trace; balance coverage vs cost. |
| Safety / policy | 1.0 | Prefer full coverage where required. |

Add cheap heuristic scorers at higher rates; reserve LLM judges for samples.

---

## Self-Contained Custom Scorers

Registered scorers are **serialized for remote execution**. They must not import your app package or reference module-level helpers.

**Requirements (production monitoring):**

- Only `@scorer` decorator functions (not class-based `Scorer` subclasses).
- **All** imports and helpers **inside** the function body (or inline literals).
- Avoid signature type hints that require imports (e.g. `List` from `typing`).
- Databricks recommends defining/registering from a **notebook** so serialization matches the monitoring environment.

**DO — self-contained**

```python
from mlflow.genai.scorers import scorer, ScorerSamplingConfig

@scorer
def production_domain_check(inputs: dict, outputs: dict) -> float:
    import re

    text = str(outputs.get("response", ""))
    return 1.0 if re.search(r"\d", text) else 0.0

registered = production_domain_check.register(name="prod_numeric_hint")
registered = registered.start(sampling_config=ScorerSamplingConfig(sample_rate=0.2))
```

**DON'T — project imports or outer scope**

```python
from my_app.validators import check_quality  # breaks on workers

@scorer
def bad_scorer(outputs):
    return check_quality(outputs)
```

---

## Multi-Turn Production Judges & Conversation Context

Production supports **multi-turn judges** that evaluate full sessions (e.g. `ConversationCompleteness`, `UserFrustration`). Prerequisites:

- Set **`mlflow.trace.session`** on traces (same session ID per conversation). See [Track users and sessions](https://mlflow.org/docs/latest/genai/tracing/track-users-sessions/).
- Judges run after a **session completion buffer** (default: no new traces for that session for several minutes; configurable via `MLFLOW_ONLINE_SCORING_DEFAULT_SESSION_COMPLETION_BUFFER_SECONDS` on the monitoring job).

```python
from mlflow.genai.scorers import (
    ConversationCompleteness,
    UserFrustration,
    ScorerSamplingConfig,
)

completeness = ConversationCompleteness().register(name="prod_completeness")
completeness = completeness.start(sampling_config=ScorerSamplingConfig(sample_rate=0.1))
frustration = UserFrustration().register(name="prod_frustration")
frustration = frustration.start(sampling_config=ScorerSamplingConfig(sample_rate=0.1))
```

**Custom conversation judges (offline pattern):** use `make_judge` with `{{ conversation }}` in instructions when evaluating traces/sessions—see [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations).

**Custom `@scorer` and span-level context:** when the API allows, accept an optional **`trace`** argument so the scorer can inspect spans (not just last-turn `inputs`/`outputs`). Confirm the signature against your MLflow version’s custom-scorer docs; keep the body self-contained.

```python
@scorer
def span_aware_check(inputs, outputs, trace=None):
    # Example: inspect trace/spans only if provided; keep logic serializable.
    if trace is None:
        return 0.5
    return 1.0
```

---

## Unity Catalog Traces: Monitoring SQL Warehouse

When traces live in UC OTEL tables, bind a SQL warehouse so scorer results persist correctly:

```python
from mlflow.tracing import set_databricks_monitoring_sql_warehouse_id

set_databricks_monitoring_sql_warehouse_id(
    sql_warehouse_id="<WAREHOUSE_ID>",
    experiment_id="<EXPERIMENT_ID>",
)
```

Call **once at startup**, after `set_experiment` / trace destination. Then register and `.start()` scorers as usual.

**DON'T** skip this when using UC trace storage—scorers may run without durable UC annotations.

---

## Trace Archival (Delta)

Persist traces and assessments to a UC Delta table for long-term SQL and dashboards.

Use the **`mlflow.tracing`** entry point (not `mlflow.tracing.archival`):

```python
import mlflow

mlflow.tracing.enable_databricks_trace_archival(
    delta_table_fullname="my_catalog.my_schema.archived_traces",
    experiment_id="YOUR_EXPERIMENT_ID",  # optional; defaults to active experiment
)
```

To stop exporting, use the disable API for your MLflow version (see **Archive traces** in [Production monitoring](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring)); do not import enable from `mlflow.tracing.archival`.

**DO** enable **once** at process startup (same as trace destination / experiment setup).

**DON'T** call enable/disable per HTTP request.

---

## Backfill Scorers

Retroactively score historical traces (e.g. after changing a judge). Prefer **`databricks.agents.scorers`** APIs as in the production monitoring guide.

**Simple backfill** (uses current registered scorers / defaults):

```python
from databricks.agents.scorers import backfill_scorers

job_id = backfill_scorers(scorers=["prod_safety_check", "prod_numeric_hint"])
```

**Custom sample rates and time window** with `BackfillScorerConfig`:

```python
from datetime import datetime
from databricks.agents.scorers import backfill_scorers, BackfillScorerConfig
from mlflow.genai.scorers import Safety, get_scorer

safety = get_scorer(name="prod_safety_check")

job_id = backfill_scorers(
    experiment_id="YOUR_EXPERIMENT_ID",
    scorers=[
        BackfillScorerConfig(scorer=safety, sample_rate=0.8),
    ],
    start_time=datetime(2026, 4, 1),
    end_time=datetime(2026, 4, 10),
)
```

**DO** verify names via `list_scorers()` and start with a **short** time range.

**DON'T** rely on typo’d scorer names—jobs may report scorers “not found”.

---

## Manage Scorers

```python
from mlflow.genai.scorers import list_scorers, get_scorer, delete_scorer

for s in list_scorers():
    print(s.name, s.sample_rate)

judge = get_scorer(name="prod_safety_check")
judge = judge.update(sampling_config=ScorerSamplingConfig(sample_rate=0.5))
delete_scorer(name="deprecated_scorer")
```

Namespace names by environment (`prod_`, `staging_`) to avoid collisions.

---

## Unified Scorer Definitions

Use the **same** `@scorer` functions or built-in instances for:

1. **Development** — `mlflow.genai.evaluate(...)` on golden sets (Step 4).
2. **Production** — `.register(name=...).start(sampling_config=...)`.

Production adds only registration, sampling, and experiment/model association—reduces drift between offline gates and live monitors.

---

## Human Feedback in Production

Two complementary feedback streams land on production traces:

1. **End-user feedback** (👍/👎, ratings, comments) from the deployed app.
   Owned by [04c-end-user-feedback](../04c-end-user-feedback/SKILL.md):
   `mlflow.log_feedback(trace_id, name="user_feedback", source=AssessmentSource(HUMAN, source_id=user_id), ...)`.
   Surface `feedback_rate` and `positive_rate` on this skill's monitoring
   dashboards alongside scorer outputs; alert when they diverge from your
   automated quality signal.
2. **Expert / SME labeling sessions** on a sampled slice of production traffic.
   See **Skill 04 (Evaluation Runs) → Human Feedback** for label schemas
   (`InputCategorical`, `InputText`, `InputTextList`), `create_labeling_session()`,
   and `session.sync()`.

Automated scorers drift; **periodically** pull production traces (especially those with negative end-user feedback) into labeling sessions so experts score a sample. The production twist: schedule sessions weekly or per-release, feed synced labels back into evaluation datasets, and re-run `mlflow.genai.evaluate` to align automated scorers with human judgment.

---

## Monitoring Dashboards

**Load** [`references/monitoring-dashboard-queries.md`](references/monitoring-dashboard-queries.md) **if** you need SQL queries for archival table dashboards (quality trends, errors, latency, alerts). Use relative windows (`DATEADD`), `DESCRIBE` the table, and join business dimensions when present in trace tags or payloads.

Layer views for: safety failures, rolling mean drops, volume anomalies, scorer-specific slices.

---

## UC OTEL Dashboards & Export

When using UC OTEL storage, scorer outputs align with `*_otel_metrics` / `*_otel_annotations` (see trace UC docs). **Load** [`references/uc-otel-queries.md`](references/uc-otel-queries.md) **if** you need span-level SQL for UC OTEL tables or export patterns.

---

## Common Mistakes

**Load** [`references/common-mistakes.md`](references/common-mistakes.md) **if** you encounter scorer registration failures, sampling issues, archival errors, or dashboard SQL problems.

---

## DO / DON'T (Quick)

| DO | DON'T |
|----|--------|
| Reassign every `.register` / `.start` / `.update` / `.stop` result | Call `.start()` without assigning |
| Use `ScorerSamplingConfig` tuned by traffic and cost | Run every LLM judge at 1.0 on huge volume without budget |
| Keep custom scorers fully self-contained | Import application packages inside scorers |
| Enable trace archival once at startup | Enable archival inside request handlers |
| Bind UC monitoring warehouse when using UC traces | Register scorers without warehouse when UC traces require it |
| Verify scorer names before backfill | Backfill with unverified names / huge ranges first run |

---

## Validation Checklist

**Scorers**

- [ ] Every lifecycle call’s return value is assigned.
- [ ] Sampling: safety high; expensive judges lower; launch strategy documented.
- [ ] Custom scorers: inline imports, no project modules, serializable logic (numeric or structured return types per SDK docs).
- [ ] Scorer names namespaced by environment.
- [ ] At most **20** scorers per experiment (platform limit).

**Traces & UC**

- [ ] Experiment `trace_location` (Unity Catalog) aligned with deployment.
- [ ] `set_databricks_monitoring_sql_warehouse_id` set when UC OTEL monitoring is used.
- [ ] `mlflow.tracing.enable_databricks_trace_archival(...)` configured with UC grants.
- [ ] Dashboard SQL validated against actual columns.

**Operations**

- [ ] Backfill smoke-tested on a short window.
- [ ] Old scorers removed with `delete_scorer` when superseded.
- [ ] Archival table retention / `OPTIMIZE` policy defined.

**Human loop**

- [ ] Periodic labeling sessions from production samples (Skill 04 schemas).
- [ ] Labels feed judge tuning or eval datasets.

---

## References

**Databricks (canonical)**

- [Production monitoring](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring)
- [Scorers & registered scorers](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers)
- [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations)
- [Human feedback](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/)
- [Trace storage / Unity Catalog](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog)
- [Enable production monitoring with UC traces](https://docs.databricks.com/aws/en/mlflow3/genai/tracing/trace-unity-catalog#enable-production-monitoring)
- [Label existing traces / labeling sessions](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces)

**Related skills**

- Step 4 — offline GenAI evaluation and human-feedback schemas.
- Steps 4–6 — tracing and deployment surfaces that feed this step.

**Local reference files**

| File | Purpose |
|------|---------|
| [`references/registered-scorers.md`](references/registered-scorers.md) | Scorer lifecycle, serialization, management |
| [`references/trace-archival.md`](references/trace-archival.md) | Archival table behavior and queries |
| [`references/metric-backfill.md`](references/metric-backfill.md) | Backfill operations |
| [`references/monitoring-dashboard-queries.md`](references/monitoring-dashboard-queries.md) | Dashboard SQL recipes |
| [`references/common-mistakes.md`](references/common-mistakes.md) | Mistake → impact → fix |
| [`references/uc-otel-queries.md`](references/uc-otel-queries.md) | UC OTEL SQL and export |

---

## Version History

| Version | Date | Notes |
|---------|------|--------|
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific code. Fixed trace archival API (`mlflow.tracing.enable_databricks_trace_archival`, not `mlflow.tracing.archival`). Added sampling strategies, human feedback loop, conversation monitoring, UC binding via `set_experiment(..., trace_location=UnityCatalog(...))`, `BackfillScorerConfig`, generic patterns. Grounded in official production-monitoring docs. |
| 3.2.1 | 2026-04-10 | Split references to keep SKILL concise. |
| 3.2.0 | 2026-04-10 | UC OTEL monitoring warehouse binding section. |
| 3.1.0 | 2026-03-27 | Reference files and expanded validation. |
| 3.0.0 | 2026-03-26 | MLflow 3.10+ scorer lifecycle baseline. |
