---
name: e1004-debris
description: "Use when a space project must define which space debris flux model (MASTER-class or ORDEM-class) to select and apply, under ECSS-E-ST-10-04C clause 10.2.2.1, for a mission's orbit and analysis epoch: validating that a candidate model's declared altitude/inclination/epoch/diameter envelope actually covers the mission envelope, building a complete model run request, and determining when a prior result needs re-assessment. Trigger: space debris flux, debris environment model, MASTER model, ORDEM model, orbital debris, debris flux envelope, debris risk input, E-ST-10-04, ecss, e-st-10c."
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
  tags: [ecss, e-st-10-04c, debris, master, ordem, space-environment, flux-model]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Space Debris Flux Model Selection (space-systems/ecss/e1004-debris)

Use when the task is selecting and applying, under ECSS-E-ST-10-04C clause
10.2.2.1, a space debris flux model for a mission's orbit and analysis
epoch, ahead of the debris/meteoroid impact risk assessment
(see e1004-impact-risk) and its margin policy (e1004-mm-margins).

## Domain quick reference

- Clause 10.2.2.1 requires a project to select and apply a space debris
  flux model appropriate to the mission's orbit and epoch. "MASTER-class"
  and "ORDEM-class" name the two accepted families of such models (ESA's
  MASTER line and NASA's ORDEM line); any specific release from either
  family is acceptable provided its declared validity envelope actually
  covers the mission's orbit and analysis epoch -- the clause does not
  mandate one specific tool or version.
- The tracked/catalogued and modelled debris population changes over
  time (new breakups, decays, projected growth), so every model release
  is published against a stated epoch validity window. A release whose
  epoch window does not reach the mission's analysis year(s) cannot be
  applied to that mission without sourcing an updated release.
- Debris flux is strongly regime-dependent: altitude (LEO shells are far
  denser than GEO), inclination (sun-synchronous/polar bands concentrate
  certain populations), and particle diameter (flux is cumulative in
  diameter -- smaller thresholds always see higher flux) all shape the
  result, so a model run must fix all of these, not just pick a model
  name.
- A model run request is only complete once it fixes: one or more
  diameter thresholds (ascending, strictly positive), an exposure
  duration, and a target surface/exposure geometry identifier; the
  resulting flux number cannot be interpreted without all three.
- A debris-flux result stops being valid for a requirement once the
  mission's analysis end-year passes the selected model's declared
  epoch validity, or once the orbit regime the flux was computed for
  changes (e.g. an orbit-raising/lowering maneuver) -- either condition
  forces re-selection and re-run before the result can be relied on
  further.

## Workflow

1. Capture the mission envelope needed for the debris flux run: altitude
   range (km), inclination range (deg), analysis epoch (start/end
   year), and particle diameter range of interest (mm). Reject an
   envelope with a missing field or an inverted min/max range before
   proceeding.
2. For each candidate model (each declaring a family -- MASTER or ORDEM
   -- and its own declared altitude/inclination/epoch/diameter
   envelope), check that the mission envelope fits entirely inside the
   model's declared envelope on every field; drop any candidate with
   even one field where the mission range exceeds the model's declared
   range.
3. If the customer/agency mandates a specific family, filter the
   covering candidates down to that family. If no covering candidate
   remains -- in-family or not -- the run cannot proceed: a newer model
   release or an alternate family must be sourced before continuing.
4. From the remaining covering candidates, select one deterministically
   (alphabetically by name, since either family is equally acceptable
   when both cover the envelope) and record which model was chosen and
   that its envelope was checked against the mission envelope.
5. Build the model run request: normalize the diameter thresholds
   (strictly positive, strictly ascending), the exposure duration
   (> 0), and the target surface identifier (non-empty); reject an
   incomplete or malformed request before it is handed to the model
   tool, rather than letting the tool run on partial inputs.
6. After a run's results are used to close a requirement or feed the
   impact risk assessment, track epoch drift and orbit changes: if the
   mission's analysis end-year exceeds the selected model's declared
   epoch validity, or the orbit regime changed after the run, flag the
   result for re-assessment before it is used further.

## Pitfalls

- Picking a model purely because it is the "usual" family (e.g. always
  MASTER) without checking that its declared epoch window actually
  reaches the mission's analysis year(s).
- Running the model against a single diameter threshold when the
  downstream impact-risk assessment needs a cumulative flux curve
  across several thresholds.
- Leaving a debris-flux result in force after an orbit-raising or
  orbit-lowering maneuver changed the regime the flux was originally
  computed for.
- Treating "MASTER/ORDEM-class" as one fixed tool version instead of
  checking the actual declared validity envelope of the specific
  release in use.
- Omitting the exposure duration or target surface identifier from the
  run request, leaving a flux number that cannot be interpreted or
  reproduced.

## Behavior contract (gate 3)

The envelope-validation, model-selection, run-request-construction, and
re-assessment-trigger logic is exercised by the gate 3 contract test:
scripts/test_e1004_debris.py against scripts/e1004_debris_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1004_debris.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
