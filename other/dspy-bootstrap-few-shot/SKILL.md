---
name: dspy-bootstrap-few-shot
description: Automatically generate and select few-shot demonstrations for a DSPy program from labeled data using dspy.BootstrapFewShot - the simplest and fastest optimizer. Use when you have 50+ labeled examples and want a quick accuracy boost as your first optimization step. Common scenarios - your first optimization attempt on a new DSPy program, adding few-shot examples automatically from labeled data, quick accuracy boost before trying heavier optimizers, bootstrapping demonstrations from a teacher model, or getting started with DSPy optimization. Related - ai-improving-accuracy, dspy-labeled-few-shot. Also used for dspy.BootstrapFewShot, simplest DSPy optimizer, first optimizer to try, automatic few-shot example selection, bootstrap demonstrations from labels, quick optimization baseline, add examples to prompt automatically, teacher bootstrapping, labeled data to few-shot demos, starting point for DSPy optimization, easy accuracy improvement, how to optimize DSPy program for the first time.
---

# Bootstrap Few-Shot Demonstrations

Guide the user through using `dspy.BootstrapFewShot` to automatically generate and select high-quality few-shot demonstrations for their DSPy program. This is the simplest optimizer and the recommended first step before trying heavier optimizers.

## What is BootstrapFewShot

`dspy.BootstrapFewShot` takes your program, a training set, and a metric, then:

1. Runs your program on each training example
2. Keeps the traces (input/output pairs) where the metric passes
3. Attaches the best traces as few-shot demonstrations to your program's predictors

The result is a copy of your program with working examples baked into the prompt — so the LM sees "here's how I solved similar problems" every time it runs.

```python
optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
optimized = optimizer.compile(my_program, trainset=trainset)
```

## When to use it

- **First optimizer to try** — it is fast, simple, and often gives a meaningful lift
- You have **~50+ labeled examples** (fewer can work but results vary)
- You want to **add few-shot demonstrations** without hand-writing them
- You want a **quick baseline** before trying heavier optimizers

## Step 1 — Understand your setup

Before generating code, clarify:

1. **What does your DSPy program do?** (classification, QA, extraction, summarization, etc.) — this shapes the metric and example structure.
2. **How many labeled examples do you have?** If fewer than ~20, consider `/dspy-labeled-few-shot` instead (hand-picked demos, no bootstrapping overhead).
3. **What metric will you use to judge quality?** Exact match, fuzzy match, LLM-as-judge, or a task-specific function? The metric is the heart of BootstrapFewShot — if it is too strict (less than ~10% pass rate on your trainset), barely any demos will be bootstrapped.

## Basic usage

```python
import dspy
from dspy.evaluate import Evaluate

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

# 1. Define your program
qa = dspy.ChainOfThought("question -> answer")

# 2. Prepare your data (mark inputs with .with_inputs())
trainset = [
    dspy.Example(question="What is the capital of France?", answer="Paris").with_inputs("question"),
    dspy.Example(question="What is 2+2?", answer="4").with_inputs("question"),
    # ... ~50+ examples
]

devset = [
    dspy.Example(question="Who wrote Hamlet?", answer="Shakespeare").with_inputs("question"),
    # ... held-out examples for evaluation
]

# 3. Define a metric
def metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()

# 4. Evaluate baseline
evaluator = Evaluate(devset=devset, metric=metric, num_threads=4)
baseline = evaluator(qa)
print(f"Baseline: {baseline:.1f}%")

# 5. Optimize
optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
optimized_qa = optimizer.compile(qa, trainset=trainset)

# 6. Evaluate optimized program
improved = evaluator(optimized_qa)
print(f"Optimized: {improved:.1f}%")
```

## Key parameters

