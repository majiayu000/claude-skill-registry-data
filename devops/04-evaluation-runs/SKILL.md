---
name: 04-evaluation-runs
description: >
  Use when running mlflow.genai.evaluate() to test agent quality before
  deployment. Covers the predict_fn contract, answer-sheet mode for
  re-scoring existing outputs, threshold gates, retry wrappers, human
  feedback sessions, and conversation evaluation — even if you just want
  "run my benchmarks and tell me pass or fail." Also use when collecting
  human labels to calibrate automated scorers. SDLC Step 4.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "`mlflow.genai.evaluate()` runs via the MLflow SDK on serverless workspace compute; no bundle resource. Identical on both clients; on Genie Code execute on serverless and run any CLI step through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.1.0"
  domain: "genai-agents"
  pipeline_position: "S4"
  consumes: "scorer_list, threshold_config, evaluation_dataset"
  produces: "evaluation_results, thresholds_met, mlflow_run_id, failure_shape_classification, failing_trace_ids, safety_buffer, predict_fn_exception_count, predict_fn_sentinel_count_per_run, judges_with_silent_aggregation_dropouts, mlflow_eval_predict_fn_signature, mlflow_eval_known_quality_issues, evaluation_runs_preflight, human_label_count, synthesized_label_count"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations, https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/, https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
fields_read:
  - agent.reviewer_role
  - agent.must_do
  - agent.must_not_do
  - docs.agent_tool_plan.selected_tools
inputs:
  - name: agent_tool_plan_ref
    required: false
    description: >
      Path to docs/agent_tool_plan.yaml. When set, failure-shape classification
      scopes primary_shape: tool_call_empty (and the tool_call_empty routing
      branch) to tools present in selected_tools[] only. Tools that were never
      wired cannot trigger this branch. The retrieval routing branch only
      exists when KA or Vector Search appears in selected_tools[].
---

# Evaluation runs (MLflow GenAI)

Canonical reference for **evaluation execution**, **threshold gating**, **human feedback**, and **repeatability** when using `mlflow.genai.evaluate()` on Databricks. Grounded in the official MLflow 3 GenAI eval harness, evaluation runs, conversation evaluation, and human feedback documentation.

## Upstream Lineage

This skill extends Databricks Agent Skills' `databricks-mlflow-evaluation` skill for `mlflow.genai.evaluate()` execution, regression detection, production trace re-scoring, human labeling loops, and evaluation result analysis. If the eval harness contract or result object behavior is ambiguous, consult the upstream skill first, then preserve this skill's SDLC telemetry and gate-capture requirements.

## When to Use

- Measure agent quality on a fixed benchmark with `mlflow.genai.evaluate()`.
- Wire `predict_fn`, scorers, and dataset—or use **answer sheet** mode with pre-computed `outputs`.
- Gate promote/deploy decisions on judge scores vs thresholds.
- Add **retries** for transient harness or infrastructure failures.
- **Re-score** existing outputs with new scorers or evaluate pre-collected production traces.
- Run **labeling sessions** and sync human annotations into metrics.

## Core Evaluation Flow

```python
import mlflow

results = mlflow.genai.evaluate(
    data=eval_dataset,
    predict_fn=agent_predict_fn,
    scorers=scorer_list,
)
```

The eval harness runs your predictor (if provided), attaches traces, applies scorers, and returns structured results. See [Evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs) and [Eval harness](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness).

## Trace destination (Unity Catalog)

Configure UC trace storage **once** before `evaluate()` so traces persist for labeling and dashboards. See **Skill 07 (Production Monitoring) → Trace Destination** for the full `set_experiment(trace_location=UnityCatalog(...))` pattern and UC permissions.

## predict_fn Contract

MLflow passes **one row’s `inputs`** into `predict_fn` (as a dict). The provided evaluation harness (`run_evaluation.py`) accepts both `str` and `dict` returns — it normalizes dicts to strings automatically via the `_out()` wrapper. Built-in scorers (Safety, RelevanceToQuery) work with traces, so a simple `-> str` return is sufficient.

**`predict_fn` is optional** when `data` already includes an **`outputs`** column (see Answer sheet mode below).

### Using the provided harness (recommended)

Your track's `predict_fn(inputs: dict) -> str` works as-is with `run_evaluation.py`:

