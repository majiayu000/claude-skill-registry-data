---
name: 02-evaluation-datasets
description: >
  Use when you need to create, manage, or load evaluation datasets for
  testing agent quality. Covers the MLflow GenAI data format, persisting
  benchmarks in Unity Catalog, merging records without duplicates, and
  validating data before evaluation — even if you just want "give me a
  dataset I can pass to mlflow.genai.evaluate()." Also use when building
  benchmarks from production traces or SME labels. SDLC Step 2.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Evaluation datasets persisted in UC via the MLflow GenAI SDK; no bundle resource. Identical on both clients; on Genie Code run any CLI step through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.1.0"
  domain: "genai-agents"
  pipeline_position: "S2"
  consumes: "registered_prompts"
  produces: "evaluation_dataset, mlflow_dataset_entity"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
fields_read:
  - ui.user_journeys
  - agent.benchmark_seeds.coverage_buckets
  - agent.benchmark_seeds.seed_examples
  - docs.agent_tool_plan.selected_tools
  - docs.agent_tool_plan.verification.tool_smoke_tests
inputs:
  - name: agent_tool_plan_ref
    required: false
    description: >
      Path to docs/agent_tool_plan.yaml. When set, the skill APPENDS one
      tool-shaped benchmark row per verification.tool_smoke_tests[] entry on top
      of the generic Spec rows. Tool families absent from selected_tools[]
      contribute zero appended rows.
---

# Evaluation Dataset Creation

Patterns for building, validating, versioning, and logging evaluation datasets for GenAI agents. Complements SDLC Step 4 (evaluation runs and scorers) by focusing on **data shape**, **UC persistence**, and **dataset lifecycle**, grounded in [Databricks MLflow GenAI eval monitor](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness) documentation.

## Upstream Lineage

This skill extends Databricks Agent Skills' `databricks-mlflow-evaluation` skill for evaluation dataset construction, production trace-to-dataset workflows, and expectation schema guidance. If local dataset guidance is insufficient or MLflow evaluation dataset APIs drift, consult the upstream skill first, then adapt its patterns to this workshop's canonical row fields and SDLC artifact contracts.

## When to Use

- Defining benchmark suites for agent quality gates
- Persisting rows to Unity Catalog Delta tables behind `mlflow.genai.datasets`
- Loading and merging records without schema surprises across jobs or tasks
- Validating rows **before** `mlflow.genai.evaluate()` so bad data never skews metrics
- Balancing splits (`train` / `held_out`) and provenance (`curated`, `synthetic`, `human_labeled`)

---

## Official data format (`mlflow.genai.evaluate`)

