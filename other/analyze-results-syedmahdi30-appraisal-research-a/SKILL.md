---
name: analyze-results
description: Use this skill when aggregating experiment outputs into interpretable metrics, tables, plots, ablations, and paper-ready summaries for the appraisal-transfer project, including comparison across runs, layers, baselines, and failure modes.
---

# Analyze Results

This skill converts raw experimental outputs into interpretable evidence suitable for decision-making, internal review, and paper-ready presentation.

## Use this skill when

- The task is to summarize, compare, visualize, or interpret results from Stage A, Stage C, or verification runs.
- Metrics exist but are scattered across files, runs, or directories.
- A user asks for tables, plots, ablations, error analysis, or LaTeX-ready result summaries.
- The goal is to decide whether the evidence supports the experimental hypothesis.

## Do not use this skill for

- First-time environment setup.
- Running an experiment from scratch unless a tiny recomputation is necessary to complete analysis.
- Writing the full paper from zero.

## Objective

Produce a clean, reproducible analysis layer that answers:
1. what happened,
2. how strong the effects are,
3. how robust they are,
4. what the main caveats and failure modes are,
5. what should be written up next.

## Read these first

- `CLAUDE.md`
- `docs/probes.md`
- `docs/experiment-1.md`
- any results directories, metrics CSVs, JSON logs, or saved artifacts
- any plotting or reporting utilities already present in the repo

## Analysis workflow

### Step 1: Inventory the outputs

Identify:
- completed runs,
- their configs,
- available metrics,
- saved checkpoints,
- plots/tables already generated,
- missing metadata that could make comparisons invalid.

Build a run map before drawing conclusions.

### Step 2: Standardize comparison units

Make sure runs are comparable:
- same split or not,
- same metric definition or not,
- same hook/layer choices or not,
- same dataset slice or not,
- same steering strength or not.

If not comparable, separate them rather than forcing a single table.

### Step 3: Compute the key comparisons

Typical analyses include:
- best layer / best hook point,
- baseline vs probe vs steering,
- Stage A vs Stage C transfer gap,
- model A vs fallback model,
- effect of label mapping choices,
- sensitivity to hyperparameters or steering strength.

Prefer a few defensible comparisons over a long list of weak ones.

### Step 4: Generate interpretable artifacts

Create:
- summary tables,
- simple plots,
- ablation tables,
- selected qualitative examples where they genuinely clarify a mechanism,
- concise bullet summaries for each run group.

Favor clarity over ornamental graphics.

### Step 5: Interpret the results

Explain:
- what is strongly supported,
- what is weak or unstable,
- what is likely artifact vs signal,
- what the evidence implies for the project hypothesis.

When uncertainty is high, say exactly why.

### Step 6: Prepare paper-ready outputs

When appropriate, generate:
- LaTeX-friendly tables,
- figure captions,
- concise results paragraphs,
- a caveats list,
- a “threats to validity” summary.

## Expected outputs

At the end, produce:
- a short executive result summary,
- one or more clean comparison tables,
- recommended figures,
- the main takeaway per experiment block,
- the next write-up or experiment priority.

## Guardrails

- Do not compare incompatible runs without labeling the mismatch.
- Do not bury negative or null results.
- Do not rely on a single cherry-picked qualitative example.
- Do not imply causal conclusions from correlational summaries alone.
- Do not create plots whose axes, units, or subsets are unclear.

## Completion criteria

This skill is complete when:
- results are inventoried and comparable,
- the main comparisons are explicit,
- artifacts are readable and reproducible,
- the interpretation is cautious but useful,
- the next action is obvious.

## Example invocations

- “Aggregate all Stage A metrics into one summary.”
- “Create paper-ready tables for the transfer experiments.”
- “Compare the best layer across runs.”
- “Analyze whether the positive result survives the baselines.”