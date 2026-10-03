---
name: llm-evaluation
description: Design and run an evaluation for an AI or agent feature using representative tasks, explicit success criteria, failure taxonomy, baselines, and reproducible evidence.
---
# LLM Evaluation

Use before relying on a model, prompt, retrieval flow, or agent behavior in a consequential product workflow.

## Procedure
1. Define the behavior being evaluated and the real user/task distribution it must serve.
2. Build representative test cases including normal, difficult, adversarial, ambiguous, and known-failure examples.
3. Define scoring criteria before running the evaluation. Prefer observable task success and structured rubrics over vibes.
4. Establish a meaningful baseline: previous prompt/model, simpler method, human result, or deterministic system where appropriate.
5. Run with fixed configuration and record model, prompt/version, tools, retrieval inputs, temperature/reasoning settings, and relevant environment.
6. Classify failures by cause: instruction following, reasoning, retrieval, tool use, format, hallucination, safety, latency, or cost.
7. Compare changes on the same evaluation set and inspect regressions, not just average score.

## Quality gate
A model change is better only when evidence shows improvement on the intended task without unacceptable regression, cost, latency, or safety tradeoffs.