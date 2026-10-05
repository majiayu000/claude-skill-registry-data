---
name: prompt-token-optimization
description: Reduce prompt, tool, retrieval, and conversation token overhead without weakening measured task quality. Use for context-budget audits, oversized.
license: MIT
---

# Prompt and Token Optimization

Optimize measured waste, not length for its own sake.

## Baseline

Record the task, runtime, instruction/retrieval/tool/history sizes, input/output usage when exposed by the active host/API, tool-call count, compactions, latency, cost, and quality metrics. If the host exposes no token counter, use byte/word/section estimates and say they are estimates; do not invent `/cost` or `/usage` commands.

Build a representative evaluation set including normal, boundary, adversarial, and rare high-cost failures. Preserve a baseline output and behavior checklist.

## Optimization order

1. Remove exact duplicates and stale platform/model instructions.
2. Replace repeated prose with one decision table or invariant.
3. Put trigger/selection metadata in the description and detailed material behind progressive references.
4. Retrieve only relevant files/ranges; summarize evidence with pointers rather than copying entire sources.
5. Reduce tool schemas and enabled tools to those needed for the current task.
6. Move stable large examples/reference data to versioned files or caching when the runtime supports it.
7. Compress history into facts, decisions, unresolved items, and artifact paths while preserving user constraints.
8. Shorten output formatting only when it does not reduce usability or verification.

Never remove authority boundaries, security rules, acceptance criteria, uncertainty handling, or rare but severe failure checks merely because they consume tokens.

## Compare

Run baseline and candidate with the same inputs and runtime settings. Measure task success, constraint violations, factual support, schema validity, tool errors, latency, tokens/cost, and variance. Revert when savings are not statistically or practically meaningful, or when any critical behavior regresses.

## Deliverable

Report baseline/candidate measurements, removed/moved content, quality deltas, token/cost savings, limitations, rollout, and rollback. Do not change the selected provider/model or its reasoning level as a hidden token optimization.