```python
optimizer = dspy.BootstrapFewShot(
    metric=metric,                # Scoring function(example, prediction, trace) -> bool/float
    max_bootstrapped_demos=4,     # Max bootstrapped (generated) demos per predictor. Default: 4
    max_labeled_demos=16,         # Max labeled (from trainset) demos per predictor. Default: 16
    max_rounds=1,                 # Number of bootstrap rounds. Default: 1
    max_errors=None,              # Error tolerance. Default: None (uses dspy.settings.max_errors)
    metric_threshold=None,        # Numerical threshold for accepting bootstrap examples
    teacher_settings=None,        # Config dict for the teacher model (e.g., {"lm": teacher_lm})
)
```

### What the parameters control

- **`max_bootstrapped_demos`** — How many auto-generated demonstrations to include in the prompt. These come from running the program on training examples and keeping traces that pass the metric. Start with 4, increase to 8 if you have a complex task.

- **`max_labeled_demos`** — How many examples from your trainset to include directly as demonstrations (without running through the program first). These are simpler input/output pairs. Set to 0 if you only want bootstrapped demos.

- **`max_rounds`** — Number of bootstrapping iterations. In each round, the optimizer runs the program (with any demos from previous rounds) and collects new passing traces. More rounds can find better demos but take longer. Usually 1 is sufficient.

- **`max_errors`** — How many failed examples to tolerate before the optimizer stops. Defaults to `None` (uses `dspy.settings.max_errors`). Increase if your task is noisy or the metric is strict.

- **`metric_threshold`** — Numerical threshold for accepting bootstrap examples. When set, only traces scoring above this threshold become demos. Useful when your metric returns floats rather than booleans.

- **`teacher_settings`** — Configuration dict for a teacher model. Pass `{"lm": teacher_lm}` to use a stronger model for generating traces while the student uses a cheaper model.

## How bootstrapping works

Understanding the process helps you debug when results are unexpected.

**Round 1:**
1. The optimizer picks examples from `trainset`
2. For each example, it runs your program to get a prediction
3. It scores the prediction with your `metric(example, prediction, trace)`
4. If the metric passes, the full trace (inputs + outputs, including intermediate reasoning) is saved as a candidate demo
5. The best `max_bootstrapped_demos` traces are attached to each predictor

**Round 2+ (if `max_rounds > 1`):**
1. The program now has demos from round 1
2. The optimizer runs the program again on more training examples
3. New passing traces are collected — these are often better because the program already has some demos
4. The demo set is updated with the best traces so far

**The result:** Your program's predictors now have few-shot demonstrations in their prompts. When the program runs, the LM sees these worked examples before processing the new input.

## Trace-aware metrics

The `trace` parameter in your metric is `None` during evaluation but set during optimization. Use this to apply stricter filtering during bootstrapping:

```python
def metric(example, prediction, trace=None):
    correct = prediction.answer.strip().lower() == example.answer.strip().lower()
    if trace is not None:
        # During optimization: require good reasoning too
        has_reasoning = len(getattr(prediction, "reasoning", "")) > 50
        return correct and has_reasoning
    # During evaluation: only check correctness
    return correct
```

This ensures bootstrapped demos have both correct answers and clear reasoning, producing higher-quality demonstrations.

## Saving and loading optimized programs

After optimization, save the program so you don't have to re-optimize every time:

```python
# Save
optimized_qa.save("optimized_qa.json")

# Load later
loaded_qa = dspy.ChainOfThought("question -> answer")
loaded_qa.load("optimized_qa.json")

# Use it
result = loaded_qa(question="What is the capital of Japan?")
```

For custom modules:

```python
class MyPipeline(dspy.Module):
    def __init__(self):
        self.step1 = dspy.ChainOfThought("question -> search_query")
        self.step2 = dspy.ChainOfThought("question, search_query -> answer")

    def forward(self, question):
        query = self.step1(question=question)
        return self.step2(question=question, search_query=query.search_query)

# Save after optimization
optimized_pipeline.save("pipeline.json")

# Load
loaded = MyPipeline()
loaded.load("pipeline.json")
```

The saved file contains the few-shot demonstrations for each predictor. The program structure itself is defined in code — `save` and `load` only handle the learned demos and parameters.

## Using with multi-step programs

BootstrapFewShot works on every predictor in your program. For a multi-step pipeline, each step gets its own demonstrations:

