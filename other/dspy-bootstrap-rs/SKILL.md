---
name: dspy-bootstrap-rs
description: Optimize few-shot demos for a DSPy program by searching over multiple candidate demo sets using dspy.BootstrapFewShotWithRandomSearch. Use when basic BootstrapFewShot is not enough and you want better results at the cost of more LM calls. Common scenarios - BootstrapFewShot alone is not reaching target accuracy, you want to search over multiple candidate demo sets and pick the best, optimizing for tasks where example selection matters a lot, or you have compute budget for a more thorough search. Also used for random search over demonstrations, search for optimal few-shot examples, brute force demo selection, try many demo combinations, more compute for better demos, upgrade from BootstrapFewShot, intermediate optimizer between simple and MIPROv2, when basic few-shot optimization is not enough, explore demonstration space.
---

# Optimize Few-Shot Demos with dspy.BootstrapFewShotWithRandomSearch

Guide the user through using DSPy's `BootstrapFewShotWithRandomSearch` optimizer to find the best set of few-shot demonstrations for their program. This optimizer runs BootstrapFewShot multiple times with different random seeds and keeps the candidate program that scores highest on a metric.

## Step 1 — Gather context

Before writing any code, ask the user:

1. **How many training examples do you have?** BootstrapRS works best with 50-200+ examples. Fewer than ~50 → suggest plain `BootstrapFewShot` instead; the random search has too little data to meaningfully differentiate candidates.
2. **What is your metric / success criterion?** (exact match, semantic similarity, a custom function — needed to write the metric)
3. **Single module or multi-step pipeline?** Multi-step pipelines accumulate demos across every predictor — use `max_bootstrapped_demos=2` and `max_labeled_demos=2` to avoid context overflow.
4. **What is your compute budget?** Each candidate run costs roughly the same as one BootstrapFewShot pass. With the default 16 candidates, plan for ~16x that cost. Adjust `num_candidate_programs` accordingly.

## What it is

`BootstrapFewShotWithRandomSearch` (also known as BootstrapRS) is a prompt optimizer that searches over multiple candidate sets of few-shot demonstrations to find the best one. It wraps `BootstrapFewShot` and runs it repeatedly with different random subsets of training examples, then evaluates each candidate program on a held-out portion of the trainset.

```
trainset ──> [ BootstrapFewShot run 1 ] ──> candidate program 1 ──┐
         ──> [ BootstrapFewShot run 2 ] ──> candidate program 2 ──┤
         ──> [ BootstrapFewShot run 3 ] ──> candidate program 3 ──┼──> evaluate all ──> best program
         ──> ...                                                  │
         ──> [ BootstrapFewShot run N ] ──> candidate program N ──┘
```

## How it improves on BootstrapFewShot

`BootstrapFewShot` runs once: it bootstraps demonstrations from your training data, picks a fixed set, and returns a single optimized program. The result depends heavily on which examples happened to be selected and which traces succeeded. You might get lucky or unlucky.

`BootstrapFewShotWithRandomSearch` removes that luck factor. It runs the bootstrap process multiple times (controlled by `num_candidate_programs`), each time with a different random sample of training examples. Each candidate program gets scored on a validation set, and the optimizer returns the highest-scoring one.

The trade-off is straightforward: more compute for more reliable results.

| | BootstrapFewShot | BootstrapFewShotWithRandomSearch |
|---|-----------------|----------------------------------|
| **Bootstrap runs** | 1 | `num_candidate_programs` (default 16) |
| **Selection** | Returns the single result | Evaluates all candidates, returns the best |
| **Reliability** | Results vary between runs | More consistent, higher-quality results |
| **Cost** | 1x | ~Nx (N = num_candidate_programs) |
| **When to use** | Quick iteration, <50 examples | You want the best few-shot demos, 50-200+ examples |

## Basic usage

```python
import dspy
from dspy.evaluate import Evaluate

lm = dspy.LM("openai/gpt-4o-mini")  # or any LiteLLM-supported provider
dspy.configure(lm=lm)

# 1. Define your program
qa = dspy.ChainOfThought("question -> answer")

# 2. Prepare training data (50-200+ examples recommended)
trainset = [
    dspy.Example(question="What is the capital of France?", answer="Paris").with_inputs("question"),
    dspy.Example(question="What is 2 + 2?", answer="4").with_inputs("question"),
    # ... more examples
]

# 3. Define a metric
def metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()

# 4. Optimize with random search
optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
    num_candidate_programs=16,
)
optimized_qa = optimizer.compile(qa, trainset=trainset)

# 5. Use the optimized program
result = optimized_qa(question="What is the capital of Germany?")
print(result.answer)

# 6. Save for later
optimized_qa.save("optimized_qa.json")
```