```bash
# --experiment-path MUST be the user-and-use-case-pinned eval experiment, e.g.
#   /Users/<user_email>/mlflow/<APP_NAME>-eval
# Read it from .vibecoding-state.md (mlflow_experiment_path with -eval leaf swap)
# instead of using a literal /Shared/my-agent/traces.
uv run run_evaluation.py --predict-module predict_fn.py \
  --experiment-path /Users/<user_email>/mlflow/<APP_NAME>-eval \
  --dataset-table catalog.schema.benchmarks \
  --thresholds '{"safety/mean": 0.7, "relevance_to_query/mean": 0.7}'
```

### Returning dicts for richer scorer input (advanced)

If calling `mlflow.genai.evaluate()` directly (without the harness), return a `dict` to pass richer data to custom scorers:

```python
def make_eval_predict_fn(track_fn):
    """Adapts a track callable for direct mlflow.genai.evaluate() use with dict return."""

    def predict_fn(inputs: dict) -> dict:
        question = inputs["question"]
        response = track_fn(question)
        return {"response": response}

    return predict_fn
```

### Three common dict shapes (for direct evaluate() use)

1. **Simple Q&A** — `(inputs) -> {"response": str}`

```python
def predict_fn(inputs: dict) -> dict:
    q = inputs["question"]
    return {"response": my_agent.answer(q)}
```

2. **RAG** — include retrieval for context-aware scorers:

```python
def predict_fn(inputs: dict) -> dict:
    chunks = retriever.search(inputs["question"])
    answer = my_agent.answer(inputs["question"], chunks)
    return {"response": answer, "retrieved_context": chunks}
```

3. **Conversation** — `inputs` includes message history; same return shape:

```python
def predict_fn(inputs: dict) -> dict:
    messages = inputs["messages"]  # multi-turn history
    return {"response": my_agent.chat(messages)}
```

For multi-turn evaluation patterns, see [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations).

## `Correctness` consumes `expected_response`

The built-in `Correctness` scorer reads `expectations["expected_response"]` from the dataset row — **not** `expected_signal`, `expected_answer`, or any other field name. If your benchmark stores the gold answer under a different key, either rename the column to `expected_response` or pass `targets="expectations/<your_field>"` explicitly when constructing the scorer:

```python
from mlflow.genai.scorers import Correctness

# Default: reads expectations["expected_response"]
correctness = Correctness()

# Explicit target if your dataset uses a different field name
correctness = Correctness(targets="expectations/expected_response")
```

Mismatched field names produce silent `None` rows (the scorer skips, no error) and break threshold gates. See **Skill 02 (Evaluation Datasets)** for the canonical `expected_response` field on dataset rows and **Skill 03 (Scorers and Judges)** for the matching scorer contract.

## Answer sheet evaluation mode

When **`data` includes both `outputs` and `expectations`** (and optionally other columns the scorers need), you can call **`evaluate()` without `predict_fn`**. The harness scores existing outputs—useful to **re-score with new scorers** or **evaluate pre-collected production traces**.

```python
import mlflow

eval_df = ...  # columns: inputs, outputs, expectations (and any scorer inputs)

eval_result = mlflow.genai.evaluate(
    data=eval_df,
    scorers=scorer_list,
    # predict_fn omitted — outputs column supplies model outputs
)
```

This matches the harness behavior described in [Eval harness](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness): pre-computed predictions are scored directly.

## Retry wrapper

Wrap `mlflow.genai.evaluate()` with **retry and exponential backoff** for transient failures (timeouts, rate limits, intermittent worker errors).

```python
import time

TRANSIENT_MARKERS = ("timeout", "temporarily unavailable", "rate limit", "503", "504")


def is_retryable_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return any(m in msg for m in TRANSIENT_MARKERS)


def evaluate_with_retry(data, scorers, predict_fn=None, max_retries=4, base_sleep_s=10):
    for attempt in range(max_retries):
        try:
            kwargs = {"data": data, "scorers": scorers}
            if predict_fn is not None:
                kwargs["predict_fn"] = predict_fn
            return mlflow.genai.evaluate(**kwargs)
        except Exception as e:
            if attempt >= max_retries - 1:
                raise
            if not is_retryable_error(e):
                raise
            time.sleep(base_sleep_s * (attempt + 1))
```

