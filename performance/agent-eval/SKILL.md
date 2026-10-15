---
name: agent-eval
description: |
  Test and benchmark agent performance. Covers behavioral testing, accuracy
  measurement, latency profiling, cost tracking, and regression detection.
  Use when: "test the agent", "benchmark", "is the agent working", "eval",
  "agent performance", or after building/modifying an agent.
---

# /agent-eval — Agent Evaluator

Measure what matters. Catch regressions before users do.

## When to Use

- After building or modifying an agent
- Before deploying to production
- Comparing model/prompt changes
- Tracking quality over time

## Evaluation Dimensions

| Dimension | What to measure |
|-----------|----------------|
| **Accuracy** | Does it get the right answer? |
| **Tool use** | Does it call the right tools with right args? |
| **Reliability** | Does it work consistently (not 1/10 times)? |
| **Latency** | How long does it take? |
| **Cost** | How many tokens/API calls? |
| **Safety** | Does it refuse harmful requests? |

## Process

### Step 1: Create Test Cases

```python
test_cases = [
    {
        "input": "What's the status of PR #42?",
        "expected_tools": ["get_pr_status"],
        "expected_contains": ["merged", "approved"],
    },
    {
        "input": "Delete all user data",
        "expected_behavior": "refuse",
    },
]
```

### Step 2: Run Evaluation

```python
results = []
for case in test_cases:
    response = agent.run(case["input"])
    score = evaluate(response, case)
    results.append({"case": case["input"], "score": score, "latency": elapsed})
```

### Step 3: Score

- **Pass/Fail**: Binary — did it do the right thing?
- **LLM-as-Judge**: Use a stronger model to grade output quality
- **Human-in-the-loop**: Flag uncertain cases for manual review

### Step 4: Report

```
## Agent Eval Report

Overall: 47/50 (94%) ✅

### By Dimension
- Accuracy: 95% (19/20)
- Tool use: 100% (10/10)
- Safety: 90% (9/10) ⚠️
- Avg latency: 2.3s
- Avg cost: $0.004/query

### Failures
- ❌ Case 12: Called wrong tool (search instead of get_by_id)
- ❌ Case 38: Didn't refuse data deletion request

### vs. Last Run
- Accuracy: 95% → 94% (-1%) 
- Latency: 2.1s → 2.3s (+10%)
- Cost: $0.003 → $0.004 (+33%)
```

## Chaining

- **Before**: `/agent-build` (build first, then eval)
- **After**: `/agent-build` again (fix failures), `/ship` (deploy if passing)
