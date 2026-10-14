---
name: q2030-hv
description: "Compute the high-voltage provisions an electrical harness owes under ECSS-Q-ST-20-30C section 6.20 and its IPC section 20 basis. Use when the task is sizing clearance and creepage at a harness termination and grading the as-built distances: derating the breakdown gradient of air with operating pressure, refusing air as an insulator inside the Paschen minimum band unless the feature is encapsulated, taking the surface-flashover gradient below that band, scaling creepage with the insulating material group and contamination category, and deriving the proof voltage, dwell and leakage limit of the high-voltage test. Trigger: ecss, q-st-20-30c, harness-high-voltage-clearance, harness-creepage-distance, paschen-minimum-band, vacuum-surface-flashover, harness-proof-voltage-test."
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
  tags: [ecss, q-st-20-30-harness-scope, q2030-hv, harness-high-voltage-clearance, harness-creepage-distance, paschen-minimum-band, vacuum-surface-flashover, harness-proof-voltage-test]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Harness Manufacturing — High-Voltage Application (space-systems/ecss/q2030-hv)

Use when the task is the high-voltage provision of ECSS-Q-ST-20-30C
section 6.20, which binds the high-voltage section of the
IPC/WHMA-A-620 acceptance basis — sizing the clearance and creepage a
harness termination owes at its working voltage and operating pressure,
grading what was actually built, and setting the proof test that
demonstrates it.

## Domain quick reference

- The provisions have an entry condition. Below the high-voltage
  threshold a termination is graded by the ordinary acceptance criteria
  and owes no clearance, creepage or proof test under this section;
  applying them anyway adds stress and cost without adding evidence.
- The insulating medium follows the pressure, and it does so
  non-monotonically. Well above the Paschen minimum the medium is air
  and its breakdown gradient falls roughly with pressure, so a cabin
  or a launch ascent is worse than the ground. Well below it the
  residual gas cannot sustain an avalanche and the limiting mechanism
  becomes flashover along the insulating surface, at a far higher
  gradient. Between the two lies the band where the breakdown voltage
  of air passes through its minimum.
- Inside that band no practical spacing holds off a high voltage. The
  answer is not a larger gap: it is encapsulation, potting or a
  pressurized enclosure, so that the band is never the medium the
  feature is asked to work in. A feature sized by a gap there has been
  sized against a curve it is not on.
- Clearance and creepage are different paths and are sized differently.
  Clearance is through the medium and follows the breakdown gradient;
  creepage is along an insulating surface and follows the tracking
  performance of the material and how dirty the surface is allowed to
  get. Creepage is never allowed to be shorter than the clearance it
  parallels, because the surface path would otherwise be the weaker of
  the two.
- The proof test is derived, not chosen. Its voltage comes from the
  working voltage, its dwell has to be long enough for a weakness to
  show, and the leakage current during the dwell is the measurement
  that actually says whether the insulation is sound.

## Workflow

1. Validate the feature record: identifier, working voltage, operating
   pressure, insulating material group, contamination category,
   encapsulation flag, as-built distances and the proof-test record. A
   non-positive voltage or pressure, or an unknown material group or
   contamination category, is an input error, not a case to clamp.
2. Decide whether the high-voltage provisions apply at this working
   voltage and report a feature below the threshold as not applicable
   rather than as compliant by accident.
3. Pick the insulation regime from the operating pressure, then take
   the breakdown gradient of that regime — pressure-derated air above
   the band, surface flashover below it.
4. Raise the encapsulation finding for an unencapsulated feature inside
   the band, and do not size a gap for it: there is no gradient there
   to size against.
5. Size the clearance from the working voltage, the gradient and the
   safety factor, with a floor no feature goes below.
6. Size the creepage from the working voltage, the material group and
   the contamination category, with its own floor and never below the
   clearance.
7. Grade the as-built distances, derive the proof voltage and grade the
   applied voltage, dwell and leakage, absorbing representation error
   at each limit with a named tolerance rather than by widening it.

## Pitfalls

- Sizing a gap for a feature that operates inside the Paschen minimum
  band. The curve has no usable gradient there, so a larger gap buys
  nothing; encapsulation or pressurization is the only answer.
- Using the sea-level breakdown gradient for a feature that flies. The
  gradient falls with pressure across the air regime, and the ascent
  profile passes through the worst of it.
- Treating vacuum as free insulation. The gas stops breaking down, but
  the surface does not, and a contaminated or tracked surface flashes
  over well below the clean-surface gradient.
- Sizing creepage without the material and contamination inputs. The
  same voltage on the same geometry needs very different surface paths
  on a high-tracking-performance material in a controlled environment
  and a poor one in a dirty one.
- Accepting a proof test that reached a voltage someone picked. The
  level comes from the working voltage, and a short dwell or an
  unrecorded leakage current leaves the test without its measurement.

## Behavior contract (gate 3)

The feature validation, applicability threshold, pressure-regime
selection and gradient derivation, encapsulation finding, clearance and
creepage sizing with their floors and the creepage-not-below-clearance
rule, as-built grading and the proof-voltage, dwell and leakage checks
are exercised by the gate 3 contract test: scripts/test_q2030_hv.py
against scripts/q2030_hv_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_q2030_hv.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
