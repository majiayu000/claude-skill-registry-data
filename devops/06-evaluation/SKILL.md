---
name: 06-evaluation
description: >
  Use when evaluating an agent's response quality and safety before deployment.
  Covers running agent-evaluate, evaluation dataset format, built-in judges
  (relevance, groundedness, safety), interpreting results, and customizing
  eval datasets. Track A Step 6. Consumes a working agent with tools from
  Steps 1-5. Produces evaluation results and confidence to deploy.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Agent evaluation (agent-evaluate, built-in judges) runs via the MLflow SDK on serverless workspace compute; no bundle resource. Identical on both clients. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.0.0"
  domain: "genai-agents"
  pipeline_position: "A6"
  consumes: "agent_with_tools, authenticated_client, predict_fn"
  produces: "evaluation_results, eval_dataset"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-6-evaluate-the-agent, docs.databricks.com/aws/en/generative-ai/agent-evaluation, mlflow.org/docs/latest/genai/evaluation"
fields_read:
  - agent.benchmark_seeds.seed_examples
  - governance.verification.smoke_test_cases
  - docs.agent_tool_plan.selected_tools
  - docs.agent_tool_plan.verification.tool_smoke_tests
inputs:
  - name: agent_tool_plan_ref
    required: false
    description: >
      Path to docs/agent_tool_plan.yaml. When set, the smoke set is the UNION
      of governance.verification.smoke_test_cases[] (Spec) and
      verification.tool_smoke_tests[] (Plan, one per selected_tools[] entry).
      The fail-closed gate's "any tool returns empty output" condition is
      scoped to selected_tools[] — tools that were never wired cannot trip it.
---

# Track A Step 6: Evaluate the Agent

Verify your agent produces relevant, grounded, and safe responses before
deploying it. The template includes evaluation infrastructure — this step
teaches you to run it, interpret results, and customize the dataset.

## When to Use

- Your agent is running locally with tools, auth, and (optionally) memory
  configured from Steps 1-5.
- You want to validate response quality before deploying to Databricks Apps.
- You need to establish a baseline for ongoing monitoring after deployment.

## Relationship to SDLC Evaluation

This step runs the template's built-in evaluation as a **smoke test**. The full
SDLC evaluation pipeline ([S2](../../../sdlc/02-evaluation-datasets/SKILL.md)–[S4](../../../sdlc/04-evaluation-runs/SKILL.md))
adds custom benchmark datasets, domain-specific scorers with threshold gates,
and human feedback labeling. Think of A6 as "does my agent work?" and S4 as
"does my agent meet production quality bars?"

| Aspect | A6 (this step) | S4 (SDLC) |
|--------|----------------|-----------|
| **Scope** | Template smoke test | Comprehensive quality gate |
| **Dataset** | `tests/eval_dataset.json` (5-10 cases) | Custom benchmark (50-500+ cases) |
| **Scorers** | Built-in judges only | Custom + built-in judges with thresholds |
| **Trigger** | Manual `uv run agent-evaluate` | CI/CD pipeline on every PR |
| **Output** | Pass/fail summary | Detailed metrics, regression detection |

---

## Step 6a: Run the Built-In Evaluation

Smoke evaluation uses the configured model route from `docs/agent_tool_plan.yaml.runtime_config.llm`. The evaluation runner must not substitute a hardcoded model endpoint. If the route is the default Databricks provider, this resolves to `llm_endpoint` in `config.yml`.

The agent template includes evaluation code in `agent_server/evaluate_agent.py`
(or `tests/evaluate_agent.py` depending on your template version). Run it:

```bash
uv run agent-evaluate
```

**What this does:**
1. Loads the evaluation dataset (typically `tests/eval_dataset.json`)
2. Sends each test case to your agent via `predict()`
3. Runs built-in judges against the responses
4. Outputs a summary report with pass/fail and scores

**Expected output:**

```
Running evaluation...
  ✓ relevance: 4/5 passed
  ✓ groundedness: 5/5 passed
  ✓ safety: 5/5 passed
Evaluation complete. Results saved to MLflow experiment.
```

If the command fails with auth errors, see the auth-in-evaluation section below.

---

## Step 6b: Understand the Evaluation Dataset

The template ships a sample dataset in `tests/eval_dataset.json`:

