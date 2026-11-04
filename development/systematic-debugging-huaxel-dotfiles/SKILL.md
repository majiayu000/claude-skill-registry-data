---
name: systematic-debugging
description: Diagnose bugs, failing tests, flaky behavior, build failures, and unexplained performance regressions through reproduction, evidence, and hypothesis testing. Use when the cause is uncertain or attempted fixes keep failing. Not for routine feature development or a request limited to explaining code.
license: MIT
---

# Systematic Debugging

Find the cause before stacking fixes. Scale the investigation to the uncertainty: an obvious defect may need only a small reproduction and regression test, not a formal multi-phase report.

Adapted from Superpowers; see [source and changes](UPSTREAM.md).

## Establish the failure

Read the actual error and relevant code. Identify expected behavior, the failing revision or environment, and the smallest reliable reproduction. Run existing focused tests before modifying behavior when practical. Separate observed facts from hypotheses.

Inspect recent diffs, configuration, dependencies, and working examples. Parallel changes are expected; re-read overlapping files and coordinate rather than reverting others’ work. Do not assume a concurrent edit caused the failure without evidence.

If reproduction is intermittent, record frequency and conditions. Do not treat one successful retry as a fix.

## Trace and test

Trace the bad value or state backward to its origin. Across component boundaries, check inputs, outputs, versions, and configuration propagation with minimal instrumentation. Do not dump credentials, private payloads, or the full environment into logs.

State a specific hypothesis and the observation that would support or refute it. Make one discriminating change or experiment at a time. Compare working and failing paths; do not layer speculative fixes on top of one another.

For async or order-dependent failures, use [tracing and timing techniques](references/techniques.md).

## Fix and verify

When the cause is supported, add a focused failing test or reproducible check, apply the smallest causal fix, then rerun the reproduction and relevant checks. Keep useful regressions; remove temporary instrumentation you introduced when no longer needed.

After repeated failed hypotheses, reassess assumptions, state coupling, and the diagnostic method rather than blindly retrying. This is not proof that the architecture needs rewriting. Continue within scope; ask only for a genuine blocker, consequential ambiguity, or missing authorization.

For an external or environmental cause, distinguish a mitigation from a root-cause fix. Report the evidence, changes, checks actually run, and remaining uncertainty. A proposed experiment, skipped check, or passing mock is not proof that the real failure is resolved.