## Key parameters

```python
dspy.BootstrapFewShotWithRandomSearch(
    metric,                          # Scoring function: (example, prediction, trace) -> float|bool
    max_bootstrapped_demos=4,        # Max demos generated by running the program on training examples
    max_labeled_demos=16,            # Max demos taken directly from labeled training data
    num_candidate_programs=16,       # How many random bootstrap runs to try
    num_threads=None,                # Threads for parallel evaluation of candidates
    stop_at_score=None,              # Early-stop if a candidate reaches this score
    metric_threshold=None,           # Min metric score for a bootstrapped demo to be kept
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `metric` | `Callable` | required | Scoring function `(example, prediction, trace=None) -> float\|bool` |
| `max_bootstrapped_demos` | `int` | `4` | Maximum bootstrapped (program-generated) demos per predictor |
| `max_labeled_demos` | `int` | `16` | Maximum labeled (from trainset) demos per predictor |
| `num_candidate_programs` | `int` | `16` | Number of random bootstrap attempts to evaluate |
| `num_threads` | `int \| None` | `None` | Threads for evaluating candidates. Falls back to `dspy.settings.num_threads`. |
| `stop_at_score` | `float \| None` | `None` | Early-stop search if a candidate reaches this score |
| `metric_threshold` | `float \| None` | `None` | Minimum metric score for a bootstrapped demo to be included |
| `teacher_settings` | `dict \| None` | `None` | LM config for the teacher model (e.g., `{"lm": big_model}`) |
| `max_rounds` | `int` | `1` | Bootstrap rounds per candidate (>1 generates diverse traces at temperature=1.0) |
| `max_errors` | `int \| None` | `None` | Error tolerance before aborting |

### max_bootstrapped_demos vs max_labeled_demos

These two parameters control where demonstrations come from:

- **Bootstrapped demos** are generated by running your program on training examples and keeping the traces where the metric passes. These are powerful because they show the LM its own successful reasoning patterns, including intermediate steps like chain-of-thought reasoning.

- **Labeled demos** are taken directly from your training data as input-output pairs. They don't include intermediate reasoning steps, but they're reliable because they use your gold-standard answers.

The optimizer includes up to `max_bootstrapped_demos` bootstrapped demos plus up to `max_labeled_demos` labeled demos in each candidate program's prompt.

**Guidance:**
- Start with `max_bootstrapped_demos=4, max_labeled_demos=4` for most tasks.
- Increase `max_labeled_demos` (up to 8-16) if you have high-quality labeled data and your model benefits from more examples.
- Increase `max_bootstrapped_demos` (up to 4-8) if your task involves chain-of-thought or multi-step reasoning where seeing worked examples helps.
- Keep the total number of demos reasonable -- too many demos bloat the prompt and can hurt performance or exceed context limits.

## How random search works

Each candidate program is built by a separate BootstrapFewShot run. The randomness comes from:

1. **Shuffled training data**: Each run sees a different random ordering of training examples, so different examples get bootstrapped.
2. **Different demo subsets**: The random ordering means each candidate ends up with a different combination of bootstrapped and labeled demos.

After all candidate programs are generated, the optimizer evaluates each one on a validation set (a portion of your trainset that was held out). The candidate with the highest validation score wins.

This is conceptually similar to hyperparameter random search: instead of searching over learning rates or layer sizes, you're searching over which few-shot demos to include in the prompt.

## Computational cost

The cost scales linearly with `num_candidate_programs`:

| num_candidate_programs | Approximate cost multiplier | When to use |
|------------------------|----------------------------|-------------|
| 4-8 | 4-8x base BootstrapFewShot | Quick search, limited budget |
| 16 (default) | 16x | Good balance for most tasks |
| 25-50 | 25-50x | Maximum quality, budget allows |

Each candidate program requires:
1. One BootstrapFewShot run (bootstrapping demos from trainset)
2. One evaluation pass over the validation set

**Cost estimate**: If a single BootstrapFewShot run costs ~$0.50, then 16 candidate programs costs ~$8. With a larger trainset or more expensive model, plan for $5-$20.

**Tip**: Start with `num_candidate_programs=8` to get a quick sense of how much random search helps, then increase to 16 or 25 if the improvement justifies the cost.

## When to use BootstrapFewShotWithRandomSearch

**Use BootstrapFewShotWithRandomSearch when:**
- You have 50-200+ training examples
- Basic BootstrapFewShot gives inconsistent results across runs
- You want better few-shot demos without optimizing instructions
- You have budget for 10-20x the cost of a single BootstrapFewShot run
- You want a solid middle ground between BootstrapFewShot and MIPROv2

**Use BootstrapFewShot instead when:**
- You have fewer than 50 examples
- You want the fastest possible optimization
- Budget is very tight
- You're just prototyping and will optimize more later

**Use MIPROv2 instead when:**
- You want to optimize instructions and demos together (BootstrapRS only optimizes demos)
- You have 200+ examples and budget for a thorough search
- You've already tried BootstrapRS and want to push further
- You want the best prompt optimization DSPy offers

```
Quick & cheap          Solid middle ground         Best quality
BootstrapFewShot  -->  BootstrapFewShotWithRS  -->  MIPROv2
~$0.50                 ~$5-20                       ~$5-50
Few-shot demos only    Few-shot demos (searched)    Instructions + few-shot demos
1 candidate            N candidates                 Bayesian optimization
```

## Using a teacher model

Use a larger model to generate high-quality bootstrapped demos, then deploy with a cheaper student model:

```python
teacher_lm = dspy.LM("openai/gpt-4o")  # or any LiteLLM-supported provider
student_lm = dspy.LM("openai/gpt-4o-mini")  # or any LiteLLM-supported provider

