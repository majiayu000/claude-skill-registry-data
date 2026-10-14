---
name: e1004-gcr
description: "Use when specifying the galactic cosmic ray (GCR) radiation environment for a mission under ECSS-E-ST-10-04C: select the applicable GCR reference model (heavy-ion energy spectra for single-event-effects analyses, integral LET/dose spectra for total-dose analyses) based on the analysis type and required ion species coverage, classify the solar activity condition from a solar modulation potential, apply solar modulation to scale the reference solar-minimum energy spectra to the mission epoch, and verify that the selected worst-case condition and species coverage meet the analysis's requirements. Trigger: galactic cosmic ray, GCR, solar modulation, CREME96, Badhwar-O'Neill, ISO 15390, heavy ion spectrum, SEE analysis, total dose, e-st-10-04, ecss, space environment, radiation environment."
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
  tags: [ecss, e-st-10-04c, gcr, galactic-cosmic-ray, solar-modulation, radiation-environment, see, dose]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Galactic Cosmic Ray Environment (space-systems/ecss/e1004-gcr)

Use when the task is selecting and applying a galactic cosmic ray (GCR)
model under ECSS-E-ST-10-04C clause 9.2.3, to characterize the GCR
energy spectra and their solar modulation for single-event-effects
(SEE) or total-dose radiation analyses.

## Domain quick reference

- GCR is a persistent background of high-energy protons and heavier
  ions of galactic origin. Its flux at a given epoch is modulated by
  solar activity: the outgoing solar wind and its embedded magnetic
  field suppress the incoming GCR flux, so GCR flux is highest near
  solar minimum and lowest near solar maximum -- the opposite sense to
  the solar-particle-event environment (see sibling e1004-sep-fluence,
  e1004-sep-peakflux leaves).
- The degree of suppression is summarized by a solar modulation
  potential (heliocentric potential, in MV): a low potential
  corresponds to solar-minimum conditions (least suppression, highest
  GCR flux) and a high potential to solar-maximum conditions (most
  suppression, lowest GCR flux).
- SEE analyses need the full heavy-ion energy-spectra set (species
  from hydrogen through the heaviest ions of interest, historically to
  around uranium/actinide charge numbers) and are evaluated at the
  worst-case solar-minimum condition, since that epoch gives the
  highest GCR flux and therefore the highest single-event rate.
- Total-dose analyses instead need an integral flux/LET spectrum
  accumulated over the mission duration, which spans varying solar
  conditions across the mission's position in the solar cycle rather
  than a single worst-case epoch; species coverage needed for dose is
  narrower than for SEE because the heaviest, rarest ions contribute
  negligibly to total dose.
- Reference GCR models (e.g. CREME96/CREME2009-class or ISO
  15390-class models for SEE heavy-ion spectra; Badhwar-O'Neill-class
  models for dose) provide the solar-minimum reference spectra and a
  parameterized solar-modulation scaling; the model choice follows
  from the analysis type, not personal preference.
- This leaf scopes GCR model selection, solar-condition
  classification, and solar-modulation scaling only. Geomagnetic
  shielding of GCR/SEP at low-inclination low-Earth orbits is the
  sibling e1004-stormer leaf (clause 9.2.4); rolling the result into
  the radiation environment specification is the sibling
  e1004-rad-env-spec leaf (clause 9.3).

## Workflow

1. For each radiation analysis case, record its analysis type ("see"
   or "dose"), the maximum ion charge number (species_max_z) the
   analysis covers, the solar modulation potential (MV) assumed for
   the case, and the solar-minimum reference flux to be scaled.
2. Select the applicable GCR reference model from the analysis type
   (heavy-ion spectra model for "see", integral dose/LET spectra model
   for "dose").
3. Determine the minimum ion species coverage the analysis type
   requires and verify the case's species_max_z meets it; flag
   insufficient coverage rather than silently truncating the ion set.
4. Classify the case's solar modulation potential into a solar
   condition (solar minimum, solar maximum, or intermediate).
5. Apply solar modulation: scale the solar-minimum reference flux by
   the modulation-potential-dependent scale factor to obtain the flux
   applicable to the case's assumed epoch.
6. Determine the worst-case solar condition required for the analysis
   type ("see" requires solar minimum; "dose" requires integration
   across the mission's solar-cycle exposure rather than a single
   epoch) and check the case against it.
7. Mark the case compliant only when its species coverage is adequate
   and, for "see" cases, its solar condition is solar minimum; roll
   every case's compliance into the assessment record and do not close
   the radiation environment specification while any case remains
   non-compliant.

## Pitfalls

- Using a solar-maximum or intermediate modulation potential for an
  SEE worst-case analysis instead of solar minimum, understating the
  GCR flux and therefore the single-event rate.
- Truncating the heavy-ion species set below what the analysis type
  needs (e.g. stopping short of the heaviest ions of interest for an
  SEE analysis) because those ions are rare, when rare high-LET ions
  can still dominate the single-event rate for sensitive parts.
- Treating GCR and solar-particle-event flux as modulated the same way
  by solar activity -- GCR flux falls as solar activity rises, while
  SPE occurrence rises with solar activity; the two environments peak
  at opposite phases of the solar cycle.
- Applying a single worst-case epoch to a total-dose analysis instead
  of accumulating exposure across the mission's actual solar-cycle
  coverage, which over- or under-states the total dose depending on
  mission timing.

## Behavior contract (gate 3)

The model-selection, species-coverage, solar-condition classification,
solar-modulation scaling, and compliance logic is exercised by the
gate 3 contract test: scripts/test_e1004_gcr.py against
scripts/e1004_gcr_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1004_gcr.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
