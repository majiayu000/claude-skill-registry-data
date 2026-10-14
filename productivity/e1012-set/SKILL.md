---
name: e1012-set
description: "Use when compute Single Event Transient (SET) rates for a spacecraft device population under ECSS-E-ST-10C §9.4.1.7: identify each sensitive device and its cross-section model (Weibull for heavy ions, threshold/saturation for protons, effective cross-section for neutrons), integrate each cross-section against the mission particle environment (heavy-ion LET spectrum, proton energy spectrum, ambient neutron flux) to derive per-device rates for all three particle families, sum the three contributions to obtain a total SET rate per device per day, and compare that rate against each device's system-level SET rate budget to flag exceedances. Trigger: ecss, e-st-10-system-scope, set, single-event-transient, heavy-ion, proton, neutron, let-spectrum, weibull, transient-rate."
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
  tags: [ecss, e-st-10-system-scope, set, single-event-transient, heavy-ion, proton, neutron, let-spectrum, weibull, transient-rate]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Space Environment — Single Event Transients (space-systems/ecss/e1012-set)

Use when the task is computing Single Event Transient (SET) rates for spacecraft
electronics under ECSS-E-ST-10C §9.4.1.7 — integrating device cross-section
models against the mission heavy-ion, proton, and neutron environments and checking
each device's total SET rate against its system-level budget.

## Domain quick reference

- An SET is a radiation-induced transient voltage or current pulse in a circuit,
  caused by the passage of a single ionizing particle (heavy ion, proton) or a
  nuclear reaction product from neutron/proton spallation. Unlike a Single Event
  Upset (SEU), an SET does not alter a storage element — it propagates as a glitch
  through combinational logic or an analog circuit until it is captured or
  dissipates. Sensitive device types include analog ICs, clock buffers, ADCs,
  comparators, and fast logic.
- Heavy-ion SET rates are computed by integrating the device's cross-section
  versus LET curve over the mission differential LET spectrum. The cross-section
  is typically fit with a four-parameter Weibull function: LET threshold L_th
  (MeV·cm²/mg), saturation cross-section σ_sat (cm²/device), width W
  (MeV·cm²/mg), and shape exponent s (dimensionless). Below L_th the
  cross-section is zero; above L_th it rises to σ_sat following the Weibull
  shape.
- Proton SETs arise when energetic protons or their nuclear reaction products
  deposit sufficient charge. The cross-section is modeled as a threshold/step
  function: zero below an energy threshold E_th (MeV) and equal to σ_sat above
  it. A more detailed Weibull proton model may be substituted when device
  characterization data warrant it.
- Neutrons do not ionize directly; they produce SET-causing charge via elastic
  nuclear recoils and spallation fragments. The rate is approximated as the
  total neutron flux (particles/cm²/s) multiplied by an effective cross-section
  (cm²/device).
- The total SET rate is the sum of heavy-ion, proton, and neutron contributions,
  expressed in events/device/day. Each sensitive device must have a system-derived
  allowable SET rate budget; any exceedance is a compliance finding. A device with
  no budget on record is also a finding — an absent budget means the system
  requirement was never captured, not that no limit applies.

## Workflow

1. Inventory every sensitive device in scope (analog ICs, logic gates, clock
   buffers, ADCs, comparators). For each device, record its cross-section model
   parameters: Weibull (L_th, σ_sat, W, s) for heavy ions; threshold energy
   E_th and σ_sat for protons; effective cross-section σ_n for neutrons. Reject
   a device record that is missing any required parameter before it enters the
   rate calculation.
2. Obtain the mission particle environment for the target orbit: the differential
   heavy-ion LET spectrum in particles/(cm²·s·MeV·cm²/mg), the differential
   proton energy spectrum in particles/(cm²·s·MeV), and the total neutron flux
   in particles/(cm²·s). Verify all flux values are non-negative; a negative
   flux is a data error, not a conservative choice.
3. Compute the heavy-ion SET rate for each device: evaluate the Weibull
   cross-section σ(LET) at each spectral LET point, then integrate
   σ(LET) × φ(LET) over the full LET range using the trapezoidal rule. Multiply
   by 86 400 s/day to convert to events/device/day.
4. Compute the proton SET rate for each device: apply the threshold cross-section
   model (σ = σ_sat for E ≥ E_th, else 0), integrate σ(E) × φ(E) over the
   proton energy spectrum with the trapezoidal rule, and convert to
   events/device/day.
5. Compute the neutron SET rate for each device as:
   R_n = σ_n × Φ_n × 86 400 (events/device/day),
   where Φ_n is the total neutron flux in particles/(cm²·s).
6. Sum the three contributions to the total SET rate per device. Compare each
   total against the device's allowable SET rate budget. Flag every exceedance
   as a compliance finding. Separately flag every device for which no budget is
   on record as a requirement-capture gap.

## Pitfalls

- Substituting the saturation cross-section σ_sat for the full Weibull curve
  and integrating the entire spectrum at that constant value — the Weibull
  roll-on suppresses σ sharply near L_th and the step-function approximation
  overpredicts risk for spectra that are LET-soft (heavy on low-LET particles).
- Omitting the neutron contribution for orbits with significant trapped or
  secondary neutron flux (e.g. low-altitude equatorial) — the neutron rate
  can be comparable to the proton rate for devices with low effective
  cross-section thresholds.
- Reading a missing budget as zero exceedance — an absent budget means the
  system requirement was never captured, which is itself a compliance finding,
  not a pass.
- Summing contributions that were integrated over different mission durations
  without normalizing — reduce all three to a common per-day basis before
  adding them.
- Applying the proton model to energies below the device's nuclear reaction
  threshold without zeroing the cross-section — direct ionization by protons
  is negligible below ~10–30 MeV for most devices and the threshold model must
  drop to zero in that regime.

## Behavior contract (gate 3)

The Weibull cross-section evaluation, heavy-ion trapezoidal integration, proton
threshold integration, neutron rate formula, total rate summation, and budget
compliance check logic is exercised by the gate 3 contract test:
scripts/test_e1012_set.py against scripts/e1012_set_logic.py (stdlib unittest,
offline). Run:
python3 scripts/test_e1012_set.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and paraphrase
  per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
