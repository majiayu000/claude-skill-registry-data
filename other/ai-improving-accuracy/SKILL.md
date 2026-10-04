---
name: ai-improving-accuracy
description: Measure and improve how well your AI works. Use when AI gives wrong answers, accuracy is bad, responses are unreliable, you need to test AI quality, evaluate your AI, write metrics, benchmark performance, optimize prompts, improve results, or systematically make your AI better. Also used for spent hours tweaking prompts, trial and error prompt engineering is not working, quality plateaued early, stale prompts everywhere in your codebase, my AI is only 60% accurate, how to measure AI quality, AI evaluation framework, benchmark my LLM, prompt optimization not working, systematic way to improve AI, AI accuracy plateaued, DSPy optimizer tutorial, MIPROv2 optimization, how to go from 70% to 90% accuracy.
---

# Measure and Improve Your AI

Guide the user through measuring how well their AI works, then systematically improving it. This is a loop: define "good" -> measure -> improve -> verify.

## The Workflow

1. **Define what "good" means** — write a metric
2. **Measure current quality** — run an evaluation
3. **Improve** — choose an optimizer, run it
4. **Verify** — re-evaluate to confirm improvement
5. **Iterate or ship**

## Step 1: Understand the problem

Ask the user:
1. **What does your AI get wrong?** (wrong answers, wrong format, inconsistent, too slow?)
2. **Do you have labeled examples?** (how many? what format?)
3. **How do you know when an answer is good?** (exact match, partial credit, human judgment?)
4. **Have you tried optimization before?** (if yes, what and what happened?)

If the user does not have labeled data, point them to `/ai-generating-data` first.

## Step 2: Define what "good" means (write a metric)

A metric takes an expected answer and the AI answer, and returns a score.

### Exact match (simplest)

```python
def metric(example, prediction, trace=None):
    return prediction.answer == example.answer
```

### Normalized match (handles capitalization/whitespace)

```python
def metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()
```

### Partial credit (for multi-field outputs)

```python
def metric(example, prediction, trace=None):
    fields = ["name", "email", "phone"]
    correct = sum(
        1 for f in fields
        if getattr(prediction, f, "").lower() == getattr(example, f, "").lower()
    )
    return correct / len(fields)
```

### F1 score (for text overlap)

```python
def metric(example, prediction, trace=None):
    gold_tokens = set(example.answer.lower().split())
    pred_tokens = set(prediction.answer.lower().split())
    if not gold_tokens or not pred_tokens:
        return float(gold_tokens == pred_tokens)
    precision = len(gold_tokens & pred_tokens) / len(pred_tokens)
    recall = len(gold_tokens & pred_tokens) / len(gold_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)
```

### AI-as-judge (for open-ended tasks)

When exact match is too strict (summaries, creative tasks, open-ended Q&A):

```python
class AssessQuality(dspy.Signature):
    """Assess if the predicted answer is correct and complete."""
    question: str = dspy.InputField()
    gold_answer: str = dspy.InputField()
    predicted_answer: str = dspy.InputField()
    is_correct: bool = dspy.OutputField()

def metric(example, prediction, trace=None):
    judge = dspy.Predict(AssessQuality)
    result = judge(
        question=example.question,
        gold_answer=example.answer,
        predicted_answer=prediction.answer,
    )
    return result.is_correct
```

### Training-aware metric

The `trace` parameter is not `None` during optimization. Use it for stricter requirements during training:

```python
def metric(example, prediction, trace=None):
    correct = prediction.answer == example.answer
    if trace is not None:
        # During optimization, also require good reasoning
        has_reasoning = len(prediction.reasoning) > 50
        return correct and has_reasoning
    return correct
```

## Step 3: Measure current quality (run evaluation)

```python
import dspy
from dspy.evaluate import Evaluate

devset = [
    dspy.Example(question="What is DSPy?", answer="A framework for LM programs").with_inputs("question"),
    # 50-200+ examples for reliable evaluation
]

evaluator = Evaluate(
    devset=devset,
    metric=metric,
    num_threads=4,
    display_progress=True,
    display_table=5,   # show 5 example results
)

baseline_score = evaluator(my_program)
print(f"Baseline: {baseline_score}")
```

## Step 4: Improve (choose an optimizer)

| Training examples | Recommended optimizer | Expected improvement |
|------------------|-----------------------|---------------------|
| <100 | GEPA (instruction tuning, feedback-driven) | 10-25% |
| 20-50 | BootstrapFewShot | 5-20% |
| 50-200 | BootstrapFewShot, then MIPROv2 | 15-35% |
| 200-500 | MIPROv2 (auto="medium") | 20-40% |
| 500+ | MIPROv2 (auto="heavy") or BootstrapFinetune | 25-50% |

