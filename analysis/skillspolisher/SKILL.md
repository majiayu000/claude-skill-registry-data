---
name: skillspolisher-research-loop
description: Standard research workflow for this repository. Use when running or improving SkillsPolisher experiments, especially SkillsBench evaluations, iterative prompt/baseline tuning, result analysis, and experiment reporting.
---

# SkillsPolisher Research Loop

Use this workflow as the default experimental loop for this repository.

## When To Use

Use this skill when:

- running `eval_pipeline/run_compare.py` or `eval_pipeline/run_eval.py`
- iterating on prompting, retrieval, skill selection, or output formatting
- evaluating on `skillsbench`
- analyzing experiment failures
- updating the persistent experiment report

## Default Iteration Policy

Unless the user explicitly asks for a full run, use **small-sample research iteration**:

- default experiment size: `10` samples
- preferred command:

```bash
python eval_pipeline/run_compare.py --dataset skillsbench --model_name <model_name>
```

- this repo is configured so the default `--n_samples` is already `10`
- use `--rerun` only when the same experiment signature must be rerun intentionally

Only scale beyond `10` samples after a small run shows a meaningful improvement or validates a new idea.

## Standard Workflow

### 1. Run the experiment

Default first pass:

```bash
python eval_pipeline/run_compare.py --dataset skillsbench --model_name gpt-4-o
```

Use `run_eval.py` only when isolating a single baseline is the actual goal.

### 2. Check generated artifacts

Primary outputs:

- compare summary:
  - `./results/{model_name}/{dataset_name}/compare_result.json`
- per-method outputs:
  - `./results/{model_name}/{dataset_name}/{baseline}_result.json`
- experiment summary table:
  - `./statistics/results.csv`

If the experiment is still running, inspect the JSON status fields instead of assuming completion.

### 3. Analyze failure patterns

After each completed real experiment, summarize:

- which baseline performed best
- token cost differences
- failure type clusters
- whether failures come from:
  - incomplete executable output
  - wrong skill/demo selection
  - weak task understanding
  - truncation / insufficient generation budget
  - formatting mismatch with evaluator expectations

For `skillsbench`, prioritize identifying whether the model returned:

- a complete executable script
- only a high-level plan
- a partial / truncated script
- the wrong kind of artifact

### 4. Update the persistent report

After every completed experiment worth keeping, update:

- `./report/report.md`

The report entry must include:

- current date
- experiment command
- dataset / model / sample count / seed
- per-baseline metrics
- key findings
- failure type summary
- next-step optimization plan

Do not leave experiment insights only in terminal conversation history.

### 5. Choose the next intervention

Default priority order for SkillsBench-style failures:

1. enforce executable output format
2. increase generation budget for long solutions
3. add answer self-check / repair
4. improve retrieval or demo selection

Do not start with larger demo pools when small runs already show that the main failure mode is incomplete output closure.

## Repo-Specific Rules

- Run commands from the project root.
- Keep `./results/` organized as:
  - `./results/{model_name}/{dataset_name}/...`
- Keep `./statistics/results.csv` as the structured experiment ledger.
- Keep `./report/report.md` as the human-readable research log.
- Preserve the dated history in the report instead of replacing conclusions with a single latest note.

## Recommended Reporting Style

For each dated experiment block in `report/report.md`, keep this structure:

1. date
2. experiment setup
3. result table
4. main findings
5. failure types
6. interpretation
7. next iteration plan

This format is intended to stay useful later for paper writing and ablation tracking.