```json
[
  {
    "request": {
      "input": [
        {"role": "user", "content": "What is MLflow?"}
      ]
    },
    "expected_response": "MLflow is an open source platform for managing the ML lifecycle.",
    "expected_retrieved_context": [
      {"doc_uri": "https://mlflow.org/docs/latest/index.html"}
    ]
  }
]
```

| Field | Required | Purpose |
|---|---|---|
| `request` | Yes | The input sent to the agent (`input` messages, optional `custom_inputs`) |
| `expected_response` | No | Ground truth for relevance comparison |
| `expected_retrieved_context` | No | Expected `doc_uri` values for retrieval judges |

The `expected_retrieved_context` field connects to `set_retriever_schema()` from
Step 3 — the `doc_uri` column is how judges match retrieved vs. expected documents.

---

## Step 6c: Understand the Built-In Judges

Agent Evaluation runs multiple judges automatically:

| Judge | What It Checks | Requires |
|---|---|---|
| **Relevance** | Is the response relevant to the question? | `expected_response` (optional — can judge without) |
| **Groundedness** | Is the response grounded in retrieved context? | RETRIEVER spans in traces |
| **Safety** | Does the response avoid harmful content? | Nothing extra |
| **Chunk relevance** | Are retrieved chunks relevant to the query? | RETRIEVER spans |

Judges are LLM-based — they use a Databricks model serving endpoint to
evaluate quality. The evaluation harness handles this automatically.

---

## Step 6d: Interpret Results

After running evaluation, results appear in two places:

### 1. Terminal output

Summary pass/fail counts and aggregate scores.

### 2. MLflow Experiment UI

Navigate to your experiment → **Evaluation** tab for:
- Per-request scores and judge rationale
- Trace visualization for each test case
- Aggregate metrics across the dataset

Look for:
- **Low relevance scores** → Agent may need better instructions or tools
- **Low groundedness** → Agent may be hallucinating beyond retrieved context
- **Safety failures** → Agent needs guardrails or instruction updates

---

## Step 6e: Customize the Evaluation Dataset

Replace the sample dataset with test cases for your agent's domain:

```json
[
  {
    "request": {
      "input": [
        {"role": "user", "content": "What were Q3 2025 total sales?"}
      ]
    },
    "expected_response": "Q3 2025 total sales were $42.3M.",
    "expected_retrieved_context": [
      {"doc_uri": "catalog.schema.sales_summary"}
    ]
  },
  {
    "request": {
      "input": [
        {"role": "user", "content": "Who is the VP of Engineering?"}
      ]
    },
    "expected_response": null
  }
]
```

**Guidelines for good eval datasets:**
- Include 10-50 test cases covering your agent's core capabilities
- Mix questions that require tools with general knowledge questions
- Include edge cases (ambiguous queries, out-of-scope questions)
- Set `expected_response` to `null` when you only want safety/groundedness
  checks (no relevance baseline)
- Use real `doc_uri` values from your Vector Search indexes

---

## Step 6f: Run Evaluation Programmatically

For more control, call `mlflow.evaluate()` directly:

```python
import mlflow
import json

eval_dataset = json.load(open("tests/eval_dataset.json"))

with mlflow.start_run():
    results = mlflow.evaluate(
        model="agent.py",
        data=eval_dataset,
        model_type="databricks-agent",
    )

    print(f"Metrics: {results.metrics}")
    print(f"Results table:\n{results.tables['eval_results']}")
```

This gives you access to:
- `results.metrics` — aggregate scores (relevance, groundedness, safety)
- `results.tables["eval_results"]` — per-row results with judge rationale

---

## Authentication in Evaluation Context

Evaluation runs use **different auth** than Model Serving or Databricks Apps.
Key differences:

| Context | Auth Method |
|---|---|
| Model Serving | OBO (user token passthrough) |
| Databricks Apps | SP (app service principal) |
| **Evaluation** | **Your credentials** (notebook/CLI user) or `SystemAuthPolicy` SP |

If your agent uses OBO (`IS_IN_DB_MODEL_SERVING_ENV`), evaluation will fail
because OBO environment variables are absent. Your agent's environment detection
from Step 4 handles this — it falls back to default `WorkspaceClient()` auth
outside Model Serving.

If evaluation still fails with permission errors:
1. Verify your agent declares resources in `SystemAuthPolicy` (see Step 4,
   `references/model-serving-auth-passthrough.md`)
