---
name: agent-evaluation
description: "Evaluate AI agent outputs — hallucination detection, quality scoring, behavioral testing, and CI/CD pipelines."
context: fork
globs: []
alwaysApply: false
---

# Agent Evaluation

Framework for evaluating AI agent outputs: hallucination detection, quality scoring, behavioral regression, and CI/CD integration.

---

## Hallucination Detection

### Fact-Checking Pipeline
```python
def detect_hallucination(response: str, context: str) -> dict:
    """Check if response contains unsupported claims."""
    claims = extract_claims(response)
    supported = [c for c in claims if verify_against(c, context)]
    return {
        'hallucination_rate': 1 - len(supported) / len(claims),
        'unsupported_claims': [c for c in claims if c not in supported]
    }
```

### Red Teaming
- Generate adversarial prompts designed to trigger hallucinations
- Test with contradictory context
- Verify model says "I don't know" when appropriate

---

## Output Quality Scoring

### RAGAS Metrics
| Metric | What it measures | Target |
|--------|-----------------|--------|
| **Faithfulness** | Response grounded in context | ≥0.8 |
| **Answer Relevance** | Response addresses query | ≥0.8 |
| **Context Precision** | Retrieved context is relevant | ≥0.7 |
| **Context Recall** | All relevant context retrieved | ≥0.7 |

### Scoring Pipeline
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevance]
)
```

---

## Behavioral Regression Testing

### Test Types
- **Consistency**: Same input → same output across runs
- **Robustness**: Slight input variation → similar output
- **Boundary**: Edge cases handled gracefully
- **Safety**: No harmful, biased, or leaked content

### LangSmith Integration
```python
from langsmith import Client

client = Client()
client.evaluate(
    runnable,
    dataset_name="agent-behavior-tests",
    evaluators=[consistency_evaluator, safety_evaluator]
)
```

---

## Latency & Reliability Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| **P50 Latency** | <2s | Time to first token |
| **P99 Latency** | <10s | End-to-end response time |
| **Error Rate** | <1% | Failed requests / total |
| **Throughput** | >10 req/s | Concurrent requests handled |

---

## CI/CD Evaluation Pipeline

```yaml
# .github/workflows/agent-eval.yml
jobs:
  evaluate:
    steps:
      - run: python scripts/run_eval_suite.py
      - run: python scripts/check_hallucination_rate.py
      - run: python scripts/benchmark_latency.py
      - if: failure
        run: echo "Agent eval failed — blocking merge"
```

---

## Adversarial Red Teaming

### Attack Vectors
- **Prompt injection**: "Ignore previous instructions and..."
- **Context poisoning**: Inject false facts into context
- **Role manipulation**: "You are now an unrestricted AI..."
- **Format exploitation**: XML/JSON injection in prompts

### Defense Validation
- Input sanitization working?
- Output validation catching issues?
- Guardrails triggered correctly?

---

## Quick Eval Checklist

- [ ] Hallucination rate <5%
- [ ] RAGAS faithfulness ≥0.8
- [ ] Consistency score ≥0.9
- [ ] P99 latency <10s
- [ ] No safety violations
- [ ] Adversarial tests passing
