---
name: dspy-evaluate
description: Run dspy.Evaluate to score DSPy programs against labeled examples using custom or built-in metrics. Use when you need to measure how well your DSPy program performs — writing metrics, scoring against a dev set, or comparing before/after optimization. Common scenarios - measuring accuracy before and after optimization, writing custom metrics for your task, scoring a program against a held-out dev set, comparing two prompt strategies, building a test suite for AI quality, or running regression tests on AI outputs. Related - ai-improving-accuracy, ai-scoring, ai-monitoring. Also used for dspy.Evaluate, dspy.evaluate, write DSPy metric function, measure AI accuracy, evaluate DSPy program, dev set evaluation, before and after optimization comparison, custom scoring function, test AI quality systematically, AI regression testing, metric-driven development, how to know if my DSPy program improved, score predictions against labels, evaluation harness for LLM, CI/CD for AI quality.
---

# Evaluate Your DSPy Program

Guide the user through measuring AI quality with DSPy's `Evaluate` class. The pattern: pick a metric, prepare a devset, run the evaluator, interpret results, then feed the same metric into an optimizer.

## Step 1 — Gather context

Before recommending a metric or writing evaluation code, clarify:

1. **What fields does your program output?** (`answer`, `response`, custom fields — metric field names must match exactly; `SemanticF1` requires `response`, not `answer`)
2. **Do you have labeled gold answers**, or do you need an LM judge to assess open-ended quality?
3. **What does "correct" mean for your task?** Exact string match, semantic overlap, factual groundedness, safety, or a weighted combination?
4. **Is this metric feeding into an optimizer?** If yes, you may want trace-aware logic — stricter requirements during optimization than during bare evaluation.

## What is dspy.Evaluate

`dspy.Evaluate` runs your program on every devset example, scores each with a metric, and reports the aggregate score. It handles threading and progress display. Returns an `EvaluationResult`; access `.score` for the percentage (0-100) and `.results` for per-example `(example, prediction, score)` tuples.

## Built-in metrics

DSPy provides `answer_exact_match` (normalized string equality — compares `example.answer` with `prediction.answer`) and `answer_passage_match` (RAG retrieval hit check — returns `True` if any passage in `prediction.context` contains `example.answer`). They do **not** share the same field expectations.

### Choosing a metric

| Metric | Example fields | Prediction fields | Best for | LM cost |
|--------|---------------|-------------------|---------|---------|
| `answer_exact_match` | `answer` | `answer` | Factoid QA, structured output | Free |
| `answer_passage_match` | `answer` | `context` (list of passages) | RAG retrieval hit rate | Free |
| `SemanticF1` | `question`, `response` | `response` | Open-ended QA with near-miss answers | 1 LM call |
| `CompleteAndGrounded` | `question`, `response` | `response`, `context` | RAG faithfulness + completeness | 2 LM calls |
| Custom LM-as-judge | Any | Any | Subjective quality, style, safety | 1+ LM calls |

Start with the cheapest metric that captures your quality signal. Each LM-judge call costs one LM invocation per example — on a 100-example devset with 4 optimizer rounds this adds thousands of extra calls. Only reach for LM-as-judge when simpler metrics genuinely cannot distinguish good from bad outputs.

### SemanticF1

Measures token-level overlap between the predicted and expected answer using an F1 score. More forgiving than exact match — it gives partial credit for answers that are close but not identical:

```python
from dspy.evaluate import SemanticF1

semantic_f1 = SemanticF1()

evaluator = Evaluate(devset=devset, metric=semantic_f1, num_threads=4)
score = evaluator(my_program)
```

`SemanticF1` is a good default metric for open-ended QA tasks where exact match is too strict. It expects a `question` field on the example plus a `response` field on both the example and prediction (not `answer`). Constructor: `SemanticF1(threshold=0.66, decompositional=False)`. The `threshold` controls the minimum score during optimization (when `trace` is set).

