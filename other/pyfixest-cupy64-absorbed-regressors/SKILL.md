---
name: pyfixest-cupy64-absorbed-regressors
description: |
  pyfixest demeaner_backend="cupy64" (including its CPU fallback when cupy is
  absent) is NOT numerically identical to the default numba backend and does
  NOT drop fully-absorbed/collinear regressors the same way. Use when: (1)
  adding demeaner_backend="cupy64" to existing pf.feols/fepois calls changes
  the printed coefficient table, (2) a regression report suddenly gains rows
  with absurd estimates (e.g. coef 435.8, SE 7106) for controls absorbed by
  the fixed effects, (3) diffing outputs before/after a backend change, or
  (4) anything parses a pyfixest text report by line position.
author: Claude Code
version: 1.0.0
date: 2026-07-18
---

# pyfixest cupy64 backend: absorbed regressors survive, reports change shape

## Problem
Adding `demeaner_backend="cupy64"` to an existing `pf.feols()` call is treated
as a pure performance switch, but it changes the output: regressors with zero
within-FE identifying variation (fully absorbed by the fixed effects) that the
default numba backend silently drops are RETAINED by the cupy64 path (also in
its scipy/CPU fallback when cupy is not installed). They appear in the
coefficient table as non-identified garbage (huge coefficient, huge SE).

## Context / Trigger Conditions
Observed 2026-07-18 (Specialist Directors US, H5 re-baseline audit): adding
the kwarg to 4 feols sites left the headline triple stable to 4 decimals
(B1 diff 1.45e-6, SE diff 9.9e-6) but the text report grew from 366 to 390
lines — 24 new rows for absorbed controls (e.g. `event_x_lrisk = 435.8059`,
SE `7106.3365`) under firm-year + director FE, where firm-year-level
variables have no identifying variation.

## Solution
1. Treat a backend change as a POTENTIALLY OUTPUT-CHANGING edit: diff the
   report and expect schema changes, not byte equality. Verify the
   coefficients of interest at ~4-decimal precision instead.
2. Never interpret retained absorbed-regressor rows as estimates; check
   within-FE variation before reading nuisance coefficients.
3. Never parse pyfixest text reports by line position; anchor on the
   variable name of the coefficient you need.
4. When byte-stable reports matter (regression-tested pipelines), pin the
   backend consistently everywhere rather than mixing backends across runs.

## Verification
Re-run one model with and without the kwarg; compare: headline coef equal to
~1e-6, coefficient-row sets DIFFERENT (absorbed regressors present only under
cupy64). That asymmetry confirms this behavior rather than a data change.

## Notes
- Applies even with no GPU: the fail-open CPU fallback shows the same
  retention behavior, so "cupy isn't installed" does not make the kwarg inert.
- The headline inference (identified coefficients, clustered SEs) agrees to
  reporting precision; this is a report-shape/nuisance-row issue, not a
  correctness issue for identified estimates.
