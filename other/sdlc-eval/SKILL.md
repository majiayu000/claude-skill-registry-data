---
name: sdlc-eval
description: Invoked explicitly by /eval. For AI features, builds or runs the golden-set evaluation harness for a prompt version, records the quality metrics and cost as a baseline, and compares against the previous version to detect regression. Kept separate from the default test run so a provider call is always a deliberate command.
argument-hint: "<prompt-name>[@version] [--baseline]"
disable-model-invocation: true
---

# /eval — prompt evaluation

The only command in the framework that deliberately spends money. Everything else reads
the results this one records.

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

**Phase inputs** — feeds gate `G5b`. Inputs `{{paths.eval_spec_dir}}/EVAL-{name}.md`,
`{{paths.eval_data_dir}}/{name}/{version}/cases.jsonl`, the registry version file.
Outputs `.agent/state/evals/{name}@{version}.json` and the updated prompt `metadata`.
This command costs money, so gate Step 4 (CHECKPOINT) always applies and must state the
case count and the estimated spend.

---

## Step 1 — Input check

There is no `input_contracts` entry for `/eval` — it is not a phase — so check these
directly. Stop with a clear message if any is missing, rather than evaluating something
undefined. **List what is missing; do not ask for it.**

- the feature's `ai_class` is `none` → this command does not apply
- no `EVAL-{name}.md` → run `/techdoc` first; thresholds are a design decision
- no `cases.jsonl` for this version → run `/gen-testcase` first
- the registry version file does not exist → run `/gen-code` first

Read the eval spec's metrics table, its thresholds, its judge rubric, and the baselines
table.

## Step 2 — Resolve the version and the baseline

Default to the newest version in the registry for that prompt. The baseline is the
previous version's recorded run in `.agent/state/evals/`, or the version named in the
spec's baselines table.

If no baseline exists, this run **becomes** the baseline. Say so explicitly — a first run
cannot detect regression, and reporting it as "no regression" would be misleading.

## Step 3 — Run the suite

Run `quality_commands.evals` for this prompt and version.

Per the oracle ladder in `.agent/modules/ai-llm/stack-profile.yaml`:

- **Tier 1 structural** — schema validity, required fields, token and length caps, banned
  strings, refusal detection, latency. These assert **hard**, per case, even inside an
  eval. A case with no structural expectation cannot fail deterministically and therefore
  protects nothing.
- **Tier 2 reference** — exact match for classification and extraction; similarity
  against `expect.reference` otherwise. Recorded per case, gated on the **suite pass
  rate**.
- **Tier 3 judge** — rubric scored 1–5 against the written anchors. Recorded per case,
  gated **only on regression versus baseline**.

Run judge and similarity cases **n=3 and take the median**, recording the variance. A
case whose variance exceeds the spec's threshold is flagged as a **bad eval case, not a
bad prompt** — an unstable case adds noise to every future comparison, so it is fixed or
retired rather than tolerated.

Capture per case: outcome, scores, tokens in and out, latency, cost.

## Step 4 — Aggregate and compare

```json
{
  "prompt": "summarize@1.2.0",
  "at": "<ISO8601>",
  "cases": { "total": 42, "passed": 39, "failed": 3 },
  "pass_rate": 0.929,
  "by_origin": { "golden": 0.95, "adversarial": 0.83, "regression": 1.0 },
  "judge": { "faithfulness": 4.3, "coverage": 3.9, "variance_flags": ["EV-summarize-017"] },
  "cost": { "p50_input_tokens": 1840, "p95_output_tokens": 190,
            "cost_per_call_usd": 0.0031, "p95_latency_ms": 3120, "total_run_usd": 0.13 },
  "baseline": "summarize@1.1.0",
  "delta": { "pass_rate": 0.01, "judge_faithfulness": -0.1 },
  "verdict": "pass | regression | below_threshold"
}
```

Verdict rules from the spec, defaults from `ai_conventions.oracles`:

- **below_threshold** — suite pass rate under the spec's minimum
- **regression** — judge mean dropped more than the tolerance (default 0.3), or pass rate
  dropped more than the tolerance (default 5 percentage points)
- **pass** — neither

**Regression on `by_origin.regression` is always a blocker**, whatever the aggregate
says. Those cases exist because something already failed once; letting one of them break
while the average holds is exactly how a fixed bug comes back.

## Step 5 — Record

Write `.agent/state/evals/{name}@{version}.json`, add a row to the spec's baselines
table, add a row to the prompt spec's version-history table, and update the registry
file's `metadata` — `eval_set`, `eval_score`, `eval_run`.

`metadata` is the **only** part of a published version file that may be written after
publication, because it describes the file rather than changing its behaviour. The
template and rules do not change.

With `--baseline`, also mark this run as the comparison point for the next version.

## Step 6 — Report

State pass rate, judge means, cost per call, p95 latency, the delta versus baseline, and
the verdict. List the failed cases with their ids and what they expected — an aggregate
number with no failing examples is not actionable.

On `regression` or `below_threshold`, write a finding routed to `prompt` (quality
dropped, contract unchanged) or `techdoc` (the contract or the model must change).

---

## Boundaries

- **Do not edit the prompt to make the eval pass.** A prompt change is a new version,
  decided in `/techdoc` and written by `/gen-code`. Tuning a prompt against its own eval
  inside the eval command is overfitting with extra steps.
- Do not add or remove eval cases here. `/gen-testcase` authors them. Deleting the case
  that fails is the most direct way to make an eval suite meaningless.
- Do not renumber case ids — the baseline comparison depends on them being stable.
- Do not lower a threshold to pass. That is a design decision with an ADR.
- Do not run automatically as part of another command. The cost must always be a
  deliberate choice.
