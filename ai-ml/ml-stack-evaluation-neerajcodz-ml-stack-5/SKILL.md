---
name: ml-stack-evaluation
description: Evaluate ML models or systems when a user asks for benchmarks, metrics, slices, calibration, robustness, LLM evaluation, smoke tests, pass/fail thresholds, or go/no-go decisions; preserve revisions and uncertainty.
---

# Evaluation

Require task contract, candidate model revision, benchmark or acceptance set, backend, thresholds, data license, compute budget, and evaluation environment.

## Workflow

1. Select task, benchmark, backend, metrics, slices, and leakage controls; pin model, dataset, code, and environment revisions.
2. Run a small smoke stage before scale, validate output schema, then execute the approved matrix.
3. Report aggregate and slice metrics, calibration/robustness, uncertainty, failures, missing values, and cost/latency.
4. For `inspect-ai`/`lighteval`-style LLM backends, produce an executable evaluation plan unless an equivalent registry operation exists; do not claim execution.
5. Return pass/fail thresholds and a go/no-go recommendation to `ml-stack-deployment` or `ml-stack-audit`.

## Boundary and outputs

Never tune on the acceptance set, hide failed slices, or publish results without approval. Abstain when benchmark provenance, model revision, threshold, or uncertainty is missing. Next owner: `ml-stack-deployment` for a gated release, `ml-stack-experiment` for a controlled follow-up, or `ml-stack-audit` for independent reconciliation.

See [benchmark matrix](references/benchmark-matrix.md), [smoke to scale](references/smoke-to-scale.md), [metrics and slices](references/metrics-and-slices.md), [robustness](references/robustness.md), and [evaluation report](references/evaluation-report.md).
