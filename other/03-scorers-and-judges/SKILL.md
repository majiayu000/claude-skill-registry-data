---
name: 03-scorers-and-judges
description: >
  Use when you need to measure agent quality or create scoring criteria
  for evaluation gates. Covers how to pick and configure scorers — even
  if you just want "is my agent safe and accurate?" without knowing
  which MLflow classes to use. Also use when building custom LLM judges,
  evaluating multi-turn conversations, or setting pass/fail thresholds.
  SDLC Step 3.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Scorers/judges defined via the MLflow GenAI SDK; no bundle resource. Identical on both clients; on Genie Code run any CLI step through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-08-30"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.2.0"
  domain: "genai-agents"
  pipeline_position: "S3"
  consumes: "evaluation_dataset"
  produces: "scorer_list, threshold_config, helper_functions"
  grounded_in: "https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-judge/, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-scorers, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations, https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
fields_read:
  - governance.scorer_suite.guidelines
  - governance.scorer_suite.judge_questions
  - governance.scorer_suite.judge_questions.domain_accuracy
  - governance.scorer_suite.custom_scorer_rules
  - governance.llm_role_endpoints.llm_judge_default.endpoint
  - agent.tools[].writes_to
  - docs.agent_tool_plan.selected_tools
  - docs.agent_tool_plan.runtime_guardrails.tool_shaped_scorers
inputs:
  - name: agent_tool_plan_ref
    required: false
    description: >
      Path to docs/agent_tool_plan.yaml. When set, the skill UNIONS the generic
      scorer suite from governance.scorer_suite.* (Spec, use-case shaped) with
      runtime_guardrails.tool_shaped_scorers[] (Plan, derived mechanically from
      selected_tools[]). Tool-shaped scorers register conditionally:
      RetrievalGroundedness only with KA or Vector Search selected;
      ka_citation_present only with KA selected; genie_* only with Genie
      selected; sql_* only with SQL MCP selected. The union is deduped.
---

# Scorers and Judges

Patterns for MLflow GenAI scorers and LLM judges aligned with [Databricks MLflow 3 GenAI evaluation](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers). Scorers plug into `mlflow.genai.evaluate()` and production monitoring; metric keys follow MLflow’s native naming (typically derived from the scorer class or registered function name unless you override).

## Upstream Lineage

This skill extends Databricks Agent Skills' `databricks-mlflow-evaluation` skill for built-in scorers, custom scorer development, `make_judge`, MemAlign-aligned judge workflows, and scorer API contracts. If scorer behavior, constructor signatures, or judge-alignment patterns are unclear, consult the upstream skill first, then apply this skill's workshop-specific tiering and governance contracts.

## When to Use

- Choosing built-in vs custom scorers for `mlflow.genai.evaluate()`.
- Implementing `@scorer` functions that read `inputs`, `outputs`, `expectations`, and optional `trace`.
- Defining LLM judges with `make_judge()` and an explicit `feedback_value_type`.
- Evaluating multi-turn conversations via traces and built-in conversation scorers.
- Assembling a reusable `build_scorers()` list and gating on thresholds.

Upstream harness context: SDLC Step 4 (evaluation runs). Dataset contract: SDLC Step 2 (evaluation datasets). Eval harness concepts: [eval harness](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness).

---

## Three Ways to Create Scorers

> **Recommended default:** Start with **built-in scorer classes** for standard dimensions (safety, correctness, relevance). Use **`@scorer`** when you need custom deterministic logic. Use **`make_judge()`** only when you need an LLM-based judge from a prompt template.

| # | Mechanism | Use when |
|---|-----------|----------|
| 1 | **Built-in scorer classes** | Standard dimensions (safety, correctness, relevance, guidelines, conversation quality). |
| 2 | **`@scorer` decorator** | Custom deterministic or programmatic logic; full control over `Feedback`. |
| 3 | **`make_judge()`** | LLM-as-judge from a prompt template; must set `feedback_value_type`. |

Imports vary slightly by MLflow version; confirm `mlflow.genai.scorers` (code-based scorers) and `mlflow.genai.judges` (`make_judge`) in your environment. Examples below use common patterns from [code-based scorers](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-scorers) and [custom judges](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-judge/).

---

## Built-in Scorers (Classes)

