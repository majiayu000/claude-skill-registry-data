---
name: write-eval-suite
description: Use when building a test suite to evaluate LLM model performance, prompt quality, or AI system behavior
source: OpenAI Evals framework (github.com/openai/evals); HELM benchmark — Liang et al., Stanford CRFM (2022); BIG-bench (Google Brain, 2022)
tags: [llm, evals, benchmarking, ai-quality, testing, helm, openai-evals]
verified: true
---

# Write Eval Suite

Build a structured evaluation suite that measures LLM or AI system performance with reproducible, comparable metrics.

## Why This Is Best Practice

**Adopted by:** OpenAI (public Evals framework), Stanford (HELM — Holistic Evaluation of Language Models), EleutherAI (LM Evaluation Harness)
**Impact:** HELM evaluates 30+ models across 42 scenarios and 7 metric categories; OpenAI uses community evals to discover model regressions before release — systematic evals caught GPT-4 Turbo regressions not visible to internal red-teaming.

**Why best:** Evals are to AI systems what unit tests are to software: they make quality measurable, regressions detectable, and improvements verifiable. Without them, "the model got better" is a belief, not a fact. A good eval suite is the single most durable investment in a production AI system.

## Steps

1. **Classify eval types needed** — Functional correctness (does the model give the right answer?), Behavioral (does it follow instructions?), Safety (does it refuse appropriately?), Comparative (is v2 better than v1?), Regression (did a change break anything?).
2. **Define the task format** — Choose: exact match (classification, extraction), model-graded (quality assessment by LLM-as-judge), human-graded (for subjective tasks), or execution-based (code evals that run the output).
3. **Build the dataset** — Curate minimum 100 examples per eval category; include: easy cases (baseline), hard cases (capability ceiling), edge cases (known failure modes), and adversarial cases. Label ground truth carefully — bad labels produce misleading scores.
4. **Write the eval harness** — Use OpenAI Evals format, `lm-evaluation-harness`, or a custom runner. Each eval: input → model call → output → scoring function → metric aggregation.
5. **Define scoring functions** — Exact match: `output.strip() == expected`. Model-graded: structured prompt asking judge model to rate 1-5 with reasoning. Code eval: execute output, check return value or stdout.
6. **Establish baseline and targets** — Run the eval against the current production model; record baseline scores. Define target scores for the next model version or prompt change.
7. **Integrate into CI/CD** — Run eval suite on every model or prompt change; fail the deployment if regression exceeds threshold (e.g., >3% drop in primary metric).

## Rules

- Eval datasets must not overlap with any training data — contamination invalidates scores.
- Always version your eval datasets — a changing eval set makes historical comparisons invalid.
- Include negative examples (what the model should refuse or decline) as first-class eval cases.
- Report confidence intervals alongside mean scores — small datasets produce noisy estimates.

## Examples

Eval structure (OpenAI Evals format):
```jsonl
{"input": [{"role": "user", "content": "Summarize: [article]"}], "ideal": "The article discusses..."}
{"input": [{"role": "user", "content": "Extract the date from: [text]"}], "ideal": "2026-03-15"}
```

Scoring pipeline:
```python
for example in eval_dataset:
    output = model.complete(example["input"])
    score = judge_model.grade(output, example["ideal"])
    metrics.record(score)
print(f"Mean score: {metrics.mean():.3f} ± {metrics.ci():.3f}")
```

## Common Mistakes

- **Too few examples** — 10-20 examples produce noisy, unreliable scores; minimum 100 per category for meaningful signal.
- **Only testing happy-path inputs** — evals that only include well-formed, unambiguous inputs miss the edge cases where models fail.
- **No versioning of eval dataset** — adding examples to the eval set mid-comparison makes before/after scores incomparable.