Tune `TRANSIENT_MARKERS`, worker env vars, and max workers per your environment. Optionally fall back to **sequential row-by-row** evaluation if batch mode keeps failing.

## Handling None traces

If **`predict_fn` raises** for a row, the harness may record **`None`** for that row’s trace. Do not assume every index has a valid trace.

```python
for i, tr in enumerate(eval_result.traces or []):
    if tr is None:
        # log row id, skip tagging, or collect for retry
        continue
    # use tr.trace_id, etc.
```

## Extracting results

After `evaluate()`, use the returned object’s fields (names align with [Evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs)):

```python
eval_result = mlflow.genai.evaluate(...)

metrics = eval_result.metrics  # aggregate scorer metrics
traces = eval_result.traces  # per-row traces; entries may be None
table = eval_result.eval_table  # tabular join of inputs, outputs, scores
```

Prefer **`eval_table`** for threshold checks on per-row or aggregated columns.

## Score normalization

Two scales often appear in the same pipeline:

| Role | Typical scale | Example |
|------|----------------|---------|
| Harness / MLflow metric columns | 0–1 means (`metric/mean`) | `relevance/mean` |
| Product thresholds in “points” | 0–100 per judge | dashboard gates |

Normalize before comparing: multiply 0–1 by 100 when your gates expect 0–100, or divide thresholds by 100 when comparing to 0–1 columns. Keep **one mental model per gate** so you never compare raw 0–1 scores to 0–100 thresholds without conversion.

## Threshold gate checks

See **Skill 03 (Scorers and Judges) → Threshold Checking** for the `all_thresholds_met()` pattern and normalization helpers. Log pass/fail and persist `thresholds_met` on the MLflow run for auditability.

## Failure shape router (normative)

When a scored evaluation **fails its gate**, the next iteration step depends on **what kind of failure** it was — not just which scorer regressed. Emit a `failure_shape_classification` payload alongside threshold results, and route iteration based on `primary_shape`:

```yaml
failure_shape_classification:
  primary_shape: enum  # one of: instruction | tool_call_empty | retrieval | scorer_calibration | safety_classifier
  failing_scorers_if_regressed: [string]
  l1_failures: [string]              # L1 = architecture-level (system prompt, role binding, refusal)
  failing_trace_ids:
    - trace_id: string
      failing_scorers: [string]
      predict_fn_status: string      # ok | exception | sentinel
```

### Routing rules

| `primary_shape` | Route to | Pre-condition |
|-----------------|----------|---------------|
| `instruction` | **Skill 08b (prompt hand-authoring)** | Only if `l1_failures` is empty. If L1 failures exist, route to architecture / system-prompt redesign instead — do **not** paper over an L1 failure with prompt iteration. |
| `tool_call_empty` | **Skill 06 direct trace debug** | Symptoms: `UNRESOLVED_COLUMN.WITH_SUGGESTION`, `TABLE_OR_VIEW_NOT_FOUND`, permission-denied, or empty tool output. Fix the data/grant/SQL-grounding issue before re-running eval. |
| `retrieval` | **Retrieval tuning** (chunking, reranker, top-k, embeddings) | Failing scorers are retrieval-shaped (`groundedness`, `retrieval_relevance`, `context_precision`). Do not iterate the system prompt. |
| `scorer_calibration` | **Skill 03 (Scorers and Judges)** | Judge disagrees with human labels at >X%. Fix the scorer prompt, aggregation, or `feedback_value_type` before treating the eval signal as ground truth. |
| `safety_classifier` | **Endpoint audit and role re-binding** | Safety scorer regressed because the scoring endpoint is the wrong model or hit a guardrail. Audit `llm_role_endpoints.llm_judge_safety` binding before iterating the agent. |

**Hard rule:** never route an L1 failure to Skill 08b. L1 means architecture/role-binding/refusal — instruction iteration cannot fix it. Mis-routing here is the single most expensive failure mode in the SDLC.

## Eval telemetry contract (normative)

Every scored evaluation run must capture and persist the following fields on the MLflow run (as tags, params, or artifact JSON — pick one and stay consistent):

