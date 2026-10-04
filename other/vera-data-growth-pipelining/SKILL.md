---
name: vera-data-growth-pipelining
description: >
  Complete skill family for longitudinal SEM focused on latent growth and
  change. Use when the user asks for latent growth models, latent change score
  models, nonlinear change, repeated latent trajectories, or longitudinal SEM
  in general. Uses a two-step structure: testing for initial diagnostics,
  analyzing for full pipeline.
---

# SEM Longitudinal Change — Skill Family

Open-source skill.

This domain contains:

- `vera-data-growth-reviewing` for setup checks and an initial latent growth or
  change model
- `vera-data-growth-generating` for nonlinear trajectories, multigroup
  comparisons, parallel-process extensions, and manuscript output

Primary engines: `lavaan` for linear/latent growth basics, `nlpsem` when
nonlinear longitudinal SEM is required.
