---
name: 08-prompt-optimization
description: >
  Use when prompt quality has plateaued on your evaluation dataset and you need
  to programmatically improve one or more registered prompts. Covers
  `mlflow.genai.optimize_prompts()` and `GepaPromptOptimizer`, `predict_fn`
  contracts, single and multi-prompt optimization, custom scorers, budget
  controls, registering the optimized output back to UC with a staging alias,
  and the promote-after-eval loop. SDLC Step 8 — run AFTER Step 4 evaluation
  reveals specific regressions or unmet guideline checks. Do NOT use for the
  first pass of an agent (Step 1 Prompt Registry first), or when quality gaps
  are tool/retrieval problems rather than instruction problems.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow >= 3.11 and Unity Catalog Prompt Registry. Preview feature — confirm region availability."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "`optimize_prompts()` / `GepaPromptOptimizer` run via the MLflow SDK on serverless workspace compute; optimized prompts re-registered in the UC Prompt Registry. No bundle resource. Identical on both clients; on Genie Code execute on serverless. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.1.0"
  domain: "genai-agents"
  pipeline_position: "S8"
  consumes: "registered_prompts, evaluation_dataset, scorers, predict_fn"
  produces: "optimized_prompt_versions, staging_aliases, optimization_reports"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/automatically-optimize-prompts, https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/prompt-optimization-quickstart, https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/multi-prompt-optimization, https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/custom-scorers"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Prompt Optimization (MLflow `optimize_prompts` + GEPA)

> **Optional/advanced path.** The default reusable MLflow workshop routes instruction-shaped prompt iteration to `08b-prompt-handauthoring`. This GEPA skill remains maintained for operators who explicitly opt into automated prompt optimization after the cheaper hand-authored loop has been attempted or when a workshop variant intentionally teaches GEPA. Do not invoke this skill from the default seeded prompt flow unless the prompt explicitly declares `prompt_iteration_strategy: gepa`.

## Upstream Lineage

This skill extends Databricks Agent Skills' `databricks-mlflow-evaluation` skill for automated prompt optimization with GEPA and `mlflow.genai.optimize_prompts()`. If optimizer contracts, dataset shape, scorer requirements, or promotion patterns are unclear, consult the upstream skill first, then apply this skill's workshop-specific safeguards and default-routing constraints.

Use this skill when your agent has a **real evaluation dataset** (SDLC Step 2), **real scorers** (Step 3), and an **evaluation run** (Step 4) that identifies specific prompt-related failure modes — e.g. the agent misses guideline checks, cites wrong sources, or omits required structure — but the retrieval and tools are otherwise healthy.

Optimization rewrites registered prompts **against your scorers**, then hands the rewritten version back through your normal eval + alias promotion flow. It is not a substitute for evaluation; it is the automated loop on top of it.

---

## Required GEPA Safeguards

When this skill **is** explicitly invoked (`prompt_iteration_strategy: gepa`), it MUST honor every safeguard below. These are normative requirements, not suggestions — failure to honor any of them must abort the run and emit one of the four structured exits listed below.

- Run `_preflight_reflection_lm` with synthetic 80k-character and 150k-character payloads before committing any GEPA budget. If either probe fails, abort and route the operator to choose a larger-context reflection model.
- Require `gepa>=0.0.26` or document the project optional dependency that installs it. Refuse to import `GepaPromptOptimizer` if the installed version is older.
- Refuse promotion when `holdout_rows < 10`; fall back to full-dataset re-eval and register only as `@candidate_v<N>` (never advance to `@production`).
- Add a circuit breaker after two consecutive no-proposal iterations — abort the loop and emit the `optimization_did_not_beat_baseline_no_candidate` exit.
- Emit one of four structured exits at end of run:
  - `optimization_beat_baseline_promoted`
  - `optimization_did_not_beat_baseline_no_candidate`
  - `optimization_beat_baseline_holdout_inadequate`
  - `optimization_did_not_beat_baseline_anti_correlation`
- Read `llm_role_endpoints.reflection_lm.endpoint` and `workspace_policy_workarounds[]` from the live state file before selecting any reflection model. Never hardcode an endpoint name.
- Capture the following metrics into state on every run:
  - `mlflow_prompt_optimize_compute_budget_used_seconds`
  - `mlflow_prompt_optimize_holdout_size`
  - `mlflow_prompt_optimize_v<N>_template_diff_summary`

---

