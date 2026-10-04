---
name: vera-data-cfa-pipelining
description: >
  Complete skill family for confirmatory factor analysis (CFA) and measurement
  model evaluation. Use when the user asks for CFA, latent factor validation,
  measurement models, factor loadings, convergent/discriminant validity, or
  measurement invariance. Uses a two-step structure: testing for initial diagnostics,
  analyzing for full pipeline.
---

# SEM CFA — Skill Family

Open-source skill.

This domain contains:

- `vera-data-cfa-reviewing` for identification checks, estimator selection, and an
  initial CFA fit with interpreted fit indices and standardized loadings
- `vera-data-cfa-generating` for reliability/validity, invariance, model
  comparison, and manuscript-ready methods/results

Primary engine: `lavaan` in R. Secondary Python support may use `semopy`, but
R is the default path whenever full SEM features are needed.
