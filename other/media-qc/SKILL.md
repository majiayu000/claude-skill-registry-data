---
name: media-qc
description: Review generated candidate takes with structured script-faithfulness, identity, background, spatial, action, motion, physics, artifact, dialogue-sync, and subtitle-sync checks before creative take selection.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Media QC

## Workflow

1. Read core contract, `MEDIA_QC.md`, source shot brief, take record, approved references, and adjacent approved material when continuity matters.
2. Inspect the actual generated media. Do not score from the prompt alone.
3. Append or update the take's record in `04_generation/take_qc.jsonl`.
4. Use pass, warn, fail, not-applicable, or not-checked for each relevant dimension and provide concise evidence.
5. Optional automated metrics may be recorded with evaluator/version metadata, but do not convert them into taste judgments automatically.
6. Set `overall` to fail for hard script, identity, continuity, physics, corruption, or sync failures that make the take unusable as planned. For visible dialogue with approved-audio authority, treat wrong speaker ownership, unexpected mouth movement on a non-speaker, or generation/review audio hash drift as a hard sync failure.
7. Pass the QC record to `take-selection`.

## Done

The take has an evidence-backed production-quality record that separates objective/observable defects from later creative preference.