## Do I Need This Skill?

Use prompt optimization only when **all** of the following are true. Otherwise go back to the listed SDLC step.

| Check | If false → go to |
|-------|------------------|
| Prompt is registered in UC Prompt Registry with an alias (e.g. `@production`). | [01-prompt-registry](../01-prompt-registry/SKILL.md) |
| Evaluation dataset with ≥ 20 rows and expected facts/ids exists. | [02-evaluation-datasets](../02-evaluation-datasets/SKILL.md) |
| Scorers produce a *numeric* signal (or boolean) per row. | [03-scorers-and-judges](../03-scorers-and-judges/SKILL.md) |
| You have a baseline evaluation run showing the failing scorer(s). | [04-evaluation-runs](../04-evaluation-runs/SKILL.md) |
| Quality gap is **instruction-shaped** (guidelines missed, wrong format, wrong tone), not a tool/retrieval gap. | Debug: [tracks/A-custom-agent-apps/08-debugging](../../tracks/A-custom-agent-apps/08-debugging/SKILL.md) |

> **Load** [references/when-to-optimize.md](references/when-to-optimize.md) **if** you need a longer decision checklist and counter-examples where prompt optimization wastes budget.

---

## Minimum Viable Optimization Call

`mlflow.genai.optimize_prompts()` takes three things: a `predict_fn` that exercises the prompt, a labeled `train_data` list, and one or more `prompt_uris`. It returns an `OptimizationResult` with the new prompt version(s).

```python
import mlflow
from mlflow.genai.optimize import GepaPromptOptimizer
from mlflow.genai.scorers import Correctness

experiment = mlflow.set_experiment("/Shared/skyloyalty/agent")

prompt_uri = "prompts:/main.skyloyalty.system_instructions@production"

train_data = mlflow.genai.datasets.get_dataset(
    "main.skyloyalty.skyloyalty_agent_benchmarks"
).to_df().to_dict(orient="records")

def predict_fn(inputs: dict, system_instructions: str) -> dict:
    """Resolve the prompt variable `system_instructions` at call time."""
    from skyloyalty_agent import run_agent  # your agent entrypoint
    answer = run_agent(
        user_question=inputs["question"],
        system_instructions=system_instructions,
    )
    return {"answer": answer}

result = mlflow.genai.optimize_prompts(
    predict_fn=predict_fn,
    train_data=train_data,
    prompt_uris=[prompt_uri],
    optimizer=GepaPromptOptimizer(
        reflection_model="databricks:/databricks-claude-sonnet-4-6",
        max_metric_calls=150,
    ),
    scorers=[Correctness()],
)

optimized = result.optimized_prompts[0]
print(f"New version: {optimized.name} v{optimized.version}")
print(f"Baseline score: {result.initial_eval_score:.3f} → "
      f"Optimized: {result.final_eval_score:.3f}")
```

Key contract rules:

1. **`predict_fn` accepts one keyword argument per prompt variable in `prompt_uris`.** If you optimize the prompt `system_instructions`, your function signature must include `system_instructions: str`. The optimizer substitutes candidate bodies into that parameter — your function must actually *use* it (not re-load a hard-coded copy from UC).
2. **`predict_fn` returns a `dict`.** Include every key your scorers read (for `Correctness`, return `{"answer": ...}`). Extra keys are passed through.
3. **`train_data` is a list of dicts** with `inputs` (the payload passed to `predict_fn`) and optionally `expectations` (used by scorers).
4. **Scorers are regular MLflow scorers.** Built-in (`Correctness`, `RelevanceToQuery`, `Guidelines`) or custom `@scorer` functions.

> **Load** [references/predict-fn-contract.md](references/predict-fn-contract.md) **if** your agent has >1 prompt variable, streams output, or requires session state.

---

## Custom Scorers for Optimization Signal

`Correctness` alone is a blunt signal. Domain-specific scorers improve optimizer direction because GEPA uses **per-row score + per-row textual justification** to decide what to change in the prompt.

```python
from mlflow.genai.scorers import scorer
from mlflow.entities import Feedback

@scorer
def source_citation_scorer(outputs: dict, expectations: dict) -> Feedback:
    """1 if all expected_source_ids appear in answer, else 0.

    Return a rationale — GEPA reflects on rationales to rewrite the prompt.
    """
    expected = set(expectations.get("expected_source_ids", []))
    answer = outputs.get("answer", "") or ""
    found = {sid for sid in expected if sid in answer}
    missing = expected - found
    score = 1.0 if expected and not missing else 0.0 if expected else None
    rationale = (
        f"All {len(expected)} expected source ids cited."
        if not missing else
        f"Missing source ids: {sorted(missing)}. Answer did not cite them."
    )
    return Feedback(value=score, rationale=rationale)
```

