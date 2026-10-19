---
name: build-agent-evals
description: Build or improve an agent evaluation program with versioned datasets, evaluators, and release gates. Use when creating datasets, cases, evaluators, trajectory checks, durable-execution failure scenarios, regression suites, multi-run measurements, release gates, online evaluations, or quality-cost-latency scorecards.
---

# Build Agent Evals

Convert product claims and operational risks into reproducible evidence and release gates.

## Workflow

1. Extract testable claims from the Agent Spec. Include quality, safety, tool use, latency, cost, escalation, and recovery claims.
2. Separate hard invariants from graded quality. A policy violation must not be averaged away by a high mean score.
3. Build a dataset with happy paths, boundaries, adversarial inputs, historical regressions, tool failures, permission denials, and durable-execution cases.
4. Attach stable case IDs, provenance, risk tags, capability tags, expected invariants, and dataset version.
5. Prefer evaluators in this order:
   - deterministic assertions;
   - structured-output checks;
   - tool and trajectory checks;
   - task-specific graders;
   - model-based judges for qualities that cannot be measured directly.
6. Test the full execution path when it matters, including tool results and durable-execution recovery behavior, not only the final answer.
7. Repeat stochastic cases and report pass rate, variance, and confidence—not one lucky run.
8. Track quality beside latency, tokens, tool calls, retries, and estimated cost.
9. Run evals and release checks through the project's own validation tooling or CI so provenance is normalized and gates fail closed; treat that output as release evidence.
10. Establish a trusted baseline and fail CI on hard-gate violations or material regressions beyond an explicit tolerance.
11. Sample production traces into reviewed datasets while redacting sensitive data and separating monitoring from release evidence.

## Required Output

Produce versioned eval datasets, evaluator code, a runnable entry point, a machine-readable report, human-readable failure summaries, and documented release thresholds.

Read [the eval standard](references/standard.md) before choosing metrics. Use [the examples](references/examples.md) for case design, evaluator selection, and release gates.

## Guardrails

- Do not use only happy-path examples.
- Do not rely solely on a model judge.
- Do not edit expected results merely to make a failing change pass.
- Do not compare model variants without controlling prompts, tools, datasets, and run counts.
- Do not log sensitive production content into eval datasets without a review and retention policy.

## Completion Check

Confirm that failures identify the case, violated claim, evaluator, execution trace, model and prompt versions, cost, latency, and whether the failure blocks release.
