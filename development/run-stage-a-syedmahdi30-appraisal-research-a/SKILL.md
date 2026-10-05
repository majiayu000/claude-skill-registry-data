---
name: run-stage-a
description: Use this skill when executing the text-only replication stage of the appraisal-transfer project, including dataset preparation, prompt/label checks, activation caching, probe training, steering tests, and baseline metric generation on the primary text-side pipeline.
---

# Run Stage A

This skill executes the text-side replication stage that establishes the project’s foundation before any cross-modal transfer claims are made.

## Use this skill when

- The task is to reproduce or implement the text-only appraisal probe workflow.
- A user asks to run, debug, or evaluate the “Stage A” or “text-side” experiment.
- The project needs appraisal direction learning, activation extraction, probe fitting, or steering validation on text data.
- The cross-modal stage depends on first proving that the text-side mechanism works.

## Do not use this skill for

- Initial package/environment setup from scratch.
- Final image-side transfer experiments.
- Full paper writing or final presentation formatting.

## Objective

Build a reliable text-side benchmark that shows:
1. the data pipeline works,
2. labels and tokenization are understood,
3. internal activations can be captured consistently,
4. probes can be trained and evaluated,
5. steering yields interpretable directional effects.

## Read these first

- `CLAUDE.md`
- `docs/experiment-1.md`
- `docs/probes.md`
- `docs/datasets.md`
- `docs/models-gemma3.md`
- relevant experiment code under `src/experiments/`, `src/probes/`, `src/data/`

## Stage A workflow

### Step 1: Confirm the task definition

Determine:
- the text dataset(s) to use,
- the exact appraisal targets,
- the split strategy,
- the model variant,
- the hidden states / hook points to test,
- the evaluation metrics,
- the steering evaluation protocol.

If any of these are unclear, resolve from repo docs before writing new assumptions.

### Step 2: Validate labels and tokenization

Before probe training:
- inspect label names,
- verify any closed-vocabulary outputs,
- test whether target labels are single-token or multi-token where relevant,
- note any tokenization mismatch that could invalidate logit-based scoring.

Never assume emotion or appraisal labels tokenize cleanly.

### Step 3: Build or verify activation extraction

Implement or validate:
- the chosen hook path(s),
- batch handling,
- layer selection,
- caching strategy,
- final-token vs full-sequence extraction logic,
- reproducible saving of activations or derived matrices.

Prefer the smallest cache that still supports the analysis. Avoid full-sequence caching unless the experiment truly requires it.

### Step 4: Train the probes

Use the repo’s canonical modeling approach when documented. If not documented, prefer a simple, defensible baseline such as ridge regression or another lightweight linear probe.

For probe training:
- separate train/validation/test cleanly,
- standardize features if required by the method,
- record hyperparameters,
- save metrics and artifacts in a reproducible location,
- avoid leaking validation choices into the test set.

### Step 5: Evaluate the probes

Report:
- primary metric(s),
- layer-wise performance if applicable,
- baseline comparisons,
- obvious failure modes,
- sensitivity to hook location or representation choice.

If the repo is designed around a “hard gate,” be explicit about whether the gate is met.

### Step 6: Run steering checks

If Stage A includes steering:
- compute or load the steering direction,
- apply it at the documented hook point,
- compare controlled before/after outputs,
- inspect whether the effect is directional and interpretable rather than noisy.

Use small, representative examples first before scaling.

### Step 7: Save reproducible outputs

Persist:
- configs,
- metrics,
- trained probe objects or weights if appropriate,
- run notes,
- summary plots or tables if the repo expects them.

Ensure a later skill can consume these outputs without recomputing the entire stage.

## What to produce

At the end, produce:
- a concise run summary,
- pass/fail status for the Stage A gate,
- key metrics,
- paths to outputs,
- known caveats,
- the recommended next step.

## Failure handling

If Stage A fails:
- localize the failure to one of data, tokenization, hooking, modeling, or steering,
- recommend the cheapest next diagnostic,
- avoid running the full pipeline repeatedly without narrowing the fault.

## Guardrails

- Do not claim replication success from partial metrics alone.
- Do not mix train/test data.
- Do not treat a noisy qualitative output change as sufficient evidence of valid steering.
- Do not change appraisal definitions mid-run without documenting it.
- Do not proceed to Stage C automatically unless the text-side gate is satisfied or the user explicitly requests it.

## Completion criteria

This skill is complete when:
- the text-side pipeline runs end to end,
- probes are trained and evaluated,
- steering has been checked if required,
- outputs are saved reproducibly,
- the readiness for Stage C is explicit.

## Example invocations

- “Run Stage A on the current text dataset.”
- “Fit the appraisal probes and summarize the results.”
- “Check whether the text-side steering direction actually works.”
- “Debug the activation extraction for the replication stage.”