Pass multiple scorers in a list; the optimizer aggregates scores with equal weight by default.

> **Load** [references/custom-scorers-for-optimization.md](references/custom-scorers-for-optimization.md) **if** you need weighted aggregation, guideline-style boolean judges, or scorer shape debugging.

---

## Multi-Prompt Optimization

When two prompts work together (e.g. a **planner** and an **answerer**), optimize them jointly so the optimizer can coordinate changes.

```python
prompt_uris = [
    "prompts:/main.skyloyalty.planner_instructions@production",
    "prompts:/main.skyloyalty.answer_instructions@production",
]

def predict_fn(
    inputs: dict,
    planner_instructions: str,
    answer_instructions: str,
) -> dict:
    plan = call_planner(inputs["question"], planner_instructions)
    answer = call_answerer(plan, inputs["question"], answer_instructions)
    return {"answer": answer, "plan": plan}

result = mlflow.genai.optimize_prompts(
    predict_fn=predict_fn,
    train_data=train_data,
    prompt_uris=prompt_uris,
    optimizer=GepaPromptOptimizer(
        reflection_model="databricks:/databricks-claude-sonnet-4-6",
        max_metric_calls=200,  # scale with # prompts
    ),
    scorers=[Correctness(), source_citation_scorer],
)
for p in result.optimized_prompts:
    print(f"{p.name} v{p.version}")
```

`result.optimized_prompts` is returned in the **same order** as `prompt_uris`.

---

## Budget Controls

`GepaPromptOptimizer(max_metric_calls=N)` caps total scorer invocations across *all* candidates and iterations. Rough sizing guide:

| Dataset size | Prompts | Suggested `max_metric_calls` | Approx wall time |
|--------------|---------|------------------------------|------------------|
| 20–50 rows | 1 | 100–150 | 10–20 min |
| 50–100 rows | 1 | 150–300 | 20–45 min |
| 50–100 rows | 2–3 | 200–400 | 30–60 min |

Also set:

- `reflection_model` — use a strong model (Claude Sonnet 4.6+, GPT-4-class) for reflection; weaker reflection models produce worse rewrites.
- `seed` (optional) — for reproducibility during debugging.

> **Load** [references/budget-and-cost.md](references/budget-and-cost.md) **if** optimization is exceeding budget, timing out, or showing no improvement after N calls.

---

## Alias Promotion After Optimization

The optimizer creates a **new version** of the prompt. Do **not** move `@production` directly to it. Instead, flip `@staging`, re-run Step 4 evaluation, and promote only on sustained improvement.

```python
optimized = result.optimized_prompts[0]

mlflow.genai.set_prompt_alias(
    name=optimized.name,
    alias="staging",
    version=optimized.version,
)
```

Then:

1. Re-run [04-evaluation-runs](../04-evaluation-runs/SKILL.md) with the `@staging` prompt on a **held-out** eval split.
2. Compare against the baseline run in the MLflow UI Run Compare view.
3. Only if all gates pass, promote: `mlflow.genai.set_prompt_alias(name=..., alias="production", version=optimized.version)`.

The optimization run itself is logged as an MLflow run containing the metric history and the final prompt body — link it from your PR description.

---

## SDLC Loop — Where Optimization Fits

```
Step 1 register ─▶ Step 2 eval dataset ─▶ Step 3 scorers ─▶ Step 4 evaluate
                                                              │
                                                              ▼
                                             scorer below threshold?
                                                   ├─ yes ─▶ Step 8 optimize ─▶ Step 4 re-evaluate ─▶ promote
                                                   └─ no ──▶ Step 5 agent-as-judge / ship
```

Re-run optimization at most **1–2 iterations per scorer**. If three iterations produce no improvement, the quality gap is not prompt-shaped — go to debugging.

---

## Do's and Don'ts

