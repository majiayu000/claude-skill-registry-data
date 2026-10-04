---
name: eval
description: Evaluate LLM outputs systematically — benchmarks, automated metrics, human preference, and regression tracking
triggers:
  - eval
  - evaluate
  - benchmark
  - test the model
  - measure quality
  - llm quality
  - output quality
---

# Eval

Measure before you ship. An LLM that feels better may not score better. Verify with evidence.

## Evaluation Modes

| Mode              | When to use                              | Cost         |
| ----------------- | ---------------------------------------- | ------------ |
| Automated metrics | Fast feedback during dev                 | Low          |
| LLM-as-judge      | Nuanced quality without human annotation | Medium       |
| Human preference  | Ground truth for alignment               | High         |
| Regression suite  | Pre-release gate — catch regressions     | Low (cached) |

## Automated Metrics

Use for text generation quality:

- **ROUGE-L**: recall-oriented overlap — good for summarization
- **BLEU**: precision-oriented n-gram overlap — good for translation
- **BERTScore**: semantic similarity via embeddings — better than n-gram overlap
- **Exact Match / F1**: for extractive QA (spans, named entities)
- **Pass@K**: for code generation — does any of K samples pass tests?

```text
Score threshold: ROUGE-L > 0.4, BERTScore F1 > 0.85 for production tasks
```

## LLM-as-Judge

Ask a capable model (e.g., Claude Opus) to score outputs:

```text
Rate the following response on a scale of 1–5 for:
- Correctness: is the answer factually accurate?
- Completeness: does it address all parts of the question?
- Conciseness: is it appropriately brief?

Question: <original prompt>
Response: <model output>
Reference: <expected answer>

Return JSON: {"correctness": N, "completeness": N, "conciseness": N, "reasoning": "..."}
```

Rules:

- Use a different model as judge than the one being evaluated (avoids self-serving bias)
- Always include a reference answer when available
- Run each judgment 3× and average (judges are noisy)

## Regression Suite

Build and maintain a golden dataset:

1. **Capture**: after each manual review, save `{input, expected_output, tags}` to `evals/golden.jsonl`
2. **Run**: on every PR, score all golden cases and report delta
3. **Gate**: fail PR if regression > 5% on any dimension
4. **Evolve**: add new cases for every fixed bug or edge case found

```text
eval/
├── golden.jsonl       — curated input/output pairs
├── run.ts             — eval runner (loads golden, calls model, scores)
└── report.md          — latest results (committed, not gitignored)
```

## Benchmark Suites (Public)

For capability measurement against known standards:

- **MMLU** — broad knowledge (57 subjects)
- **GSM8K** — multi-step math reasoning
- **HumanEval / MBPP** — code generation
- **TruthfulQA** — hallucination resistance
- **HellaSwag** — commonsense reasoning

Use `lm-evaluation-harness` (EleutherAI) to run standardized benchmarks.

## Steps

1. Define what "good" means — pick 2–3 dimensions that matter for your use case
2. Collect 50+ representative inputs (cover happy path, edge cases, adversarial)
3. Run baseline (current model/prompt) and record scores
4. Make your change (new prompt, model, RAG config)
5. Re-run and compare — report delta, not just absolute scores
6. Commit passing evals to golden suite; add failing cases as regression tests

## Output

```text
Eval Report
───────────
Suite:       <golden | benchmark name>
Cases:       <N total>
Dimensions:  <correctness, completeness, ...>
Baseline:    <scores>
Current:     <scores>
Delta:       <+/- per dimension>
Regressions: <list of failing cases if any>
Decision:    PASS | FAIL
```
