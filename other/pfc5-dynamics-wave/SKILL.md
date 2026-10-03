---
name: pfc5-dynamics-wave
description: Design and audit PFC 5.0 asphalt dynamic loading and stress-wave studies with damping, timestep, rate, dispersion, source direction, boundary reflection, histories, and wheel-load handoff checks.
---

# PFC5 Dynamics And Stress Waves

Use this skill for inertial wheel loading, vibration, impact, waveform sources,
wave-speed checks, or sensor arrival-time studies in a PFC5 asphalt model.

## Required Inputs

- PFC2D/PFC3D 5.0 and dynamic capability;
- loading/source type, direction, amplitude, frequency and duration;
- particle spacing/diameter and expected wave speed;
- damping, timestep, boundaries and sensor coordinates;
- required histories and acceptance tolerances.

## Workflow

1. Solve and save the static preparation state.
2. Check direction against model dimension.
3. Check wavelength-to-spacing and timestep/samples-per-period with
   `scripts/check_dynamic_resolution.py`.
4. Declare damping changes and reset the loading-time origin. If energy output is
   required, enable PFC5 mechanical energy tracking before the measured interval;
   energy accumulation is off by default.
5. Test the source and one sensor before the full domain.
6. Compare free/rigid/absorbing boundary response as required.
7. Export input, time, timestep, energy, velocity/displacement and sensor signals.
8. Run resolution, timestep, damping and boundary sensitivity.

Read [dynamic-contract.md](references/dynamic-contract.md) for acceptance checks.

## Working Rules

- Do not use preparation damping or calm operations during a physical response without justification.
- `calm` zeroes unfixed linear and angular velocities; using it inside the measured
  response changes the physics rather than merely improving convergence.
- Do not use density scaling for wave-speed validation.
- A moving-wheel surrogate is accepted only after comparison with the intended kinematics.
- Cross-correlation/localization is offline analysis; sensor geometry degeneracy must be reported.

## Output Contract

Return source/loading definition, resolution report, timestep/damping/boundary
assumptions, sensor layout, histories, sensitivity results and runtime status.

## Local Contents

- `references/dynamic-contract.md` — dynamic and wave acceptance gates.
- `scripts/check_dynamic_resolution.py` — wavelength/direction/timestep checker.
- `agents/openai.yaml` — interface metadata.
