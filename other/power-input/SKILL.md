---
name: power-input
description: "Use when reviewing a power-input test plan, analyzing captured input-power waveforms against the equipment category, or deciding whether a transient event stays within its category envelope. Assess DO-160 Section 16 power-input characteristics of airborne equipment: verify measured AC and DC steady-state voltages against normal and emergency limits, compute voltage-sag depth and voltage-surge height as percentages of nominal, check frequency-variation tolerance for 400 Hz AC buses, and verify transient-recovery time after a sag or surge event. Trigger: DO-160, power-input, voltage-sag, voltage-surge, frequency-variation, transient-recovery, emergency-power."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-160
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: do160
  tags: [power-input, voltage-sag, voltage-surge, frequency-variation, transient-recovery, voltage-limits, steady-state-limits, emergency-power]
  version: 0.1.0
  author: Aero Agent Skills
---

# DO-160 Power Input (avionics/do160/power-input)

Use when the task is DO-160 Section 16 power input characteristics of
airborne equipment: checking steady-state AC and DC voltage limits
(normal and emergency), quantifying voltage-sag depth and voltage-surge
height as percentages of nominal, verifying frequency-variation tolerance
on AC buses, and confirming transient-recovery time after a sag or surge
event. The module is data-driven: you supply the applicable limit values
and category envelopes from the current revision, and the functions
validate inputs, compute derived quantities, and give pass-fail margins.

## Domain quick reference

- DO-160G Section 16 (power input) covers the electrical input
  characteristics of equipment connected to aircraft power: steady-state
  normal and emergency voltage limits, voltage sag and surge transients
  (assessed against the equipment category), frequency variation for AC
  buses, and recovery behavior after transients.
- Sag depth as percent of nominal: (V_nom - V_sag) / V_nom x 100.
  Worked: nominal 28.0 V, sag trough 21.0 V -> 25.0 percent.
- Surge height as percent of nominal: (V_surge - V_nom) / V_nom x 100.
  Worked: nominal 28.0 V, surge peak 32.2 V -> 15.0 percent.
- Frequency deviation: dev_hz = f_meas - f_nom, and percent of nominal.
  Worked: 412.0 Hz against 400.0 Hz -> 12.0 Hz, 3.0 percent. A 5.0
  percent tolerance band is 380.0 to 420.0 Hz: 412.0 Hz passes, 422.0 Hz
  fails.
- Steady-state limits check: 27.5 V inside [22.0, 29.0] passes with
  margins (5.5 V low, 1.5 V high); 21.0 V fails the lower edge.
- Transient envelope check (duration and depth): 80.0 ms at 20.0 percent
  depth against a 100.0 ms / 25.0 percent envelope passes with margins
  (20.0 ms, 5.0 percent). Recovery: 60.0 ms against 100.0 ms allowable
  passes.
- Ripple as percent of nominal: amplitude = (V_peak - V_min) / 2.
  Worked: 29.0 V peak, 27.0 V minimum, 28.0 V nominal -> 1.0 V amplitude
  -> 3.5714 percent.
- Emergency range classification: with normal [22.0, 29.0] and emergency
  [18.0, 32.2], a measured 20.5 V is 'emergency-only'; 27.0 V is
  'normal'; 15.0 V is 'out-of-range'.
- Typical aircraft buses: 115 VAC 400 Hz three-phase, 26 VAC, 28 VDC,
  and 270 VDC. The exact limit tables and category envelopes are
  revision-specific standard data; confirm them against the current
  revision (e.g. DO-160G) before freezing a test plan.

## Workflow

1. Identify the power bus (AC or DC, nominal voltage, nominal frequency
   for AC) and the equipment category; pull the applicable normal and
   emergency limit values from the current revision as data inputs.
2. Verify the measured steady-state voltage against the normal band with
   voltage_within_limits, and quantify headroom with limits_margins.
3. When the equipment is rated for emergency operation, classify the
   measured voltage across both bands with emergency_range_check.
4. For captured transients, compute sag depth and surge height with
   sag_depth_percent and surge_height_percent.
5. Check the transient against its category envelope with
   transient_check (duration and depth margins), then confirm recovery
   with transient_recovery_ok.
6. For AC buses, compute frequency_deviation and check
   frequency_within_tolerance against the applicable tolerance.
7. Quantify DC ripple with ripple_percent.
8. Report the pass-fail verdicts and margins; flag every limit value that
   still needs confirmation against the current revision.

## Pitfalls

- Confusing section 16 (power input) with section 20 RF susceptibility
  (do160/radio-frequency-susceptibility): both are "susceptibility"
  tests, but 16 is power-bus voltage and frequency behavior, while 20 is
  radiated and conducted RF immunity (RS103, CS114).
- Confusing this leaf with do160/environmental-qualification: that leaf
  scopes the whole DO-160 test matrix per equipment category; this leaf
  only does section 16 power-input calculations.
- Confusing this leaf with do178c/verification: coverage percentages
  there are structural software coverage (MC/DC, statement, decision),
  not voltage margins; route coverage questions to do178c/verification.
- Applying steady-state normal limits to transient events, or category
  envelopes to steady state; the two assessments use different bands.
- Mixing AC and DC conventions: frequency tolerance applies only to AC
  buses; a 28 VDC bus has no 400 Hz component to check.
- Computing sag depth against the trough value instead of nominal; the
  percent-of-nominal convention keeps sag and surge comparable.
- Forgetting that emergency-power limits are a separate, wider band
  (lower minimum) that only applies when the equipment is rated for
  emergency operation.
- Treating typical category values as fixed; DO-160 limit tables are
  revision-specific, so confirm every value against the current revision
  before freezing the test plan.

## Behavior contract (gate 3)

The logic is exercised by the gate 3 contract test:
scripts/test_power_input.py against scripts/power_input_logic.py (stdlib
unittest, offline). Run: python3 scripts/test_power_input.py

## Compliance

- Standards referenced, not reproduced: DO-160 text is proprietary
  (RTCA); summary-only per standards-map.yaml and brief 06.
- The module is data-driven: limit values and category envelopes are
  inputs, so no standard table is embedded in the code.
- compliance: STANDARDS-REF, gated: false.