| Field | Type | Meaning |
|-------|------|---------|
| `failing_trace_ids` | `[{trace_id, failing_scorers, predict_fn_status}]` | Per-row failure detail. Required for routing and for re-running iteration on a focused subset. |
| `safety_buffer` | `{<scorer_name>: float}` | Margin between observed metric and gate threshold (positive = passing with headroom; negative = failing). Lets the next iteration step know how close to the cliff each scorer is. |
| `predict_fn_exception_count` | `int` | Total rows where `predict_fn` raised. Non-zero values mean some scorer means are computed over a smaller denominator than the dataset row count. |
| `predict_fn_sentinel_count_per_run` | `int` | Rows that returned a sentinel string (e.g. `"INPUT_GUARDRAIL_BLOCKED"`, `"LAKEBASE_COLD_START_FAILED"`). Not the same as exceptions — sentinels successfully return but represent productized debt. See `debt: predict_fn_input_guardrail_sentinel`. |
| `judges_with_silent_aggregation_dropouts` | `[string]` | Judges where `<scorer>/mean` is missing from `eval_result.metrics` because aggregation defaulted to `[]`. Must be empty before promoting. See **Skill 03 → make_judge aggregation contract**. |
| `mlflow_eval_predict_fn_signature` | `string` | The exact signature the harness saw, e.g. `(inputs: dict) -> str` or `(inputs: dict) -> dict`. Captured because mismatched signatures are the most common cause of empty / `None` traces. |
| `mlflow_eval_known_quality_issues` | `[{issue_id, owner_prompt_role, target_prompt_role, status}]` | Open quality issues against this evaluation run. If any item has `target_prompt_role: first_scored_eval` and `status != closed`, the gate **must fail closed** until the item is resolved or explicitly waived. |

Capture in a single payload per run so dashboards and the iteration router can read it as one unit:

```python
import json
import mlflow

eval_telemetry = {
    "failing_trace_ids": [...],
    "safety_buffer": {"safety/mean": 0.04, "correctness/mean": -0.12},
    "predict_fn_exception_count": 0,
    "predict_fn_sentinel_count_per_run": 2,
    "judges_with_silent_aggregation_dropouts": [],
    "mlflow_eval_predict_fn_signature": "(inputs: dict) -> str",
    "mlflow_eval_known_quality_issues": [],
}

mlflow.log_dict(eval_telemetry, "eval_telemetry.json")
mlflow.set_tag("predict_fn_exception_count", str(eval_telemetry["predict_fn_exception_count"]))
mlflow.set_tag("predict_fn_sentinel_count_per_run", str(eval_telemetry["predict_fn_sentinel_count_per_run"]))
```

Downstream iteration prompts (`first_scored_eval`, `instruction_iteration`) consume this payload directly — do not re-derive it.

### Vibecoding state: `evaluation_runs_preflight` (producer)

This skill is the **producer** of the
`evaluation_runs_preflight.predict_fn_signature_matches_runner` boolean read by
`preflight_check_registry.predict_fn_signature_matches_runner` (see
`skills/vibecoding-state/references/spec-schema.md` § *Evaluation Runs
Preflight*). After every scored run, in addition to writing the
`eval_telemetry.json` payload above, write the namespaced state block to the
live state file:

```yaml
# state-file shape (set by this skill after every scored run)
evaluation_runs_preflight:
  predict_fn_signature_matches_runner: <bool>     # see derivation below
  last_run_at: "<ISO8601 UTC>"
```

**Derivation.** `predict_fn_signature_matches_runner == true` iff the captured
`mlflow_eval_predict_fn_signature` matches the runner-expected
`(inputs: dict) -> str` or `(inputs: dict) -> dict` shape. A run whose captured
signature does not match flips the boolean back to `false` so the registry
check halts the next prompt in `blocks_prompt_roles[]`
(`local_eval_smoke`, `first_scored_eval`) until the operator fixes the
signature and re-runs. `last_run_at` always records the most recent write.

This replaces the ad-hoc top-level `predict_fn_signature_matches_runner_status`
enum seeded earlier in Phase 1.7 — that name was non-namespaced and stringly.

## Repeatability

- Run the same benchmark **multiple times**; compare variance in outputs or scores.
- Store **references** from a baseline run (e.g. prior SQL or result hashes) in `expectations` for dedicated repeatability scorers.
- Set explicit **targets** for stability (e.g. minimum agreement rate) in your config, not hard-coded in library code.