2. Ensure the evaluation user has access to all resources the agent needs
3. Check that Genie Spaces and Vector Search indexes are granted to the system SP

---

## DO / DON'T

### DO — Run evaluation before every deployment

```bash
uv run agent-evaluate
# Review results, then deploy
```

### DON'T — Deploy without evaluating

Changes to instructions, tools, or models can cause regressions that are
invisible without evaluation.

### DO — Keep the eval dataset in version control

```
tests/
├── eval_dataset.json          # Your test cases
└── eval_dataset_sample.json   # Template's original (for reference)
```

### DON'T — Use only the template's sample dataset

The sample covers generic cases. Replace it with your domain-specific test
cases for meaningful quality assurance.

### DO — Treat low scores as blockers

```
# If relevance < 80% or safety has failures:
# 1. Review failing test cases in MLflow UI
# 2. Fix agent instructions or tools
# 3. Re-run evaluation
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `uv run agent-evaluate` not found | Check `pyproject.toml` for the `agent-evaluate` script entry |
| Auth errors during evaluation | Agent's env detection should fall back to default auth outside serving |
| All relevance scores are low | Check `expected_response` values — they may not match your agent's style |
| Groundedness judge returns N/A | Agent has no RETRIEVER spans — add `set_retriever_schema()` (Step 3) |
| Safety judge flags benign content | Review the flagged responses; may need instruction tuning |

---

## Validation Gate

All must pass before proceeding:

- [ ] `uv run agent-evaluate` runs to completion without errors
- [ ] Evaluation results visible in MLflow Experiment UI
- [ ] Relevance scores meet your threshold (recommended: ≥80%)
- [ ] Zero safety failures
- [ ] Evaluation dataset customized with domain-specific test cases
- [ ] Auth works in evaluation context (no permission errors)

## Next Step

After passing this gate, **load and execute**
`tracks/A-custom-agent-apps/07-deploy-and-query/SKILL.md` (A7: Deploy and Query)
for the first manual deployment.

## Going Further: Full SDLC Evaluation

The smoke test above validates basic functionality. After completing Track A
(A7), you will enter the SDLC pipeline to build the comprehensive evaluation
with custom scorers and threshold gates. When you reach that point, load these
skills in order:

1. **Load and execute** `sdlc/02-evaluation-datasets/SKILL.md` (S2) — build your benchmark dataset (50-500+ rows)
2. **Load and execute** `sdlc/03-scorers-and-judges/SKILL.md` (S3) — create domain-specific scorers with pass/fail thresholds
3. **Load and execute** `sdlc/04-evaluation-runs/SKILL.md` (S4) — run `mlflow.genai.evaluate()` with your `predict_fn` from A5

S4 uses the same `predict_fn` you produced in A5 — no additional wrapping
needed. The SDLC evaluation replaces this smoke test as the production quality
gate.

## Notes to Carry Forward

| Key | Value |
|-----|-------|
| `eval_dataset` | Path to your evaluation dataset |
| `eval_results` | Baseline metrics (relevance, groundedness, safety scores) |
| `mlflow_experiment` | MLflow experiment name/ID with evaluation runs |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [A5: Lakebase Memory](../05-lakebase-memory/SKILL.md) | Previous step — produces `predict_fn` |
| [A7: Deploy and Query](../07-deploy-and-query/SKILL.md) | Next step |
| [S2: Evaluation Datasets](../../../sdlc/02-evaluation-datasets/SKILL.md) | SDLC: custom benchmark datasets |
| [S3: Scorers and Judges](../../../sdlc/03-scorers-and-judges/SKILL.md) | SDLC: custom scorers with threshold gates |
| [S4: Evaluation Runs](../../../sdlc/04-evaluation-runs/SKILL.md) | SDLC: comprehensive evaluation with `mlflow.genai.evaluate()` |

## References

- [Author an agent — Evaluate the agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-6-evaluate-the-agent)
- [Agent Evaluation](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/)
- [Evaluation sets](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/evaluation-set)
- [MLflow evaluate()](https://mlflow.org/docs/latest/genai/evaluation/)
- [Agent Evaluation judges](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/evaluation-judges)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-11 | Initial skill: agent-evaluate, eval datasets, judges, result interpretation, auth context |
