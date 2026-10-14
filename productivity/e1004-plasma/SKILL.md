---
name: e1004-plasma
description: "Use when defining the plasma environment required by ECSS-E-ST-10-04C clause 8.2 for spacecraft charging analysis: determine which plasma regions (ionosphere, plasmasphere, auroral, outer magnetosphere, solar wind, magnetosheath, magnetotail/L2, planetary, induced) apply to each orbit segment, verify that a model and the electron density, electron temperature, ion density, and ion temperature are recorded for every applicable region, and identify missing regions or incomplete entries before the charging environment definition is closed out. Trigger: plasma environment, spacecraft charging, e-st-10-04, ecss, electron density, ion temperature, surface charging, auroral charging, outer magnetosphere plasma, plasmasphere, induced plasma."
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
  tags: [ecss, e-st-10-04c, plasma-environment, spacecraft-charging, space-systems]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Plasma Environment for Charging (space-systems/ecss/e1004-plasma)

Use when the task is defining the ambient plasma environment for a
mission under ECSS-E-ST-10-04C clause 8.2: selecting the plasma
region models that apply to each orbit segment and recording the
electron/ion density and temperature that drive surface- and
internal-charging risk assessments.

## Domain quick reference

- Clause 8.2 covers nine plasma regions, each with its own
  characteristic density/temperature regime and its own charging
  concern: ionosphere (cold, dense, low charging risk), plasmasphere
  (cold, dense, low risk), auroral (precipitating keV electrons,
  surface-charging risk at high latitude LEO), outer magnetosphere
  (hot, tenuous substorm-injected plasma, the dominant GEO/GTO/HEO
  surface-charging driver), solar wind (tenuous, supersonic flow),
  magnetosheath (shocked, heated solar wind at the magnetopause),
  magnetotail/L2 (hot, tenuous lobe and plasma-sheet plasma), planetary
  (non-Earth plasma environments), and induced (spacecraft-generated
  plasma from electric propulsion plumes or outgassing).
- Which regions apply depends on orbit regime: LEO sees the
  ionosphere, plus the auroral region if the orbit's inclination
  carries it through high-latitude/polar field lines; MEO sits inside
  the plasmasphere; GEO orbits the plasmasphere boundary and are
  exposed to the outer magnetosphere's substorm charging environment;
  GTO/HEO add magnetosheath crossings at apogee; L2 and the deep
  magnetotail see magnetotail/L2 plasma and, at L2, solar wind; purely
  interplanetary trajectories see only the solar wind; non-Earth
  missions use the planetary region. The induced region applies to
  any mission carrying an onboard plasma source (electric
  propulsion, outgassing) regardless of orbit regime.
- For every applicable region the charging environment definition
  must record: the model used, electron density, electron
  temperature, ion density, and ion temperature. An entry naming a
  model but omitting any of the four density/temperature values is
  incomplete — charging risk cannot be assessed from a partial
  characterization.
- The outer magnetosphere and auroral regions are the ones most
  often under-specified because their worst-case (substorm/
  precipitation) values, not their average values, are what drive
  the charging design case; recording only average conditions for
  these two regions understates the charging risk.

## Workflow

1. Enumerate the mission's orbit segments and classify each by
   regime (LEO, MEO, GEO, GTO, HEO, L2, deep-tail, interplanetary,
   planetary), noting whether the orbit carries high-latitude/polar
   coverage and whether the spacecraft carries an onboard plasma
   source (electric propulsion, significant outgassing).
2. For each orbit segment, derive the set of applicable plasma
   regions from its regime, polar flag, and plasma-source flag,
   rather than assuming every mission needs every region.
3. For each applicable region, record the model choice and the
   electron density, electron temperature, ion density, and ion
   temperature; do not leave any of the four values blank or
   non-positive.
4. For the outer magnetosphere and auroral regions specifically,
   confirm the recorded values are the worst-case (substorm or
   precipitation-event) characterization used for the charging
   design case, not a long-term average.
5. Check each orbit segment against its derived region set: any
   applicable region with no entry is a missing region; any entry
   missing model or any density/temperature value is an incomplete
   entry.
6. Only mark the charging environment definition complete when every
   orbit segment has no missing regions and no incomplete entries;
   otherwise report the specific gaps so they can be closed before
   the charging analysis proceeds.

## Pitfalls

- Applying one plasma region (typically the ionosphere) to the whole
  mission instead of deriving the region set per orbit segment, which
  hides the outer-magnetosphere/auroral charging drivers for
  GEO/GTO/HEO and high-latitude LEO segments.
- Recording only electron density and temperature and omitting the
  ion values — internal-charging screens use the electron
  environment, but a complete plasma definition still needs the ion
  side for spacecraft-potential and differential-charging analysis.
- Using long-term-average outer-magnetosphere or auroral values
  instead of the worst-case substorm/precipitation values, which
  understates the surface-charging design case.
- Omitting the induced region for a spacecraft with electric
  propulsion or significant outgassing because it is easy to treat as
  a hardware topic rather than part of the plasma environment
  definition.

## Behavior contract (gate 3)

The region-applicability derivation, region-entry completeness, and
orbit-segment roll-up logic is exercised by the gate 3 contract test:
scripts/test_e1004_plasma.py against scripts/e1004_plasma_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1004_plasma.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