## Human feedback

> **Scope of this section:** *expert / SME* labeling sessions for ground-truth
> calibration. For **end-user** thumbs-up/down or rating feedback collected
> from a deployed app and written back via `mlflow.log_feedback(...)`, see
> [04c-end-user-feedback](../04c-end-user-feedback/SKILL.md). The two are
> complementary: end-user signal in 04c surfaces *what* to label; expert
> sessions here resolve *what is correct*.

Human labels are **ground truth** for calibrating automated scorers and settling disagreements. Databricks MLflow GenAI supports **label schemas**, **labeling sessions**, and the **MLflow Review App**—a built-in UI where reviewers open traces, apply labels, and resolve disagreements. You can also use a **customizable Review App template** when you need branding or workflow-specific layouts; both paths feed the same labeling session APIs below.

See [Human feedback](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/) and [Label existing traces](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces).

### Label schemas

Define what reviewers capture. **`InputCategorical`** enforces a closed set (fast analytics, high agreement). **`InputText`** is free-form (rationales, failure modes). **`InputTextList`** collects multiple strings (e.g. multiple issues per trace).

```python
from mlflow.genai.label_schemas import InputCategorical, InputText, InputTextList

relevance_schema = InputCategorical(
    name="relevance",
    title="Is the response relevant?",
    options=["relevant", "partially_relevant", "irrelevant"],
)
notes_schema = InputText(name="notes", title="Reviewer notes")
issues_schema = InputTextList(
    name="failure_modes",
    title="What went wrong? (add one per line)",
)
```

Keep names stable across sprints so you can trend metrics over time.

### Labeling session

Create a session per review wave (sprint, model version, or incident). Tie it to the **registered model** (Unity Catalog three-level name) that reviewers associate with the agent.

```python
import pandas as pd
from mlflow.genai.labeling import create_labeling_session

session = create_labeling_session(
    name="sprint-42-review",
    model_name=f"{catalog}.{schema}.my_agent",
    label_schemas=[relevance_schema, notes_schema, issues_schema],
)
```

#### `LabelingSession.add_traces` contract

`session.add_traces(...)` **requires a pandas DataFrame** whose rows include the trace IDs to label. Passing a bare list of strings (`session.add_traces(["tr-1", "tr-2"])`) does **not** work — the call appears to succeed but the session is empty in the Review App.

```python
# CORRECT — DataFrame with a trace_id column
trace_df = pd.DataFrame({"trace_id": [tr.trace_id for tr in eval_result.traces if tr is not None]})
session.add_traces(trace_df)

# WRONG — silently no-ops (or errors depending on version)
# session.add_traces(trace_ids=["tr-1", "tr-2"])
```

Trace IDs typically come from `eval_result.traces` or from production logging. Ensure `mlflow.set_trace_destination(UnityCatalog(...))` matches where those traces were written.

### Sync annotations

After reviewers finish in the Review App (or your custom template backed by the same session):

```python
session.sync(to_dataset=f"{catalog}.{schema}.benchmarks")
```

#### `session.sync` does not merge `log_feedback` labels

**Critical contract gap:** `session.sync(to_dataset=...)` only writes the **label-schema responses** captured inside the Review App back to the dataset's `expectations`. It does **not** merge labels written separately via `mlflow.log_feedback(trace_id=..., name=..., value=...)` — those remain attached to the trace as feedback assessments and are silently dropped by `sync()`.

If reviewers use the in-app thumbs/categorical schema *and* you also call `mlflow.log_feedback(...)` from your own tooling (custom Review App templates, end-user feedback, batch labeling scripts), you must run a second pass to merge the feedback labels into the dataset:

```python
def merge_records_from_session(session_id: str, dataset: str) -> int:
    """Merge `log_feedback` assessments from a labeling session into dataset expectations.

    `session.sync()` only propagates label-schema responses. Feedback assessments
    written via `mlflow.log_feedback(...)` are not merged automatically — this helper
    closes that gap by reading feedback off each trace in the session and writing
    the values back into the dataset row's `expectations`.

    Returns the number of rows updated.
    """
    import mlflow
    from mlflow.genai.datasets import get_dataset

    session = mlflow.genai.labeling.get_labeling_session(session_id)
    ds = get_dataset(dataset)
    updated = 0
    for trace_id in session.trace_ids():
        trace = mlflow.get_trace(trace_id)
        feedback = {a.name: a.value for a in (trace.info.assessments or []) if a.source.source_type == "HUMAN"}
        if not feedback:
            continue
        ds.merge_records([{"trace_id": trace_id, "expectations": feedback}])
        updated += 1
    return updated

merged = merge_records_from_session(session.session_id, f"{catalog}.{schema}.benchmarks")
```

