---
name: 05-logged-model-and-uc-registration
description: >
  Use when you need to log an agent to MLflow, register it in Unity Catalog,
  or promote a new version as champion. Covers the full model lifecycle —
  even if you just want "log my agent and make it the production version."
  Also use when setting up MLFLOW_ACTIVE_MODEL_ID for production trace
  linking, metric-based promotion gating, or rollback. SDLC Step 5.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Agent logged to MLflow and registered in UC (with champion alias) via the MLflow SDK; the UC model lands under the per-user prefixed catalog/schema. No bundle resource. Identical on both clients; on Genie Code run any CLI step through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.0.0"
  domain: "genai-agents"
  pipeline_position: "S5"
  consumes: "evaluation_results, thresholds_met, mlflow_run_id"
  produces: "logged_model_id, uc_model_version, champion_alias"
  grounded_in: "https://docs.databricks.com/en/mlflow/models-in-uc.html, https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Logged Model and Unity Catalog Registration

## Upstream Lineage

This skill references Databricks Agent Skills' `databricks-mlflow-evaluation` skill for metric-based promotion gates, evaluation result interpretation, and production trace/model lineage. If registration or champion promotion depends on scorer outputs or eval harness behavior, consult the upstream skill first, then apply this skill's LoggedModel and UC alias conventions.

## When to Use

Use this skill when you need to:

- Persist a GenAI agent (or agent-like artifact) to MLflow with correct **resources** (serving endpoints, vector search, and so on) for lineage and deployment.
- Create **LoggedModel** entities that tie iterations, configs, and evaluation metrics together.
- **Register** a model version in **Unity Catalog** under a stable naming convention.
- **Promote** a **champion** only when evaluation metrics meet thresholds (gating), or use aliases for rollback and discovery.
- Link **production traces** to a specific logged model via `MLFLOW_ACTIVE_MODEL_ID`.

This step assumes upstream **evaluation results**, **thresholds**, and an **MLflow run** (SDLC Step 4). Downstream artifacts include **logged model id**, **UC model version**, and **champion** / alias state.

### Track Applicability

- **Track A (Custom Agent):** Log the agent with `mlflow.pyfunc.log_model()`, register in UC, apply champion gating.
- **Track B (Supervisor API):** Model registration is optional — you may still register a wrapper for versioning and lineage.
- **Track C (Model Serving):** Model registration is typically mandatory for governed deployment.

---

## Part A: Agent Logging