```python
class RAG(dspy.Module):
    def __init__(self):
        self.generate_query = dspy.ChainOfThought("question -> search_query")
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        query = self.generate_query(question=question)
        # Assume some retrieval step here
        context = retrieve(query.search_query)
        return self.generate_answer(context=context, question=question)

optimizer = dspy.BootstrapFewShot(metric=metric, max_bootstrapped_demos=4)
optimized_rag = optimizer.compile(RAG(), trainset=trainset)
# Both generate_query and generate_answer now have bootstrapped demos
```

## When to upgrade to a heavier optimizer

BootstrapFewShot is a great starting point, but you may want to upgrade if:

| Signal | Next step |
|--------|-----------|
| Accuracy plateaus after bootstrapping | Try `dspy.BootstrapFewShotWithRandomSearch` — it runs multiple bootstrap trials and picks the best set of demos |
| You have 200+ examples and want the best prompts | Try `dspy.MIPROv2` — it optimizes both instructions and few-shot demos |
| You want maximum quality and can fine-tune | Try `dspy.BootstrapFinetune` — it uses bootstrapped traces to fine-tune the LM weights |

A typical progression:

1. **BootstrapFewShot** — fast, first pass (~50 examples)
2. **BootstrapFewShotWithRandomSearch** — better demo selection (~200 examples)
3. **MIPROv2** — full prompt optimization (~200 examples)
4. **BootstrapFinetune** — weight tuning (~500+ examples)

## Troubleshooting

**No demos were bootstrapped:**
- Your metric may be too strict — check that at least some training examples pass
- Run a quick evaluation on your trainset to see the pass rate
- Lower the bar in your metric or fix data quality issues

**Accuracy didn't improve (or got worse):**
- Try increasing `max_bootstrapped_demos` (e.g., 8)
- Try setting `max_labeled_demos=0` to only use bootstrapped demos
- Check that your trainset is representative of the task
- Ensure your devset is held out (not overlapping with trainset)

**Optimization is slow:**
- Reduce trainset size (50-100 examples is often enough)
- Use a faster/cheaper LM for bootstrapping, then evaluate with the target LM
- Reduce `max_rounds` to 1

## Gotchas

- **Claude sets `max_labeled_demos` too high, bloating the prompt.** The default is 16, which adds up to 16 raw input/output pairs from the trainset to the prompt. For tasks with long inputs, this can consume most of the context window. Start with `max_labeled_demos=4` and increase only if accuracy improves.
- **Claude forgets `.with_inputs()` on training examples.** Every `dspy.Example` in the trainset must call `.with_inputs("field1", "field2")` to mark which fields are inputs vs labels. Without it, the optimizer cannot distinguish inputs from expected outputs and bootstrapping silently produces garbage demos.
- **Claude overlaps trainset and devset.** If the devset contains examples also in the trainset, evaluation scores are inflated because the optimizer has already seen those examples. Always use a held-out devset with no overlap.
- **Claude uses a strict exact-match metric that rejects most traces.** If fewer than ~10% of training examples pass the metric, barely any demos get bootstrapped. Check your metric pass rate on the trainset first. Relax the metric (e.g., use containment instead of exact match) or fix data quality before optimizing.
- **Claude does not compare baseline vs optimized scores.** Without a baseline evaluation, there is no way to know if optimization helped or hurt. Always evaluate the unoptimized program on the devset first, then compare after optimization.

## Additional resources

- [dspy.BootstrapFewShot API docs](https://dspy.ai/api/optimizers/BootstrapFewShot/)
- [reference.md](reference.md) — constructor parameters, compile() method, key behaviors
- [examples.md](examples.md) — QA optimization, classification with trace-aware metrics

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Need to prepare training data? Use `/dspy-data`
- Need to write a metric or run evaluation? Use `/dspy-evaluate`
- Want to try random search over demo sets? Use `/dspy-bootstrap-rs`
- Want the best prompt optimization? Use `/dspy-miprov2`
- For the full measure-improve-verify loop, see `/ai-improving-accuracy`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`