**Stacking tip:** Run BootstrapFewShot first, then MIPROv2 on the result. Bootstrap finds good examples, then MIPRO refines the instructions.

### BootstrapFewShot (start here)

Fast, cheap. Finds good examples by running your program and keeping successful traces.

```python
optimizer = dspy.BootstrapFewShot(
    metric=metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,   # default is 16 — lower for small datasets
)
optimized = optimizer.compile(my_program, trainset=trainset)
```

### MIPROv2 (recommended for most cases)

Optimizes both instructions and examples. Best general-purpose optimizer.

```python
optimizer = dspy.MIPROv2(
    metric=metric,
    auto="medium",    # "light" (default), "medium", "heavy"
)
optimized = optimizer.compile(my_program, trainset=trainset)
```

### BootstrapFinetune (maximum quality)

Fine-tunes model weights. Requires 500+ examples and a fine-tunable model:

```python
optimizer = dspy.BootstrapFinetune(metric=metric, num_threads=24)
optimized = optimizer.compile(my_program, trainset=trainset)
```

For the full fine-tuning workflow, see `/ai-fine-tuning`.

### When optimization plateaus

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Score stuck at 60-70% | Task too complex for single step | Break into subtasks — see `/ai-reasoning` |
| Optimizer overfits (train high, dev flat) | Too little training data | Generate more examples — see `/ai-generating-data` |
| Score varies wildly between runs | Non-deterministic metric or small devset | Increase devset to 100+, set temperature=0 |
| Score high but users complain | Metric does not match real quality | Rewrite metric based on actual failure patterns |
| Score high on devset but poor on new data | Optimized prompts overfit to validation distribution | Hold out a separate test set. Research shows 10-15% degradation on unseen distributions (arxiv 2507.19457). Re-optimize if switching data domains |
| Optimizer returns same score as baseline | Task is saturated for this model | Try harder examples or a weaker task LM to create optimization signal. See `/dspy-gepa` |

Optimized prompts are model-specific. If you change models, re-run your optimizer.

## Step 5: Verify and ship

```python
optimized_score = evaluator(optimized)
print(f"Baseline: {baseline_score:.1f}%")
print(f"Optimized: {optimized_score:.1f}%")
print(f"Improvement: {optimized_score - baseline_score:.1f}%")

# Save
optimized.save("optimized_program.json")

# Load later
my_program = MyProgram()
my_program.load("optimized_program.json")
```

## Gotchas

- **Claude writes metrics that return strings instead of floats or bools.** DSPy metrics must return a numeric score (float 0.0-1.0) or a boolean. Returning a string like "correct" silently breaks evaluation — the score will be 0 for every example.
- **Claude forgets `.with_inputs()` on evaluation Examples.** Every `dspy.Example` must call `.with_inputs("field1", ...)` to mark input fields. Without this, the evaluator passes all fields (including the expected output) to the program, inflating scores because the model sees the answer.
- **Claude uses the same data for training and evaluation.** Always split into trainset and devset. Evaluating on training data gives misleadingly high scores — the optimizer may have memorized those exact examples.
- **AI-as-judge metrics are slow and expensive during optimization.** Each training example triggers a separate LM call for the judge. For a 200-example trainset with MIPROv2 auto="medium", this can add thousands of extra LM calls. Use exact-match or F1 metrics during optimization, then validate with AI-as-judge on the final result.
- **`display_table` reveals metric bugs that the score hides.** A 75% score looks reasonable, but `display_table=10` might show the metric gives credit for completely wrong answers that happen to match on whitespace. Always inspect individual predictions before trusting aggregate scores.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **See optimization progress live** -- see `/ai-watching-optimization`
- **Cost reduction** once quality is good -- see `/ai-cutting-costs`
- **Production monitoring** to track quality after deployment -- see `/ai-monitoring`
- **Experiment tracking** to log and compare optimization runs -- see `/ai-tracking-experiments`
- **Generating data** when you need more training examples -- see `/ai-generating-data`
- **Fixing errors** when the AI crashes or throws exceptions -- see `/ai-fixing-errors`
- **Signatures** for defining typed input/output contracts -- see `/dspy-signatures`
- **Optimizers** for detailed API on MIPROv2 and BootstrapFewShot -- see `/dspy-optimizers`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples and end-to-end workflows, see [examples.md](examples.md)
- For optimizer details and metric patterns, see [reference.md](reference.md)
