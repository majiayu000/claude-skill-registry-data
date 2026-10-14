---
name: e1012-sehe
description: "Use when compute the SEHE (single event housekeeping and functional interrupt) rate for a spacecraft device under ECSS-E-ST-10-12C §9.4.1.8: fit the device's measured cross-section versus LET data to a Weibull model (LET threshold, width parameter, shape exponent, saturation cross-section), integrate that curve against the mission heavy-ion LET spectrum using the trapezoidal rule to obtain the unshielded event rate, apply a shielding attenuation factor to produce the shielded rate, and verify the result meets the mission requirement under the applicable design margin. A device with no captured rate requirement but with nonzero computed rate is itself a finding. Trigger: ecss, e-st-10-system-scope, sehe, single-event-housekeeping, single-event-functional-interrupt, see-rate, weibull-fit, let-spectrum, shielding, design-margin."
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
  tags: [ecss, e-st-10-12c, e-st-10-system-scope, sehe, single-event-housekeeping, see-rate, weibull-fit, let-spectrum, shielding, design-margin]
  version: 0.1.0
  author: Aero Agent Skills
---

# ECSS Space Environment — SEHE Rate Prediction (space-systems/ecss/e1012-sehe)

Use when the task is predicting the rate of single event housekeeping and
functional interrupts (SEHE) for a spacecraft device, following the procedure
in ECSS-E-ST-10-12C §9.4.1.8 using a Weibull cross-section fit integrated
against the mission heavy-ion LET spectrum.

## Domain quick reference

- A **Single Event Housekeeping Effect (SEHE)** is a non-destructive single
  event effect that causes a spurious interrupt, mode transition, or false alarm
  in a spacecraft housekeeping or functional subsystem. Unlike a bit flip in a
  data memory, a SEHE disrupts execution flow; it is logged and the subsystem
  recovers through a reset sequence, but each event consumes ground contact
  time and may mask genuine anomalies.
- The **LET threshold (LETth)** is the minimum linear energy transfer
  (MeV·cm²/mg) at which a heavy ion can trigger a SEHE in the device. Ions with
  LET below LETth produce no SEHE events regardless of fluence.
- The **Weibull cross-section** σ(L) = σsat × (1 − exp(−((L − LETth)/W)^s))
  for L > LETth, and zero otherwise, describes how the SEHE event probability
  per unit fluence grows from zero at LETth to the saturated cross-section σsat
  as LET increases. Parameters LETth, width W, shape exponent s, and σsat are
  obtained from device-level heavy-ion characterisation tests.
- **RPP integration**: the SEHE rate is obtained by numerically integrating
  σ(L) × φ(L) over the differential heavy-ion LET spectrum φ(L)
  (ions/cm²/day per MeV·cm²/mg) at the shielded device location. The
  trapezoidal rule is applied across the spectrum points.
- **Shielding attenuation**: a shielding factor in (0, 1] scales the integrated
  rate to account for the spectral reduction provided by the device's surrounding
  mass at the mission location. A factor of 1.0 means no attenuation (used for
  worst-case bounding analyses); values below 1.0 are derived from shielding
  transport calculations at the specific location.
- **Design margin**: ECSS SEE practice requires a design margin (typically 10×)
  applied to the predicted rate before comparing against the system requirement,
  meaning the computed rate must not exceed one-tenth of the allowable rate.
  Missing a captured requirement for a device with nonzero computed rate is
  itself a finding.

## Workflow

1. Obtain the Weibull parameters for the SEHE cross-section from the device's
   heavy-ion test report: LETth (MeV·cm²/mg), W (MeV·cm²/mg), s (dimensionless
   exponent), and σsat (cm²/device). Confirm LETth > 0, W > 0, s > 0, and that
   the test data reach saturation (σ at the highest test LET ≥ 0.99 σsat).
   If the test range does not reach saturation, σsat is unconstrained — record
   this as a test-data gap and use the highest measured cross-section as a
   lower bound on σsat for a conservative estimate.

2. Obtain the differential heavy-ion LET spectrum φ(L) at the shielded device
   location for the mission duration. The spectrum must span from below LETth to
   well above the Weibull saturation region. Confirm the spectrum's maximum LET
   exceeds LETth; if it does not, the device cannot produce a SEHE in this
   environment (predicted rate is zero — record as environment-limited, not a
   device result). Verify the spectrum represents the shielded location; using
   the free-space GCR spectrum overstates the rate in most orbits.

3. Evaluate the Weibull cross-section at every LET point in the spectrum.
   Points at or below LETth contribute zero. Do not extrapolate σ above σsat.

4. Integrate σ(L) × φ(L) over LET using the trapezoidal rule. The result is
   the unshielded SEHE rate in events/device/day.

5. Apply the shielding attenuation factor (from step 2 transport analysis) to
   the unshielded rate to obtain the shielded rate.

6. Compare the shielded rate against the system SEHE requirement applying the
   design margin: the shielded rate × design margin factor must not exceed the
   allowable rate. Flag a margin violation separately from a raw rate exceedance.
   Flag any device with a nonzero shielded rate but no captured allowable rate
   as a missing-requirement finding.

7. Record all inputs (Weibull parameters, spectrum provenance, shielding factor,
   design margin factor, allowable rate) and the computed rates in the assessment
   output so the calculation is reproducible and auditable.

## Pitfalls

- Using the free-space GCR spectrum instead of the shielded spectrum at the
  actual device location — shielding suppresses low-LET ions and reduces the
  integral; the error is orbit- and shielding-thickness-dependent but can
  easily reach a factor of 2–10 for heavily shielded devices.
- Setting the cross-section to σsat for all LET bins rather than applying the
  Weibull shape — the Weibull rises steeply from zero and reaches σsat only at
  high LET; using σsat everywhere overstates the rate at every bin below
  saturation and masks the real design margin.
- Ignoring the LETth check: if the environment's maximum LET falls below LETth,
  the integral is zero by physics. Failing to record this explicitly can lead a
  reviewer to assume the integration was omitted in error.
- Applying the design margin to the allowable rate instead of the computed rate:
  the margin is a multiplier on the predicted value, not a divisor on the
  requirement. Swapping the direction of the margin check passes a device that
  actually fails by a factor equal to the square of the margin.
- Recording "compliant" when the allowable rate has not been captured — an
  absent requirement means the system-level SEHE budget has not been closed, not
  that the device passes. This finding must block acceptance.

## Behavior contract (gate 3)

The Weibull cross-section evaluation, trapezoidal LET integration, shielding
reduction, design-margin rate check, and full assessment logic are exercised by
the gate 3 contract test: scripts/test_e1012_sehe.py against
scripts/e1012_sehe_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_e1012_sehe.py

## Compliance

- ECSS standards are freely downloadable from ESA; cite the standard and clause
  as anchor only — no verbatim reproduction.
- compliance: STANDARDS-REF, gated: false.
