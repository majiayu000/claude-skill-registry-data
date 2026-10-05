---
name: eval-authoring
description: This skill should be used when the user mentions "llm eval", "evaluation", "promptfoo", "deepeval", "regression test", "llm judge", "golden dataset", "eval suite", "test a prompt", or wants to prove a prompt/model change improved rather than regressed behavior. It provides a standardized methodology for authoring assertion-based, LLM-as-judge, and golden-dataset eval suites that gate CI.
---

# Eval Authoring

## Purpose
Give LLM apps a repeatable way to escape "vibes-based" development, where a prompt is changed, a few outputs are eyeballed, and the change ships with no evidence it helped. An eval suite turns that into a measured, versioned, CI-gated check: every prompt or model change is scored against fixed cases, and a regression fails the build. This skill standardizes what to test, how to grade it, and how to wire it in, riding an existing framework (promptfoo, DeepEval, Ragas) when one is present, and falling back to plain unit tests plus an LLM judge when none is.

## The three grader types

| Grader | Use for | Cost / stability | Example |
|---|---|---|---|
| **Assertion** | Deterministic, checkable facts about the output | Cheap, stable, run every commit | `is-json`, `json-schema`, `contains`, `regex`, `not-contains` (banned strings), latency/cost budget |
| **LLM-as-judge** | Qualities assertions can't capture | Costs a call, needs a threshold | Faithfulness, helpfulness, tone, "answers the question", pairwise vs. baseline |
| **Golden dataset** | Regression over a curated set of real cases | Grows from production traffic | `input → expected/assert`, tagged, versioned in the repo |

Prefer assertions wherever the property is checkable, they are free and non-flaky. Reach for a judge only for genuinely subjective qualities, and always give it a pass threshold. Use the golden set to lock in behavior you've already fixed so it never regresses.

## Authoring workflow
1. **Name the contract.** For the prompt/agent under test: its inputs, the output shape it promises, and the failure modes worth catching (wrong format, missing field, hallucination, ignored instruction, unsafe content, verbosity).
2. **Collect real cases.** Pull 3–6 representative inputs from fixtures, logs, or the prompt's own examples. Never invent domain facts, a wrong "expected" answer is worse than no test.
3. **Layer the graders.** Start with assertions for everything checkable; add judge tests for the rest; seed a golden file with the cases.
4. **Set thresholds.** Every judge assertion needs a numeric pass bar. For regression gating, prefer pairwise (new output must be ≥ baseline) over an absolute score.
5. **Gate CI.** Run the suite on PRs and fail on any assertion failure or judge score below threshold/baseline. Keep model-calling tests out of the every-commit path where possible.
6. **Grow the set.** Every production failure becomes a new golden case, so the same bug can never ship twice.

## What makes a suite trustworthy
- **Deterministic where possible**: assertion tests should not call a model; run them offline against recorded or synthesized outputs so they never flake.
- **Grounded**: every expected value traces to a real fixture or the prompt's own contract, cited by `file:line`.
- **Thresholded**: a judge test with no failing score is documentation, not a gate.
- **Baseline-aware**: regression gates compare against the current-production prompt, not an absolute ideal.
- **Tagged**: cases carry tags (feature, risk, source) so a subset can gate a fast path and the full set runs nightly.

## Additional Resources
### Reference Files
- **`references/eval-frameworks.md`**: promptfoo `promptfooconfig.yaml` and DeepEval scaffolds, the full assertion-type catalog, a provider-agnostic Vitest/pytest + LLM-judge pattern for when neither framework is present, and a GitHub Actions job that fails a PR on regression.
- **`references/llm-judge-rubrics.md`**: how to write reliable LLM-as-judge rubrics: criteria design, scoring scales, pointwise vs. pairwise, and the bias mitigations (position, verbosity, self-preference) that keep judge scores honest.
