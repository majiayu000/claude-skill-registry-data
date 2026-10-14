---
name: 01-mlflow-genai-foundation
description: >
  Use when starting any new GenAI agent project on Databricks. Covers MLflow 3.x
  GenAI setup: install dependencies, enable autolog, configure connection pooling,
  understand model signatures, detect runtime environment. Foundation Step 1.
  Produces the configured MLflow environment consumed by all subsequent skills.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "MLflow 3.x GenAI environment setup — no deployed resource; configured via the MLflow SDK identically on both clients. On Genie Code the runtime is serverless workspace compute (pre-authenticated); see `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-08-30"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.1.1"
  domain: "genai-agents"
  pipeline_position: "F1"
  produces: "mlflow_environment, autolog_enabled, connection_pool"
  grounded_in: "docs.databricks.com/aws/en/mlflow3/genai, mlflow.org/docs/latest/genai/serving/responses-agent/"
---

# MLflow GenAI foundation

## When to Use

Use this skill when you are:

- Starting a new GenAI agent project on Databricks
- Standardizing MLflow 3.x setup before tracing, evaluation, or deployment
- Aligning dependencies and autolog behavior with the Genie Space Optimizer job bundle

Downstream skills assume this foundation: experiment configuration, `ResponsesAgent` logging, and template formatting for UC-backed resources.

## CRITICAL: ResponsesAgent is MANDATORY

For Databricks agents that must interoperate with AI Playground and MLflow GenAI tooling:

- **`ResponsesAgent` auto-infers model signatures** that are compatible with AI Playground. Rely on that inference instead of hand-written signatures.
- **Never pass `signature=` to `log_model()`** when using `ResponsesAgent` (or other GenAI agent flavors that supply their own schema). Manual signatures often drift from what the runtime and UI expect.
- **Use the `input` key in input examples**, not `messages`. Example payloads must match the schema the agent and evaluator consume.

### DO / DON'T: Model Logging

```python
# DON'T: Manual signature overrides auto-inference
sig = ModelSignature(
    inputs=Schema([ColSpec("string", "messages")]),
    outputs=Schema([ColSpec("string", "response")]),
)
mlflow.pyfunc.log_model(python_model=agent, signature=sig)
```

```python
# DO: Let MLflow infer the signature from ResponsesAgent
mlflow.pyfunc.log_model(
    python_model=agent,
    artifact_path="agent",
    input_example={"input": [{"role": "user", "content": "Hello"}]},
)
```

For complete signature compatibility rules, migration patterns, and verification steps, see: [`references/model-signatures.md`](references/model-signatures.md)

### Decision tree

| Path | When | Notes |
|------|------|--------|
| **ResponsesAgent** | New agents, Playground, standard GenAI flows | Recommended default |
| **ChatAgent** | Legacy chat-style agents already on this API | Maintain only if required |
| **PythonModel** | Custom arbitrary Python | Avoid for standard LLM agents; more manual signature and tracing burden |

## Dependencies

Versions are pinned in the bundle job environment (`databricks.yml`):

| Package | Constraint | Purpose |
|---------|------------|---------|
| `mlflow[databricks]` | `>=3.10.1` | GenAI tracing, evaluation, model registry |
| `databricks-sdk` | `>=0.40.0` | WorkspaceClient, API access |
| `databricks-agents` | `>=1.1.0` | Agent deployment, production monitoring |
| `openai` | `>=1.17` | OpenAI-compatible API client |
| `databricks-openai` | `>=0.3.0` | Supervisor API client (Track B) |

Install locally (use `uv pip` per project convention):

```bash
uv pip install "mlflow[databricks]>=3.10.1" "databricks-sdk>=0.40.0" "databricks-agents>=1.1.0" "openai>=1.17"
```

Track B also needs `databricks-openai`. All dependencies are declared in the
course-level `pyproject.toml` and each track's template `pyproject.toml`.

### DO / DON'T: Dependency Pinning

```python
# DON'T: Unpinned — may resolve to MLflow 2.x with incompatible APIs
# requirements.txt
mlflow
databricks-sdk
```

```yaml
# DO: Lower-bounded — ensures GenAI features are available
dependencies:
  - mlflow[databricks]>=3.10.1
  - databricks-sdk>=0.40.0
```