dspy.configure(lm=student_lm)

optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=metric,
    max_bootstrapped_demos=4,
    num_candidate_programs=16,
    teacher_settings={"lm": teacher_lm},
)
optimized = optimizer.compile(my_program, trainset=trainset)
# optimized runs on student_lm but uses demos generated by teacher_lm
```

## Early stopping with stop_at_score

Skip evaluating remaining candidates once a "good enough" program is found:

```python
optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=metric,
    num_candidate_programs=25,
    stop_at_score=95.0,  # stop as soon as a candidate scores >= 95%
)
```

This is useful when you set `num_candidate_programs` high but want to save cost if an early candidate is already excellent.

## Passing an optimized program to further optimization

You can stack optimizers. Run BootstrapRS first to find great demos, then pass the result to MIPROv2 to refine instructions on top:

```python
# Step 1: Find best demos with random search
bootstrap_optimizer = dspy.BootstrapFewShotWithRandomSearch(
    metric=metric,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
    num_candidate_programs=16,
)
bootstrapped = bootstrap_optimizer.compile(my_program, trainset=trainset)

# Step 2: Refine instructions with MIPROv2
mipro_optimizer = dspy.MIPROv2(metric=metric, auto="medium")
final = mipro_optimizer.compile(bootstrapped, trainset=trainset)
```

## Gotchas

1. **Claude uses the same data for training and validation.** BootstrapRS evaluates candidates on a held-out validation set. If you pass all data as `trainset` without a separate `valset`, the optimizer splits it internally, but you get no control over the split. Pass `valset` explicitly for reproducible results: `optimizer.compile(program, trainset=trainset, valset=devset)`.
2. **Claude sets `num_candidate_programs` too low.** With `num_candidate_programs=3` the random search barely explores the space. The default of 16 is a good starting point. Fewer than 8 rarely finds materially better demos than plain BootstrapFewShot.
3. **Claude sets `max_labeled_demos=16` with multi-step pipelines.** Each predictor in the pipeline gets up to `max_labeled_demos` + `max_bootstrapped_demos` demos. A 3-step pipeline with 16+4 demos per step = 60 demos total, which can blow past context limits. Use 2-4 demos per type for multi-step pipelines.
4. **Claude forgets the `candidate_programs` attribute on the result.** The optimized program has a `candidate_programs` attribute containing all scored candidates. This is useful for inspecting how much variance exists and whether more search would help.
5. **Claude runs BootstrapRS with fewer than 50 training examples.** With fewer than ~50 examples, the random search has too little data to meaningfully differentiate candidates. Use plain `BootstrapFewShot` instead, or collect more data.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- **BootstrapFewShot** for the simpler single-run version -- see `/dspy-bootstrap-few-shot`
- **MIPROv2** for instruction + demo optimization -- see `/dspy-miprov2`
- **Evaluate** for measuring quality with metrics and devsets -- see `/dspy-evaluate`
- **Data handling** for preparing training sets -- see `/dspy-data`
- **Improving accuracy** for the full optimizer decision framework -- see `/ai-improving-accuracy`
- For worked examples, see [examples.md](examples.md)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- [dspy.BootstrapFewShotWithRandomSearch API docs](https://dspy.ai/api/optimizers/BootstrapFewShotWithRandomSearch/)
- [DSPy optimizer selection guide](https://dspy.ai/diving-deeper/choosing-an-optimizer/)
- For constructor signatures and method reference, see [reference.md](reference.md)
- For worked examples (QA optimization, multi-step pipeline), see [examples.md](examples.md)
