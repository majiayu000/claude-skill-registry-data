---
name: rag-experiment
description: Run one controlled RAG experiment (chunking, embeddings, top-k, rerank, threshold, prompt or LLM) and save config, raw results, metrics and run IDs. Use when testing a hypothesis from docs/RESEARCH_PLAN.md.
---

# rag-experiment

## Inputs
Hypothesis, baseline config, the single factor to change, dataset version and split (dev by default).

## Steps
1. Write the hypothesis and metric before running. One factor per comparison; same context budget.
2. Freeze: git SHA (clean tree), corpus SHA, dataset version, model IDs, prompt version.
3. Smoke 2–3 questions first to check quota and provider; stop on repeated 429.
4. Retrieval-only metrics first (Recall@K, Hit@K, MRR), then generation for candidates.
5. Save `lab1/experiments/runs/<run_id>/{config.yaml,raw.jsonl,metrics.json,meta.json}`,
   including failed requests, latency, token usage, Langfuse trace IDs.
6. The final test split is used only after a configuration is chosen on dev (`--final`).

## Outputs
Run directory, a results table generated from raw files, conclusion with limitations.

## Boundaries
No invented numbers. No silent model fallback. Small dataset ≠ proof of general superiority.