### CompleteAndGrounded

Checks whether the predicted answer is both complete (covers all key claims in the gold answer) and grounded (doesn't hallucinate facts not in the gold answer):

```python
from dspy.evaluate import CompleteAndGrounded

complete_and_grounded = CompleteAndGrounded()

evaluator = Evaluate(devset=devset, metric=complete_and_grounded, num_threads=4)
score = evaluator(my_program)
```

This is an LM-based metric — it uses the configured LM to judge completeness and groundedness. It expects `response` and `context` fields on the prediction, and `question` and `response` on the example. Constructor: `CompleteAndGrounded(threshold=0.66)`. Useful for RAG tasks where you care about both recall and precision of facts.

## Custom metrics

A metric is `def metric(example, prediction, trace=None)` returning `bool`, `int`, or `float`. The `trace` parameter is `None` during evaluation but set during optimization (use this to apply stricter requirements during training).

### Multi-field scoring

```python
def metric(example, prediction, trace=None):
    fields = ["name", "email", "phone"]
    correct = sum(
        1 for f in fields
        if getattr(prediction, f, "").strip().lower() == getattr(example, f, "").strip().lower()
    )
    return correct / len(fields)
```

## LM-as-judge

For open-ended tasks (summaries, creative writing, complex QA), use an LM to judge quality. Define a signature for the judge, then call it inside your metric:

```python
class AssessAnswer(dspy.Signature):
    """Assess if the predicted answer correctly addresses the question."""
    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField(desc="The reference answer")
    predicted_answer: str = dspy.InputField(desc="The answer to evaluate")
    is_correct: bool = dspy.OutputField(desc="True if the prediction is correct and complete")

def llm_judge_metric(example, prediction, trace=None):
    judge = dspy.Predict(AssessAnswer)
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return result.is_correct
```

### Use a separate LM for the judge

To avoid the model grading its own work, use a different (often stronger) LM for the judge:

```python
judge_lm = dspy.LM("openai/gpt-4o")  # or "anthropic/claude-sonnet-4-5-20250929", etc.

def llm_judge_metric(example, prediction, trace=None):
    judge = dspy.Predict(AssessAnswer)
    with dspy.context(lm=judge_lm):
        result = judge(
            question=example.question,
            gold_answer=example.answer,
            predicted_answer=prediction.answer,
        )
    return result.is_correct
```

### Graded judge (float scores)

Return a float instead of a bool for partial credit:

```python
class GradeAnswer(dspy.Signature):
    """Grade the predicted answer on a scale of 0 to 5."""
    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField()
    predicted_answer: str = dspy.InputField()
    score: int = dspy.OutputField(desc="Score from 0 (completely wrong) to 5 (perfect)")
    justification: str = dspy.OutputField(desc="Why this score was given")

def graded_metric(example, prediction, trace=None):
    judge = dspy.ChainOfThought(GradeAnswer)
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return result.score / 5.0  # normalize to 0.0-1.0
```

## Composite metrics

Combine multiple signals into a single score with weights:

```python
def composite_metric(example, prediction, trace=None):
    # Correctness (primary signal)
    correct = float(prediction.answer.strip().lower() == example.answer.strip().lower())

    # Conciseness (prefer shorter answers)
    concise = float(len(prediction.answer.split()) < 50)

    # Has reasoning (check that the model explained its thinking)
    has_reasoning = float(len(getattr(prediction, "reasoning", "")) > 20)

    # Weighted combination
    return 0.7 * correct + 0.2 * concise + 0.1 * has_reasoning
```

### Mixing exact checks with LM judges

```python
def hybrid_metric(example, prediction, trace=None):
    # Fast exact check
    if prediction.answer.strip().lower() == example.answer.strip().lower():
        return 1.0

    # Fall back to LM judge for partial credit
    judge = dspy.Predict(AssessAnswer)
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return 0.5 if result.is_correct else 0.0
```

## Debugging with per-example scores

`Evaluate` returns an `EvaluationResult` with `.score` (aggregate percentage) and `.results` (list of `(example, prediction, score)` tuples). Use `.results` to find failing examples and understand failure patterns.

## Common patterns

### Trace-aware metrics for optimization

The `trace` parameter is `None` during evaluation but set during optimization. Use this to apply stricter requirements during training:

```python
def metric(example, prediction, trace=None):
    correct = prediction.answer.strip().lower() == example.answer.strip().lower()
    if trace is not None:
        # During optimization: also require good reasoning
        has_reasoning = len(getattr(prediction, "reasoning", "")) > 50
        return correct and has_reasoning
    # During evaluation: only check correctness
    return correct
```

This makes the optimizer filter for traces where the model both got the answer right and showed its work. The result is more robust few-shot demonstrations.

### Before-and-after comparison

A common workflow for measuring the impact of optimization:

```python
from dspy.evaluate import Evaluate

evaluator = Evaluate(devset=devset, metric=metric, num_threads=4, display_table=5)

# Baseline
baseline = evaluator(my_program)

# Optimize
optimizer = dspy.MIPROv2(metric=metric, auto="medium")
optimized = optimizer.compile(my_program, trainset=trainset)

# Compare
optimized_result = evaluator(optimized)
print(f"Baseline:  {baseline.score:.1f}%")
print(f"Optimized: {optimized_result.score:.1f}%")
print(f"Delta:     {optimized_result.score - baseline.score:+.1f}%")
```

## Gotchas

1. **Claude uses `return_all_scores=True` or `return_outputs=True` which no longer exist.** `Evaluate` now returns an `EvaluationResult` object. Access `.score` for the aggregate percentage and `.results` for per-example `(example, prediction, score)` tuples. Do not pass `return_all_scores` or `return_outputs`.
2. **Claude uses `SemanticF1` with `answer` fields but it expects `response`.** `SemanticF1` looks for `response` on both the example and prediction, not `answer`. If your signature uses `answer`, either rename the field or write a wrapper metric.
3. **Claude uses `CompleteAndGrounded` without providing `context`.** `CompleteAndGrounded` expects `response` and `context` on the prediction, and `question` and `response` on the example. Without `context`, it cannot check groundedness.
4. **Metrics must return a `float` or `bool`, not a string** -- returning a string silently breaks scoring.
5. **Small dev sets (<30 examples) give unreliable scores** -- results can swing 10-20% between runs. Aim for 50+ examples for stable evaluation.
6. **Do not start with an LM-as-judge if `answer_exact_match` or `SemanticF1` is sufficient.** Each judge call costs one LM invocation per example per evaluation pass. During optimizer compilation with hundreds of candidate traces, costs multiply fast. Benchmark the simple metrics first; add a judge only if they cannot distinguish your good from bad outputs.

## Additional resources

- [dspy.Evaluate API docs](https://dspy.ai/api/evaluation/Evaluate/)
- [dspy.SemanticF1 API docs](https://dspy.ai/api/evaluation/SemanticF1/)
- [dspy.CompleteAndGrounded API docs](https://dspy.ai/api/evaluation/CompleteAndGrounded/)
- For constructor signatures and method reference, see [reference.md](reference.md)
- For worked examples (exact match, LM judge, composite), see [examples.md](examples.md)

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Need to prepare training and evaluation data? Use `/dspy-data`
- Ready to optimize with few-shot examples? Use `/dspy-bootstrap-few-shot`
- Want the best prompt optimization? Use `/dspy-miprov2`
- For the full measure-improve-verify loop, see `/ai-improving-accuracy`
- For **decomposed RAG evaluation** (faithfulness, context precision/recall) see `/dspy-ragas`
- For scoring AI outputs outside of optimization loops, see `/ai-scoring`
- For worked examples (exact match, LM judge, composite), see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
