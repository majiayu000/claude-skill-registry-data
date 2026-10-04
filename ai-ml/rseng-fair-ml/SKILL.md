---
name: rseng-fair-ml
description: >-
  Covers applying FAIR principles to machine learning artifacts: making models
  findable and reusable with model cards and rich repository metadata,
  documenting datasets with Croissant and datasheet-style records, licensing
  models and weights, linking the model-data-code-paper cluster with
  persistent identifiers, and the RDA FAIR4ML metadata direction. Use when a
  project trains, fine-tunes, publishes or reuses ML models or ML-ready
  datasets, when the user mentions model cards, Croissant, datasheets, FAIR4ML
  or model licensing, when a model heads to a hub or archive, or when
  evaluating whether a third-party model is documented well enough to build
  on. (General software FAIR is rseng-fair-software; automated repository
  scoring is rseng-fairguard.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# FAIR for machine learning

FAIR was written for data, extended to software (FAIR4RS -
rseng-fair-software), and is now being worked out for machine
learning (the RDA FAIR4ML interest group leads the metadata
standardization). ML needs its own treatment because a model is
neither data nor ordinary software: its behavior is inseparable
from its training data, its "source" includes weights that no
license default covers, and reuse without documentation reproduces
biases invisibly. The practical FAIR-ML unit is the CLUSTER -
model + data + code + evaluation + paper - linked both ways with
persistent identifiers.

## Findable: metadata that machines and reviewers read

- Model cards are the model's README and its FAIR metadata in one:
  intended use and out-of-scope uses, training data description,
  evaluation results with conditions, limitations and biases,
  licensing. Hub-hosted cards (Hugging Face's structured format)
  double as searchable metadata; write them from the actual
  training run, not memory (the experiment config and logs are the
  source - rseng-reproducibility).
- Datasets get Croissant: the MLCommons format describes ML
  datasets (schema, distribution, provenance) in machine-readable
  form that major hubs and search index - the ML-ready complement
  to the generic dataset documentation in rseng-data-management.
- Identifiers: archive released models and dataset snapshots with
  DOIs (rseng-archiving; hub storage is not preservation), and
  cross-link model card, dataset record, code repository
  (rseng-citation-metadata) and paper so each cites the others.

## Accessible and licensed honestly

- State exactly what is released: weights, architecture, training
  code, data, all or some - and license each part explicitly.
  Code licenses do not fit weights cleanly; dedicated model
  licenses (including use-restricted ones) exist, and "weights on
  a hub with no license" is the ML version of unlicensed code:
  unusable (rseng-licensing, rseng-license-compliance for
  compatibility when models build on models).
- Gated access is legitimate (safety, privacy, data terms) when
  the CONDITIONS are stated and the metadata stays public - as
  closed as necessary, as open as possible
  (rseng-regulatory-compliance where personal data trained the
  model; the EU AI Act documentation duties overlap helpfully
  with a good model card).

## Interoperable: formats and conventions

- Export to exchange formats where the ecosystem has them (ONNX-
  class interchange for deployment; standard checkpoint formats
  per framework) and pin the framework versions that load the
  weights (rseng-reproducible-environments) - a checkpoint nobody
  can load is a dead artifact.
- Follow the target hub's metadata conventions (tags, task
  taxonomy, evaluation fields) - interoperability for models is
  largely hub-convention compliance today, while FAIR4ML
  standardization matures.

## Reusable: the documentation that prevents misuse

Reuse-readiness is a checklist an agent can run on any model
(the user's own before release, third-party models before
adoption - the rseng-software-reuse evaluation instinct):

1. Can I tell what data trained it, and under what terms?
2. Are evaluation claims reproducible - metric, dataset version,
   split, conditions stated (rseng-research-integrity for the
   numbers)?
3. Are limitations and known failure modes documented, or must I
   rediscover them?
4. Is the license compatible with my use, including the data's
   terms flowing through?
5. Can I load it - format, framework versions, hardware
   requirements (rseng-gpu-computing)?

A "no" on any of these is a finding: fix it for your own models,
weigh it for others'. Record AI/ML provenance in aidecl.yaml
(rseng-ai-declaration) - a project that trains models with AI
assistance has two provenance layers, and both belong in the
record.

## Working with this skill

This skill is source-independent: its authority is the FAIR4ML
work, the Croissant specification and model-card practice linked
below. It extends rseng-fair-software to ML artifacts; rseng-fairguard
assesses the software side.

Learn more (verified):
  - https://www.rd-alliance.org/groups/fair-machine-learning-fair4ml-ig/ -
    RDA FAIR4ML interest group
  - https://mlcommons.org/working-groups/data/croissant/ -
    Croissant ML dataset format
  - https://huggingface.co/docs/hub/en/model-cards - model card
    format and guidance
  - https://www.gofair.foundation/fair-principles - the FAIR principles
  - https://onnx.ai - ONNX model interchange format

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - DOIs for model and dataset snapshots
- rseng-data-management - dataset documentation beneath Croissant
- rseng-fair-software - the general FAIR baseline
- rseng-gpu-computing - hardware requirements for model reuse
- rseng-licensing - licensing weights and training data
- rseng-reproducibility - model cards written from actual runs

<!-- related-skills:end -->
