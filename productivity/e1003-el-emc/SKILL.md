---
name: e1003-el-emc
description: "Use when running element electromagnetic compatibility tests under ECSS-E-ST-10-03C §6.5.5: determine auto-compatibility by verifying that each internal emitter's frequency has sufficient isolation margin against every internal receive band, evaluate passive intermodulation (PIM) products for RF-bearing elements to confirm no odd-order products fall within the receive band, perform residual magnetic dipole moment checks against the element magnetic budget, and identify the correct test mode—stand-alone or embedded—per §6.5.5.2 for each applicable test category. Trigger: ecss, e-st-10-03c, emc, electromagnetic-compatibility, pim, passive-intermodulation, magnetic-field, auto-compatibility, stand-alone, embedded."
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
  tags: [ecss, e-st-10-03c, emc, electromagnetic-compatibility, pim, passive-intermodulation, magnetic-field, auto-compatibility]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS AIT — Element Electromagnetic Compatibility Tests (space-systems/ecss/e1003-el-emc)

Use when the task is the electromagnetic compatibility assessment of a space
element under ECSS-E-ST-10-03C §6.5.5, covering auto-compatibility verification,
passive intermodulation (PIM) evaluation for RF-carrying elements, residual
magnetic dipole moment measurement, and selection of stand-alone versus embedded
test mode per §6.5.5.2.

## Domain quick reference

- §6.5.5 groups element EMC tests into four categories: auto-compatibility
  (internal emitter vs. internal receiver), passive intermodulation (two carriers
  mixing in passive components to produce unwanted products), magnetic field
  measurement (residual dipole moment), and the general EMC conducted/radiated
  emission and susceptibility suite.
- §6.5.5.2 separates tests into two modes. Stand-alone mode applies to every
  element: the element is powered and exercised in isolation under representative
  electrical boundary conditions. Embedded mode supplements stand-alone when
  the element is available assembled into its higher-level unit; conducted and
  radiated susceptibility are the primary candidates for embedded re-check
  because the higher-level assembly provides realistic cable harness and grounding
  that cannot be fully replicated stand-alone.
- Auto-compatibility: a finding occurs when an internal emitter frequency falls
  inside an internal receive band and the measured isolation margin is below the
  required minimum. An emitter whose frequency sits outside all internal receive
  bands requires no margin check against those bands.
- PIM: applies only to elements with RF transmission paths through passive
  components (connectors, cables, waveguides, filters, antennas). For each pair
  of carrier frequencies, odd-order intermodulation products (3rd, 5th, 7th, ...)
  are computed as m·f1 − n·f2 (and m·f2 − n·f1) where m + n equals the order.
  A product that falls within the element's receive band is a finding.
- Magnetic field: the element's residual magnetic dipole moment is measured in
  three orthogonal axes and the vector magnitude is compared against the
  element-level magnetic budget. Exceeding the budget is a finding.

## Workflow

1. Obtain the element's internal frequency plan (all emitter center frequencies
   and all receive band definitions) and the EMC requirements (isolation margin
   per emitter–receiver pair, magnetic dipole budget, PIM-free receive band).
   Reject an assessment that lacks a frequency plan or magnetic budget.
2. For auto-compatibility, iterate every emitter–receiver pair: if the emitter
   frequency lies within the receiver's band, check that the measured isolation
   margin meets or exceeds the required margin; flag any pair where it does not.
   Emitter frequencies outside all receive bands are out-of-scope for margin
   checking and are recorded as not applicable.
3. If the element carries RF paths through passive components, list every pair
   of simultaneous carrier frequencies. For each pair, compute odd-order PIM
   products up to at least the 9th order; flag any product that falls within a
   receive band.
4. Measure the element's residual magnetic dipole moment (three axes) and
   compare the vector magnitude against the budget. Record a finding if the
   budget is exceeded.
5. Assign the test mode for each test type per §6.5.5.2: stand-alone is
   mandatory for the full suite; if the element is available in its assembled
   higher-level unit, schedule conducted and radiated susceptibility re-checks
   in embedded mode as a supplement.
6. Aggregate all findings. The element is compliant for EMC when the
   auto-compatibility list, the PIM list, and the magnetic finding are all clear.

## Pitfalls

- Skipping PIM evaluation because no active mixing occurs — PIM arises from
  non-linearity in passive junctions (connector interfaces, cable ferrite
  material, oxidised contacts) and must be assessed for any element with RF
  transmission paths, regardless of whether it contains an active mixer.
- Treating the embedded-mode susceptibility re-check as optional when the
  element is available assembled — §6.5.5.2 makes the embedded supplement
  mandatory for susceptibility once the higher-level assembly exists; skipping
  it leaves the realistic harness/grounding environment unverified.
- Accepting a zero-margin auto-compatibility result as a pass — the required
  margin is a positive value set in the EMC requirements; a measured margin of
  exactly 0 dB is only acceptable if the requirement explicitly allows it.
- Omitting the magnetic measurement for elements that appear non-magnetic —
  residual ferromagnetic content in structure, connectors, and PCB materials can
  produce non-trivial dipoles; the check is mandatory for all elements in the
  §6.5.5 scope, not limited to elements with obvious magnetic components.

## Behavior contract (gate 3)

The auto-compatibility, PIM, magnetic-field, and test-mode-selection logic is
exercised by the gate 3 contract test:
scripts/test_e1003_el_emc.py against scripts/e1003_el_emc_logic.py
(stdlib unittest, offline). Run:
python3 scripts/test_e1003_el_emc.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
