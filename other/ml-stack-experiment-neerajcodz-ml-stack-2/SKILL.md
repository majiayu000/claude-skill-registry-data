---
name: ml-stack-experiment
description: Plan or review an isolated ML experiment when a user asks to test a hypothesis, compare runs, tune one variable, reproduce a result, or lock validation; prevent self-promotion and preserve reproducible evidence.
---

# Isolated experiments

Require a hypothesis, declared baseline, one main variable by default, immutable validation revision, seeds/folds/slices, resource and environment constraints, budget, stop rules, and artifact destination.

## Workflow

1. Capture or verify requirements with `ml_stack.capture_requirements`; reject a run whose requirements are unlocked.
2. Define baseline, variable, controls, randomization, folds/slices, metrics, and eligibility before execution.
3. Create a run directory and record code/data/model/environment revisions, resource use, seeds, logs, and artifact hashes.
4. Compare only runs with compatible validation and provenance; investigate NaN, divergence, stalls, and budget overruns.
5. Hand results to `ml-stack-evaluation` and independent `ml-stack-audit`; never promote the experiment's own result.

## Boundary and outputs

Do not change validation data, tune on held-out results, delete evidence, or claim a remote job ran. If execution is unavailable, emit a bounded run specification and comparison schema. Return hypothesis, baseline, immutable inputs, measured metrics, uncertainty, artifacts, and eligibility decision. Next owner: `ml-stack-evaluation` for quality gates or `ml-stack-audit` for independent release review.

See [hypothesis and baseline](references/hypothesis-and-baseline.md), [validation protocol](references/validation-protocol.md), [reproducibility](references/reproducibility.md), and [result comparison](references/result-comparison.md).
