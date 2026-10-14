---
name: e1002-models
description: "Use when a space project must define its verification model philosophy under ECSS-E-ST-10-02C: choosing prototype vs protoflight, listing the physical models (STM, EM, QM, PFM, FM, EQM) with purpose/configuration/stages for the Verification Plan, checking a model is representative of the item it stands in for, and flagging re-verification after a design change. Trigger: model philosophy, prototype model, protoflight, qualification model, flight model, engineering model, model list, verification plan, VP, model-based verification, E-ST-10-02, ecss, e-st-10c."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: ecss
    reference-only: true
gated: false
domain: space-systems
pack: space-systems
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: space-systems
  subdomain: ecss
  tags: [ecss, e-st-10-02c, model-philosophy, protoflight, prototype, verification-plan]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Verification Model Philosophy (space-systems/ecss/e1002-models)

Use when the task is defining, under ECSS-E-ST-10-02C clause 5.2.5,
which physical models a project builds to carry out verification, and
recording model-based verification rules ahead of detailed
verification planning.

## Domain quick reference

- ECSS-E-ST-10-02C clause 5.2.5 requires a project to define a model
  philosophy: which physical models will be built, what each model is
  for, and how verification results on a model transfer to the item it
  represents. The model list is recorded in the Verification Plan
  (VP, clause 5.2.8.1 / Annex A).
- Recognised model designations: STM (structural/thermal model), EM
  (engineering model, functional breadboard), QM (qualification
  model, absorbs qualification-level stresses so the flight article is
  not stressed beyond acceptance levels), PFM (protoflight model, a
  single article that absorbs qualification-level tests at reduced
  duration and then flies), FM (flight model), EQM (engineering
  qualification model).
- Two philosophies: the prototype approach builds a disposable/
  refurbishable QM for qualification and a separate FM that only sees
  acceptance-level testing, preserving full flight-article margins;
  the protoflight approach tests a single PFM at full qualification
  amplitude (but usually reduced duration/cycles) and then flies that
  same article, saving cost and schedule at the price of consuming
  some of the flight article's life margin.
- A verification result performed on a model is only creditable
  against a requirement for an item that shares the model's
  configuration; a configuration mismatch between model and item means
  the result cannot be claimed without re-verification.
- A design change to an item (or to the model itself) after a model
  has already been exercised against a requirement invalidates the
  prior verification credit for that requirement.

## Workflow

1. Determine the model philosophy driver set for the project: whether
   full qualification-margin preservation on the flight article is
   required, and whether schedule or cost pressure exists.
2. Select the philosophy: margin preservation, if required, forces the
   prototype approach regardless of schedule/cost pressure; otherwise
   schedule or cost pressure justifies protoflight; with neither
   driver present, default to prototype as the conservative choice.
3. Build the model list for the VP: for every model, record its
   designation (from the recognised set), its purpose, its
   configuration/design standard, and the verification stage(s) it
   supports. Reject an empty list, a missing field, an unrecognised or
   duplicated designation, or a model with no stages.
4. Before crediting a model's test result against a requirement on a
   given item, check representativeness: the model's configuration and
   the item's configuration must match; a mismatch blocks crediting
   the result until re-verification.
5. If the philosophy is protoflight, check test severity on the PFM:
   applied amplitude must not fall below the qualification amplitude
   (protoflight does not reduce stress level, since the article will
   still fly), while applied duration may be at or below the
   qualification duration to conserve life margin.
6. Track design changes against every requirement already closed by a
   model-based result: a change to the item or to the model after that
   result was recorded triggers re-verification before the requirement
   can stay closed.

## Pitfalls

- Choosing protoflight purely for cost/schedule savings on a
  first-of-kind item where margin preservation was actually required
  -- record the margin-preservation driver before picking the
  philosophy, not after.
- Reducing protoflight test amplitude instead of duration -- amplitude
  reduction under-tests the article that will fly; only duration/cycle
  count is the intended lever.
- Crediting a QM test result against the FM's requirements without
  checking that QM and FM configurations actually match.
- Leaving a requirement closed on a model-based result after the item
  or model design changed, instead of triggering re-verification.
- Omitting the model list from the VP, or listing a model without a
  purpose, configuration, or the stages it supports.

## Behavior contract (gate 3)

The philosophy-selection, model-list-validation, representativeness,
protoflight-severity, and re-verification-trigger logic is exercised
by the gate 3 contract test: scripts/test_e1002_models.py against
scripts/e1002_models_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1002_models.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
