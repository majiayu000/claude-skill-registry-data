---
name: e1004-b6-esp
description: "Use when generating the Annex B.6 Emission of Solar Protons (ESP) worst-case fluence spectra for a mission under ECSS-E-ST-10-04C: build the reference annual integral fluence spectrum, apply the confidence-level scale factor for the required design percentile, apply the mission-duration scale factor for the exposure period, assemble the resulting fluence-above-energy spectrum, and verify the selected confidence level meets the mission's worst-case design threshold. Trigger: ESP, emission of solar protons, solar proton fluence, solar particle event, worst-case fluence, confidence level, JPL model, Annex B.6, e-st-10-04, ecss, space environment, radiation environment."
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
  tags: [ecss, e-st-10-04c, esp, solar-proton, fluence, confidence-level, annex-b, radiation-environment]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Emission of Solar Protons (ESP) Fluence Spectra (space-systems/ecss/e1004-b6-esp)

Use when the task is generating the Annex B.6 Emission of Solar Protons
(ESP) worst-case fluence spectra under ECSS-E-ST-10-04C, to obtain a
design integral fluence-above-energy spectrum for a solar-proton
radiation-design case.

## Domain quick reference

- The ESP model is probabilistic, not deterministic: instead of a
  single fixed event spectrum, it returns a design fluence keyed to two
  case parameters -- the mission's exposure duration and a design
  confidence level (the probability that the true mission fluence will
  not exceed the returned value).
- Longer exposure duration raises the design fluence: a longer mission
  has more opportunity to encounter a large solar-proton event, so its
  worst-case fluence grows with duration, though not in direct
  proportion to it.
- A higher confidence level raises the design fluence: bounding a
  larger fraction of the event-size probability distribution requires
  reaching further into the rare, large-event tail, so fluence grows
  as the confidence level approaches its upper limit.
- The model reports fluence at a fixed set of proton energy thresholds
  (an integral spectrum: fluence of protons at or above each threshold
  energy), not a continuous differential spectrum and not a peak
  (instantaneous) flux -- confusing the ESP integral design fluence
  with a peak flux figure understates or overstates dose/SEE-rate
  estimates depending on which quantity the downstream calculation
  actually needs.
- Most radiation-design guidance treats a confidence level below about
  90% as insufficient for a worst-case design fluence; lower confidence
  levels are appropriate only for trade studies or non-worst-case
  sensitivity analysis, not for the design case itself.
- This leaf scopes ESP fluence-spectrum generation and the worst-case
  confidence-level check only. Rolling the ESP result into the mission
  radiation environment specification alongside GCR (sibling e1004-gcr
  leaf) and trapped-radiation environments is the sibling
  e1004-rad-env-spec leaf (clause 9.3).

## Workflow

1. For each solar-proton radiation-design case, record its mission
   exposure duration (years), the design confidence level (percent)
   the case requires, and the energy thresholds the downstream
   shielding/dose/SEE-rate calculation needs.
2. Build the reference 1-year, 50%-confidence annual integral fluence
   spectrum across the model's supported energy thresholds.
3. Compute the confidence-level scale factor for the case's design
   confidence level; verify the requested level falls within the
   model's supported range before scaling.
4. Compute the mission-duration scale factor for the case's exposure
   duration.
5. Apply both scale factors to the reference spectrum to assemble the
   case's design fluence-above-energy spectrum at each requested
   threshold energy.
6. Check that the assembled spectrum still decreases monotonically
   with increasing energy threshold -- the expected shape of an
   integral fluence spectrum -- flagging any deviation before the
   result is used downstream.
7. Mark the case compliant only when its design confidence level meets
   the mission's worst-case threshold and its spectrum passes the
   monotonicity check; roll every case's compliance into the
   assessment record and do not close the radiation environment
   specification while any case remains non-compliant.

## Pitfalls

- Selecting a design confidence level below the mission's worst-case
  threshold (e.g. using a trade-study confidence level for the actual
  design case), understating the design fluence and the resulting
  shielding, dose, or SEE-rate margin.
- Treating the ESP integral fluence-above-energy spectrum as a
  continuous differential spectrum or as a peak (instantaneous) flux,
  which produces the wrong input to a downstream shielding, total-dose,
  or SEE-rate calculation expecting a different quantity.
- Reusing a design fluence computed for one mission duration on a
  mission with a different exposure duration instead of recomputing
  the duration scale factor, understating fluence for a longer mission
  or over-designing for a shorter one.
- Querying the spectrum at an energy threshold the model does not
  support instead of at one of its defined thresholds, or silently
  substituting a nearby threshold's fluence without accounting for the
  spectrum's shape between thresholds.

## Behavior contract (gate 3)

The confidence-level scaling, duration scaling, spectrum assembly,
monotonicity check, and worst-case compliance logic is exercised by
the gate 3 contract test: scripts/test_e1004_b6_esp.py against
scripts/e1004_b6_esp_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1004_b6_esp.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