|  | Do | Don't |
|---|---|---|
| **When** | Run only after Step 4 shows a specific scorer below threshold. | Use as the first pass to "make the agent good." |
| **`predict_fn`** | Pass prompt variables as kwargs and actually inject them into the LLM call. | Hard-code the prompt body in the function and ignore the kwarg. |
| **Scorers** | Use ≥ 2 scorers (aggregate + domain) with meaningful rationales. | Return raw booleans with no `rationale` — GEPA loses signal. |
| **Aliases** | Write optimized version to `@staging`, re-evaluate, then promote to `@production`. | Point `@production` at the optimized version directly. |
| **Budget** | Start at `max_metric_calls=150`, raise only if convergence curve still climbs. | Set `max_metric_calls=10000` "just in case" — cost and time blow up. |
| **Prompts** | Optimize prompts that are registered in UC with proper `{{variable}}` templates. | Optimize inline f-string prompts — nothing is versioned. |

---

## Common Mistakes

| Mistake | Why it hurts | What to do instead |
|---------|--------------|-------------------|
| `predict_fn` ignores the injected kwarg | Optimizer rewrites bodies that never reach the LLM; scores don't change | Verify by logging `len(system_instructions)` inside `predict_fn`; it must vary between calls |
| Scorers return only booleans with no rationale | GEPA reflection has nothing to reason over | Always fill `Feedback.rationale` with a concrete reason |
| Optimize with `Correctness` only on short answers | Signal is too coarse; optimization oscillates | Add a domain scorer with binary + rationale |
| Re-run optimization on full eval data | Overfits; wall time and $$ | Use train/dev split (80/20); validate on dev |
| Promote straight to `@production` | No safety net if optimized prompt breaks an edge case | Gate via `@staging` + re-evaluation + human spot check |
| Use weak reflection model (small local model) | GEPA rewrites are low quality | Use Claude Sonnet 4.6 / GPT-4-class or equivalent for `reflection_model` |

---

## Validation Checklist

- [ ] Baseline eval run exists showing the specific scorer(s) you want to improve.
- [ ] All prompts to optimize are registered in UC and resolvable via `prompts:/...@production`.
- [ ] `predict_fn` kwargs match the prompt URIs order and variable names.
- [ ] Every scorer returns `Feedback(value=..., rationale=...)` with a non-empty rationale.
- [ ] `max_metric_calls` is sized per the budget table (not left at defaults).
- [ ] Optimized version is aliased to `@staging`, not `@production`.
- [ ] A held-out eval split is re-run with `@staging` before promotion.
- [ ] The optimization MLflow run URL is linked in the promotion PR / change ticket.

---

## Example Script (Reference Implementation)

**Example script** (copy or adapt): [`scripts/optimize_prompt.py`](scripts/optimize_prompt.py) — loads baseline metrics, runs `optimize_prompts`, writes `@staging` alias, emits a markdown optimization report with before/after scores. Run `python scripts/optimize_prompt.py --help` for flags.

---

## References

### Official documentation (Databricks)

- [Automatically optimize prompts](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/prompt-registry/automatically-optimize-prompts)
- [Prompt optimization quickstart](https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/prompt-optimization-quickstart)
- [Multi-prompt optimization](https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/multi-prompt-optimization)
- [Custom scorers](https://docs.databricks.com/aws/en/mlflow3/genai/tutorials/examples/custom-scorers)

### Local deep-dives

| File | Topic |
|------|-------|
| [references/when-to-optimize.md](references/when-to-optimize.md) | Decision checklist, when NOT to optimize, cost/benefit |
| [references/predict-fn-contract.md](references/predict-fn-contract.md) | Multi-prompt, streaming, session state, validation |
| [references/custom-scorers-for-optimization.md](references/custom-scorers-for-optimization.md) | Rationale quality, weighted aggregation, debugging |
| [references/budget-and-cost.md](references/budget-and-cost.md) | `max_metric_calls` sizing, convergence curves, early stopping |

### Related skills

[01-prompt-registry](../01-prompt-registry/SKILL.md) · [03-scorers-and-judges](../03-scorers-and-judges/SKILL.md) · [04-evaluation-runs](../04-evaluation-runs/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-19 | Initial skill: `optimize_prompts` + `GepaPromptOptimizer`, predict_fn contract, multi-prompt, alias promotion, budget controls. |
| 1.1.0 | 2026-04-26 | Marked optional/advanced — default flow now routes to `08b-prompt-handauthoring`. Added required GEPA safeguards (reflection-LM preflight, version pin, holdout floor, no-proposal circuit breaker, four structured exits, role-endpoint resolution, captured metrics). |