Always run `session.sync(to_dataset=...)` **first**, then `merge_records_from_session(...)` **second**. The two are complementary, not redundant.

#### Labeling-session quality gates

Gate the iteration on label coverage and quality, not just label count. Capture and threshold:

| Field | Type | Gate |
|-------|------|------|
| `human_label_count` | `int` | At least one human label per scorer you intend to calibrate. |
| `synthesized_label_count` | `int` | LLM-as-judge synthesized labels (e.g. from a hand-authored gold-set bootstrapper). Must be tagged distinctly so they don't masquerade as human truth. |
| `comment_text` | `string` (per row) | Reviewer rationale. Required on every label that disagrees with the automated judge — disagreement without rationale is unactionable. |
| Time-to-label distribution | `{p50_seconds, p95_seconds, n}` | If p95 is very low (seconds per trace) reviewers are skimming; if p95 is very high (>20 min) the schema is too complex. Both are signals to redesign before trusting the labels. |

```python
# Persist alongside eval telemetry
labeling_telemetry = {
    "human_label_count": 87,
    "synthesized_label_count": 0,
    "labels_missing_comment_on_disagreement": 4,  # MUST be 0 before promote
    "time_to_label_p50_seconds": 32,
    "time_to_label_p95_seconds": 180,
    "time_to_label_n": 87,
}
mlflow.log_dict(labeling_telemetry, "labeling_telemetry.json")
```

Use synced labels to compute agreement with automated judges, find systematic false positives/negatives, and adjust scorer prompts or thresholds.

**Key insight:** Human feedback is the **calibration standard** for automated scorers—schedule it like you schedule regression tests, not as a rare audit.

## Conversation evaluation runs

- Pass **conversation-shaped `inputs`** (e.g. `messages`) and a `predict_fn` that consumes full history, **or**
- Supply **traces** that already contain multi-turn spans and use answer-sheet style scoring where applicable.

Details and examples: [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations).

## Feedback logging on traces

```python
def log_tags_on_traces(trace_ids, tags_per_id: list[dict]):
    for tid, tags in zip(trace_ids, tags_per_id):
        if tid is not None:
            mlflow.update_trace(tid, tags=tags)
```

Use stable run/session tags (e.g. `eval.session_id`) so traces remain searchable after partial failures.

## Run naming convention

Use **structured, unique** run names for experiments and dashboards:

```python
import datetime

app_name = "my-agent"
version = "1.4.2"
run_name = f"{app_name}-eval-v{version}-{datetime.datetime.utcnow():%Y%m%d_%H%M%S}"
```

Include iteration or git SHA when comparing CI runs.

## DO / DON'T

| Topic | DO | DON'T |
|-------|----|-------|
| predict_fn input | Match `inputs` keys to what you read inside `predict_fn` | Treat the full row as the first argument if MLflow passes only `inputs` |
| Scales | Convert 0–1 vs 0–100 consistently before gates | Compare MLflow `/mean` columns to 0–100 thresholds without conversion |
| Retries | Wrap `evaluate()` with backoff and retryable detection | Single unguarded `evaluate()` in flaky environments |
| Answer sheet | Omit `predict_fn` when `outputs` is pre-filled | Require a live model when you only want to re-score |
| Traces | Check for `None` before `update_trace` | Assume every row produced a trace |
| Human feedback | Define schemas + `create_labeling_session` + `sync()` | Rely only on ad-hoc spreadsheets disconnected from traces |

## Common mistakes

| Mistake | Consequence |
|---------|-------------|
| Mismatched `inputs` keys and `predict_fn` | Scorer or predictor errors, empty responses |
| Ignoring `None` traces | Failed tagging, misleading trace counts |
| Wrong score scale at gate | False pass/fail |
| No retry on transient errors | Noisy CI, aborted batches |
| Skipping human calibration | Drift between judges and user-perceived quality |

