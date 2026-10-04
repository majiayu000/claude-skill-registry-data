---
name: rseng-numerical-accuracy
description: >-
  Covers floating-point correctness in research code: why 0.1 + 0.2 != 0.3,
  choosing absolute vs relative tolerances in tests, accumulation error and
  safe summation, precision choices (float32 vs float64), catastrophic
  cancellation, NaN and infinity handling, and cross-platform or cross-library
  result drift. Use PROACTIVELY when floating-point comparisons fail
  mysteriously, when writing numerical tests or choosing tolerances, when
  results differ across machines, compilers, BLAS builds or library versions,
  or when precision or numerical stability questions arise in analysis or
  simulation code.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Numerical accuracy in research code

Floating-point numbers are approximations with well-defined rules,
and research conclusions can hinge on respecting them. The two
recurring failures: treating floats as exact (== comparisons,
accumulating error blindly) and treating all differences as noise
(tolerances loosened until tests pass). Both are avoidable with a
small set of habits - and both matter more in research than
elsewhere, because the numbers ARE the result.

## The ground rules

- Never compare floats with == (except against an exactly
  representable sentinel like 0.0 you assigned yourself). Use
  tolerance-based comparison: `math.isclose`, `numpy.isclose`, or
  the testing helpers below.
- Decimal literals are usually not representable: 0.1 is stored as
  the nearest binary fraction, which is why 0.1 + 0.2 != 0.3.
  Format-rounding for display hides this; arithmetic does not.
- NaN propagates and never equals anything, including itself; test
  with isnan, and decide explicitly whether NaN in data means
  missing, invalid or bug (rseng-data-management's missing-data
  discipline). Silent NaN propagation into published numbers is the
  classic silent failure.
- Precision-degrading operations (subtracting nearly equal numbers -
  catastrophic cancellation; summing numbers of very different
  magnitude) lose precision structurally; restructure the formula
  (e.g. use expm1/log1p, two-pass variance algorithms) rather than
  adding digits.

## Tolerances: choose, do not tune

- Relative tolerance compares magnitudes ("within 1e-9 of each
  other, proportionally") - right for values far from zero.
  Absolute tolerance is required near zero, where relative
  comparison degenerates. Robust comparisons combine both
  (numpy.testing.assert_allclose(rtol=, atol=)).
- Derive tolerances from the problem: input data precision,
  algorithm order, condition number of the operation - and record
  the justification in a comment or the test name. A tolerance
  someone loosened until CI passed documents nothing and hides
  regressions (rseng-testing).
- Scientific sign-off: when a characterization or migration test
  needs a tolerance decision (rseng-legacy-code), make it with the
  domain expert - it is a statement about the science, not the code.

## Precision and reproducibility across platforms

- float64 is the scientific default; float32 halves memory and can
  double throughput (and is common on GPUs - rseng-gpu-computing) but
  carries ~7 decimal digits: justify it per-array, not globally.
  Mixed precision is an optimization to apply deliberately
  (rseng-performance-profiling).
- Bit-identical results across machines are NOT promised by
  IEEE-conformant code: compiler flags, SIMD width, BLAS
  implementation, thread count and reduction order all legitimately
  change last bits. Cross-platform tests therefore assert within
  tolerances, never bitwise (a policy mature projects like the
  astronomy stack encode in their contribution rules).
- What IS controllable: pin library versions
  (rseng-reproducible-environments), fix seeds for stochastic parts,
  avoid fast-math-style flags for result-bearing code, and document
  the platform in published results (rseng-publishing-releasing).
- Parallel reductions reorder sums; if run-to-run variation appears
  under threading, that is why - use deterministic-reduction options
  where offered, or widen tolerances knowingly.

## Accumulation and safe patterns

- Long naive sums accumulate error linearly; library sums (numpy)
  use pairwise summation - prefer them over hand loops. Kahan
  compensated summation is available when a manual loop is
  unavoidable and precision matters.
- Prefer numerically stable library routines (lstsq over normal
  equations, logsumexp over exp-sum-log) - the stable formulation is
  usually one function call away.
- Validate against known solutions: analytic cases, conservation
  laws and invariants make the best numerical tests because their
  expected error is reasoned, not guessed.

## Working with this skill

This skill is source-independent: it encodes IEEE-754 floating-point
practice as applied in scientific computing.

Learn more (verified):
  - https://floating-point-gui.de - the floating-point guide
  - https://numpy.org/doc/stable/reference/routines.testing.html -
    NumPy testing helpers (assert_allclose and friends)
  - https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html -
    Goldberg, What Every Computer Scientist Should Know About
    Floating-Point Arithmetic

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-debugging - diagnosing cross-platform result differences
- rseng-gpu-computing - float32 and mixed precision trade-offs
- rseng-legacy-code - characterization-test tolerance sign-off
- rseng-performance-profiling - precision changes as deliberate optimization
- rseng-reproducible-environments - pinned libraries limit result drift
- rseng-testing - tolerance-based numerical test design

<!-- related-skills:end -->
