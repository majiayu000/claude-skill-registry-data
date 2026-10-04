---
name: resilient-llm-benchmark
description: Design and run recoverable large-scale LLM benchmark jobs with checkpointing, append-only results, retry/backoff, model switching, sharding, status manifests, logs, and cost boundaries. Use for multi-model or multi-profile evaluation runs that may fail, resume, or feed paper results.
---

# Resilient LLM Benchmark

Use this skill when an evaluation is too large or expensive to treat as a one-shot script.

## Workflow

1. Define the evaluation matrix:
   - dataset/profile ids;
   - models;
   - modes/baselines/ablations;
   - metrics and acceptance thresholds;
   - simulator/evaluator model boundaries.
2. Choose a stable resume key such as `(model, profile_id, mode, seed)`.
3. Write results append-only. On startup, load existing rows and skip completed keys.
4. Write a manifest and status file before and during execution.
5. Use bounded retries:
   - retry rate limits and transient connection errors with exponential backoff;
   - mark invalid input or deterministic evaluator failures separately;
   - log enough context to reproduce failed rows.
6. Shard large runs by model, profile range, or provider lane.
7. Summarize results only after completeness checks pass.

## Guardrails

- Do not switch the simulator/evaluator model unless the experiment definition explicitly says so.
- Do not overwrite partial results when resuming.
- Do not hide failed rows in aggregate metrics.
- Do not claim model-agnostic results unless all intended model lanes completed or the partial scope is clearly stated.
- Keep API keys out of manifests and logs.

## Useful Resources

- Read `references/benchmark-checklist.html` before implementing a new runner.
- Use `assets/experiment-manifest.html` as a run-manifest starter.
