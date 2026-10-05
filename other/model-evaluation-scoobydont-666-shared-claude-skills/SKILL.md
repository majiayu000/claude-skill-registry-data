---
name: model-evaluation
description: >
  LLM evaluation methodology — side-by-side comparison, domain-specific benchmarking,
  regression detection for fine-tuned models. Trigger on: "evaluate model", "benchmark",
  "model comparison", "A/B test models", "model quality", "accuracy test",
  "regression test model", or any discussion about measuring LLM output quality.
---

# Model Evaluation — Systematic LLM Quality Assessment

## Evaluation Framework

### 5 Dimensions (Always Test All)

| Dimension | What to Measure | How |
|-----------|----------------|-----|
| **Factual Recall** | Specific numbers, dates, thresholds | Known-answer questions |
| **Calculation** | Step-by-step math, correct final answer | Problems with verifiable solutions |
| **Edge Cases** | Ambiguous scenarios requiring judgment | Tricky questions with nuanced answers |
| **Citation** | References real sources (IRC §, IRS Pub) | Check every citation exists |
| **Coherence** | Well-structured, complete, no degeneration | Length, structure, readability |

### Scoring

```
PASS:    Correct answer, well-reasoned, properly cited
PARTIAL: Correct concept, wrong number or missing citation
FAIL:    Wrong answer, hallucinated citation, or degenerated output
```

## Comparison Methodology

### Side-by-Side Evaluation
```python
# Run same question through both models
for question in eval_set:
    response_a = query(model_a, question)
    response_b = query(model_b, question)
    # Score independently on 5 dimensions
```

### Regression Detection
When fine-tuning iterations:
1. Run eval BEFORE training (baseline)
2. Run eval AFTER training (candidate)
3. Compare dimension-by-dimension
4. **Any dimension regression → investigate before deploying**

### Overfit Detection Signs
- Model outputs dots, repeating characters, or gibberish
- Responses are exact copies of training examples
- Model can't handle questions outside training distribution
- Response length dramatically changes (too short or infinite)

**Root cause:** Too many epochs on too little data.
**Fix:** Reduce epochs, add more diverse training data.

## Evaluation Set Design

### For Domain-Specific Models (e.g., Tax)

| Category | Count | Purpose |
|----------|-------|---------|
| Factual (known answers) | 10 | Tests memorization of current facts |
| Calculation | 5 | Tests reasoning + arithmetic |
| Scenario-based | 5 | Tests application of rules |
| Edge cases | 5 | Tests judgment under ambiguity |
| Out-of-domain | 3 | Tests guardrails (should refuse/deflect) |
| **Total** | **28** | Minimum viable eval set |

### Question Quality Rules
1. Every question must have a **verifiable correct answer**
2. Include the **year** in factual questions (tax rates change)
3. Calculation questions must have **worked solutions** for comparison
4. Edge cases should have **multiple valid perspectives**
5. Out-of-domain questions test that the model **doesn't hallucinate** expertise

## Evaluation Tooling

### evaluate.py Pattern
```python
def evaluate(models: list[str], questions: list[dict]) -> list[dict]:
    results = []
    for q in questions:
        row = {"question": q["text"], "expected": q["answer"], "responses": {}}
        for model in models:
            response = query_ollama(model, q["text"])
            row["responses"][model] = {
                "text": response,
                "tokens": token_count,
                "latency_ms": latency,
                "matches_expected": check_answer(response, q["answer"]),
            }
        results.append(row)
    return results
```

### Automated Scoring (Where Possible)
- **Factual:** Extract numbers, compare to expected
- **Calculation:** Extract final answer, compare to expected
- **Citation:** Regex for IRC §, IRS Pub — verify they exist
- **Coherence:** Check length > 100 chars, no repeated tokens
- **Edge cases:** Requires human review

## Training Data vs Model Quality Correlation

```
Quality = f(data_quality × data_quantity × model_size) / epochs²

More data → linear improvement
Better data → exponential improvement
More epochs → diminishing returns → overfit
Bigger model → better reasoning, same fact accuracy
```

## Production Deployment Checklist

Before deploying a fine-tuned model:
- [ ] Run full eval set (28+ questions)
- [ ] Compare against baseline on all 5 dimensions
- [ ] No dimension regression
- [ ] Overfit check: test 5 out-of-domain questions
- [ ] Coherence check: 10 random prompts, all produce structured output
- [ ] Latency check: <5s for typical responses
- [ ] VRAM check: fits in target GPU with room for inference