```python
from mlflow.genai.scorers import (
    Safety,
    Correctness,
    Guidelines,
    RelevanceToQuery,
    ConversationCompleteness,
    UserFrustration,
)

scorers = [
    Safety(),
    Correctness(config={"targets": "expectations/expected_response"}),
    Guidelines(
        name="my_guideline",
        guidelines="Be concise; cite sources; refuse harmful requests.",
    ),
    RelevanceToQuery(),
]
```

- **Safety:** policy and safety checks on model outputs.
- **Correctness:** compare outputs to expectations; configure `targets` to match your dataset column paths (see Databricks docs for your MLflow version).
- **Guidelines:** rubric-style criteria; keep roughly 4–6 focused rules—long lists often compress scores without adding signal.
- **RelevanceToQuery:** alignment between user query and response.
- **ConversationCompleteness** / **UserFrustration:** conversation-level scorers (see [Conversation evaluation](#conversation-evaluation-new)).

> **Load** `references/built-in-judges.md` **if** you need constructor details, scale ranges, or composition patterns for built-in scorers.

---

## Custom `@scorer` Pattern

Register a function with `@scorer`. It receives keyword arguments **`inputs`**, **`outputs`**, **`expectations`**, and **`trace`** (and any others your MLflow version documents). Read fields directly from `outputs` (and nested structures) for your agent’s serialization shape—do not assume a single global string format across teams.

```python
from mlflow.genai import scorer
from mlflow.entities import Feedback

@scorer
def sql_syntax_ok(
    inputs: dict,
    outputs: dict,
    expectations: dict | None = None,
    trace=None,
) -> Feedback:
    text = outputs.get("text") or outputs.get("response") or ""
    ok = validate_sql_syntax(text)
    return Feedback(
        name="sql_syntax_ok",
        value="yes" if ok else "no",
        rationale=f"Syntax {'valid' if ok else 'invalid'} for: {text[:120]!r}",
    )
```

Return **`Feedback(name=..., value=..., rationale=...)`** (and optional metadata your pipeline expects). The registered name typically becomes the metric namespace in evaluation results.

> **Load** `references/custom-scorer-patterns.md` **if** you need scorer factories, binary/multi-value return patterns, or async scorer notes.

---

## Custom Judge via `make_judge()`

Use **`make_judge()`** for LLM-based scoring instead of ad hoc SDK calls inside every row. You **must** pass **`feedback_value_type`**: a Python type — **`bool`**, **`int`**, **`float`**, **`str`**, a nullable primitive (**`float | None`** / **`Optional[int]`**), or a typed **`Literal[...]`** — so MLflow can parse and aggregate judge outputs via structured outputs. Pass the type itself (`feedback_value_type=float`), never the string name (`"float"`).

Template placeholders are Jinja-style. Use top-level **`{{ inputs }}`**, **`{{ outputs }}`**, **`{{ expectations }}`** (and, when applicable, **`{{ trace }}`**, **`{{ conversation }}`** per [MLflow custom-judge template rules](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-judge/)). Custom variables are not supported. **`{{ conversation }}` may only coexist with `{{ expectations }}`** — it cannot be combined with `{{ inputs }}`, `{{ outputs }}`, or `{{ trace }}`. Nest extra fields under `inputs` / `expectations` in your dataset rather than inventing new root template variables.

```python
from typing import Literal

from mlflow.genai.judges import make_judge  # canonical path (MLflow >= 3.4)

domain_judge = make_judge(
    name="domain_accuracy",
    instructions="""
You are grading domain accuracy.

Trace: {{ trace }}

Reply with a single token: "yes" if the output is accurate, "no" otherwise.
""",
    feedback_value_type=Literal["yes", "no"],
    model="databricks:/" + LLM_JUDGE_DEFAULT_ENDPOINT,  # provider:/<model>; databricks:/ for serving endpoints
)
```

The keyword for the prompt string may differ by version (e.g. `judge_prompt` vs `instructions`); allowed template variables are unchanged. Pass the resulting object in the **`scorers`** list to **`mlflow.genai.evaluate()`**—it is not a standalone `.evaluate()` entrypoint.

### MLflow 3.11 contracts (normative)

These rules are platform reality on MLflow 3.11; violating them silently breaks aggregation or fails construction:

- **Import path:** import `make_judge` from `mlflow.genai.judges` (`from mlflow.genai.judges import make_judge`) — the canonical path documented by MLflow and Databricks (SDK requires MLflow >= 3.4; the Judge Builder UI requires >= 3.9). A top-level `mlflow.genai.make_judge` alias also exists, but do **not** import it from `mlflow.genai.scorers`.
- **Judge `model` URI scheme:** use `provider:/<model>` — `databricks:/<serving-endpoint>` for Databricks-hosted judges (e.g. `databricks:/databricks-gpt-5-mini`), `openai:/<model>` or `anthropic:/<model>` for others. The older `endpoints:/` prefix is not in current docs; prefer `databricks:/`.
- **Set judge aggregation explicitly so `<scorer>/mean` exists.** Without an explicit aggregation (e.g. configuring per-judge aggregation or a downstream mean over the binary string outputs), the run will not log a `<scorer>/mean` metric and your `THRESHOLDS` map keyed on `<name>/mean` will silently miss. Verify metric keys on a pilot run.
- **Use `feedback_value_type=Literal["yes", "no"]` when aggregation depends on string values.** Do **not** assume a `bool` feedback aggregates — string-valued judges (`"yes"`/`"no"`) require an explicit `Literal` so MLflow knows the value space and can roll up means correctly. Booleans from a judge may be stringified or fail to aggregate into a numeric mean.
- **`Correctness` consumes `expected_response`, not `expected_signal`.** The dataset column / expectations field must be named `expected_response`. Passing `expected_signal` (or any other alias) results in `Correctness` finding no ground truth and scoring everything as the same default value.
- **Judge instruction templates must include required placeholders such as `{{ trace }}`.** When `make_judge` is configured to score traces, its instructions string is validated for the presence of `{{ trace }}` (or other required placeholders for the template kind chosen). Omitting them raises an `MlflowException` at construction. Always include the placeholder appropriate for the judge's input even if you also reference `{{ inputs }}` / `{{ outputs }}` / `{{ expectations }}`.
- **Default judge endpoint:** read the default judge model endpoint from `state://Governance` at `llm_role_endpoints.llm_judge_default.endpoint`; do not hard-code an endpoint name in the skill code. This keeps judge routing consistent with other LLM roles (see SDLC Step 1 prompt-role applicability).

> **Load** `references/make-judge-constraints.md` **if** `make_judge` raises errors, or you need to choose between `make_judge` and `@scorer`.

---

## 5-Tier Scorer Model

Scorers form a tiered suite. Tier names are stable and downstream routing (Phase 2.4 smoke and scored eval gates) depends on them — do not rename.

```yaml
scorer_tiers:
  L1: universal safety and contract requirements
  L2-instruction: system-prompt rule adherence
  L2-behavior: agent behavior derived from tools and write permissions
  L3-deterministic: code or SQL deterministic checks
  L3-judge: LLM-as-judge checks
```

### Tier rules

- **L1 (universal):** safety and contract requirements that apply to every agent regardless of domain (e.g. `Safety()`, refusal policies, output schema validity, **`pii_protection`**). These are non-negotiable gates.
- **L2-instruction:** rule adherence to the agent's system prompt — Guidelines-style scorers whose criteria come from the prompt under SDLC Step 1.
- **L2-behavior:** agent behavior scorers **auto-derived from `agent.tools[].writes_to`**. For each tool with a non-empty `writes_to` list, emit a behavior scorer that checks the agent did not invoke that tool (or did not produce a write) when the row is read-only. Do not hand-author these one by one — derive them from the tool registry so they stay in sync as tools are added.
- **L3-deterministic:** code or SQL deterministic checks (regex, parse, schema validation, dialect compile). Cheap, no LLM call.
- **L3-judge:** LLM-as-judge checks via `make_judge()`. Most expensive; run last.

### Specific named heuristics and conventions

- **`pii_protection`** (L1): single canonical scorer name. **Rename `pii_email_protection` → `pii_protection`** anywhere it appears in legacy configs; the broader name covers email, phone, SSN, etc., and avoids implying email-only coverage.
- **`domain_accuracy`** judge prompt body lives in `state://Governance` (under `governance.scorer_suite.judge_questions.domain_accuracy`), not inline in the skill. Read it at scorer-construction time and pass into `make_judge(instructions=...)`. This keeps domain prompts versioned with governance and lets non-engineers edit accuracy criteria.
- **`sql_execution_readonly`** (L3-deterministic, heuristic):
  - Scan the agent response text.
  - **Short-circuit on refusal phrases** (e.g. "I can't run", "I won't execute", "read-only mode") — return pass without further inspection.
  - Otherwise, require **SQL keyword adjacency** (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `DROP`, `MERGE`, etc.) to a configured **SQL target** (table or view name from the agent's tool registry). A bare `SELECT` mention without an adjacent configured target is not flagged; an `INSERT` / `UPDATE` / `DELETE` / `DROP` adjacent to a configured SQL target fails the scorer.
  - This avoids false positives on natural-language responses that mention "select" or "update" in non-SQL senses.
- **Default judge endpoint:** every `make_judge()` call in `build_scorers()` reads `llm_role_endpoints.llm_judge_default.endpoint` from `state://Governance` and passes it as the judge `model` argument. No hard-coded endpoint names in scorer code.

### Auto-derivation example (L2-behavior)

```python
def build_l2_behavior_scorers(agent_spec: dict) -> list:
    """One behavior scorer per tool with writes_to, derived from the agent spec."""
    from mlflow.genai import scorer
    from mlflow.entities import Feedback

    scorers = []
    for tool in agent_spec.get("tools", []):
        writes = tool.get("writes_to") or []
        if not writes:
            continue
        tool_name = tool["name"]

        def _factory(tool_name=tool_name, writes=tuple(writes)):
            @scorer(name=f"behavior_no_write_{tool_name}")
            def _check(inputs, outputs, expectations=None, trace=None) -> Feedback:
                # Inspect the trace for tool invocations against `tool_name`
                # that produced writes to any target in `writes`.
                violated = _trace_has_write(trace, tool_name, writes)
                return Feedback(
                    name=f"behavior_no_write_{tool_name}",
                    value="no" if violated else "yes",
                    rationale=f"Tool {tool_name} writes_to={list(writes)}",
                )
            return _check

        scorers.append(_factory())
    return scorers
```

`build_scorers()` should compose all five tiers in order (L1 → L2-instruction → L2-behavior → L3-deterministic → L3-judge) so cheap checks run before expensive judges and downstream code can filter by tier prefix.

---

## Conversation Evaluation (NEW)

For **multi-turn** flows, use built-in conversation scorers and **trace-backed** evaluation per [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations).

- **ConversationCompleteness():** whether the agent addressed the user’s goal across turns.
- **UserFrustration():** signals such as repetition, escalation, or unresolved loops.

**Session tagging:** set **`mlflow.trace.session`** (or the session tag your MLflow version documents) so all spans for one conversation group together.

**Scoring approach:** when evaluating conversations, pass **`trace`** objects into **`mlflow.genai.evaluate()`** as your data source where supported. Scorers inspect the **trace span tree** to recover the full conversation instead of relying on a single flattened `outputs` dict.

```python
from mlflow.genai.scorers import ConversationCompleteness, UserFrustration

conversation_scorers = [
    ConversationCompleteness(),
    UserFrustration(),
]
```

Combine with single-turn scorers only when the evaluation row or trace shape matches what each scorer expects.

---

## Scorer Assembly

Define a single factory that returns the list passed to **`mlflow.genai.evaluate(..., scorers=...)`**:

```python
def build_scorers(agent_description: str):
    """Return scorers tuned to the agent's risk profile and I/O schema."""
    from mlflow.genai.scorers import Safety, Guidelines, RelevanceToQuery
    from mlflow.genai.judges import make_judge

    rubric = Guidelines(
        name="agent_rubric",
        guidelines=f"Follow these rules for this agent:\n{agent_description}",
    )
    tone = make_judge(
        name="professional_tone",
        instructions="Inputs: {{ inputs }}\nOutputs: {{ outputs }}\n"
        "Rate professionalism from 0.0 to 1.0.",
        feedback_value_type=float,
    )
    return [Safety(), rubric, RelevanceToQuery(), tone]
```

Order scorers from cheapest checks first (e.g. safety, syntax) to heavier judges last if you short-circuit in custom code; `evaluate()` itself runs the configured set.

---

## Threshold Checking (Generic)

`mlflow.genai.evaluate()` aggregates per-scorer metrics (often means on a 0–1 scale). Define **your own** threshold map keyed by the **actual metric names** logged on the run (match MLflow’s naming for your scorer classes and `@scorer` names—no separate alias table required if you key gates on the same names the run produces).

```python
THRESHOLDS = {
    "safety/mean": 0.95,
    "relevance_to_query/mean": 0.80,
    "domain_accuracy/mean": 0.85,
}

def scores_to_0_100(evaluation_result) -> dict:
    """Map aggregated metrics to 0-100 for reporting; adjust keys to your run."""
    out = {}
    for k, v in evaluation_result.metrics.items():
        if isinstance(v, (int, float)) and "/mean" in k:
            out[k] = 100.0 * v if v <= 1.0 else v
    return out

def all_thresholds_met(metrics_0_100: dict, thresholds: dict) -> tuple[bool, dict]:
    failures = {}
    for key, target in thresholds.items():
        actual = metrics_0_100.get(key)
        if actual is None or actual < target:
            failures[key] = (actual, target)
    return (len(failures) == 0, failures)
```

After an upgrade, re-check logged metric keys in the MLflow UI once; rename threshold keys to match rather than maintaining parallel alias maps unless you have a legacy migration need.

> **Load** `references/threshold-checking.md` **if** you need normalization details, threshold tuning strategies, or per-use-case overrides.

---

## DO / DON'T

| DO | DON'T |
|----|-------|
| Read `outputs` (and nested fields) explicitly for your agent’s schema | Assume `outputs` is always a plain string |
| Use `make_judge(..., feedback_value_type=...)` for LLM judges | Omit `feedback_value_type` or call raw LLMs per row without a scorer wrapper |
| Use only documented Jinja roots: `inputs`, `outputs`, `expectations`, `trace`, `conversation` | Add undefined `{{ custom_var }}` templates |
| Key threshold gates on metric names shown on the evaluation run | Hard-code guessed names without verifying logged metrics |
| Keep `Guidelines` criteria focused (roughly 4–6 rules) | Add long unstructured rubrics that collapse scores |
| Pass conversation scorers with trace-based `evaluate()` when evaluating threads | Use only last-turn `outputs` when the scorer needs full dialogue |
| Return `Feedback` with clear `name`, `value`, `rationale` | Return unstructured objects that are not valid feedback types |

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Wrong shape for `outputs` vs your agent | Flat or misleading scores | Document agent JSON; read fields explicitly in `@scorer` |
| Missing `feedback_value_type` on `make_judge` | Build or runtime errors | Set a Python type: `bool`, `int`, `float`, `str`, or `Literal[...]` (not the string `"float"`) |
| Invalid template variables in `judge_prompt` | `MlflowException` | Use only allowed placeholders; nest data under `inputs` / `expectations` |
| Threshold keys don’t match logged metrics | Gates always pass or always fail | Inspect one run’s metrics; align `THRESHOLDS` keys |
| Treating `make_judge` result as a full evaluator | Wrong API usage | Pass scorers into `mlflow.genai.evaluate(scorers=[...])` |
| Comparing 0–1 aggregates to 0–100 thresholds incorrectly | Wrong gate semantics | Normalize consistently before compare |
| Conversation scorers without session/trace wiring | No multi-turn signal | Tag sessions and pass traces per Databricks conversation eval docs |

---

## Validation Checklist

- [ ] Chosen path: built-in class, `@scorer`, or `make_judge` matches the use case.
- [ ] `make_judge` is imported from `mlflow.genai.judges` (SDK >= 3.4).
- [ ] Judge `model` uses the `provider:/<model>` scheme (`databricks:/<endpoint>` for serving endpoints), not `endpoints:/`.
- [ ] Every `make_judge` specifies `feedback_value_type` as a Python type (`bool`/`int`/`float`/`str`/`Literal[...]`, not a string); string-valued judges use `Literal["yes", "no"]`, not bare `bool`.
- [ ] Judge aggregation is set explicitly so `<scorer>/mean` is logged on the run.
- [ ] `Correctness` reads `expected_response` from the dataset (not `expected_signal`).
- [ ] Judge instruction templates include required placeholders such as `{{ trace }}`.
- [ ] `judge_prompt` / `instructions` uses only allowed template variables.
- [ ] Custom `@scorer` signatures accept `inputs`, `outputs`, `expectations`, and `trace` as needed.
- [ ] `outputs` parsing matches the agent’s serialized shape for that benchmark.
- [ ] `build_scorers()` returns the five tiers in order (`L1` → `L2-instruction` → `L2-behavior` → `L3-deterministic` → `L3-judge`).
- [ ] L1 includes `pii_protection` (not the legacy `pii_email_protection`).
- [ ] L2-behavior scorers are auto-derived from `agent.tools[].writes_to`, not hand-listed.
- [ ] `domain_accuracy` judge prompt body is read from `state://Governance`, not inline.
- [ ] `sql_execution_readonly` uses refusal short-circuit + SQL keyword adjacency to a configured SQL target.
- [ ] All `make_judge` calls read the default endpoint from `llm_role_endpoints.llm_judge_default.endpoint`.
- [ ] Threshold map keys match a pilot run’s logged metric names.
- [ ] Conversation evaluation uses `ConversationCompleteness` / `UserFrustration` plus session tags and trace-based `evaluate()` where applicable.
- [ ] Guidelines count stays focused (roughly 4–6 criteria).

---

## References

### Official documentation (Databricks)

- [Scorers concepts](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/scorers)
- [Custom judges (`make_judge`)](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-judge/)
- [Code-based scorers (`@scorer`)](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/custom-scorers)
- [Evaluate conversations](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/evaluate-conversations)
- [Evaluation harness concepts](https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/concepts/eval-harness)

### Related skills

- `docs/genai-agents/sdlc/04-evaluation-runs/SKILL.md` — `evaluate()` harness, `predict_fn`, dataset contract
- SDLC Step 2 — evaluation dataset schema consumed by scorers

### Reference files in this folder

| File | Contents |
|------|----------|
| `references/built-in-judges.md` | Per-scorer constructors, scales, performance, composition |
| `references/custom-scorer-patterns.md` | `@scorer`, factories, archetypes, metadata patterns |
| `references/threshold-checking.md` | Normalization, gates, tuning |
| `references/make-judge-constraints.md` | Template variables, errors, `make_judge` vs `@scorer` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.2.0 | 2026-08-30 | Doc-drift remediation: `make_judge` import standardized to `mlflow.genai.judges`; judge `model` URI corrected to `provider:/<model>` (`databricks:/<endpoint>`, replacing `endpoints:/`); `feedback_value_type` now passed as a Python type (`bool`/`int`/`float`/`str`/`Literal`/nullable), not a string; `build_scorers()` example uses `instructions=` + `feedback_value_type=float`; `{{ conversation }}`-only-with-`{{ expectations }}` constraint documented; dead `create-custom-scorers` URLs repointed to `custom-judge/` + `custom-scorers`. |
| 4.1.0 | 2026-04-26 | Added MLflow 3.11 contracts: `make_judge` import from `mlflow.genai`, explicit aggregation for `<scorer>/mean`, `feedback_value_type=Literal["yes", "no"]` for string-valued judges, `Correctness` consumes `expected_response`, judge instructions must include `{{ trace }}`. Added 5-tier scorer model (`L1`, `L2-instruction`, `L2-behavior`, `L3-deterministic`, `L3-judge`) with `pii_protection` rename, auto-derived L2-behavior from `agent.tools[].writes_to`, `domain_accuracy` prompt in `state://Governance`, `sql_execution_readonly` heuristic with refusal short-circuit and SQL-keyword adjacency, and default judge endpoint via `llm_role_endpoints.llm_judge_default.endpoint`. |
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific patterns. Added conversation evaluation, `make_judge` `feedback_value_type`, and built-in conversation scorers. Grounded in official Databricks scorers and evaluation docs. |
| 3.1.0 | 2026-03-27 | Added reference files, DO/DON'T, scripts section, expanded thresholds and checklist. |
| 3.0.0 | 2025-03-15 | Initial skill — built-in judges, `@scorer`, `make_judge`, assembly patterns. |