For the full list of dependency anti-patterns, see: [`references/anti-patterns.md`](references/anti-patterns.md) (entry #8)

## Autolog Setup

Enable autolog **early** (typically at module import or top of the job entrypoint) so traces and model calls are captured consistently.

```python
import mlflow

mlflow.openai.autolog()  # OpenAI-compatible / Databricks Foundation Models
# OR
mlflow.langchain.autolog()  # LangChain / LangGraph agents
```

Call autolog at the top of your agent module or job entrypoint, before any LLM calls.

### DO / DON'T: Autolog Placement

```python
# DON'T: Autolog inside a nested function — misses early calls
def run_evaluation(space_id: str):
    import mlflow
    mlflow.openai.autolog()
    result = call_llm("Analyze this space")
    return result
```

```python
# DO: Module-level autolog — captures everything
import mlflow
mlflow.openai.autolog()

def run_evaluation(space_id: str):
    result = call_llm("Analyze this space")
    return result
```

For all autolog and tracing anti-patterns, see: [`references/anti-patterns.md`](references/anti-patterns.md) (entry #4)

## UC Naming Conventions

Use consistent naming for Unity Catalog resources. Build fully qualified names
from catalog, schema, and resource name parts using f-strings or config values:

```python
catalog = "main"
schema = "my_agent_project"
table_name = "benchmarks"

full_name = f"{catalog}.{schema}.{table_name}"
# Result: "main.my_agent_project.benchmarks"
```

For prompt registry names, follow the same pattern:

```python
prompt_name = f"{catalog}.{schema}.system_prompt"
```

For UC naming anti-patterns, see: [`references/anti-patterns.md`](references/anti-patterns.md)

## Connection pooling

Reuse long-lived clients instead of creating a new HTTP stack per request:

- Instantiate **`WorkspaceClient`** (and OpenAI-compatible clients) once per process or request scope and pass them into agent code.
- Avoid constructing a fresh SDK client inside hot loops; the `databricks-sdk` and typical OpenAI clients keep connection pools internally when reused.

Downstream skills may specify pool sizes or timeouts for serving vs notebook; this skill only establishes the rule: **one shared client pattern per runtime**.

### DO / DON'T: Client Reuse

```python
# DON'T: New client per benchmark — TLS overhead, rate limit risk
for b in benchmarks:
    w = WorkspaceClient()
    result = w.serving_endpoints.query(...)
```

```python
# DO: Shared client — connection pool reused across all calls
w = WorkspaceClient()
for b in benchmarks:
    result = w.serving_endpoints.query(...)
```

For the full connection pooling anti-pattern, see: [`references/anti-patterns.md`](references/anti-patterns.md) (entry #6)

## Environment detection

Use environment variables to branch behavior (serving vs app vs cluster vs local):

```python
import os


def detect_environment() -> str:
    if os.environ.get("IS_IN_DB_MODEL_SERVING_ENV"):
        return "model_serving"
    if os.environ.get("DATABRICKS_APP_NAME"):
        return "databricks_apps"
    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        return "notebook"  # or job
    return "local"
```

Adjust return values or add finer distinctions (e.g. job vs notebook) if your agent needs different connection or logging settings per runtime.

For the complete implementation with `RuntimeEnvironment` enum, per-environment configuration table, client factory, and testing patterns, see: [`references/environment-detection.md`](references/environment-detection.md)

## Common mistakes

| Mistake | Why it hurts | Fix |
|---------|----------------|-----|
| Passing `signature=` to `log_model()` for `ResponsesAgent` | Breaks auto-inferred GenAI schema; Playground/eval mismatch | Omit `signature=`; use framework defaults |
| Using `messages` in input examples | Wrong schema for many GenAI agents and scorers | Use `input` (and keys your model expects) |
| Logging with `PythonModel` for simple LLM agents | Extra maintenance; easy to get traces/signatures wrong | Prefer `ResponsesAgent` |
| Autolog only inside a nested function | Misses early calls; inconsistent traces | Call autolog at module level or job start |
| Pinning MLflow 2.x patterns on 3.x | Deprecated APIs, wrong tracing hooks | Stay on `mlflow[databricks]>=3.10.1` and current docs |
| Hardcoding UC names without templates | Environment-specific drift | Use `format_mlflow_template` for shared patterns |

For 12 complete DO/DON'T pairs with code examples, see: [`references/anti-patterns.md`](references/anti-patterns.md)

## Validation checklist

- [ ] `mlflow[databricks]>=3.10.1` installed (match `databricks.yml` job env when deploying)
- [ ] Autolog enabled at module level or immediately after experiment setup
- [ ] `ResponsesAgent` used for new agents (not `PythonModel` unless justified)
- [ ] No manual `signature=` in `log_model()` for GenAI agent types
- [ ] `input` key used in examples (not `messages`)

## References

### Related skills

- **Foundation Step 2 — experiment tracing:** [`../02-experiment-tracing-and-uc-storage/SKILL.md`](../02-experiment-tracing-and-uc-storage/SKILL.md) for experiment IDs, run lifecycle, and tracing details beyond autolog.
- **Track A Step 2 — Agent Framework & ResponsesAgent:** [`../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md`](../../tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) for implementation patterns and logging.

### Official documentation

- [MLflow GenAI concepts](https://mlflow.org/docs/latest/genai/)
- [MLflow tracing](https://mlflow.org/docs/latest/tracing/)
- [MLflow Model Signatures](https://mlflow.org/docs/latest/models.html#model-signature)
- [ResponsesAgent API](https://mlflow.org/docs/latest/genai/serving/responses-agent/)

### Reference files (this skill)

| File | Content |
|------|---------|
| [`references/model-signatures.md`](references/model-signatures.md) | Signature auto-inference, compatibility matrix, migration guide, verification |
| [`references/environment-detection.md`](references/environment-detection.md) | Full `detect_environment()` implementation, per-env config, client factory, tests |
| [`references/anti-patterns.md`](references/anti-patterns.md) | 12 DO/DON'T pairs with code examples covering all common mistakes |

## Reference Implementation

The patterns in this skill are demonstrated in the
[Genie Space Optimizer](../../README.md) codebase. In your own project,
apply them to your module structure — the principles (autolog placement,
connection pooling, environment detection) are framework-agnostic.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2026-03-26 | Initial skill: dependencies, autolog, signatures, environment detection, common mistakes |
| 3.1.0 | 2026-03-26 | Added reference files (`model-signatures.md`, `environment-detection.md`, `anti-patterns.md`); inline DO/DON'T pairs for model logging, dependency pinning, autolog placement, client reuse; version history table; expanded References section with reference file pointers |
