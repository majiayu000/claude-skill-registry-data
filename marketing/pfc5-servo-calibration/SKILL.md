---
name: pfc5-servo-calibration
description: Design and audit PFC 5.0 wall servo, loading-rate control, equilibrium checks, micro-to-macro calibration, two-target local solves, DOE campaigns, and independent confirmation for asphalt models.
---

# PFC5 Servo And Calibration

Use this skill for compaction pressure, confining/load control, Marshall/rutting
reaction control, Burger fitting, or multi-target PFC5 calibration.

## Required Inputs

- controlled axis, actuator, sign convention, target and tolerance;
- effective stiffness estimate, timestep/update interval, velocity limits;
- active micro-parameters with units/bounds;
- macro targets, tolerances, experimental provenance and run budget;
- baseline save, seed policy and evaluator output schema.

## Workflow

1. Prove wall/axis/reaction sign with a short motion probe.
2. Estimate effective stiffness and choose a conservative dimensionless gain.
3. Clamp actuator velocity and record target, reaction, error, gain and velocity.
4. Require equilibrium/inertia checks before accepting a stage.
5. Calibrate in sequence: elastic response, strength/interface, time dependence,
   then post-peak/rutting behavior.
6. Use the two-target solver only when exactly two active levers produce a
   well-conditioned local response matrix.
7. For larger problems use DOE with real PFC5 runs; treat regression/surrogates as
   proposal tools only.
8. Confirm the final parameters on an independent seed or loading condition.

Use `scripts/servo_gain.py` for a bounded proportional step and
`scripts/dual_target_solver.py` for a guarded local 2x2 solve. Read
[calibration-contract.md](references/calibration-contract.md) before campaigns.

## Working Rules

- Do not prescribe reaction force by writing a read-only contact-force quantity.
- Do not tune more parameters than the data can identify.
- Reject near-singular local solves; do not hide them with huge parameter jumps.
- Every proposed parameter set needs a true PFC5 confirmation run.

## Output Contract

Return controller equations/signs, gain and clamp, histories, parameter/target
tables, run manifest, conditioning diagnostics, confirmation result and runtime status.

## Local Contents

- `references/calibration-contract.md` — servo and campaign gates.
- `scripts/servo_gain.py` — bounded controller-step calculator.
- `scripts/dual_target_solver.py` — conditioned two-target update.
- `agents/openai.yaml` — interface metadata.
