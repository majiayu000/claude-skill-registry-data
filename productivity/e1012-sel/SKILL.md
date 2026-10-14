---
name: e1012-sel
description: "Use when compute heavy-ion and proton/neutron single-event latch-up (SEL) and single-event snapback (SESB) rates for a spacecraft electronic device under ECSS-E-ST-10-12C §9.4.1.4–9.4.1.5: fit a Weibull cross-section curve to heavy-ion test data, integrate it against the mission LET spectrum, apply the Bendel two-parameter model to proton cross-section data and integrate over the proton energy spectrum, sum both contributions into a combined rate, and categorize the result as acceptable, monitor, or critical against per-device thresholds. Trigger: ecss, e-st-10-system-scope, sel, sesb, single-event-latch-up, single-event-snapback, heavy-ion, proton, let-spectrum, weibull, bendel."
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
  tags: [ecss, e-st-10-system-scope, sel, sesb, single-event-latch-up, single-event-snapback, heavy-ion, proton, let-spectrum, weibull, bendel]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Space Environment — SEL/SESB Rate Prediction (space-systems/ecss/e1012-sel)

Use when the task is predicting the single-event latch-up (SEL) or
single-event snapback (SESB) rate for a spacecraft electronic device
per ECSS-E-ST-10-12C §9.4.1.4–9.4.1.5 — fitting measured cross-section
data, integrating over the mission particle environment, and categorizing
the combined rate against acceptance thresholds.

## Domain quick reference

- SEL (Single-Event Latch-up): a high-current state triggered in a CMOS
  device when a heavy ion or high-energy proton/neutron deposits sufficient
  charge in the parasitic thyristor structure to switch it on. Left
  unmitigated it can destroy the device. It is characterised by a
  threshold LET (heavy-ion path) or threshold proton energy (proton path)
  below which the event cannot occur.
- SESB (Single-Event Snapback): an analogous high-current state in
  n-channel MOSFETs triggered by impact ionisation; treated with the
  same rate methodology as SEL.
- Heavy-ion cross-section vs LET is modelled by a Weibull curve:
  σ(L) = σ_sat × (1 − exp(−((L − L_th)/W)^s)) for L > L_th, else 0.
  Parameters (L_th, σ_sat, W, s) come from measured heavy-ion test data
  (e.g. a Brookhaven or GSI heavy-ion facility run).
- Proton/neutron cross-section vs energy is modelled by the Bendel
  two-parameter formula: σ(E) = B × (1 − exp(−0.18 × (18/A)^0.5 × (E−A)))^4
  for E > A, else 0. Parameter A is the threshold energy (MeV) and B is
  the asymptotic cross-section (cm²/device).
- The mission rate for each particle type is the integral of
  (cross-section × differential particle flux) over the relevant variable
  (LET or energy), computed numerically via the trapezoidal rule over the
  environment spectrum supplied by the ECSS-E-ST-10-04 environment model.
- Thresholds for rate categorization (per §9.4.1.5):
  - acceptable: combined rate < 1×10⁻⁷ events/device/day
  - monitor:    1×10⁻⁷ ≤ rate < 1×10⁻⁵ events/device/day
  - critical:   rate ≥ 1×10⁻⁵ events/device/day (latch-up protection required)

## Workflow

1. Obtain heavy-ion test data for the device and fit a Weibull curve
   (four parameters: L_th, σ_sat, W, s) to the measured cross-section vs
   LET points. If only a single-parameter fit is available, derive the
   remaining Weibull parameters from the given effective fluence test data.
   Reject any device for which no heavy-ion characterisation data exist.
2. Obtain the mission differential LET spectrum (particles/(cm²·day·
   (MeV·cm²/mg))) from the approved environment model for the orbit and
   solar condition. Integrate the Weibull cross-section over this spectrum
   using the trapezoidal rule to obtain the heavy-ion SEL/SESB rate
   (events/device/day).
3. Obtain Bendel parameters (A, B) for the device from proton test data
   or the literature. Obtain the mission differential proton energy
   spectrum (particles/(cm²·day·MeV)) from the same environment model.
   Integrate the Bendel cross-section over this spectrum to obtain the
   proton/neutron SEL/SESB rate.
4. Sum the heavy-ion and proton rates into a combined rate.
5. Categorize the combined rate: acceptable / monitor / critical per the
   thresholds in the domain quick reference. Flag any device in the
   monitor or critical band; a critical result mandates latch-up current
   limiting and power-cycle recovery circuitry.
6. Check dominance: if one particle type contributes more than 10× the
   other, flag it for review — spectrum coverage or model applicability
   may need re-examination before closing the assessment.

## Pitfalls

- Using a single-point saturation cross-section without fitting the full
  Weibull curve: this overestimates the rate at LET values just above the
  threshold (where the cross-section is still rising) and can give a
  pessimistic result that invalidates an otherwise acceptable device.
- Treating the Bendel model as universally applicable to every CMOS
  technology: the model was derived for bipolar devices; for advanced CMOS
  nodes the direct ionisation path from proton recoils may dominate, and
  the cross-section must then be measured rather than inferred.
- Summing heavy-ion and proton rates without checking which environment
  model was used for each: LET spectra and proton spectra must come from
  the same orbit epoch and shielding assumption, otherwise the combined
  rate mixes inconsistent environments.
- Interpreting a zero computed rate as automatically acceptable: a zero
  result usually means the spectrum did not extend above the device
  threshold; verify that the spectrum spans the full relevant LET or
  energy range before concluding the device is safe.

## Behavior contract (gate 3)

The Weibull cross-section fit, Bendel proton model, trapezoidal rate
integration, severity categorization, and combined assessment logic are
exercised by the gate 3 contract test:
  scripts/test_e1012_sel.py  against  scripts/e1012_sel_logic.py
(stdlib unittest, offline). Run:
  python3 scripts/test_e1012_sel.py

## Compliance

- ECSS standards are freely downloadable (ESA); cite the source and
  paraphrase per standards-map.yaml.
- compliance: STANDARDS-REF, gated: false.
