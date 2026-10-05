---
name: run-stage-c
description: Use this skill when executing the cross-modal transfer stage of the appraisal project, including image-side data preparation, label mapping, multimodal inference, application of frozen text-derived directions, transfer evaluation, and comparison against caption-mediated or baseline explanations.
---

# Run Stage C

This skill runs the image-side cross-modal appraisal transfer experiment using the frozen or previously learned text-side machinery.

## Use this skill when

- The task is to run the multimodal or image-side transfer experiment.
- A user refers to “Stage C,” “cross-modal transfer,” “EMOTIC evaluation,” or image-conditioned appraisal readout/steering.
- Stage A outputs already exist and the next goal is transfer validation.

## Do not use this skill for

- Cold-start environment setup.
- Pure text-only replication.
- Final write-up except for concise run summaries.

## Objective

Test whether text-derived appraisal directions or probes transfer meaningfully to the multimodal setting, and determine whether observed effects support genuine transfer rather than a weaker explanation such as caption mediation.

## Required precondition

Assume Stage A should already exist. Before running, verify:
- which probe/checkpoint/direction is being imported,
- whether its training setup is documented,
- whether the imported artifact is the intended one.

If Stage A is missing or ambiguous, stop and ask to resolve that dependency unless the user explicitly requests a provisional or exploratory run.

## Read these first

- `CLAUDE.md`
- `docs/experiment-1.md`
- `docs/datasets.md`
- `docs/models-gemma3.md`
- `docs/probes.md`
- any Stage A output manifest, metrics file, or checkpoint directory
- relevant multimodal code under `src/experiments/`, `src/data/`, `src/bridge/`

## Stage C workflow

### Step 1: Confirm transfer design

Determine:
- the image dataset(s),
- label space and any mapping rules,
- which frozen text-derived directions/probes are used,
- which multimodal model path is primary,
- whether transfer is readout-only, steering-based, or both,
- the baselines that must be reported.

Never proceed without a clear mapping between source-side artifacts and target-side evaluation.

### Step 2: Validate image-side data and mapping

Check:
- dataset presence and accessibility,
- subject/image counts if documented,
- split integrity,
- preprocessing steps,
- class or appraisal mapping logic,
- any ambiguous or lossy category conversions.

If mapping quality is a major source of uncertainty, make it a first-class caveat in the result summary.

### Step 3: Verify multimodal forward path

Before running a full experiment:
- test one sample end to end,
- confirm image preprocessing is correct,
- verify the model receives both text and image inputs as intended,
- confirm hook positions exist in the expected path,
- check output shapes and extracted representations.

Do not scale until the single-sample path is verified.

### Step 4: Apply frozen directions or probes

Load the Stage A artifact(s) and apply them consistently:
- use the documented hook locations,
- preserve preprocessing conventions where required,
- avoid silent re-fitting on image-side data unless the experiment explicitly calls for it.

If any adaptation is required, document exactly what changed and why.

### Step 5: Evaluate transfer

Report the planned metrics and compare against:
- no-steering or no-transfer baseline,
- simple caption or verbalization baseline when applicable,
- random or shuffled controls if defined in the repo.

The point is not just to show an effect, but to show that the effect supports the intended hypothesis.

### Step 6: Stress-test alternative explanations

Where the design allows, check whether apparent transfer could instead be explained by:
- caption mediation,
- label leakage,
- domain-shift artifacts,
- mapping artifacts,
- prompt sensitivity.

If the transfer signal collapses under these checks, say so clearly.

### Step 7: Save outputs for analysis

Persist:
- configs,
- metric tables,
- selected examples,
- plots if the repo expects them,
- run notes emphasizing transfer interpretation and caveats.

## What to produce

At the end, produce:
- transfer verdict,
- key metrics,
- baseline comparisons,
- strongest caveats,
- output paths,
- recommendation for next action.

## Interpretation rules

Use careful language:
- “supports transfer” only if the evidence beats the relevant baselines,
- “inconclusive” if the effect is weak, unstable, or confounded,
- “fails to support transfer” if results do not survive basic controls.

## Guardrails

- Do not retrain text probes inside Stage C unless the protocol explicitly requires it.
- Do not hide lossy label mappings.
- Do not interpret caption-mediated success as direct evidence of shared multimodal appraisal geometry.
- Do not overstate novelty from a single positive metric.
- Do not skip baseline comparisons.

## Completion criteria

This skill is complete when:
- the image-side pipeline has run,
- transfer metrics are computed,
- alternative explanations are addressed at least minimally,
- outputs are saved,
- the result is classified as supportive, inconclusive, or unsupportive.

## Example invocations

- “Run Stage C using the frozen Stage A probe.”
- “Evaluate cross-modal transfer on EMOTIC.”
- “Test whether the transfer beats a caption baseline.”
- “Diagnose why the multimodal steering run is failing.”