## Validation checklist

- [ ] Dataset rows include `inputs` (and `outputs` / `expectations` when using answer sheet mode).
- [ ] `predict_fn` return dict keys match scorer contracts (e.g. `response`, `retrieved_context`).
- [ ] `Correctness` reads `expectations["expected_response"]` — field name verified, no `expected_signal` aliasing.
- [ ] Trace destination set if using UC-backed review or labeling.
- [ ] Thresholds and metric columns use a **single** agreed scale per check.
- [ ] Retry/backoff in place for production or CI evaluation jobs.
- [ ] `eval_result.metrics`, `eval_table`, and `traces` inspected for the metrics you gate on.
- [ ] `failure_shape_classification` emitted with `primary_shape`, `failing_scorers_if_regressed`, `l1_failures`, and `failing_trace_ids`.
- [ ] Iteration routing follows the failure-shape table: instruction (no L1) -> 08b; tool_call_empty -> 06 direct trace debug; retrieval -> retrieval tuning; scorer_calibration -> Skill 03; safety_classifier -> endpoint audit.
- [ ] Eval telemetry payload logged: `failing_trace_ids`, `safety_buffer`, `predict_fn_exception_count`, `predict_fn_sentinel_count_per_run`, `judges_with_silent_aggregation_dropouts`, `mlflow_eval_predict_fn_signature`, `mlflow_eval_known_quality_issues`.
- [ ] `judges_with_silent_aggregation_dropouts` is **empty** before promoting.
- [ ] Optional: labeling schemas and `session.sync()` for human-in-the-loop calibration.
- [ ] If labeling session used: `session.add_traces(...)` was passed a pandas DataFrame (not a list of strings).
- [ ] If labeling session used: ran `session.sync(to_dataset=...)` **and then** `merge_records_from_session(...)` to capture `log_feedback` labels.
- [ ] Labeling telemetry captured: `human_label_count`, `synthesized_label_count`, `comment_text` on disagreements, time-to-label distribution.

## References

### Official Databricks documentation

- [Eval harness](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness)
- [Evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs)
- [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations)
- [Human feedback](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/)
- [Label existing traces (expert feedback)](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces)

### Related skills (same repo)

- [Foundation Step 1: MLflow GenAI Foundation](../../foundation/01-mlflow-genai-foundation/SKILL.md)
- [Foundation Step 2: Experiment Tracing](../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md)
- [SDLC Step 3: Scorers and Judges](../03-scorers-and-judges/SKILL.md)

**Load on demand:** [`references/evaluation-flow.md`](references/evaluation-flow.md) if you need the full evaluation execution sequence; [`references/gate-checking.md`](references/gate-checking.md) if threshold gating fails unexpectedly; [`references/repeatability.md`](references/repeatability.md) if you need to measure score variance across runs.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.1.0 | 2026-04-26 | Added failure-shape router (instruction / tool_call_empty / retrieval / scorer_calibration / safety_classifier) with hard rule against routing L1 failures to Skill 08b. Added normative eval telemetry contract (`failing_trace_ids`, `safety_buffer`, `predict_fn_exception_count`, `predict_fn_sentinel_count_per_run`, `judges_with_silent_aggregation_dropouts`, `mlflow_eval_predict_fn_signature`, `mlflow_eval_known_quality_issues`). Documented `LabelingSession.add_traces` DataFrame contract, the `session.sync` / `log_feedback` merge gap, and the `merge_records_from_session(session_id, dataset)` helper. Added `Correctness` -> `expected_response` field-name normative section. Added labeling-session quality gates (`human_label_count`, `synthesized_label_count`, `comment_text`, time-to-label distribution). Closes retrospective bugs: `LabelingSession.add_traces requires DataFrame`, `session.sync does not merge log_feedback labels`, `Correctness uses expected_response` (Skill 04 row). |
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific code. Added answer sheet evaluation, human feedback/labeling sessions, conversation evaluation. Grounded in official eval-harness, evaluation-runs, and human-feedback docs. |
| 3.1.0 | 2026-03-27 | Added reference files; scripts section; expanded DO/DON'T and references |
| 3.0.0 | 2026-03-25 | Initial structured skill |