Official guidance: log agents with explicit dependencies via `mlflow.models.resources`, validate with `mlflow.models.predict` before production rollout. See [Log an agent to MLflow](https://docs.databricks.com/aws/en/generative-ai/agent-framework/log-agent).

> **Recommended default:** Use **`mlflow.pyfunc.log_model()`** with explicit `resources` for most agents. Use `mlflow.langchain.log_model()` only if your agent is a LangChain chain/graph.

### Code-based logging

```python
import mlflow
from mlflow.models.resources import DatabricksServingEndpoint, DatabricksVectorSearchIndex

mlflow.models.set_model(MyAgent())

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        artifact_path="agent",
        python_model="/path/to/agent.py",
        input_example={"input": [{"role": "user", "content": "Hello"}]},
        resources=[
            DatabricksServingEndpoint(endpoint_name="my-llm"),
            DatabricksVectorSearchIndex(index_name="prod.docs.index"),
        ],
        pip_requirements=["mlflow[databricks]>=3.10.1", "databricks-sdk>=0.40.0"],
    )
```

Declare every external dependency the agent needs at inference time. **Load** [`references/agent-logging.md`](references/agent-logging.md) **if** you need resource types, input examples, or error-handling details.

### LangChain logging

```python
mlflow.langchain.log_model(
    lc_model="/path/to/agent.py",
    artifact_path="agent",
    resources=[...],
)
```

### DO / DON'T: Agent Logging

| DO | DON'T |
|----|--------|
| Declare `resources` and `input_example` | Log without resources (deployment and permissions break) |
| Call `mlflow.models.set_model(agent)` at module level in the agent file when using path-based logging | Omit `set_model()` when logging by file path |
| Run `mlflow.models.predict` on `model_uri` in CI/staging | Ship without a smoke prediction |

---

## Part B: LoggedModel Lifecycle

**Create a tracked model:** `mlflow.create_logged_model(name=...)` creates a **LoggedModel** entity associated with the active run (see [Models in Unity Catalog](https://docs.databricks.com/en/mlflow/models-in-uc.html) for how logged models relate to registration and lineage).

**Config snapshot (generic):** Log structured artifacts alongside the model — for example agent config, prompt version IDs, tool definitions, and feature flags as JSON under the run — so rollback and audits have full context without overloading run params.

**Aliases on the LoggedModel:**

```python
mlflow.set_logged_model_alias(model_id=model_id, alias="champion")
```

Guard with `getattr(mlflow, "set_logged_model_alias", None)` if you must support older MLflow builds.

**Link evaluation results:** After `mlflow.genai.evaluate()`, metrics are **automatically linked** to the **active LoggedModel** for that evaluation context when using the GenAI eval harness ([eval harness concepts](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness)). You can also log metrics explicitly:

```python
with mlflow.start_run():
    logged = mlflow.create_logged_model(name="my-agent-iteration-7")
    model_id = logged.model_id
    mlflow.log_metrics({"accuracy": 0.92, "latency_p95_ms": 800}, model_id=model_id)
```

**Rollback (generic):** Point the **champion** (or **production**) alias at a prior `model_id`, or re-resolve `runs:/...` / UC version in your deployment config. Document which alias means “live” vs “candidate” in your team’s runbook.

**Load** [`references/logged-model-patterns.md`](references/logged-model-patterns.md) **if** you need initialization/finalization or artifact layout patterns. **Load** [`references/model-promotion.md`](references/model-promotion.md) **if** you need promotion workflow details.

### DO / DON'T: LoggedModel

| DO | DON'T |
|----|--------|
| Create LoggedModels inside `mlflow.start_run()` | Create or finalize logged models with no active run when your stack requires run linkage |
| Prefer harness auto-linking for GenAI evals | Assume `log_metrics(..., model_id=)` exists on every MLflow minor version without a fallback |

---

## MLFLOW_ACTIVE_MODEL_ID (production trace linking)

Set **`MLFLOW_ACTIVE_MODEL_ID=<logged_model_id>`** in the environment of your **deployed** app (app config, Docker `ENV`, Databricks App `app.yml`, or job cluster env) so **production traces** attach to that LoggedModel. The Databricks UI can then show production traces for that model/version.

- **Pattern:** export or declare `MLFLOW_ACTIVE_MODEL_ID` to the id returned when you created the LoggedModel (or the id of the version you promoted).
- **Docs:** [Link production traces to app versions](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions).

This is separate from UC **registered model** aliases: LoggedModel id ties **tracing**; UC version ties **catalog** consumers and serving.

---

## Part C: UC Model Registration

Use the **Unity Catalog** registry URI for all UC operations ([Models in Unity Catalog](https://docs.databricks.com/en/mlflow/models-in-uc.html)).

### Naming convention

Use a **stable, three-level** UC name: `{catalog}.{schema}.{model_name}`. Choose `model_name` to match your product or agent family (e.g. `support_agent` or `agent_{tenant}`). Document the convention in your repo; avoid ad-hoc string concatenation across teams.

### Standard registration pattern

```python
import mlflow
from mlflow import MlflowClient

client = MlflowClient(registry_uri="databricks-uc")
catalog, schema = "main", "ml_models"
uc_model_name = f"{catalog}.{schema}.my_agent"

try:
    client.create_registered_model(uc_model_name)
except Exception:
    pass  # already exists

run_id = "..."  # run where pyfunc/langchain model was logged
result = client.create_model_version(
    uc_model_name,
    source=f"runs:/{run_id}/model",
)
```

You can also use `mlflow.register_model(model_uri, uc_model_name)` with `registry_uri` set to `databricks-uc` — equivalent intent; keep **one** style per pipeline for clarity.

### Custom aliases and metric-based gating

```python
# After comparing new eval metrics to thresholds or to the current @champion:
client.set_registered_model_alias(uc_model_name, "champion", result.version)
```

**Gating pattern** (conceptual):

```python
def promote_if_better(client, uc_model_name, new_version, new_metrics, thresholds, judges):
    champion = None
    try:
        champion = client.get_model_version_by_alias(uc_model_name, "champion")
    except Exception:
        pass
    if champion is None:
        client.set_registered_model_alias(uc_model_name, "champion", new_version)
        return
    old_metrics = load_metrics_for_version(client, champion)  # your helper
    if all(new_metrics[k] >= thresholds[k] for k in thresholds) and beats(new_metrics, old_metrics, judges):
        client.set_registered_model_alias(uc_model_name, "champion", new_version)
```

Align metric names and thresholds with your eval harness ([eval harness](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness)).

### DO / DON'T: UC Registration

| DO | DON'T |
|----|--------|
| `MlflowClient(registry_uri="databricks-uc")` for UC | Use default workspace registry by mistake |
| Compare new scores to `@champion` before alias promotion | Promote to `@champion` without gating |
| Keep MLflow LoggedModel **champion** and UC **champion** semantics documented | Assume one alias serves both tracing and catalog without defining ownership |

**Load** [`references/uc-gating.md`](references/uc-gating.md) **if** you need extended UC registration, score comparison, or gating walkthroughs.

---

## Deployment job linkage

**Pattern:** Store **deployment metadata** on the model version (tags or version description): serving endpoint name, Databricks App URL, bundle job name, or Git SHA. When promotion sets `@champion`, a **downstream job** (or orchestration webhook) reads that metadata and deploys or updates the endpoint/app to that artifact.

- On **promotion**: trigger CI/CD or a Databricks Job that resolves `models:/catalog.schema.model@champion` and updates inference infrastructure.
- Keep **rollback** as re-pointing the alias plus the same job with the previous version id.

---

## Common Mistakes

| Mistake | Why it hurts | What to do instead |
|--------|----------------|-------------------|
| Logging without `resources` | Missing endpoint/index lineage | Pass `DatabricksServingEndpoint`, indexes, etc. |
| No active `mlflow.start_run()` when creating LoggedModels | Broken run linkage | Open a run before `create_logged_model` |
| Default registry URI for UC | Wrong registry backend | `registry_uri="databricks-uc"` |
| Promoting UC `@champion` without gating | Regressions in production | Compare eval metrics to thresholds and incumbent |
| Missing `MLFLOW_ACTIVE_MODEL_ID` in prod app | Traces not tied to a model card line | Set env var per deployed version |
| Omitting `set_model()` in agent module | Path-based `log_model` fails | `mlflow.models.set_model(agent)` at import time |

---

## Validation Checklist

- [ ] Agent logged with `pip_requirements` including `mlflow[databricks]` (and SDK as needed).
- [ ] All inference dependencies in `resources`.
- [ ] `mlflow.models.predict` succeeds on a smoke input before deploy.
- [ ] LoggedModel created in the run that owns iteration artifacts (if applicable).
- [ ] Eval metrics linked via GenAI eval harness and/or `log_metrics(..., model_id=...)`.
- [ ] UC naming convention documented; client uses `databricks-uc`.
- [ ] Champion promotion policy defined: LoggedModel alias vs UC `@champion` vs both.
- [ ] Production app sets `MLFLOW_ACTIVE_MODEL_ID` when trace-to-version linkage is required.

---

## References

### Related skills

- **Foundation Step 1 — MLflow GenAI Foundation:** [`../../foundation/01-mlflow-genai-foundation/SKILL.md`](../../foundation/01-mlflow-genai-foundation/SKILL.md)
- **Foundation Step 2 — Experiment Tracing:** [`../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md`](../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md)
- **SDLC Step 4 — Evaluation Runs:** Produces `evaluation_results` and `thresholds_met` for this step

### Official documentation (grounding)

| Resource | URL |
|----------|-----|
| Models in Unity Catalog | https://docs.databricks.com/en/mlflow/models-in-uc.html |
| Link production traces to app versions | https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions |
| GenAI eval harness concepts | https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness |
| Log agent to MLflow (Databricks) | https://docs.databricks.com/aws/en/generative-ai/agent-framework/log-agent |
| MLflow Logged Models | https://mlflow.org/docs/latest/ml/tracking/log-model |
| MLflow Model Registry | https://mlflow.org/docs/latest/model-registry.html |

### Local reference files (this skill)

| File | Content |
|------|---------|
| [`references/agent-logging.md`](references/agent-logging.md) | pyfunc/LangChain logging, resources, validation, errors |
| [`references/logged-model-patterns.md`](references/logged-model-patterns.md) | LoggedModel lifecycle, artifacts, score linking |
| [`references/uc-gating.md`](references/uc-gating.md) | UC registration, score comparison, edge cases |
| [`references/model-promotion.md`](references/model-promotion.md) | Aliases, promotion criteria, rollback, audit |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific code. Added `MLFLOW_ACTIVE_MODEL_ID` for production trace linking. Grounded in official UC model registry and eval-harness docs. |
| 3.1.0 | 2026-03-27 | Reference files; DO/DON'T blocks; Scripts section; expanded references |
| 3.0.0 | 2026-03-26 | Initial skill: agent logging, LoggedModel snapshots, UC registration with gating |