Per the [eval harness parameters](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness#parameters-for-mlflowgenaievaluate), each record aligns with **`EvaluationDataset`** schema. Either **`inputs` + `outputs`** or **`trace`** is required; you cannot pass both.

| Field | Data type | Description | Direct evaluation (`predict_fn`) | Answer sheet |
| --- | --- | --- | --- | --- |
| `inputs` | `dict[Any, Any]` | Passed to `predict_fn` as `**kwargs`; keys must match parameter names; JSON-serializable | Required | From `trace` if omitted |
| `outputs` | `dict[Any, Any]` | App outputs for that input; JSON-serializable | Omit (MLflow builds from trace) | Required with `inputs` |
| `expectations` | `dict[str, Any]` | Ground truth for scorers; keys are `str`; JSON-serializable | Optional | Optional |
| `trace` | `mlflow.entities.Trace` | Full trace for the request | Omit (MLflow generates) | Required instead of `inputs`+`outputs` |

**Direct evaluation:** rows typically have `inputs` and optional `expectations` only.

**Answer sheet:** rows have `inputs` + `outputs`, or a single `trace`, plus optional `expectations`.

### `EvaluationDataset` vs DataFrame / list-of-dicts

Databricks recommends **`mlflow.genai.datasets.EvaluationDataset`** when available: it enforces schema validation and improves lineage tracking. Raw **pandas DataFrame**, **list of dicts**, or Spark DataFrame are accepted if they match the same column semantics. See [Building MLflow evaluation datasets](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset).

---

## Evaluation record schema (transferable)

`mlflow.genai.evaluate()` unpacks each row's `inputs` dict as **keyword arguments** to `predict_fn`. Every key in `inputs` must match the predictor's signature (use `**kwargs` only for optional or closure-fed values).

### Minimal shape (docs and quick tests)

```python
# Chat / generic agent
{"inputs": {"question": "What is X?"}, "expectations": {"reference_answer": "..."}}

# RAG agent — pass what your app and scorers need
{
    "inputs": {"query": "...", "retrieved_context": "..."},
    "expectations": {"citations": ["doc:page"], "answer": "..."},
}

# SQL / tool agent
{
    "inputs": {"question": "Total cost by region?"},
    "expectations": {"expected_sql": "SELECT ...", "expected_tables": ["db.schema.t"]},
}
```

### Production-oriented shapes (examples)

Use **only** fields your `predict_fn` and scorers actually read. Typical additions:

| Agent type | `inputs` (examples) | `expectations` (examples) |
| --- | --- | --- |
| Chat | `messages`, `session_id`, `user_id` | `reference_answer`, safety labels |
| RAG | `query`, `document_ids`, `max_chunks` | `answer`, `citation_spans`, `must_cite` |
| SQL / analytics | `question`, `catalog`, `schema`, `constraints` | `expected_sql` or `expected_result_hash`, lineage (`split`, `provenance`, `validation_status`) |

If scorers read ground truth from `expectations`, **mirror** any critical label from `inputs` into `expectations` when your judges expect a fixed key (for example SQL string under both `inputs["expected_sql"]` and `expectations["expected_response"]`).

---

## Canonical evaluation-dataset fields (normative)

Every row in a benchmark dataset MUST carry the following canonical fields, regardless of agent shape. These names are the contract between dataset producers, runners, and scorers — do not invent synonyms.

```yaml
eval_dataset_required_fields:
  - row_id              # stable per-row identifier (used as merge key, dedup key, regression-tracking key)
  - request             # the user-facing input (mirrored under inputs.<key> for predict_fn)
  - expected_response   # canonical ground truth consumed by the Correctness scorer
  - expected_signal     # SECONDARY classification field (e.g. intent, severity, topic) — never silently mirrored into expected_response
  - bucket              # coverage bucket (e.g. "aggregation", "ranking", "edge_case", "permission_denied")
  - journey_id          # which user journey this row exercises (links to ui.user_journeys)
  - split               # train | held_out | regression | gold
  - provenance          # curated | synthetic | auto_corrected | issue_failing_trace | labeling_session_merge
```

**Hard rules:**

- `expected_response` is the ONLY field the [`Correctness`](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/correctness) scorer reads as ground truth. Populate it directly with the answer string (or canonical SQL) the agent should produce.
- `expected_signal` is allowed only as a **secondary classification field** (e.g. `expected_signal = "policy_refusal"` for a guardrail label). The runner MUST NOT silently mirror `expected_signal` into `expected_response`. If a scorer needs the signal as ground truth, write it under `expected_response` explicitly with intent.
- `row_id` is required for `merge_records` upserts and for tagging regressions across runs. Use a stable hash of `(request, journey_id)` if you do not have a natural key.
- `bucket`, `journey_id`, and `split` together support coverage gates (see below).

### Coverage gates (normative thresholds)

Datasets that do not meet the following minima MUST fail pre-evaluation validation:

```yaml
min_rows: 40
per_bucket_min_rows: 1
per_journey_min_rows: 1
expectations_schema_complete: true              # all required fields present + non-empty for split != "regression"
eval_dataset_canonical_source: enum             # uc_table | local_json | labeling_session_merge
```

`expectations_schema_complete` means: for every row where `split != "regression"`, all canonical fields above are present and `expected_response` is non-empty. Regression rows may carry `expected_response = null` only when the row is gated on a scorer threshold (see `references/benchmark-generation.md` §11).

`eval_dataset_canonical_source` records where the row set came from. The runner reads this once at startup and refuses to evaluate if the value is unknown — this prevents silent mixing of incompatible sources.

---

## Creating and persisting datasets (UC)

**Table naming:** use a stable Unity Catalog identifier, e.g. **`{catalog}.{schema}.{app_name}_benchmarks`** (replace with your catalog, schema, and app slug).

### Tabular construction (pandas)

```python
import pandas as pd

def rows_to_eval_df(questions, expectations=None):
    records = []
    for i, q in enumerate(questions):
        r = {"inputs": {"question": q}}
        if expectations and i < len(expectations):
            r["expectations"] = expectations[i]
        records.append(r)
    return pd.DataFrame(records)
```

### `get_dataset` + `merge_records` (SDK)

Aligns with [Create a dataset using the SDK](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset#create-a-dataset-using-the-sdk):

```python
import mlflow.genai.datasets

uc_table = f"{catalog}.{schema}.{app_name}_benchmarks"
try:
    eval_dataset = mlflow.genai.datasets.get_dataset(name=uc_table)
except Exception:
    eval_dataset = mlflow.genai.datasets.create_dataset(name=uc_table)

records = [...]  # list of dicts: inputs / outputs / expectations / trace per rules above
eval_dataset.merge_records(records)
```

After merges, **`eval_dataset.to_df()`** (or your validated in-memory frame) is the source of truth for row counts and deduplication before evaluation.

---

## Loading for evaluation

1. **Preferred:** materialize from the **`EvaluationDataset`** or the DataFrame you already validated in memory.
2. **Spark / Delta:** if you read `{catalog}.{schema}.{app_name}_benchmarks` directly, use **`REFRESH TABLE`** (or equivalent) when another task may have altered the table in the same run, then parse JSON columns if `inputs` / `expectations` are stored as strings.

Generic read pattern:

```python
def load_eval_rows_spark(spark, full_table_name: str):
    spark.sql(f"REFRESH TABLE {full_table_name}")
    return spark.table(full_table_name)
```

### Best practice: evaluate from deduped in-memory data, not the raw UC table

**`merge_records`** upserts by record identity; if the same logical example is merged with **different IDs**, the Delta table can accumulate **stale duplicates**. Downstream, reading the table without the same dedupe logic as merge can inflate row counts and distort metrics.

**Do:** dedupe in memory (for example by stable business key: normalized question, session+turn, or hash of `inputs`) and pass **that** DataFrame or list to `mlflow.genai.evaluate()`.

**Don't:** assume the UC table is duplicate-free or that `merge_records` removed older variants unless your merge keys guarantee it.

---

## Generating benchmarks (generic)

Common sources (see also [Data sources for evaluation datasets](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset#data-sources-for-evaluation-datasets)):

- **Production traces** — sample via `mlflow.search_traces()`, filter for quality or failure modes, merge into the dataset after review.
- **SME-curated** — subject-matter experts label inputs and expectations; best for gold sets and regressions.
- **LLM-generated** — expand coverage quickly; always **validate** (schema, permissions, tool contracts) before merge or evaluate.

Validate structure, tool outputs, and permissions **before** calling `mlflow.genai.evaluate()` so invalid rows never enter scored runs.

> **Load** [references/synthetic-eval-generation.md](references/synthetic-eval-generation.md) **if** you need a full recipe for generating a starter eval set from production traces (cluster traces by intent → LLM-generate paraphrases → expectations harvested from SME-labeled traces → validate → merge).
>
> **Load** [references/benchmark-generation.md](references/benchmark-generation.md) **if** you need end-to-end LLM benchmark generation, Genie Q&A extraction, SQL validation, and issue-focused subsets from failing traces.

---

## Dataset versioning and lineage

- **Storage:** UC Delta tables behind `mlflow.genai.datasets` (name like `{catalog}.{schema}.{app_name}_benchmarks`).
- **Runs:** log dataset identity and row counts on the evaluation run (see [Evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs)).
- **Deduping:** enforce stable keys at merge time and again before evaluate.
- **Balance:** track counts per category or split when mixing curated and synthetic data.

---

## Common mistakes

| Mistake | Consequence | Fix |
| --- | --- | --- |
| `inputs` keys ≠ `predict_fn` parameters | `TypeError` or evaluate failures | Align names; optional args via `**kwargs` |
| Ground truth only in `inputs` or only in `expectations` | Scorers see empty labels | Put scorer-expected keys in `expectations` |
| Reading Delta without refresh after concurrent writes | Stale or schema errors | `REFRESH TABLE` + retry |
| Evaluating from raw UC after messy merges | Duplicate / stale rows skew metrics | Dedupe in memory; evaluate that frame |
| Mixing `inputs`+`outputs` with `trace` in one row | Invalid per harness rules | One mode per row |
| Using `query` in data but `predict_fn` expects `question` | Silent mismatch | Same naming in data and app |

---

## DO / DON'T

**DO** — populate every canonical field; put `Correctness` ground truth under `expected_response`:

```python
record = {
    "row_id": "billing_aggregation_001",
    "inputs": {"request": "Total by region?", "expected_sql": sql},
    "expectations": {
        "expected_response": sql,           # canonical ground truth for Correctness
        "expected_signal": "aggregation",   # SECONDARY classification — never mirrored into expected_response
        "bucket": "aggregation",
        "journey_id": "cost_analysis",
        "split": "train",
        "provenance": "curated",
    },
}
```

**DON'T** — silently mirror `expected_signal` into `expected_response` (Correctness will score against the wrong target):

```python
# WRONG — runner copying expected_signal into expected_response
record["expectations"]["expected_response"] = record["expectations"]["expected_signal"]
```

**DON'T** — empty expectations when judges need ground truth:

```python
record = {"inputs": {"request": "...", "expected_sql": sql}, "expectations": {}}
```

**DO** — `get_dataset` with fallback to `create_dataset`, then `merge_records`.

**DON'T** — always `create_dataset` without checking existence (duplicates / errors).

**DO** — validate rows (schema, tools, SQL, permissions) before evaluate.

**DON'T** — trust synthetic outputs without checks.

**DO** — log `dataset` name and `row_count` (and optional validation summaries) on the MLflow run.

**DON'T** — run `evaluate()` with no record of which dataset version was used.

---

## Validation checklist

### Schema and predictor

- [ ] Each row follows harness rules: `inputs`+`outputs` **or** `trace`, not both
- [ ] `inputs` keys match `predict_fn` for direct evaluation
- [ ] `expectations` keys match what scorers read
- [ ] All canonical fields present: `row_id`, `request`, `expected_response`, `expected_signal`, `bucket`, `journey_id`, `split`, `provenance`
- [ ] `Correctness` ground truth lives under `expected_response` only — `expected_signal` is NOT mirrored into it

### Coverage gates

- [ ] `min_rows: 40` satisfied
- [ ] `per_bucket_min_rows: 1` satisfied for every declared bucket
- [ ] `per_journey_min_rows: 1` satisfied for every `ui.user_journeys` entry
- [ ] `expectations_schema_complete: true` (all canonical fields present, `expected_response` non-empty for `split != "regression"`)
- [ ] `eval_dataset_canonical_source` set to one of `uc_table | local_json | labeling_session_merge`

### UC and MLflow

- [ ] Dataset name `{catalog}.{schema}.{app_name}_benchmarks` consistent across writers and loaders
- [ ] After concurrent DDL/DML, refresh reads in multi-task jobs
- [ ] Evaluation uses deduped data aligned with merge semantics

### Content

- [ ] Tool / SQL / RAG outputs validated where applicable
- [ ] Provenance and split fields populated for traceability
- [ ] Regression rows augment, not replace, baseline rows (see `references/benchmark-generation.md` §11)

---

## Scripts

| Script | Description |
| --- | --- |
| [`scripts/create_eval_dataset.py`](scripts/create_eval_dataset.py) | Optional: load questions from JSON, validate, dedupe, persist to UC / MLflow dataset. |

---

## References

### Official documentation

- [Building MLflow evaluation datasets](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/build-eval-dataset)
- [Evaluate GenAI during development (eval harness)](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness)
- [Evaluation runs](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/evaluation-runs)
- [Evaluation dataset reference](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-datasets) (UI + schema)
- [MLflow `genai.evaluate`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.genai.html#mlflow.genai.evaluate)

### Related skills

- **SDLC Step 3** (`03-scorers-and-judges`) — scorers, judges, `predict_fn` contract
- **SDLC Step 1** — prompts used during synthetic or judged workflows
- **SDLC Step 4** — wiring `predict_fn` and evaluation execution

### Local reference files

| Reference | Content |
| --- | --- |
| [`references/evaluation-dataset-patterns.md`](references/evaluation-dataset-patterns.md) | Record shapes, splits, dedup, builder patterns |
| [`references/dataset-lineage.md`](references/dataset-lineage.md) | `mlflow.data`, `log_input`, GenAI datasets, Delta lineage |
| [`references/benchmark-generation.md`](references/benchmark-generation.md) | Trace mining, LLM generation, validation, provenance |

---

## Version history

| Version | Date | Changes |
| --- | --- | --- |
| 4.1.0 | 2026-04-26 | Added canonical evaluation-dataset fields (`row_id`, `request`, `expected_response`, `expected_signal`, `bucket`, `journey_id`, `split`, `provenance`) and coverage gates (`min_rows: 40`, per-bucket/per-journey minima, `expectations_schema_complete`, `eval_dataset_canonical_source`). Pinned `Correctness` ground truth to `expected_response`; banned silent mirroring of `expected_signal`. |
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific patterns. Grounded in official Databricks eval-harness and build-eval-dataset docs. Generic record schemas for different agent types. |
| 3.1.0 | 2026-03-27 | Added reference files, DO/DON'T examples, version history, scripts section |
| 3.0.0 | 2026-03-25 | Initial structured skill with dataset schema, creation, loading, lineage, generation, versioning |
